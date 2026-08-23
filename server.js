const http = require("http");

const PORT = process.env.PORT || 8159;

const colony = {
  name: "MONARCH AI COLONY",
  head: "VERA",

  agents: [
    {
      id: "vera",
      name: "VERA",
      role: "Central Intelligence / Head AI",
      department: "Command",
      status: "working"
    },
    {
      id: "igris",
      name: "IGRIS",
      role: "Study & Skills",
      department: "Learning",
      status: "idle"
    },
    {
      id: "beru",
      name: "BERU",
      role: "Fitness & Health",
      department: "Health",
      status: "idle"
    },
    {
      id: "bellion",
      name: "BELLION",
      role: "Faith & Mindset",
      department: "Mindset",
      status: "idle"
    },
    {
      id: "greed",
      name: "GREED",
      role: "Income & Wealth",
      department: "Finance",
      status: "idle"
    },
    {
      id: "kaisel",
      name: "KAISEL",
      role: "Time & Utility",
      department: "Utility",
      status: "idle"
    },
    {
      id: "baran",
      name: "BARAN",
      role: "Company Growth",
      department: "Business",
      status: "idle"
    },
    {
      id: "diwan",
      name: "DIWAN",
      role: "Documents & Social Content",
      department: "Documentation",
      status: "idle"
    },
    {
      id: "aurelia",
      name: "AURELIA",
      role: "M&WEFTCO Creative & Growth Director",
      department: "M&WEFTCO Growth",
      status: "working"
    }
  ]
};

const server = http.createServer((req, res) => {

  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Access-Control-Allow-Origin", "*");

  const path = req.url.split("?")[0];

  if (req.method === "GET" && path === "/api/aurelia/health") {
    res.writeHead(200);
    res.end(JSON.stringify({
      ok: true,
      agent: "AURELIA",
      brand: "M&WEFTCO",
      status: "ready"
    }));
    return;
  }

  if (req.method === "GET" && path === "/api/aurelia/colony") {
    res.writeHead(200);
    res.end(JSON.stringify({
      ok: true,
      colony: colony.name,
      head: colony.head,
      agents: colony.agents,
      totalAgents: colony.agents.length
    }));
    return;
  }

  if (req.method === "GET" && path === "/api/aurelia/agents") {
    res.writeHead(200);
    res.end(JSON.stringify({
      ok: true,
      head: colony.head,
      agents: colony.agents,
      totalAgents: colony.agents.length
    }));
    return;
  }

  res.writeHead(404);
  res.end(JSON.stringify({
    ok: false,
    error: "Endpoint not found",
    path: path
  }));
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`AURELIA backend running on port ${PORT}`);
});
