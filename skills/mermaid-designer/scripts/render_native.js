#!/usr/bin/env node
/**
 * render_native.js - Headless Chrome / Puppeteer Native Mermaid Renderer
 * 
 * Part of jk-agy-mermaid plugin.
 * Renders Mermaid (.mmd) diagrams into 3x HiDPI PNGs using native Google Chrome,
 * local Mermaid JS engine, and offline Iconify vector icon packs (gcp, logos, material-symbols, fa6-solid, mdi, carbon, aws, azure).
 */

const fs = require("fs");
const path = require("path");
const os = require("os");

const homeDir = os.homedir();

// 1. Resolve Puppeteer module
function resolvePuppeteer() {
  const candidates = [
    process.env.PUPPETEER_PATH,
    path.join(homeDir, ".local/share/npm-global/lib/node_modules/@mermaid-js/mermaid-cli/node_modules/puppeteer"),
    path.join(homeDir, ".local/share/npm-global/lib/node_modules/puppeteer"),
    "/usr/local/share/npm-global/lib/node_modules/@mermaid-js/mermaid-cli/node_modules/puppeteer",
    "puppeteer"
  ].filter(Boolean);

  for (const p of candidates) {
    try {
      return require(p);
    } catch (e) {
      // try next
    }
  }
  throw new Error("Puppeteer could not be resolved in any standard path. Check your npm-global installation.");
}

// 2. Resolve Iconify JSON directory
function resolveIconifyDir() {
  const candidates = [
    process.env.ICONIFY_DIR,
    path.join(homeDir, ".local/share/npm-global/lib/node_modules/@iconify/json/json"),
    "/usr/local/share/npm-global/lib/node_modules/@iconify/json/json"
  ].filter(Boolean);

  for (const p of candidates) {
    if (fs.existsSync(p)) {
      return p;
    }
  }
  throw new Error("Iconify JSON directory could not be resolved. Ensure @iconify/json is installed in npm-global.");
}

// 3. Resolve Mermaid JS distribution file
function resolveMermaidJs() {
  const candidates = [
    process.env.MERMAID_JS_PATH,
    path.join(homeDir, ".local/share/npm-global/lib/node_modules/@mermaid-js/mermaid-cli/node_modules/mermaid/dist/mermaid.min.js"),
    path.join(homeDir, ".local/share/npm-global/lib/node_modules/mermaid/dist/mermaid.min.js"),
    "/usr/local/share/npm-global/lib/node_modules/@mermaid-js/mermaid-cli/node_modules/mermaid/dist/mermaid.min.js"
  ].filter(Boolean);

  for (const p of candidates) {
    if (fs.existsSync(p)) {
      return p;
    }
  }
  throw new Error("Mermaid.js engine could not be resolved. Ensure @mermaid-js/mermaid-cli is installed in npm-global.");
}

// 4. Resolve Chrome binary
function resolveChromePath() {
  const candidates = [
    process.env.CHROME_BIN,
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium"
  ].filter(Boolean);

  for (const p of candidates) {
    if (fs.existsSync(p)) {
      return p;
    }
  }
  throw new Error("Google Chrome binary could not be found at standard Linux paths.");
}

async function renderMermaidFile(mmdPath, outputPath, options = {}) {
  const absMmd = path.resolve(mmdPath);
  const absOut = path.resolve(outputPath);

  if (!fs.existsSync(absMmd)) {
    throw new Error(`Input Mermaid file not found: ${absMmd}`);
  }

  const outDir = path.dirname(absOut);
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  const puppeteer = resolvePuppeteer();
  const iconifyDir = resolveIconifyDir();
  const mermaidJsPath = resolveMermaidJs();
  const chromePath = resolveChromePath();

  // Load requested icon packs
  const iconSets = {};
  const setsToLoad = options.iconPacks || ["gcp", "logos", "material-symbols", "fa6-solid", "mdi", "carbon", "aws", "azure"];
  for (const s of setsToLoad) {
    const fpath = path.join(iconifyDir, `${s}.json`);
    if (fs.existsSync(fpath)) {
      iconSets[s] = JSON.parse(fs.readFileSync(fpath, "utf-8"));
    }
  }
  if (iconSets["fa6-solid"]) {
    iconSets["fa"] = iconSets["fa6-solid"];
  }

  const mermaidJsCode = fs.readFileSync(mermaidJsPath, "utf-8");
  const mmdCode = fs.readFileSync(absMmd, "utf-8");

  const htmlContent = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {
      margin: 0;
      padding: 40px;
      background-color: #ffffff;
      font-family: 'Roboto', 'Google Sans', sans-serif;
      display: inline-block;
    }
    #container {
      background: #ffffff;
    }
  </style>
  <script>${mermaidJsCode}</script>
