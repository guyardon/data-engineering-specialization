/**
 * fetch-notion.mjs
 *
 * Fetches all content from the Data Engineering Specialization Notion workspace
 * and generates MDX files + downloads images locally.
 *
 * Usage:
 *   NOTION_TOKEN=<your-token> node scripts/fetch-notion.mjs
 *
 * Or create a .env file with NOTION_TOKEN=...
 */

import { Client } from "@notionhq/client";
import fs from "fs";
import path from "path";
import https from "https";
import http from "http";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, "..");

// Load .env if present
const envPath = path.join(ROOT, ".env");
if (fs.existsSync(envPath)) {
  const lines = fs.readFileSync(envPath, "utf8").split("\n");
  for (const line of lines) {
    const [key, ...rest] = line.split("=");
    if (key && rest.length) process.env[key.trim()] = rest.join("=").trim();
  }
}

const NOTION_TOKEN = process.env.NOTION_TOKEN;
if (!NOTION_TOKEN) {
  console.error("Error: NOTION_TOKEN environment variable is required.");
  console.error("Create a .env file with: NOTION_TOKEN=secret_...");
  process.exit(1);
}

const ROOT_PAGE_ID = "139969a7aa018017b81fc3858c54fc8f";
const IMAGES_DIR = path.join(ROOT, "public", "images");
const CONTENT_DIR = path.join(ROOT, "src", "content", "notes");

const notion = new Client({ auth: NOTION_TOKEN });

// Ensure directories exist
fs.mkdirSync(IMAGES_DIR, { recursive: true });
fs.mkdirSync(CONTENT_DIR, { recursive: true });

// ─── Utility ───────────────────────────────────────────────────────────────

function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, "")
    .replace(/[\s_]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 60);
}

function downloadImage(url, destPath) {
  return new Promise((resolve, reject) => {
    if (fs.existsSync(destPath)) return resolve(destPath);
    const protocol = url.startsWith("https") ? https : http;
    const file = fs.createWriteStream(destPath);
    protocol
      .get(url, (res) => {
        if (res.statusCode === 301 || res.statusCode === 302) {
          file.close();
          fs.unlinkSync(destPath);
          return downloadImage(res.headers.location, destPath)
            .then(resolve)
            .catch(reject);
        }
        res.pipe(file);
        file.on("finish", () => {
          file.close();
          resolve(destPath);
        });
      })
      .on("error", (err) => {
        file.close();
        try {
          fs.unlinkSync(destPath);
        } catch {}
        reject(err);
      });
  });
}

function extractImageUUID(url) {
  // Extract the UUID from the S3 path: /46e655c5-.../UUID/image.png
  const match = url.match(
    /\/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\/image\./i,
  );
  if (match) return match[1];
  // Fallback: hash of URL
  let hash = 0;
  for (let i = 0; i < url.length; i++)
    hash = (hash << 5) - hash + url.charCodeAt(i);
  return Math.abs(hash).toString(16);
}

// ─── Notion API helpers ─────────────────────────────────────────────────────

// eslint-disable-next-line @typescript-eslint/no-unused-vars
async function getPageTitle(page) {
  const titleProp = page.properties?.title || page.properties?.Name;
  if (titleProp?.title) {
    return titleProp.title.map((t) => t.plain_text).join("") || "Untitled";
  }
  // For child pages embedded in content
  if (page.child_page?.title) return page.child_page.title;
  return "Untitled";
}

async function getChildPages(pageId) {
  const children = [];
  let cursor;
  do {
    const res = await notion.blocks.children.list({
      block_id: pageId,
      start_cursor: cursor,
      page_size: 100,
    });
    for (const block of res.results) {
      if (block.type === "child_page") {
        children.push({ id: block.id, title: block.child_page.title });
      }
    }
    cursor = res.has_more ? res.next_cursor : undefined;
  } while (cursor);
  return children;
}

// ─── Block → Markdown conversion ────────────────────────────────────────────

