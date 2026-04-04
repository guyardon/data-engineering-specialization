import rough from "roughjs";
import { JSDOM } from "jsdom";
import fs from "fs";

const dom = new JSDOM(`<!DOCTYPE html><html><body></body></html>`);
const document = dom.window.document;

const W = 1000;
const H = 500;

const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
svg.setAttribute("width", W);
svg.setAttribute("height", H);

// Embed handwriting font
const style = document.createElementNS("http://www.w3.org/2000/svg", "style");
style.textContent = `
  @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@400;600;700&display=swap');
  text { font-family: 'Caveat', cursive; }
`;
svg.appendChild(style);

// Background
const bg = document.createElementNS("http://www.w3.org/2000/svg", "rect");
bg.setAttribute("width", W);
bg.setAttribute("height", H);
bg.setAttribute("fill", "#fdf6e3");
bg.setAttribute("rx", "12");
svg.appendChild(bg);

const rc = rough.svg(svg);

// -- Color palette --
const colors = {
  generation: { fill: "#dbeafe", stroke: "#3b82f6" },   // blue
  ingestion:  { fill: "#dcfce7", stroke: "#22c55e" },    // green
  storage:    { fill: "#fef9c3", stroke: "#eab308" },    // yellow
  transform:  { fill: "#ede9fe", stroke: "#8b5cf6" },    // purple
  serving:    { fill: "#ffe4e6", stroke: "#f43f5e" },     // pink/rose
  undercurrent: { fill: "#f1f5f9", stroke: "#94a3b8" },  // slate
};

const opts = (color) => ({
  fill: color.fill,
  fillStyle: "solid",
  stroke: color.stroke,
  strokeWidth: 2,
  roughness: 1.5,
  seed: Math.floor(Math.random() * 10000),
});

// -- Helper: draw labeled box --
function drawBox(x, y, w, h, label, sublabel, color) {
  const node = rc.rectangle(x, y, w, h, {
    ...opts(color),
    fillWeight: 1.5,
  });
  svg.appendChild(node);

  const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
  text.setAttribute("x", x + w / 2);
  text.setAttribute("y", y + h / 2 - (sublabel ? 6 : 0));
  text.setAttribute("text-anchor", "middle");
  text.setAttribute("dominant-baseline", "middle");
  text.setAttribute("font-size", "22");
  text.setAttribute("font-weight", "700");
  text.setAttribute("fill", color.stroke);
  text.textContent = label;
  svg.appendChild(text);

  if (sublabel) {
    const sub = document.createElementNS("http://www.w3.org/2000/svg", "text");
    sub.setAttribute("x", x + w / 2);
    sub.setAttribute("y", y + h / 2 + 18);
    sub.setAttribute("text-anchor", "middle");
    sub.setAttribute("dominant-baseline", "middle");
    sub.setAttribute("font-size", "15");
    sub.setAttribute("fill", "#64748b");
    sub.textContent = sublabel;
    svg.appendChild(sub);
  }
}

// -- Helper: draw arrow --
function drawArrow(x1, y1, x2, y2, color = "#475569") {
  const line = rc.line(x1, y1, x2, y2, {
    stroke: color,
    strokeWidth: 2,
    roughness: 1.2,
  });
  svg.appendChild(line);

  // Arrowhead
  const angle = Math.atan2(y2 - y1, x2 - x1);
  const headLen = 14;
  const p1x = x2 - headLen * Math.cos(angle - Math.PI / 6);
  const p1y = y2 - headLen * Math.sin(angle - Math.PI / 6);
  const p2x = x2 - headLen * Math.cos(angle + Math.PI / 6);
  const p2y = y2 - headLen * Math.sin(angle + Math.PI / 6);

  const head = rc.polygon(
    [[x2, y2], [p1x, p1y], [p2x, p2y]],
    { fill: color, fillStyle: "solid", stroke: color, strokeWidth: 1, roughness: 0.5 }
  );
  svg.appendChild(head);
}

// -- Helper: draw curved arrow --
function drawCurvedArrow(points, color = "#94a3b8") {
  const path = rc.linearPath(points, {
    stroke: color,
    strokeWidth: 1.5,
    roughness: 1,
    strokeLineDash: [8, 4],
  });
  svg.appendChild(path);

  // Arrowhead at last point
  const n = points.length;
  const dx = points[n - 1][0] - points[n - 2][0];
  const dy = points[n - 1][1] - points[n - 2][1];
  const angle = Math.atan2(dy, dx);
  const headLen = 10;
  const x2 = points[n - 1][0];
  const y2 = points[n - 1][1];
  const p1x = x2 - headLen * Math.cos(angle - Math.PI / 6);
  const p1y = y2 - headLen * Math.sin(angle - Math.PI / 6);
  const p2x = x2 - headLen * Math.cos(angle + Math.PI / 6);
  const p2y = y2 - headLen * Math.sin(angle + Math.PI / 6);
  const head = rc.polygon(
    [[x2, y2], [p1x, p1y], [p2x, p2y]],
    { fill: color, fillStyle: "solid", stroke: color, strokeWidth: 1, roughness: 0.3 }
  );
  svg.appendChild(head);
}

// -- Helper: draw pill --
function drawPill(x, y, w, h, label, color) {
  // Use ellipse-like rounded rect
  const node = rc.rectangle(x, y, w, h, {
    fill: color.fill,
    fillStyle: "solid",
    stroke: color.stroke,
    strokeWidth: 1.5,
    roughness: 1,
    seed: Math.floor(Math.random() * 10000),
  });
  svg.appendChild(node);

  const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
  text.setAttribute("x", x + w / 2);
  text.setAttribute("y", y + h / 2 + 1);
  text.setAttribute("text-anchor", "middle");
  text.setAttribute("dominant-baseline", "middle");
  text.setAttribute("font-size", "14");
  text.setAttribute("fill", color.stroke);
  text.textContent = label;
  svg.appendChild(text);
}