</head>
<body>
  <div id="container"></div>
  <script>
    const iconSets = ${JSON.stringify(iconSets)};
    const iconPacks = [];
    for (const [name, icons] of Object.entries(iconSets)) {
      iconPacks.push({ name: name, icons: icons });
    }

    mermaid.registerIconPacks(iconPacks);
    mermaid.initialize({
      startOnLoad: false,
      theme: 'default',
      look: 'neo',
      flowchart: {
        useMaxWidth: false,
        htmlLabels: true
      },
      themeVariables: {
        fontFamily: 'Roboto, Google Sans, Helvetica, Arial, sans-serif',
        primaryColor: '#4285F4',
        secondaryColor: '#34A853',
        tertiaryColor: '#FBBC04',
        mainBkg: '#FFFFFF',
        nodeBorder: '#4285F4',
        clusterBkg: '#FFFFFF',
        clusterBorder: '#DADCE0',
        lineColor: '#5F6368',
        edgeLabelBackground: '#ffffff'
      }
    });

    window.renderDiagram = async function(code) {
      const { svg } = await mermaid.render('mermaid-svg', code);
      document.getElementById('container').innerHTML = svg;
      return true;
    };
  </script>
</body>
</html>`;

  const tmpHtml = path.join(os.tmpdir(), `mermaid_native_${Date.now()}_${Math.random().toString(36).substring(2, 8)}.html`);
  fs.writeFileSync(tmpHtml, htmlContent, "utf-8");

  const browser = await puppeteer.launch({
    executablePath: chromePath,
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
    defaultViewport: {
      width: options.viewportWidth || 2400,
      height: options.viewportHeight || 1600,
      deviceScaleFactor: options.deviceScaleFactor || 3
    }
  });

  try {
    const page = await browser.newPage();
    await page.goto("file://" + tmpHtml, { waitUntil: "networkidle0" });
    await page.evaluate((code) => window.renderDiagram(code), mmdCode);

    const element = await page.$("#container");
    if (!element) {
      throw new Error("Render container element #container not found in DOM.");
    }
    await element.screenshot({ path: absOut, omitBackground: false });
    console.log(`[render_native] Successfully rendered 3x HiDPI PNG: ${absOut}`);
  } finally {
    await browser.close();
    if (fs.existsSync(tmpHtml)) {
      try { fs.unlinkSync(tmpHtml); } catch (e) {}
    }
  }
}

// CLI Execution
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 1 || args.includes("--help") || args.includes("-h")) {
    console.log("Usage: node render_native.js <input.mmd> [output.png] [--scale <factor>]");
    process.exit(args.length === 0 ? 1 : 0);
  }

  const mmdInput = args[0];
  let pngOutput = args[1];

  if (!pngOutput || pngOutput.startsWith("--")) {
    const parsed = path.parse(mmdInput);
    pngOutput = path.join(parsed.dir, `${parsed.name}.png`);
  }

  let scale = 3;
  const scaleIdx = args.indexOf("--scale");
  if (scaleIdx !== -1 && args[scaleIdx + 1]) {
    scale = parseInt(args[scaleIdx + 1], 10) || 3;
  }

  renderMermaidFile(mmdInput, pngOutput, { deviceScaleFactor: scale })
    .then(() => process.exit(0))
    .catch(err => {
      console.error("[render_native ERROR]:", err.message);
      process.exit(1);
    });
}

module.exports = { renderMermaidFile };
