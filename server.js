const http = require("http");

const PORT = process.env.PORT || 8159;

const agents = [
  ["vera","VERA","Central Intelligence / Head AI","Command","working"],
  ["igris","IGRIS","Study & Skills","Learning","idle"],
  ["beru","BERU","Fitness & Health","Health","idle"],
  ["bellion","BELLION","Faith & Mindset","Mindset","idle"],
  ["greed","GREED","Income & Wealth","Finance","idle"],
  ["kaisel","KAISEL","Time & Utility","Utility","idle"],
  ["baran","BARAN","Company Growth","Business","idle"],
  ["diwan","DIWAN","Documents & Social Content","Documentation","idle"],
  ["aurelia","AURELIA","M&WEFTCO Creative & Growth Director","M&WEFTCO Growth","working"]
].map(([id,name,role,department,status]) => ({
  id,name,role,department,status
}));

const memory = {
  commands: [],
  tasks: [],
  courses: [],
  projects: []
};

function json(res, code, data) {
  res.writeHead(code, {
    "Content-Type": "application/json; charset=utf-8",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
  });
  res.end(JSON.stringify(data, null, 2));
}

function body(req) {
  return new Promise((resolve, reject) => {
    let data = "";
    req.on("data", chunk => data += chunk);
    req.on("end", () => {
      if (!data) return resolve({});
      try {
        resolve(JSON.parse(data));
      } catch {
        reject(new Error("Invalid JSON"));
      }
    });
    req.on("error", reject);
  });
}

const server = http.createServer(async (req, res) => {
  if (req.method === "OPTIONS") {
    res.writeHead(204, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    });
    return res.end();
  }

  const path = req.url.split("?")[0];

  if (req.method === "GET" && path === "/") {
    return json(res, 200, {
      ok: true,
      system: "MONARCH AI COLONY",
      head: "VERA",
      brand: "M&WEFTCO",
      status: "online"
    });
  }

  if (req.method === "GET" && path === "/api/aurelia/health") {
    return json(res, 200, {
      ok: true,
      agent: "AURELIA",
      brand: "M&WEFTCO",
      status: "ready"
    });
  }

  if (req.method === "GET" && path === "/api/aurelia/colony") {
    return json(res, 200, {
      ok: true,
      colony: "MONARCH AI COLONY",
      head: "VERA",
      agents,
      totalAgents: agents.length
    });
  }

  if (req.method === "GET" && path === "/api/aurelia/agents") {
    return json(res, 200, {
      ok: true,
      head: "VERA",
      agents,
      totalAgents: agents.length
    });
  }

  if (req.method === "GET" && path.startsWith("/api/aurelia/agent/")) {
    const id = path.split("/").pop();
    const agent = agents.find(a => a.id === id);

    if (!agent) {
      return json(res, 404, {
        ok: false,
        error: "Agent not found"
      });
    }

    return json(res, 200, {
      ok: true,
      agent
    });
  }

  if (req.method === "GET" && path === "/api/vera/dashboard") {
    return json(res, 200, {
      ok: true,
      system: "MONARCH AI COLONY",
      head: "VERA",
      totalAgents: agents.length,
      agents,
      commands: memory.commands.length,
      tasks: memory.tasks.length,
      courses: memory.courses.length,
      projects: memory.projects.length
    });
  }

  if (req.method === "GET" && path === "/api/vera/memory") {
    return json(res, 200, {
      ok: true,
      memory
    });
  }

  if (req.method === "POST" && path === "/api/vera/command") {
    try {
      const data = await body(req);

      if (!data.command) {
        return json(res, 400, {
          ok: false,
          error: "Command is required"
        });
      }

      const command = {
        id: `cmd_${Date.now()}`,
        command: data.command,
        from: "USER",
        receivedBy: "VERA",
        status: "received",
        createdAt: new Date().toISOString()
      };

      memory.commands.push(command);

      return json(res, 200, {
        ok: true,
        message: "VERA received the command",
        command
      });
    } catch {
      return json(res, 400, {
        ok: false,
        error: "Invalid JSON"
      });
    }
  }

  if (req.method === "POST" && path === "/api/vera/assign") {
    try {
      const data = await body(req);
      const agent = agents.find(a => a.id === data.agentId);

      if (!agent) {
        return json(res, 404, {
          ok: false,
          error: "Agent not found"
        });
      }

      agent.status = "working";

      const task = {
        id: `task_${Date.now()}`,
        agentId: agent.id,
        agent: agent.name,
        task: data.task || "New task",
        assignedBy: "VERA",
        status: "assigned"
      };

      memory.tasks.push(task);

      return json(res, 200, {
        ok: true,
        task
      });
    } catch {
      return json(res, 400, {
        ok: false,
        error: "Invalid JSON"
      });
    }
  }

  if (req.method === "POST" && path === "/api/vera/course") {
  try {
    const data = await body(req);

    if (!data.name) {
      return json(res, 400, {
        ok: false,
        error: "Course name is required"
      });
    }

    const agent = agents.find(a => a.id === data.agentId);

    if (!agent) {
      return json(res, 404, {
        ok: false,
        error: "Agent not found"
      });
    }

    const course = {
      id: `course_${Date.now()}`,
      name: data.name,
      agentId: agent.id,
      agent: agent.name,
      createdBy: "VERA",
      status: "active",
      createdAt: new Date().toISOString()
    };

    memory.courses.push(course);

    return json(res, 200, {
      ok: true,
      course
    });
  } catch {
    return json(res, 400, {
      ok: false,
      error: "Invalid JSON"
    });
  }
  }
  if (req.method === "GET" && path === "/api/vera/courses") {
    return json(res, 200, {
      ok: true,
      courses: memory.courses
    });
  }

  if (req.method === "GET" && path === "/api/vera/projects") {
    return json(res, 200, {
      ok: true,
      projects: memory.projects
    });
  }

  return json(res, 404, {
    ok: false,
    error: "Endpoint not found",
    path
  });
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`MONARCH AI COLONY running on port ${PORT}`);
});
