const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT || 3000;

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

let db = null;

/* =========================
   OPTIONAL POSTGRES
========================= */

async function initDatabase() {
  if (!process.env.DATABASE_URL) {
    console.log("DATABASE_URL not found - using temporary memory");
    return;
  }

  try {
    const { Pool } = require("pg");

    db = new Pool({
      connectionString: process.env.DATABASE_URL,
      ssl: {
        rejectUnauthorized: false
      }
    });

    await db.query(`
      CREATE TABLE IF NOT EXISTS monarch_commands (
        id TEXT PRIMARY KEY,
        command TEXT NOT NULL,
        sender TEXT,
        received_by TEXT,
        status TEXT,
        created_at TEXT
      );

      CREATE TABLE IF NOT EXISTS monarch_tasks (
        id TEXT PRIMARY KEY,
        agent_id TEXT,
        agent TEXT,
        task TEXT,
        assigned_by TEXT,
        status TEXT
      );

      CREATE TABLE IF NOT EXISTS monarch_courses (
        id TEXT PRIMARY KEY,
        name TEXT,
        agent_id TEXT,
        agent TEXT,
        created_by TEXT,
        status TEXT,
        created_at TEXT
      );

      CREATE TABLE IF NOT EXISTS monarch_projects (
        id TEXT PRIMARY KEY,
        name TEXT,
        description TEXT,
        agent_id TEXT,
        agent TEXT,
        created_by TEXT,
        status TEXT,
        created_at TEXT
      );
    `);

    console.log("MONARCH PostgreSQL connected");
  } catch (error) {
    console.log("PostgreSQL unavailable - using temporary memory");
    console.log(error.message);
    db = null;
  }
}

/* =========================
   JSON RESPONSE
========================= */

function json(res, code, data) {
  res.writeHead(code, {
    "Content-Type": "application/json; charset=utf-8",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
  });

  res.end(JSON.stringify(data, null, 2));
}

/* =========================
   REQUEST BODY
========================= */

