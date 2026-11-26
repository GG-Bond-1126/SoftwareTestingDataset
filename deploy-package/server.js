// 零依赖静态文件服务：把同目录下的 public/ 子目录按 0.0.0.0:PORT 提供带 MIME 与条件请求的只读服务。
// 运行契约：build.sh 会把本文件、run.sh 与 public/ 全部拷入 dist/，
// 运行时工作目录为 dist/，因此这里用 __dirname/public 解析站点根目录。
const fs = require("fs");
const path = require("path");
const http = require("http");

const ROOT = path.join(__dirname, "public");

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".txt": "text/plain; charset=utf-8",
  ".xml": "application/xml; charset=utf-8",
  ".webmanifest": "application/manifest+json",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".map": "application/json",
  ".md": "text/markdown; charset=utf-8",
  ".pdf": "application/pdf",
};

function serve() {
  const port = Number(process.env.PORT || 8000);
  const root = ROOT;
  const server = http.createServer((req, res) => {
    const url = (req.url || "/").split("?")[0];
    let file = path.join(root, decodeURIComponent(url === "/" ? "index.html" : url));
    if (!file.startsWith(root) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
      file = path.join(root, "404.html");
      if (!fs.existsSync(file)) {
        res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
        res.end("not found");
        return;
      }
      const body = fs.readFileSync(file);
      res.writeHead(404, { "Content-Type": MIME[".html"], "Content-Length": body.length });
      res.end(body);
      return;
    }
    const stat = fs.statSync(file);
    const type = MIME[path.extname(file).toLowerCase()] || "application/octet-stream";
    const headers = { "Content-Type": type, "Content-Length": stat.size };
    const ifmod = req.headers["if-modified-since"];
    if (ifmod && stat.mtime.toUTCString() <= ifmod) {
      res.writeHead(304, headers);
      res.end();
      return;
    }
    headers["Last-Modified"] = stat.mtime.toUTCString();
    const range = req.headers["range"];
    if (range && range.startsWith("bytes=")) {
      const parts = range.slice(6).split("-");
      const s = Number(parts[0] || 0);
      const e = Number(parts[1] || (stat.size - 1));
      res.writeHead(206, Object.assign(headers, {
        "Content-Range": "bytes " + s + "-" + e + "/" + stat.size,
        "Content-Length": e - s + 1,
      }));
      fs.createReadStream(file, { start: s, end: e }).pipe(res);
      return;
    }
    res.writeHead(200, headers);
    fs.createReadStream(file).pipe(res);
  });
  server.listen(port, "0.0.0.0", () => {
    console.log("static server on 0.0.0.0:" + port);
  });
}

serve();
