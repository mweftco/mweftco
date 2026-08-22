const http = require("http");

const PORT = process.env.PORT || 8159;

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

    // HEALTH
    if (req.method === "GET" && path === "/api/aurelia/health") {
        sendJSON(res, 200, {
            ok: true,
            agent: "AURELIA",
            brand: "M&WEFTCO",
            status: "ready"
        });
        return;
    }

    // COLONY
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

    // ALL AGENTS
    if (req.method === "GET" && path === "/api/aurelia/agents") {
        sendJSON(res, 200, {
            ok: true,
            head: colony.head,
            agents: colony.agents
        });
        return;
    }

    // SINGLE AGENT
    if (
        req.method === "GET" &&
        path.startsWith("/api/aurelia/agent/")
    ) {
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

    // UNKNOWN
    sendJSON(res, 404, {
        ok: false,
        error: "Endpoint not found"
    });
});

server.listen(PORT, "0.0.0.0", () => {
    console.log(
        `👑 MONARCH AI COLONY running on port ${PORT}`
    );
});