function body(req) {
  return new Promise((resolve, reject) => {
    let data = "";

    req.on("data", chunk => {
      data += chunk;
    });

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

/* =========================
   SERVER
========================= */

const server = http.createServer(async (req, res) => {

  if (req.method === "OPTIONS") {
    res.writeHead(204, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    });

    return res.end();
  }

  const pathname = new URL(
    req.url,
    "http://localhost"
  ).pathname;

  /* =========================
     ROOT
  ========================= */

  if (req.method === "GET" && pathname === "/") {
    return json(res, 200, {
      ok: true,
      system: "MONARCH AI COLONY",
      head: "VERA",
      brand: "M&WEFTCO",
      status: "online",
      totalAgents: agents.length
    });
  }

  /* =========================
     AURELIA HEALTH
  ========================= */

  if (req.method === "GET" && pathname === "/api/aurelia/health") {
    return json(res, 200, {
      ok: true,
      agent: "AURELIA",
      brand: "M&WEFTCO",
      status: "ready"
    });
  }

  /* =========================
     AGENTS
  ========================= */

  if (req.method === "GET" && pathname === "/api/aurelia/agents") {
    return json(res, 200, {
      ok: true,
      head: "VERA",
      agents,
      totalAgents: agents.length
    });
  }

  if (req.method === "GET" && pathname === "/api/aurelia/colony") {
    return json(res, 200, {
      ok: true,
      colony: "MONARCH AI COLONY",
      head: "VERA",
      agents,
      totalAgents: agents.length
    });
  }

  if (
    req.method === "GET" &&
    pathname.startsWith("/api/aurelia/agent/")
  ) {
    const id = pathname.split("/").pop();

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

  /* =========================
     VERA DASHBOARD
  ========================= */

  if (req.method === "GET" && pathname === "/api/vera/dashboard") {
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

  /* =========================
     MEMORY
  ========================= */

  if (req.method === "GET" && pathname === "/api/vera/memory") {
    return json(res, 200, {
      ok: true,
      memory
    });
  }

  /* =========================
     COMMAND
  ========================= */

  if (req.method === "POST" && pathname === "/api/vera/command") {
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

      if (db) {
        await db.query(
          `INSERT INTO monarch_commands
          (id, command, sender, received_by, status, created_at)
          VALUES ($1,$2,$3,$4,$5,$6)`,
          [
            command.id,
            command.command,
            command.from,
            command.receivedBy,
            command.status,
            command.createdAt
          ]
        );
      }

      return json(res, 200, {
        ok: true,
        message: "VERA received the command",
        command
      });

    } catch (error) {
      return json(res, 400, {
        ok: false,
        error: "Invalid JSON"
      });
    }
  }

  /* =========================
     ASSIGN TASK
  ========================= */

  if (req.method === "POST" && pathname === "/api/vera/assign") {
    try {
      const data = await body(req);

      const agent = agents.find(
        a => a.id === data.agentId
      );

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

      if (db) {
        await db.query(
          `INSERT INTO monarch_tasks
          (id, agent_id, agent, task, assigned_by, status)
          VALUES ($1,$2,$3,$4,$5,$6)`,
          [
            task.id,
            task.agentId,
            task.agent,
            task.task,
            task.assignedBy,
            task.status
          ]
        );
      }

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

  /* =========================
     CREATE COURSE
  ========================= */

  if (req.method === "POST" && pathname === "/api/vera/course") {
    try {
      const data = await body(req);

      if (!data.name) {
        return json(res, 400, {
          ok: false,
          error: "Course name is required"
        });
      }

      const agent = agents.find(
        a => a.id === data.agentId
      );

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

      if (db) {
        await db.query(
          `INSERT INTO monarch_courses
          (id, name, agent_id, agent, created_by, status, created_at)
          VALUES ($1,$2,$3,$4,$5,$6,$7)`,
          [
            course.id,
            course.name,
            course.agentId,
            course.agent,
            course.createdBy,
            course.status,
            course.createdAt
          ]
        );
      }

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

  /* =========================
     COURSES
  ========================= */

  if (req.method === "GET" && pathname === "/api/vera/courses") {
    return json(res, 200, {
      ok: true,
      courses: memory.courses
    });
  }

  /* =========================
     CREATE PROJECT
  ========================= */

  if (req.method === "POST" && pathname === "/api/vera/project") {
    try {
      const data = await body(req);

      if (!data.name) {
        return json(res, 400, {
          ok: false,
          error: "Project name is required"
        });
      }

      const agent = agents.find(
        a => a.id === data.agentId
      );

      if (!agent) {
        return json(res, 404, {
          ok: false,
          error: "Agent not found"
        });
      }

      const project = {
        id: `project_${Date.now()}`,
        name: data.name,
        description: data.description || "",
        agentId: agent.id,
        agent: agent.name,
        createdBy: "VERA",
        status: "active",
        createdAt: new Date().toISOString()
      };

      memory.projects.push(project);

      if (db) {
        await db.query(
          `INSERT INTO monarch_projects
          (id, name, description, agent_id, agent, created_by, status, created_at)
          VALUES ($1,$2,$3,$4,$5,$6,$7,$8)`,
          [
            project.id,
            project.name,
            project.description,
            project.agentId,
            project.agent,
            project.createdBy,
            project.status,
            project.createdAt
          ]
        );
      }

      return json(res, 200, {
        ok: true,
        project
      });

    } catch {
      return json(res, 400, {
        ok: false,
        error: "Invalid JSON"
      });
    }
  }

  /* =========================
     PROJECTS
  ========================= */

  if (req.method === "GET" && pathname === "/api/vera/projects") {
    return json(res, 200, {
      ok: true,
      projects: memory.projects
    });
  }

  /* =========================
     STATIC WEBSITE
  ========================= */

  let filePath;

  if (pathname === "/") {
    filePath = path.join(__dirname, "index.html");
  } else {
    filePath = path.join(__dirname, pathname);
  }

  if (
    fs.existsSync(filePath) &&
    fs.statSync(filePath).isFile()
  ) {
    const ext = path.extname(filePath);

    const types = {
      ".html": "text/html",
      ".css": "text/css",
      ".js": "application/javascript",
      ".png": "image/png",
      ".jpg": "image/jpeg",
      ".jpeg": "image/jpeg",
      ".svg": "image/svg+xml"
    };

    res.writeHead(200, {
      "Content-Type":
        types[ext] || "application/octet-stream"
    });

    return fs.createReadStream(filePath).pipe(res);
  }

  return json(res, 404, {
    ok: false,
    error: "Endpoint not found",
    path: pathname
  });
});

/* =========================
   START
========================= */

server.listen(PORT, "0.0.0.0", async () => {
  console.log(
    `MONARCH AI COLONY running on port ${PORT}`
  );

  await initDatabase();
});