async function richTextToMd(richText) {
  if (!richText || !richText.length) return "";
  return richText
    .map((rt) => {
      let text = rt.plain_text || "";
      // Escape MDX special chars but not inside code
      if (rt.annotations?.code) {
        return `\`${text}\``;
      }
      // Escape < > { } in plain text to avoid MDX parsing issues
      text = text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
      if (rt.annotations?.bold && rt.annotations?.italic)
        return `***${text}***`;
      if (rt.annotations?.bold) return `**${text}**`;
      if (rt.annotations?.italic) return `*${text}*`;
      if (rt.annotations?.strikethrough) return `~~${text}~~`;
      if (rt.annotations?.underline) return `<u>${text}</u>`;
      if (rt.type === "mention") return text;
      if (rt.href) {
        text = `[${text}](${rt.href})`;
      }
      return text;
    })
    .join("");
}

async function processBlocks(
  blocks,
  depth = 0,
  imageBasePath = "/data-engineering-specialization-website/images",
) {
  const lines = [];
  let i = 0;

  while (i < blocks.length) {
    const block = blocks[i];
    const indent = "  ".repeat(Math.max(0, depth - 1));

    switch (block.type) {
      case "paragraph": {
        const text = await richTextToMd(block.paragraph.rich_text);
        if (text.trim()) lines.push(text + "\n");
        else lines.push("");
        break;
      }

      case "heading_1": {
        const text = await richTextToMd(block.heading_1.rich_text);
        lines.push(`# ${text}\n`);
        break;
      }

      case "heading_2": {
        const text = await richTextToMd(block.heading_2.rich_text);
        lines.push(`## ${text}\n`);
        break;
      }

      case "heading_3": {
        const text = await richTextToMd(block.heading_3.rich_text);
        lines.push(`### ${text}\n`);
        break;
      }

      case "bulleted_list_item": {
        const text = await richTextToMd(block.bulleted_list_item.rich_text);
        lines.push(`${indent}- ${text}`);
        if (block.has_children) {
          const children = await getBlockChildren(block.id);
          const childMd = await processBlocks(
            children,
            depth + 1,
            imageBasePath,
          );
          lines.push(childMd);
        }
        break;
      }

      case "numbered_list_item": {
        const text = await richTextToMd(block.numbered_list_item.rich_text);
        // Count number in sequence
        let num = 1;
        for (let j = i - 1; j >= 0; j--) {
          if (blocks[j].type === "numbered_list_item") num++;
          else break;
        }
        lines.push(`${indent}${num}. ${text}`);
        if (block.has_children) {
          const children = await getBlockChildren(block.id);
          const childMd = await processBlocks(
            children,
            depth + 1,
            imageBasePath,
          );
          lines.push(childMd);
        }
        break;
      }

      case "to_do": {
        const text = await richTextToMd(block.to_do.rich_text);
        const check = block.to_do.checked ? "[x]" : "[ ]";
        lines.push(`- ${check} ${text}`);
        break;
      }

      case "toggle": {
        const text = await richTextToMd(block.toggle.rich_text);
        lines.push(`<details><summary>${text}</summary>\n`);
        if (block.has_children) {
          const children = await getBlockChildren(block.id);
          const childMd = await processBlocks(
            children,
            depth + 1,
            imageBasePath,
          );
          lines.push(childMd);
        }
        lines.push("</details>\n");
        break;
      }

      case "code": {
        const text = block.code.rich_text.map((rt) => rt.plain_text).join("");
        const lang = block.code.language || "";
        lines.push(`\`\`\`${lang}\n${text}\n\`\`\`\n`);
        break;
      }

      case "quote": {
        const text = await richTextToMd(block.quote.rich_text);
        lines.push(`> ${text}\n`);
        break;
      }

      case "callout": {
        const text = await richTextToMd(block.callout.rich_text);
        const emoji = block.callout.icon?.emoji || "ℹ️";
        lines.push(`> ${emoji} ${text}\n`);
        break;
      }

      case "divider": {
        lines.push("---\n");
        break;
      }

      case "image": {
        const imgBlock = block.image;
        const url =
          imgBlock.type === "external"
            ? imgBlock.external.url
            : imgBlock.file.url;
        const caption = imgBlock.caption?.length
          ? await richTextToMd(imgBlock.caption)
          : "";

        try {
          const uuid = extractImageUUID(url);
          const fileName = `${uuid}.png`;
          const destPath = path.join(IMAGES_DIR, fileName);
          await downloadImage(url, destPath);
          const localUrl = `${imageBasePath}/${fileName}`;
          lines.push(
            caption ? `![${caption}](${localUrl})\n` : `![](${localUrl})\n`,
          );
        } catch (err) {
          console.warn(`  Warning: failed to download image: ${err.message}`);
          lines.push(`<!-- Image could not be downloaded -->\n`);
        }
        break;
      }

      case "table": {
        if (block.has_children) {
          const rows = await getBlockChildren(block.id);
          const mdRows = [];

          for (let r = 0; r < rows.length; r++) {
            const row = rows[r];
            if (row.type !== "table_row") continue;
            const cells = await Promise.all(
              row.table_row.cells.map((cell) => richTextToMd(cell)),
            );
            mdRows.push(`| ${cells.join(" | ")} |`);
            if (r === 0) {
              mdRows.push(`| ${cells.map(() => "---").join(" | ")} |`);
            }
          }
          lines.push(mdRows.join("\n") + "\n");
        }
        break;
      }

      case "column_list": {
        if (block.has_children) {
          const columns = await getBlockChildren(block.id);
          for (const col of columns) {
            if (col.has_children) {
              const colBlocks = await getBlockChildren(col.id);
              const colMd = await processBlocks(
                colBlocks,
                depth,
                imageBasePath,
              );
              lines.push(colMd);
            }
          }
        }
        break;
      }

      case "child_page": {
        // Skip — these are navigated separately
        break;
      }

      case "equation": {
        const expr = block.equation?.expression || "";
        lines.push(`$$${expr}$$\n`);
        break;
      }

      case "embed":
      case "bookmark": {
        const url = block[block.type]?.url || "";
        lines.push(`[${url}](${url})\n`);
        break;
      }

      default:
        // Silently skip unsupported blocks
        break;
    }

    i++;
  }

  return lines.join("\n").replace(/\n{3,}/g, "\n\n");
}

