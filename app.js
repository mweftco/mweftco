const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  let filePath = req.url === "/"
    ? path.join(__dirname, "index.html")
    : path.join(__dirname, req.url);

  if (!fs.existsSync(filePath)) {
    res.writeHead(404, { "Content-Type": "text/plain" });
    res.end("404 - File not found");
    return;
  }

  const ext = path.extname(filePath);
  const types = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".xml": "application/xml"
  };

  res.writeHead(200, {
    "Content-Type": types[ext] || "application/octet-stream"
  });

  fs.createReadStream(filePath).pipe(res);
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`M&WEFTCO server running on port ${PORT}`);
});
