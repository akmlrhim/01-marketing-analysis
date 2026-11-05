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

const args = process.argv.slice(2).map((arg) =>
  arg.replace(/\$\{([A-Za-z_][A-Za-z0-9_]*)\}/g, (_, name) => {
    const value = process.env[name];
    if (!value) {
      console.error(`[mcp-remote-env] Variabel ${name} kosong atau tidak ada. Isi di file .env pada root proyek.`);
      process.exit(1);
    }
    return value;
  }),
);

if (args.length === 0) {
  console.error('[mcp-remote-env] Pemakaian: node mcp-remote-env.mjs <url> [--header "Nama: ${VAR}"]');
  process.exit(1);
}

const command = "npx -y mcp-remote " + args.map((a) => `"${a.replaceAll('"', "")}"`).join(" ");
const child = spawn(command, { shell: true, stdio: "inherit", env: process.env });
child.on("error", (err) => {
  console.error("[mcp-remote-env] Gagal menjalankan mcp-remote:", err.message);
  process.exit(1);
});
child.on("exit", (code) => process.exit(code ?? 1));