async function getBlockChildren(blockId) {
  const blocks = [];
  let cursor;
  do {
    const res = await notion.blocks.children.list({
      block_id: blockId,
      start_cursor: cursor,
      page_size: 100,
    });
    blocks.push(...res.results);
    cursor = res.has_more ? res.next_cursor : undefined;
  } while (cursor);
  return blocks;
}

// ─── Main traversal ──────────────────────────────────────────────────────────

async function fetchPageContent(pageId) {
  const blocks = await getBlockChildren(pageId);
  return processBlocks(blocks);
}

function cleanDir(dir) {
  if (fs.existsSync(dir)) fs.rmSync(dir, { recursive: true });
  fs.mkdirSync(dir, { recursive: true });
}

async function run() {
  console.log(
    "Fetching Data Engineering Specialization notes from Notion...\n",
  );

  // Clean content dir
  cleanDir(CONTENT_DIR);

  // Get courses (children of root page)
  const courses = await getChildPages(ROOT_PAGE_ID);
  console.log(`Found ${courses.length} courses`);

  for (let ci = 0; ci < courses.length; ci++) {
    const course = courses[ci];
    const courseSlug = slugify(course.title.replace(/^[^\w]+/, ""));
    const courseDir = path.join(CONTENT_DIR, courseSlug);
    fs.mkdirSync(courseDir, { recursive: true });

    console.log(`\nCourse ${ci + 1}: ${course.title}`);

    // Get weeks
    const weeks = await getChildPages(course.id);

    for (let wi = 0; wi < weeks.length; wi++) {
      const week = weeks[wi];
      const weekSlug = slugify(week.title.replace(/^[^\w]+/, ""));
      const weekDir = path.join(courseDir, weekSlug);
      fs.mkdirSync(weekDir, { recursive: true });

      console.log(`  Week ${wi + 1}: ${week.title}`);

      // Check if this week has child pages (sections) or just content
      const weekChildren = await getChildPages(week.id);

      if (weekChildren.length === 0) {
        // Week page IS the leaf — use its content directly
        console.log(`    → Leaf page (no child pages)`);
        const content = await fetchPageContent(week.id);
        const mdxContent = buildMdx({
          title: week.title,
          course: course.title,
          courseSlug,
          courseOrder: ci + 1,
          week: week.title,
          weekSlug,
          weekOrder: wi + 1,
          order: 1,
          notionId: week.id,
          content,
        });
        const fileName = `${weekSlug}.md`;
        fs.writeFileSync(path.join(weekDir, fileName), mdxContent);
      } else {
        // Has sections — recurse
        for (let si = 0; si < weekChildren.length; si++) {
          const section = weekChildren[si];
          console.log(`    Section ${si + 1}: ${section.title}`);

          // Check if section has child pages (subsections) or just content
          const sectionChildren = await getChildPages(section.id);

          if (sectionChildren.length === 0) {
            // Section is a leaf
            const content = await fetchPageContent(section.id);
            const sectionSlug = slugify(section.title.replace(/^[^\w]+/, ""));
            const mdxContent = buildMdx({
              title: section.title,
              course: course.title,
              courseSlug,
              courseOrder: ci + 1,
              week: week.title,
              weekSlug,
              weekOrder: wi + 1,
              order: si + 1,
              notionId: section.id,
              content,
            });
            fs.writeFileSync(
              path.join(weekDir, `${sectionSlug}.md`),
              mdxContent,
            );
          } else {
            // Has subsections — MERGE into parent section per D-01
            let content = await fetchPageContent(section.id);
            for (let ssi = 0; ssi < sectionChildren.length; ssi++) {
              const sub = sectionChildren[ssi];
              console.log(`      Merging subsection ${ssi + 1}: ${sub.title}`);
              const subContent = await fetchPageContent(sub.id);
              content += `\n\n## ${sub.title}\n\n${subContent}`;
              // Check for deeper nesting
              const subChildren = await getChildPages(sub.id);
              for (const deep of subChildren) {
                const deepContent = await fetchPageContent(deep.id);
                content += `\n\n### ${deep.title}\n\n${deepContent}`;
              }
            }
            const sectionSlug = slugify(section.title.replace(/^[^\w]+/, ""));
            const mdxContent = buildMdx({
              title: section.title,
              course: course.title,
              courseSlug,
              courseOrder: ci + 1,
              week: week.title,
              weekSlug,
              weekOrder: wi + 1,
              order: si + 1,
              notionId: section.id,
              content,
            });
            const safeSlug = sectionSlug || `section-${si + 1}`;
            fs.writeFileSync(path.join(weekDir, `${safeSlug}.md`), mdxContent);
          }
        }
      }
    }
  }

  console.log("\n✓ Done! Content written to src/content/notes/");
  console.log("Run `npm run dev` to preview the site.");
}

function buildMdx({
  title,
  course,
  courseSlug,
  courseOrder,
  week,
  weekSlug,
  weekOrder,
  order,
  notionId,
  content,
}) {
  const fm = [
    "---",
    `title: ${JSON.stringify(title)}`,
    `course: ${JSON.stringify(course)}`,
    `courseSlug: ${JSON.stringify(courseSlug)}`,
    `courseOrder: ${courseOrder}`,
    `week: ${JSON.stringify(week)}`,
    `weekSlug: ${JSON.stringify(weekSlug)}`,
    `weekOrder: ${weekOrder}`,
    `order: ${order}`,
    notionId ? `notionId: ${JSON.stringify(notionId)}` : "",
    "---",
  ]
    .filter(Boolean)
    .join("\n");

  return `${fm}\n\n${content}\n`;
}

run().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
