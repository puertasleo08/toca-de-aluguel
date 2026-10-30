import { spawn } from "node:child_process";
import { writeFileSync, mkdirSync, readFileSync } from "node:fs";

const EDGE = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const SAIDA = new URL("../../_shots", import.meta.url).pathname.replace(/^\/(\w:)/, "$1");
const [, , URL_ALVO, ARQ_ACAO, NOME] = process.argv;
const DESKTOP = Boolean(process.env.DESKTOP);
mkdirSync(SAIDA, { recursive: true });

const edge = spawn(EDGE, ["--headless=new", "--disable-gpu", "--remote-debugging-port=9333", "--disable-site-isolation-trials",
  "--disable-features=IsolateOrigins,site-per-process", "--user-data-dir=" + SAIDA + "\\perfil", "about:blank"], { stdio: "ignore" });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
let alvo;
for (let i = 0; i < 40 && !alvo; i++) {
  await espera(250);
  try { alvo = (await (await fetch("http://127.0.0.1:9333/json")).json()).find((t) => t.type === "page"); } catch {}
}
const ws = new WebSocket(alvo.webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));
let id = 0;
const pend = new Map();
const erros = [];
ws.onmessage = (m) => {
  const d = JSON.parse(m.data);
  if (d.id && pend.has(d.id)) return pend.get(d.id)(d), pend.delete(d.id);
  if (d.method === "Runtime.exceptionThrown") erros.push("exceção: " + (d.params.exceptionDetails.exception?.description ?? d.params.exceptionDetails.text));
  if (d.method === "Runtime.consoleAPICalled" && ["error", "warning"].includes(d.params.type)) erros.push(`console.${d.params.type}: ` + d.params.args.map((a) => a.value ?? a.description).join(" "));
  if (d.method === "Log.entryAdded" && d.params.entry.level === "error" && d.params.entry.url?.includes("localhost")) erros.push("log: " + d.params.entry.text + " " + d.params.entry.url);
};
const cdp = (method, params = {}) => new Promise((r) => { const n = ++id; pend.set(n, r); ws.send(JSON.stringify({ id: n, method, params })); });
const avaliar = async (expr) => (await cdp("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value;

await cdp("Runtime.enable");
await cdp("Log.enable");
await cdp("Emulation.setDeviceMetricsOverride", DESKTOP ? { width: 1366, height: 900, deviceScaleFactor: 1, mobile: false } : { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
if (!DESKTOP) {
  await cdp("Emulation.setUserAgentOverride", { userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1" });
  await cdp("Emulation.setTouchEmulationEnabled", { enabled: true, maxTouchPoints: 5 });
}
await cdp("Page.navigate", { url: URL_ALVO });
await espera(4500);
console.log(await avaliar(readFileSync(ARQ_ACAO, "utf8")));
await espera(800);
const r = await cdp("Page.captureScreenshot", { format: "jpeg", quality: 75 });
writeFileSync(`${SAIDA}\\${NOME}.jpg`, Buffer.from(r.result.data, "base64"));
console.log("erros de console da página:", erros.length ? erros : "nenhum");
ws.close();
edge.kill();
process.exit(0);