// ===== TITLE =====
const title = document.createElementNS("http://www.w3.org/2000/svg", "text");
title.setAttribute("x", W / 2);
title.setAttribute("y", 38);
title.setAttribute("text-anchor", "middle");
title.setAttribute("font-size", "28");
title.setAttribute("font-weight", "700");
title.setAttribute("fill", "#1e293b");
title.textContent = "The Data Engineering Lifecycle";
svg.appendChild(title);

// ===== MAIN FLOW BOXES =====
const boxH = 80;
const boxW = 160;
const startY = 80;
const gap = 30;

// Positions
const genX = 30;
const ingX = genX + boxW + gap + 40;
const stoX = ingX + boxW + gap + 40;
const traX = stoX + boxW + 20 + gap + 40;
const boxMidY = startY + boxH / 2;

drawBox(genX, startY, boxW, boxH, "Generation", "Source Systems", colors.generation);
drawBox(ingX, startY, boxW, boxH, "Ingestion", "Batch & Stream", colors.ingestion);
drawBox(stoX, startY - 10, boxW + 20, boxH + 20, "Storage", "Lakes & Warehouses", colors.storage);
drawBox(traX, startY, boxW, boxH, "Transformation", "Queries & Modeling", colors.transform);

// Arrows between main boxes
drawArrow(genX + boxW + 4, boxMidY, ingX - 4, boxMidY, colors.generation.stroke);
drawArrow(ingX + boxW + 4, boxMidY, stoX - 4, boxMidY, colors.ingestion.stroke);
drawArrow(stoX + boxW + 24, boxMidY, traX - 4, boxMidY, colors.storage.stroke);

// Arrow down to Serving
const servX = traX - 40;
const servY = startY + boxH + 80;
const servW = boxW + 80;
const servH = boxH + 10;

drawArrow(traX + boxW / 2, startY + boxH + 4, traX + boxW / 2 - 0, servY - 4, colors.transform.stroke);

drawBox(servX, servY, servW, servH, "Serving", "Analytics · ML · Reverse ETL", colors.serving);

// Reverse ETL feedback loop (dashed, from Serving back to Generation)
const feedbackY = servY + servH + 20;
drawCurvedArrow([
  [servX, servY + servH / 2],
  [servX - 30, servY + servH / 2 + 20],
  [genX + boxW / 2, feedbackY],
  [genX + boxW / 2, startY + boxH + 4],
], "#94a3b8");

// Feedback label
const feedLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
feedLabel.setAttribute("x", (servX + genX + boxW / 2) / 2);
feedLabel.setAttribute("y", feedbackY + 16);
feedLabel.setAttribute("text-anchor", "middle");
feedLabel.setAttribute("font-size", "13");
feedLabel.setAttribute("fill", "#94a3b8");
feedLabel.setAttribute("font-style", "italic");
feedLabel.textContent = "reverse ETL feedback loop";
svg.appendChild(feedLabel);

// ===== UNDERCURRENTS =====
const ucY = 370;
const ucLabelY = ucY - 14;

const ucTitle = document.createElementNS("http://www.w3.org/2000/svg", "text");
ucTitle.setAttribute("x", W / 2);
ucTitle.setAttribute("y", ucLabelY);
ucTitle.setAttribute("text-anchor", "middle");
ucTitle.setAttribute("font-size", "18");
ucTitle.setAttribute("font-weight", "600");
ucTitle.setAttribute("fill", "#64748b");
ucTitle.setAttribute("letter-spacing", "4");
ucTitle.textContent = "UNDERCURRENTS";
svg.appendChild(ucTitle);

// Draw a sketchy horizontal line spanning the width
const ucLine = rc.line(40, ucY - 4, W - 40, ucY - 4, {
  stroke: "#cbd5e1",
  strokeWidth: 1,
  roughness: 2,
});
svg.appendChild(ucLine);

// Undercurrent pills
const pillH = 32;
const pillW = 140;
const pillGap = 18;
const pillStartX = (W - (5 * pillW + 4 * pillGap)) / 2;
const pillColors = [
  { fill: "#e0f2fe", stroke: "#0284c7" },   // Security - sky
  { fill: "#fef3c7", stroke: "#d97706" },    // Data Mgmt - amber
  { fill: "#d1fae5", stroke: "#059669" },    // DataOps - emerald
  { fill: "#fce7f3", stroke: "#db2777" },    // Architecture - pink
  { fill: "#e0e7ff", stroke: "#6366f1" },    // Orchestration - indigo
];
const pillLabels = ["Security", "Data Mgmt", "DataOps", "Architecture", "Orchestration"];
const pillEmojis = ["🔒", "📋", "⚙️", "🏗️", "🔄"];

for (let i = 0; i < 5; i++) {
  const px = pillStartX + i * (pillW + pillGap);
  drawPill(px, ucY + 4, pillW, pillH, `${pillEmojis[i]} ${pillLabels[i]}`, pillColors[i]);
}

// Software Engineering pill centered below
const seW = 220;
const seX = (W - seW) / 2;
drawPill(seX, ucY + pillH + 16, seW, pillH, "💻 Software Engineering", { fill: "#f3e8ff", stroke: "#9333ea" });

// ===== OUTPUT =====
const svgString = svg.outerHTML;
const outPath = "public/images/diagrams/data-engineering-lifecycle.svg";
fs.writeFileSync(outPath, svgString);
console.log(`Written to ${outPath}`);
