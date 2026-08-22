const http = require("http");

const PORT = process.env.PORT || 8159;

/* =========================================================
   MONARCH AI COLONY
   VERA = CENTRAL COMMAND
   ========================================================= */

const colony = {
    name: "MONARCH AI COLONY",
    head: "vera",

    agents: [
        {
            id: "vera",
            name: "VERA",
            role: "Central Intelligence / Head AI",
            department: "Command",
            status: "working",
            location: "hq",
            task: "Managing the entire MONARCH AI Colony"
        },
        {
            id: "igris",
            name: "IGRIS",
            role: "Study & Skills",
            department: "Learning",
            status: "idle",
            location: "study_room",
            task: "Learning and developing skills"
        },
        {
            id: "beru",
            name: "BERU",
            role: "Fitness & Health",
            department: "Health",
            status: "idle",
            location: "fitness_room",
            task: "Managing fitness and health tasks"
        },
        {
            id: "bellion",
            name: "BELLION",
            role: "Faith & Mindset",
            department: "Mindset",
            status: "idle",
            location: "mindset_room",
            task: "Managing faith and mindset tasks"
        },
        {
            id: "greed",
            name: "GREED",
            role: "Income & Wealth",
            department: "Finance",
            status: "idle",
            location: "finance_room",
            task: "Learning income and wealth systems"
        },
        {
            id: "kaisel",
            name: "KAISEL",
            role: "Time & Utility",
            department: "Utility",
            status: "idle",
            location: "utility_room",
            task: "Managing time and utility tasks"
        },
        {
            id: "baran",
            name: "BARAN",
            role: "Company Growth",
            department: "Business",
            status: "idle",
            location: "business_room",
            task: "Managing company growth"
        },
        {
            id: "diwan",
            name: "DIWAN",
            role: "Documents, Notes & Social Content",
            department: "Documentation",
            status: "idle",
            location: "documents_room",
            task: "Managing documents, notes and social content"
        },
        {
            id: "aurelia",
            name: "AURELIA",
            role: "M&WEFTCO Creative & Growth Director",
            department: "M&WEFTCO Growth",
            status: "working",
            location: "aurelia_office",
            task: "Managing Instagram, Facebook and website growth"
        }
    ]
};


/* =========================================================
   RUNTIME MEMORY
   ========================================================= */

const memory = {
    tasks: [],
    courses: [],
    projects: [],
    commands: [],
    createdAgents: []
};


/* =========================================================
   HELPERS
   ========================================================= */

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


function readBody(req) {

    return new Promise((resolve, reject) => {

        let body = "";

        req.on("data", chunk => {
            body += chunk;
        });

        req.on("end", () => {

            if (!body) {
                resolve({});
                return;
            }

            try {
                resolve(JSON.parse(body));
            } catch (error) {
                reject(error);
            }
        });

        req.on("error", reject);
    });
}


function findAgent(id) {

    return colony.agents.find(
        agent => agent.id === String(id).toLowerCase()
    );
}


/* =========================================================
   SERVER
   ========================================================= */

