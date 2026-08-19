const http = require("http");

const PORT = process.env.PORT || 8159;

/* =========================
   MONARCH AI COLONY
   ========================= */

const colony = {
  name: "MONARCH AI COLONY",
  head: "vera",

  agents: [
    {
      id: "vera",
      name: "VERA",
      role: "Head AI",
      department: "Command",
      status: "working",
      location: "hq",
      task: "Managing the AI Colony"
    },
    {
      id: "aurelia",
      name: "AURELIA",
      role: "Growth AI",
      department: "M&WEFTCO Growth",
      status: "working",
      location: "growth_office",
      task: "Managing Instagram, Facebook and website growth"
    },
    {
      id: "orion",
      name: "ORION",
      role: "Research AI",
      department: "Research",
      status: "idle",
      location: "research_room",
      task: "Waiting for research task"
    },
    {
      id: "nova",
      name: "NOVA",
      role: "Creative AI",
      department: "Creative",
      status: "idle",
      location: "creative_room",
      task: "Waiting for creative task"
    },
    {
      id: "nexus",
      name: "NEXUS",
      role: "Technical AI",
      department: "Technology",
      status: "idle",
      location: "tech_room",
      task: "Waiting for technical task"
    }
  ]
};

function sendJSON(res, statusCode, data) {
  res.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
  });

  res.end(JSON.stringify(data, null, 2));
}

function getPath(req) {
  return req.url.split("?")[0];
}

const server = http.createServer((req, res) => {

  if (req.method === "OPTIONS") {
    res.writeHead(204, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    });

    res.end();
    return;
  }

  const path = getPath(req);

  if (req.method === "GET" && path === "/api/aurelia/health") {
    sendJSON(res, 200, {
      ok: true,
      agent: "AURELIA",
      brand: "M&WEFTCO",
      status: "ready"
    });

    return;
  }

  if (req.method === "GET" && path === "/api/aurelia/colony") {
    sendJSON(res, 200, {
      ok: true,
      colony: colony.name,
      head: colony.head,
      agents: colony.agents,
      totalAgents: colony.agents.length
    });

    return;
  }

  if (req.method === "GET" && path === "/api/aurelia/agents") {
    sendJSON(res, 200, {
      ok: true,
      agents: colony.agents
    });

    return;
  }

  if (req.method === "GET" && path.startsWith("/api/aurelia/agent/")) {

    const id = path.split("/").pop();

    const agent = colony.agents.find(
      item => item.id === id
    );

    if (!agent) {
      sendJSON(res, 404, {
        ok: false,
        error: "Agent not found"
      });

      return;
    }

    sendJSON(res, 200, {
      ok: true,
      agent
    });

    return;
  }

  sendJSON(res, 404, {
    ok: false,
    error: "Endpoint not found"
  });

});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`MONARCH AI Colony running on port ${PORT}`);
});
