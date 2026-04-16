const u="0.28.0",a=`https://cdn.jsdelivr.net/pyodide/v${u}/full/`;let o=null;function y(t){return new Promise((n,e)=>{const d=document.querySelector(`script[data-src="${t}"]`);if(d){if(d.dataset.loaded==="true"){n();return}d.addEventListener("load",()=>n()),d.addEventListener("error",()=>e(new Error(`Failed to load ${t}`)));return}const r=document.createElement("script");r.src=t,r.async=!0,r.dataset.src=t,r.addEventListener("load",()=>{r.dataset.loaded="true",n()}),r.addEventListener("error",()=>e(new Error(`Failed to load ${t}`))),document.head.appendChild(r)})}async function c(t){if(o)return o;o=(async()=>{if(t?.("Downloading Python runtime (~7MB, one-time)..."),await y(`${a}pyodide.js`),!window.loadPyodide)throw new Error("Pyodide failed to load");t?.("Initializing Python...");const n=await window.loadPyodide({indexURL:a});return t?.("Ready"),n})();try{return await o}catch(n){throw o=null,n}}async function l(t,n){const e=await c(n);e.runPython(`
import sys
import io
_sandbox_stdout = io.StringIO()
_sandbox_stderr = io.StringIO()
sys.stdout = _sandbox_stdout
sys.stderr = _sandbox_stderr
`);let d;try{await e.runPythonAsync(t)}catch(s){d=s instanceof Error?s.message:String(s)}const r=e.runPython("_sandbox_stdout.getvalue()"),i=e.runPython("_sandbox_stderr.getvalue()");return e.runPython(`
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
`),{stdout:r,stderr:i,error:d}}export{c as initPython,l as runPython};