const server = http.createServer(async (req, res) => {

    /* -----------------------------------------------------
       CORS
       ----------------------------------------------------- */

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


    /* =====================================================
       HEALTH
       ===================================================== */

    if (req.method === "GET" &&
        path === "/api/aurelia/health") {

        sendJSON(res, 200, {

            ok: true,

            agent: "AURELIA",

            brand: "M&WEFTCO",

            status: "ready",

            colony: colony.name,

            head: "VERA"

        });

        return;
    }


    /* =====================================================
       COLONY STATUS
       ===================================================== */

    if (req.method === "GET" &&
        path === "/api/aurelia/colony") {

        sendJSON(res, 200, {

            ok: true,

            colony: colony.name,

            head: colony.head,

            agents: colony.agents,

            totalAgents: colony.agents.length

        });

        return;
    }


    /* =====================================================
       ALL AGENTS
       ===================================================== */

    if (req.method === "GET" &&
        path === "/api/aurelia/agents") {

        sendJSON(res, 200, {

            ok: true,

            head: "VERA",

            agents: colony.agents,

            totalAgents: colony.agents.length

        });

        return;
    }


    /* =====================================================
       SINGLE AGENT
       ===================================================== */

    if (
        req.method === "GET" &&
        path.startsWith("/api/aurelia/agent/")
    ) {

        const id = path.split("/").pop();

        const agent = findAgent(id);

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


    /* =====================================================
       VERA DASHBOARD
       ===================================================== */

    if (
        req.method === "GET" &&
        path === "/api/vera/dashboard"
    ) {

        sendJSON(res, 200, {

            ok: true,

            system: colony.name,

            head: "VERA",

            totalAgents: colony.agents.length,

            agents: colony.agents,

            activeTasks: memory.tasks.length,

            courses: memory.courses.length,

            projects: memory.projects.length,

            commands: memory.commands.length

        });

        return;
    }


    /* =====================================================
       VERA COMMAND
       ===================================================== */

    if (
        req.method === "POST" &&
        path === "/api/vera/command"
    ) {

        try {

            const body = await readBody(req);

            const command = body.command || body.message || "";

            if (!command.trim()) {

                sendJSON(res, 400, {

                    ok: false,

                    error: "Command is required"

                });

                return;
            }


            const commandRecord = {

                id: `cmd_${Date.now()}`,

                command: command,

                from: "USER",

                receivedBy: "VERA",

                status: "received",

                timestamp: new Date().toISOString()

            };


            memory.commands.push(commandRecord);


            sendJSON(res, 200, {

                ok: true,

                system: "MONARCH AI COLONY",

                head: "VERA",

                message: "Command received by VERA",

                command: commandRecord

            });

        } catch (error) {

            sendJSON(res, 400, {

                ok: false,

                error: "Invalid JSON body"

            });
        }

        return;
    }


    /* =====================================================
       ASSIGN TASK
       ===================================================== */

    if (
        req.method === "POST" &&
        path === "/api/vera/assign"
    ) {

        try {

            const body = await readBody(req);

            const agentId = body.agentId;

            const task = body.task;

            if (!agentId || !task) {

                sendJSON(res, 400, {

                    ok: false,

                    error: "agentId and task are required"

                });

                return;
            }


            const agent = findAgent(agentId);


            if (!agent) {

                sendJSON(res, 404, {

                    ok: false,

                    error: "Agent not found"

                });

                return;
            }


            agent.status = "working";

            agent.task = task;


            const taskRecord = {

                id: `task_${Date.now()}`,

                assignedBy: "VERA",

                agent: agent.name,

                agentId: agent.id,

                task: task,

                status: "assigned",

                createdAt: new Date().toISOString()

            };


            memory.tasks.push(taskRecord);


            sendJSON(res, 200, {

                ok: true,

                message: `VERA assigned a task to ${agent.name}`,

                task: taskRecord

            });

        } catch (error) {

            sendJSON(res, 400, {

                ok: false,

                error: "Invalid JSON body"

            });
        }

        return;
    }


    /* =====================================================
       CREATE COURSE
       ===================================================== */

    if (
        req.method === "POST" &&
        path === "/api/vera/course"
    ) {

        try {

            const body = await readBody(req);

            const course = {

                id: `course_${Date.now()}`,

                name: body.name || "Untitled Course",

                agentId: body.agentId || null,

                agent: body.agentId
                    ? (findAgent(body.agentId)?.name || "Unknown")
                    : "Unassigned",

                progress: 0,

                status: "not_started",

                notes: [],

                createdBy: "VERA",

                createdAt: new Date().toISOString()

            };


            memory.courses.push(course);


            sendJSON(res, 201, {

                ok: true,

                message: "Course created by VERA",

                course

            });

        } catch (error) {

            sendJSON(res, 400, {

                ok: false,

                error: "Invalid JSON body"

            });
        }

        return;
    }


    /* =====================================================
       GET COURSES
       ===================================================== */

    if (
        req.method === "GET" &&
        path === "/api/vera/courses"
    ) {

        sendJSON(res, 200, {

            ok: true,

            total: memory.courses.length,

            courses: memory.courses

        });

        return;
    }


    /* =====================================================
       CREATE PROJECT
       ===================================================== */

    if (
        req.method === "POST" &&
        path === "/api/vera/project"
    ) {

        try {

            const body = await readBody(req);

            const project = {

                id: `project_${Date.now()}`,

                name: body.name || "Untitled Project",

                description: body.description || "",

                agentId: body.agentId || null,

                agent: body.agentId
                    ? (findAgent(body.agentId)?.name || "Unknown")
                    : "Unassigned",

                status: "planned",

                createdBy: "VERA",

                createdAt: new Date().toISOString()

            };


            memory.projects.push(project);


            sendJSON(res, 201, {

                ok: true,

                message: "Project created by VERA",

                project

            });

        } catch (error) {

            sendJSON(res, 400, {

                ok: false,

                error: "Invalid JSON body"

            });
        }

        return;
    }


    /* =====================================================
       GET PROJECTS
       ===================================================== */

    if (
        req.method === "GET" &&
        path === "/api/vera/projects"
    ) {

        sendJSON(res, 200, {

            ok: true,

            total: memory.projects.length,

            projects: memory.projects

        });

        return;
    }


    /* =====================================================
       CREATE NEW AGENT
       ===================================================== */

    if (
        req.method === "POST" &&
        path === "/api/vera/create-agent"
    ) {

        try {

            const body = await readBody(req);

            const id = String(body.id || "")
                .trim()
                .toLowerCase();

            const name = String(body.name || "")
                .trim();

            if (!id || !name) {

                sendJSON(res, 400, {

                    ok: false,

                    error: "id and name are required"

                });

                return;
            }


            if (findAgent(id)) {

                sendJSON(res, 409, {

                    ok: false,

                    error: "Agent already exists"

                });

                return;
            }


            const newAgent = {

                id: id,

                name: name,

                role: body.role || "AI Agent",

                department: body.department || "General",

                status: "idle",

                location: body.location || "new_agent_room",

                task: body.task || "Waiting for task",

                createdBy: "VERA",

                createdAt: new Date().toISOString()

            };


            colony.agents.push(newAgent);

            memory.createdAgents.push(newAgent);


            sendJSON(res, 201, {

                ok: true,

                message: "VERA created a new agent",

                agent: newAgent,

                totalAgents: colony.agents.length

            });

        } catch (error) {

            sendJSON(res, 400, {

                ok: false,

                error: "Invalid JSON body"

            });
        }

        return;
    }


    /* =====================================================
       MEMORY / SYSTEM STATE
       ===================================================== */

    if (
        req.method === "GET" &&
        path === "/api/vera/memory"
    ) {

        sendJSON(res, 200, {

            ok: true,

            memory: {

                tasks: memory.tasks,

                courses: memory.courses,

                projects: memory.projects,

                commands: memory.commands,

                createdAgents: memory.createdAgents

            }

        });

        return;
    }


    /* =====================================================
       UNKNOWN ENDPOINT
       ===================================================== */

    sendJSON(res, 404, {

        ok: false,

        error: "Endpoint not found",

        system: "MONARCH AI COLONY",

        head: "VERA"

    });

});


/* =========================================================
   START SERVER
   ========================================================= */

server.listen(PORT, "0.0.0.0", () => {

    console.log(
        `👑 MONARCH AI COLONY running on port ${PORT}`
    );

    console.log(
        `🧠 VERA Central Command active`
    );

    console.log(
        `🤖 Agents online: ${colony.agents.length}`
    );

});
