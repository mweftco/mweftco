const http = require("http");

const PORT = process.env.PORT || 8159;

const server = http.createServer((req, res) => {
  res.setHeader("Content-Type", "application/json");

  if (req.url === "/api/aurelia/health") {
    res.writeHead(200);
    res.end(JSON.stringify({
      ok: true,
      agent: "AURELIA",
      brand: "M&WEFTCO",
      status: "ready"
    }));
    return;
  }

  res.writeHead(404);
  res.end(JSON.stringify({
    ok: false,
    error: "Endpoint not found"
  }));
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`AURELIA backend running on port ${PORT}`);
});
