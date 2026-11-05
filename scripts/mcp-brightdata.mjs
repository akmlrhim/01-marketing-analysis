import { spawn } from "node:child_process";
import { readFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const projectRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const envPath = join(projectRoot, ".env");

if (existsSync(envPath)) {
  for (const line of readFileSync(envPath, "utf8").split(/\r?\n/)) {
    if (line.trim().startsWith("#")) continue;
    const m = line.match(/^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$/);
    if (!m) continue;
    let value = m[2].trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    if (!(m[1] in process.env)) process.env[m[1]] = value;
  }
}

const token = process.env.BRIGHTDATA_API_KEY;
if (!token) {
  console.error("[mcp-brightdata] BRIGHTDATA_API_KEY kosong atau tidak ada. Isi di file .env pada root proyek.");
  process.exit(1);
}

const child = process.platform === "win32"
  ? spawn("cmd", ["/c", "npx", "-y", "@brightdata/mcp"], {
      cwd: projectRoot,
      stdio: "inherit",
      env: { ...process.env, API_TOKEN: token },
    })
  : spawn("npx", ["-y", "@brightdata/mcp"], {
      cwd: projectRoot,
      stdio: "inherit",
      env: { ...process.env, API_TOKEN: token },
    });
child.on("error", (err) => {
  console.error("[mcp-brightdata] Gagal menjalankan @brightdata/mcp:", err.message);
  process.exit(1);
});
child.on("exit", (code) => process.exit(code ?? 1));
