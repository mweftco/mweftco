// ============================================================
// AGENTS.JS v6 — Shadow Army: Colony Project + Bigger Vera HQ
// + Wider lit corridor + per-agent work lights + car travel + salam ritual
// ============================================================
(function () {
    "use strict";

    let AGENTS = [
        {
            id: "igris",
            name: "Igris",
            icon: "⚔️",
            color: "#3b82f6",
            role: "Study & Skills",
            keywords: [
                "html",
                "css",
                "javascript",
                "course",
                "study",
                "learn",
                "padhai",
                "skill",
                "seekh"
            ]
        },
        {
            id: "beru",
            name: "Beru",
            icon: "🐜",
            color: "#22c55e",
            role: "Fitness & Health",
            keywords: [
                "gym",
                "workout",
                "health",
                "hp",
                "fitness",
                "exercise",
                "body"
            ]
        },
        {
            id: "bellion",
            name: "Bellion",
            icon: "💀",
            color: "#a259ff",
            role: "Faith & Mindset",
            keywords: [
                "namaz",
                "dua",
                "salah",
                "pray",
                "faith",
                "sad",
                "dukhi",
                "stress",
                "motivate",
                "motivation",
                "depressed"
            ]
        },
        {
            id: "greed",
            name: "Greed",
            icon: "💰",
            color: "#eab308",
            role: "Income & Wealth",
            keywords: [
                "money",
                "income",
                "coin",
                "coins",
                "paisa",
                "billionaire",
                "rich",
                "earning"
            ]
        },
        {
            id: "kaisel",
            name: "Kaisel",
            icon: "🐉",
            color: "#ef4444",
            role: "Time & Utility",
            keywords: ["time", "date", "weather", "mausam", "kitna baje"]
        },
        {
            id: "vera",
            name: "Vera",
            icon: "👑",
            color: "#00bfff",
            role: "Head of Shadow Army — Personal Monarch AI",
            keywords: []
        },
        {
            id: "baran",
            name: "Baran",
            icon: "📈",
            color: "#f59e0b",
            role: "Company Growth",
            keywords: [
                "company",
                "business",
                "growth",
                "marketing",
                "customer",
                "sales",
                "clients"
            ]
        },
        {
            id: "diwan",
            name: "Diwan",
            icon: "🗂️",
            color: "#0ea5e9",
            role: "Documents, Notes & Social Content Manager",
            keywords: [
                "document",
                "note",
                "notes",
                "save karo",
                "pdf banao",
                "record",
                "reel",
                "reels",
                "instagram",
                "youtube",
                "facebook",
                "social media"
            ]
        }
    ];
    let SMALL_AGENTS = AGENTS.filter(a => a.id !== "vera");
    const VERA = AGENTS.find(a => a.id === "vera");
    const agentState = {};
    AGENTS.forEach(a => {
        agentState[a.id] = "idle";
    });
    let anyoneWorking = false;
    let activeTravelers = 0;

    /* ---------------- styles ---------------- */
    const style = document.createElement("style");
    style.textContent = `
    #agentRoomsWrap { display:flex; flex-wrap:wrap; gap:10px; justify-content:center; margin:10px 0 4px; }
    .agent-room {
      width: 132px; height: 190px;
      border-radius: 14px;
      background: linear-gradient(180deg, #12161d, #090b0f);
      border: 1px solid #232830;
      position: relative; overflow: hidden;
      padding-top: 4px; text-align: center;
      transition: border-color .3s ease, box-shadow .3s ease;
    }
    .agent-room .room-name { font-size: 11px; font-weight: 700; color: #9fb0c0; }
    .agent-room .room-bond { font-size: 8px; color: #ffd54f; letter-spacing: 1px; margin-top: 1px; }
    .agent-room .room-badge { position: absolute; top: 3px; right: 6px; font-size: 13px; }
    .agent-room .room-light-bulb { position:absolute; top:4px; left:6px; width:7px; height:7px; border-radius:50%; background:#3a3f47; transition: all .3s ease; }
    .agent-room.working .room-light-bulb { background:#ffd54f; box-shadow:0 0 7px #ffd54f; }
    .agent-room .room-scene { position: relative; height: 138px; margin-top: 2px; }
    .room-gate { position: absolute; top: 50%; transform: translateY(-50%); font-size: 14px; opacity: .55; }
    .room-gate.left { left: 2px; } .room-gate.right { right: 2px; }
    .agent-room .room-desk { position: absolute; bottom: 14px; left: 50%; transform: translateX(-50%); width: 66px; height: 7px; background:#333a44; border-radius:2px; }
    .agent-room .room-laptop { position:absolute; bottom:19px; left:50%; transform:translateX(-50%); width:24px; text-align:center; }
    .agent-room .laptop-screen { width:18px; height:12px; margin:0 auto; background:#12222c; border:1px solid #3a4048; border-radius:2px 2px 0 0; transition:all .3s ease; }
    .agent-room .laptop-base { width:24px; height:3px; background:#4a505a; border-radius:1px; margin-top:1px; }
    .agent-room .room-chairs { position:absolute; bottom:5px; left:50%; transform:translateX(-50%); display:flex; gap:2.5px; }
    .agent-room .room-chairs .chair-mini { width:10px; height:7px; background:#262b32; border-top:2px solid #333c47; border-radius:1px; }
    .agent-room .room-bed { position:absolute; top:8px; left:50%; transform:translateX(-50%); width:58px; height:20px; background:#20262f; border:1px solid #333c47; border-radius:4px; }
    .agent-room .room-bed::before { content:""; position:absolute; top:2px; left:3px; width:14px; height:10px; background:#3a4552; border-radius:3px; }
    .robot { width: 34px; margin: 0 auto; position: relative; transition: transform .35s ease, opacity .35s ease, bottom .35s ease; }
    .robot-antenna { width:2px; height:6px; background:#888; margin:0 auto; position:relative; }
    .robot-antenna .antenna-dot { position:absolute; top:-4px; left:-2px; width:6px; height:6px; border-radius:50%; background:var(--accent,#00bfff); box-shadow:0 0 4px var(--accent,#00bfff); }
    .robot-head { width:22px; height:16px; background:#cbd5e1; border:1px solid #94a3b8; border-radius:4px; margin:0 auto; position:relative; transition:transform .3s ease; }
    .robot-eye { position:absolute; top:6px; width:4px; height:4px; border-radius:50%; background:#ef4444; transition:all .3s ease; }
    .robot-eye.left { left:4px; } .robot-eye.right { right:4px; }
    .robot-mouth { position:absolute; bottom:2px; left:50%; transform:translateX(-50%); width:8px; height:2px; background:#475569; border-radius:1px; }
    .robot-body { width:26px; height:18px; background:var(--accent,#475569); border-radius:4px; margin:1px auto 0; position:relative; transition:box-shadow .3s ease; }
    .robot-arm { position:absolute; top:2px; width:5px; height:12px; background:#64748b; border-radius:2px; }
    .robot-arm.left { left:-6px; } .robot-arm.right { right:-6px; }
    .robot-legs { display:flex; justify-content:center; gap:4px; margin-top:1px; }
    .robot-leg { width:6px; height:8px; background:#334155; border-radius:1px; }
    .agent-room .robot { position:absolute; bottom:70px; left:50%; transform:translateX(-50%); animation: robotIdle 2.2s ease-in-out infinite; }
    @keyframes robotIdle { 0%,100% { transform:translateX(-50%) translateY(0); } 50% { transform:translateX(-50%) translateY(-3px); } }
    .agent-room.working { box-shadow:0 0 14px rgba(0,191,255,.35); border-color:#00bfff; }
    .agent-room.working .robot { bottom:24px; animation: robotType .35s ease-in-out infinite alternate; }
    @keyframes robotType { from { transform:translateX(-50%) translateY(0); } to { transform:translateX(-50%) translateY(2px); } }
    .agent-room.working .laptop-screen { background:#00bfff; box-shadow:0 0 10px rgba(0,191,255,.9); animation: screenFlicker .5s infinite alternate; }
    @keyframes screenFlicker { from { opacity:.7; } to { opacity:1; } }
    .agent-room.done { border-color:#29e07a; box-shadow:0 0 14px rgba(41,224,122,.4); }
    .agent-room.sleeping .robot { bottom: auto; top: 14px; transform: translateX(-50%) rotate(90deg); animation:none; }
    .agent-room.sleeping .robot-eye { height:1px; top:8px; border-radius:0; background:#64748b; }
    .agent-room.away .robot { opacity:.12; }
    .room-status { font-size:9px; color:#7fd1ff; min-height:24px; padding:1px 5px; line-height:1.3; }

    #veraHQ {
      width: 100%; max-width: 480px; margin: 4px auto 14px;
      border-radius: 18px; padding: 18px;
      background: linear-gradient(160deg,#0c1420,#070a10);
      border: 1px solid #00bfff55; box-shadow: 0 0 26px rgba(0,191,255,.2);
      position: relative;
    }
    #veraHQ .hq-corner { position:absolute; width:9px; height:9px; border-radius:50%; background:#ffd54f; box-shadow:0 0 12px #ffd54f, 0 0 22px rgba(255,213,79,.5); }
    #veraHQ .hq-corner.tl { top:8px; left:8px; } #veraHQ .hq-corner.tr { top:8px; right:8px; }
    #veraHQ .hq-corner.bl { bottom:8px; left:8px; } #veraHQ .hq-corner.br { bottom:8px; right:8px; }
    #veraRoomsRow { display:flex; gap:12px; margin-bottom:10px; }
    .vera-room { flex:1; background:#0a0f18; border:1px solid #1c2734; border-radius:12px; padding:10px; position:relative; min-height:150px; transition: opacity .3s ease; }
    .vera-room .vera-room-label { font-size:10px; color:#7fd1ff; text-align:center; margin-bottom:6px; letter-spacing:.5px; }
    .vera-room.vera-work .hq-corner { width:8px; height:8px; }
    .vera-room .vera-avatar-slot { text-align:center; margin:8px 0 4px; min-height:44px; }
    .vera-room .vera-avatar-slot .robot { width:40px; margin:0 auto; }
    .vera-room.vera-work .vera-avatar-slot .robot.typing { animation: robotType .3s ease-in-out infinite alternate; }
    .vera-room.dim { opacity:.35; }
    .vera-room.vera-sleep .sleep-bed { width:80%; height:38px; margin:6px auto 0; background:#171e28; border:1px solid #263042; border-radius:8px; position:relative; }
    .vera-room.vera-sleep .sleep-bed::before { content:""; position:absolute; top:4px; left:6px; width:22px; height:16px; background:#2a3546; border-radius:5px; }
    .cctv-wall { display:grid; grid-template-columns: repeat(5, 1fr); gap:4px; margin-bottom:8px; }
    .cctv-tile { background:#050708; border:1px solid #1c2734; border-radius:5px; padding:3px 1px; text-align:center; position:relative; }
    .cctv-tile .cctv-icon { font-size:13px; }
    .cctv-tile .cctv-dot { width:5px; height:5px; border-radius:50%; margin:2px auto 0; background:#3a4552; }
    .cctv-tile .cctv-dot.working { background:#00bfff; box-shadow:0 0 5px #00bfff; }
    .cctv-tile .cctv-dot.sleeping { background:#7c3aed; }
    .cctv-tile .cctv-dot.away { background:#facc15; }
    .cctv-tile .cctv-dot.idle { background:#3a4552; }
    .cctv-caption { text-align:center; font-size:9px; color:#7fd1ff; margin-bottom:6px; }
    #veraHQ .hq-title { color:#00bfff; font-weight:800; font-size:15px; text-align:center; margin-bottom:10px; letter-spacing:1px; }
    #veraHQ .hq-body { display:flex; gap:14px; align-items:flex-start; }
    #veraHQ .hq-screen {
      flex:1; background:#000; border:2px solid #1e293b; border-radius:10px;
      height:130px; display:flex; align-items:center; justify-content:center; overflow:hidden; position:relative;
    }
    #veraHQ .hq-screen video { width:100%; height:100%; object-fit:cover; }
    #veraHQ .hq-cam-btn { margin-top:8px; font-size:11px; background:#0f2233; color:#7fd1ff; border:1px solid #00bfff55; border-radius:6px; padding:6px 8px; width:100%; }
    #veraHQ .hq-decor { display:flex; gap:8px; margin-top:14px; justify-content:center; align-items:flex-end; }
    #veraHQ .hq-cabinet { width:34px; height:46px; background:#141b25; border:1px solid #2a3542; border-radius:4px; position:relative; }
    #veraHQ .hq-cabinet::before, #veraHQ .hq-cabinet::after { content:""; position:absolute; left:3px; right:3px; height:1px; background:#2a3542; }
    #veraHQ .hq-cabinet::before { top:15px; } #veraHQ .hq-cabinet::after { top:30px; }
    #veraHQ .hq-files { width:26px; height:34px; background:#1a2230; border-radius:2px; transform:rotate(-6deg); border:1px solid #2a3542; }
    #veraHQ .hq-sofa { width:58px; height:26px; background:#182231; border:1px solid #2a3542; border-radius:8px 8px 4px 4px; position:relative; }
    #veraHQ .hq-sofa::before { content:""; position:absolute; top:-8px; left:0; right:0; height:10px; background:#1e2a3c; border-radius:8px 8px 0 0; }
    #veraHQ .hq-parking { margin-top:12px; text-align:center; font-size:12px; color:#7fd1ff; background:#0f1622; border:1px dashed #2a3542; border-radius:10px; padding:8px; }
    #veraHQ .hq-parking-car { font-size:28px; display:block; }
    #veraHQ .hq-parking-label { font-size:10px; opacity:.7; }
    #veraHQ .hq-activity-badge { font-size:17px; margin-top:6px; }
    #veraHQ .hq-status { text-align:center; font-size:10px; color:#7fd1ff; margin-top:8px; min-height:16px; }
    #veraHQ .hq-colony { margin-top:10px; background:#0f1622; border:1px solid #2a3542; border-radius:10px; padding:8px; font-size:10px; color:#ffd54f; text-align:center; display:none; }
    #veraHQ .hq-colony.show { display:block; }
    #veraHQ .hq-colony-bar { height:5px; border-radius:3px; background:#232830; margin-top:5px; overflow:hidden; }
    #veraHQ .hq-colony-bar-fill { height:100%; background:#ffd54f; width:0%; transition: width .5s ease; }

    .car-travel { position:absolute; top:0; font-size:24px; transform:translateX(-50%); transition:left 1.5s linear; z-index:25; }

    #agentCorridor { position:relative; height:52px; margin:0 6px 18px; border-top:2px dashed #2a2f37; background: linear-gradient(180deg, rgba(255,255,255,.015), transparent); }
    #agentCorridor .corridor-label { position:absolute; top:4px; left:6px; font-size:9px; color:#4b5563; }
    #agentCorridor .corridor-light { position:absolute; top:26px; width:7px; height:7px; border-radius:50%; background:#3a3f47; transition: all .3s ease; }
    #agentCorridor.lights-on .corridor-light { background:#ffd54f; box-shadow:0 0 9px #ffd54f; }
    .robot.traveling { position:absolute; top:6px; transform:translateX(-50%); transition:left 1.5s linear; z-index:20; }
    .robot.traveling .robot-legs { animation: legWalk .3s infinite alternate; }
    @keyframes legWalk { from { transform:translateY(0); } to { transform:translateY(1px); } }
    .visit-bubble { position:absolute; top:-16px; left:50%; transform:translateX(-50%); font-size:13px; opacity:0; transition:opacity .3s ease; }
    .visit-bubble.show { opacity:1; }
    .envelope-fly { position:absolute; font-size:20px; z-index:32; pointer-events:none; transition:all .9s ease; }
  `;
    document.head.appendChild(style);

    function robotInnerHTML() {
        return `
      <div class="robot-antenna"><span class="antenna-dot"></span></div>
      <div class="robot-head">
        <div class="robot-eye left"></div>
        <div class="robot-eye right"></div>
        <div class="robot-mouth"></div>
      </div>
      <div class="robot-body"></div>
      <div class="robot-arm left"></div>
      <div class="robot-arm right"></div>
      <div class="robot-legs">
        <div class="robot-leg left"></div>
        <div class="robot-leg right"></div>
      </div>
    `;
    }

    function createRoomElement(a) {
        return `
      <div class="agent-room" id="room-${a.id}" title="${a.role}" style="--accent:${a.color}; border-color:${a.color}33">
        <span class="room-gate left">🚪</span>
        <span class="room-gate right">🚪</span>
        <div class="room-light-bulb"></div>
        <div class="room-badge">${a.icon}</div>
        <div class="room-name">${a.name}</div>
        <div class="room-bond" id="bond-${a.id}">☆☆☆☆☆</div>
        <div class="room-scene">
          <div class="room-bed"></div>
          <div class="robot" id="avatar-${a.id}" style="--accent:${a.color}">${robotInnerHTML()}</div>
          <div class="room-desk"></div>
          <div class="room-laptop"><div class="laptop-screen"></div><div class="laptop-base"></div></div>
          <div class="room-chairs">
            <div class="chair-mini"></div>
            <div class="chair-mini"></div>
            <div class="chair-mini"></div>
            <div class="chair-mini"></div>
            <div class="chair-mini"></div>
          </div>
        </div>
        <div class="room-status" id="status-${a.id}"></div>
      </div>
    `;
    }

    function buildRooms() {
        if (document.getElementById("agentRoomsWrap")) return;
        const panel = document.getElementById("monarchAI");
        const chat = document.getElementById("aiChat");
        if (!panel) return;

        const hq = document.createElement("div");
        hq.id = "veraHQ";
        hq.innerHTML = `
      <div class="hq-title">👑 VERA HQ — Shadow Monarch Command Rooms</div>
      <div class="hq-screen" id="hqScreen">
        <span style="color:#334155;font-size:11px;">📷 Camera Off</span>
      </div>
      <button class="hq-cam-btn" id="hqCamBtn">📷 Camera ON (Vera aapko dekh sake)</button>
      <button class="hq-cam-btn" id="hqNotesBtn" style="margin-top:6px;">🖼️ Notes Upload (handwriting padhne ke liye)</button>
      <input type="file" id="hqNotesInput" accept="image/*" style="display:none;" />
      <div class="hq-cam-btn" id="hqNotesStatus" style="margin-top:6px; text-align:center; pointer-events:none;"></div>
      <div class="cctv-caption">👁 Vera sabhi Shadows ko dekh rahi hai</div>
      <div class="cctv-wall" id="cctvWall"></div>
      <div id="veraRoomsRow">
        <div class="vera-room vera-work" id="veraWorkRoom">
          <div class="vera-room-label">💻 Work Room</div>
          <div class="hq-corner tl"></div>
          <div class="hq-corner tr"></div>
          <div class="hq-corner bl"></div>
          <div class="hq-corner br"></div>
          <div class="vera-avatar-slot" id="veraWorkAvatarSlot"></div>
          <div class="hq-decor">
            <div class="hq-cabinet" title="Almirah"></div>
            <div class="hq-files"></div>
            <div class="hq-sofa" title="Sofa"></div>
          </div>
        </div>
        <div class="vera-room vera-sleep" id="veraSleepRoom">
          <div class="vera-room-label">🛏 Sleep Room</div>
          <div class="vera-avatar-slot" id="veraSleepAvatarSlot"></div>
          <div class="sleep-bed"></div>
        </div>
      </div>
      <div class="hq-parking">
        <span class="hq-parking-car">🚗</span>
        <span class="hq-parking-label">Vera's Car — Parking</span>
      </div>
      <div class="hq-colony" id="hqColony">
        <div id="hqColonyLabel">Colony project idle</div>
        <div class="hq-colony-bar"><div class="hq-colony-bar-fill" id="hqColonyBarFill"></div></div>
      </div>
      <div class="hq-status" id="status-vera"></div>
    `;

        const wrap = document.createElement("div");
        wrap.id = "agentRoomsWrap";
        wrap.innerHTML = SMALL_AGENTS.map(a => createRoomElement(a)).join("");

        const corridor = document.createElement("div");
        corridor.id = "agentCorridor";
        corridor.innerHTML =
            `<span class="corridor-label">↔ raasta</span>` +
            Array.from({ length: 7 })
                .map(
                    (_, i) =>
                        `<span class="corridor-light" style="left:${8 + i * 14}%"></span>`
                )
                .join("");

        if (chat && chat.parentNode) {
            chat.parentNode.insertBefore(hq, chat);
            chat.parentNode.insertBefore(wrap, chat);
            chat.parentNode.insertBefore(corridor, chat);
        } else {
            panel.appendChild(hq);
            panel.appendChild(wrap);
            panel.appendChild(corridor);
        }

        SMALL_AGENTS.forEach(a => {
            renderBond(a.id);
            addCctvTile(a);
        });
        cycleVeraActivity();
        updateColonyWidget();
        checkColonyOnLoad();

        const camBtn = document.getElementById("hqCamBtn");
        const hqScreen = document.getElementById("hqScreen");
        if (camBtn) {
            camBtn.addEventListener("click", async () => {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({
                        video: true
                    });
                    hqScreen.innerHTML = `<video autoplay muted playsinline></video>`;
                    hqScreen.querySelector("video").srcObject = stream;
                    camBtn.innerText = "📷 Camera ON ✅";
                } catch (e) {
                    alert(
                        "❌ Camera access nahi mili. Browser permission check karo."
                    );
                }
            });
        }

        const notesBtn = document.getElementById("hqNotesBtn");
        const notesInput = document.getElementById("hqNotesInput");
        const notesStatus = document.getElementById("hqNotesStatus");
        if (notesBtn && notesInput) {
            notesBtn.addEventListener("click", () => notesInput.click());
            notesInput.addEventListener("change", e => {
                const file = e.target.files && e.target.files[0];
                if (file) handleNotesFile(file, notesStatus);
            });
        }
    }

    function roomEl(id) {
        return id === "vera"
            ? document.getElementById("veraHQ")
            : document.getElementById("room-" + id);
    }
    function statusEl(id) {
        return document.getElementById("status-" + id);
    }
    function addCctvTile(a) {
        const wall = document.getElementById("cctvWall");
        if (!wall || document.getElementById("cctv-" + a.id)) return;
        const tile = document.createElement("div");
        tile.className = "cctv-tile";
        tile.id = "cctv-" + a.id;
        tile.innerHTML = `<div class="cctv-icon">${a.icon}</div><div class="cctv-dot idle" id="cctv-dot-${a.id}"></div>`;
        wall.appendChild(tile);
    }
    function updateCctvDot(id) {
        const dot = document.getElementById("cctv-dot-" + id);
        if (!dot) return;
        dot.className = "cctv-dot " + (agentState[id] || "idle");
    }

    /* ---------- Bond / Loyalty system ---------- */
    function getBond(id) {
        return Number(localStorage.getItem("shadowBond_" + id)) || 0;
    }
    function addBond(id, amount) {
        const v = getBond(id) + amount;
        localStorage.setItem("shadowBond_" + id, v);
        renderBond(id);
    }
    function renderBond(id) {
        const el = document.getElementById("bond-" + id);
        if (!el) return;
        const count = getBond(id);
        const level = Math.min(5, Math.floor(count / 5));
        el.innerText = "⭐".repeat(level) + "☆".repeat(5 - level);
        el.title = `Bond Level ${level}/5 — ${count} interactions`;
    }

    function setState(id, state, statusText) {
        agentState[id] = state;
        const el = roomEl(id);
        if (id !== "vera" && el) {
            el.classList.remove("working", "done", "sleeping", "away");
            if (state === "working") el.classList.add("working");
            if (state === "sleeping") el.classList.add("sleeping");
            if (state === "away") el.classList.add("away");
            updateCctvDot(id);
        }
        if (id === "vera") {
            if (state === "idle") cycleVeraActivity();
        }
        const s = statusEl(id);
        if (s && statusText !== undefined) s.innerText = statusText;
    }

    /* ---------- Vera idle activities — Work Room / Sleep Room ke beech move karti hai ---------- */
    const VERA_ACTIVITIES = [
        {
            icon: "🛏",
            text: "Sleep Room me aaram kar rahi hai",
            sleeping: true
        },
        {
            icon: "💻",
            text: "Work Room me desk par kaam kar rahi hai",
            sleeping: false
        },
        {
            icon: "📄",
            text: "Work Room me file padh rahi hai",
            sleeping: false
        },
        {
            icon: "💾",
            text: "Work Room me document save kar rahi hai",
            sleeping: false
        }
    ];
    let veraActivityIndex = 0;
    function cycleVeraActivity() {
        if (agentState["vera"] !== "idle") return;
        const cp = loadColonyProject();
        if (cp && !cp.completed) return; // colony status label takes over
        const act = VERA_ACTIVITIES[veraActivityIndex % VERA_ACTIVITIES.length];
        veraActivityIndex++;
        const s = statusEl("vera");
        if (s) s.innerText = `${act.icon} ${act.text}`;
        placeVeraInRoom(act);
    }
    function placeVeraInRoom(act) {
        const workSlot = document.getElementById("veraWorkAvatarSlot");
        const sleepSlot = document.getElementById("veraSleepAvatarSlot");
        const workRoom = document.getElementById("veraWorkRoom");
        const sleepRoom = document.getElementById("veraSleepRoom");
        if (!workSlot || !sleepSlot) return;
        if (act.sleeping) {
            sleepSlot.innerHTML = `<div class="robot" id="avatar-vera" style="--accent:${VERA.color}">${robotInnerHTML()}</div>`;
            workSlot.innerHTML = "";
            workRoom.classList.add("dim");
            sleepRoom.classList.remove("dim");
        } else {
            workSlot.innerHTML = `<div class="robot typing" id="avatar-vera" style="--accent:${VERA.color}">${robotInnerHTML()}</div><div style="font-size:15px;margin-top:3px;">${act.icon}</div>`;
            sleepSlot.innerHTML = "";
            sleepRoom.classList.add("dim");
            workRoom.classList.remove("dim");
        }
    }
    setInterval(cycleVeraActivity, 15000);

    function findMentions(text) {
        const t = text.toLowerCase();
        const found = [];
        AGENTS.forEach(a => {
            const iId = t.indexOf(a.id);
            const iName = t.indexOf(a.name.toLowerCase());
            let idx = -1;
            if (iId >= 0 && iName >= 0) idx = Math.min(iId, iName);
            else if (iId >= 0) idx = iId;
            else if (iName >= 0) idx = iName;
            if (idx >= 0) found.push({ agent: a, idx });
        });
        found.sort((x, y) => x.idx - y.idx);
        return found;
    }
    function pickAgent(text) {
        const mentions = findMentions(text);
        const nonVera = mentions.filter(m => m.agent.id !== "vera");
        if (nonVera.length) return nonVera[0].agent;
        if (mentions.some(m => m.agent.id === "vera")) return VERA;
        const t = text.toLowerCase();
        for (const a of SMALL_AGENTS) {
            if (a.keywords.some(k => t.includes(k))) return a;
        }
        return VERA;
    }
    function isStatusQuery(text) {
        return /kya kar rahe ho|kya kar raha hai|kya kar rahi ho|kar rahe ho|kaam kar rahe|what are you doing|kya kar rha/i.test(
            text
        );
    }
    function isSleepCommand(text) {
        return /\b(so jao|so ja|so jaiye|aaraam karo|araam karo|sleep)\b/i.test(
            text
        );
    }

    function isWakeCommand(text) {
        return /\b(uth jao|uth ja|wake up|jaag jao|kaam par aa jao)\b/i.test(
            text
        );
    }
    function parseDirectVisitCommand(text) {
        const t = text.toLowerCase();
        const goWords = [
            "jao",
            "jaana",
            "jaiye",
            "chalo",
            "milne jao",
            "paas jao"
        ];
        if (!goWords.some(w => t.includes(w))) return null;
        const mentions = findMentions(text);
        if (mentions.length < 2) return null;
        const mover = mentions[0].agent;
        const target = mentions[1].agent;
        if (mover.id === target.id) return null;
        return { mover, target };
    }
    function isCameraOn(text) {
        return /camera\s*on/i.test(text);
    }
    function isCameraOff(text) {
        return /camera\s*off/i.test(text);
    }
    function isSalam(text) {
        return /assalamu\s*alaikum|assalam\s*o\s*alaikum|salam\s*alaikum/i.test(
            text
        );
    }
    function isColonyQuery(text) {
        return /colony/i.test(text);
    }

    function activityReply(agent) {
        const st = agentState[agent.id];
        if (st === "working")
            return `${agent.icon} ${agent.name.toUpperCase()}: Main abhi kaam kar raha hoon, Meraj-nim. Thodi der me report bhejta hoon.`;
        if (st === "sleeping")
            return `${agent.icon} ${agent.name.toUpperCase()}: Zzz... main araam kar raha tha. Bataiye kya kaam hai?`;
        if (st === "away")
            return `${agent.icon} ${agent.name.toUpperCase()}: Main kisi Shadow se milne gaya tha, abhi laut raha hoon.`;
        return `${agent.icon} ${agent.name.toUpperCase()}: Apne room me hoon, aapka agla kaam ka intezaar kar raha hoon.`;
    }
    function taskReply(agent) {
        switch (agent.id) {
            case "igris":
                return `⚔️ IGRIS: Meraj-nim, skill build karna hai to roz thoda thoda seekho. "learn html" type karke course shuru kar sakte ho.`;
            case "beru":
                return `🐜 BERU: Body bhi Empire ka hissa hai, Meraj-nim. Aaj 20 min workout kar liya?`;
            case "bellion":
                return `💀 BELLION: Sabr rakho, Meraj-nim. Namaz aur dua kabhi mat chhodo — sab theek ho jayega. 🤲`;
            case "greed":
                return `💰 GREED: ${todayIncomeIdea()}`;
            case "kaisel": {
                const now = new Date();
                return `🐉 KAISEL: ${now.toLocaleDateString()} — ${now.toLocaleTimeString()}. Time waste mat karo, Meraj-nim.`;
            }
            case "vera":
                return `👑 VERA: Main hamesha aapke saath hoon, Meraj-nim. Shadow Army ka poora hisaab mere paas hai. "help" bolke commands dekh sakte ho.`;
            case "baran":
                return companyGrowthReply();
            case "diwan": {
                const st = agentState[agent.id];

                if (st === "sleeping") {
                    return `🗂️ DIWAN: Zzz... main abhi araam kar raha tha, Meraj-nim. Aapka kaam mile to turant uth jaunga.`;
                }

                if (st === "away") {
                    return `🗂️ DIWAN: Main abhi kisi Shadow ke saath hoon. Wapas aate hi aapka kaam sambhal lunga.`;
                }

                if (st === "working") {
                    return `🗂️ DIWAN: Main abhi kaam kar raha hoon, Meraj-nim. Kaam complete karke Vera ko report bhejunga.`;
                }

                return `🗂️ DIWAN: Main apne room me hoon aur aapke agle kaam ka intezaar kar raha hoon. Note, document ya PDF ka kaam ho to bataiye.`;
            }
            default:
                return `${agent.icon} ${agent.name.toUpperCase()}: Meraj-nim, main ${agent.role} sambhaal raha hoon. Vera ne mujhe pehla kaam de diya hai — main lag jaata hoon.`;
        }
    }
    function agentReply(agent, text) {
        if (isStatusQuery(text)) return activityReply(agent);
        return taskReply(agent);
    }

    function speak(text) {
        try {
            const u = new SpeechSynthesisUtterance(text);
            u.lang = "hi-IN";
            speechSynthesis.cancel();
            speechSynthesis.speak(u);
        } catch (e) {}
    }

    const AGENT_VOICE_PROFILE = {
        igris: { pitch: 0.75, rate: 0.95 },
        beru: { pitch: 1.25, rate: 1.2 },
        bellion: { pitch: 0.6, rate: 0.8 },
        greed: { pitch: 1.0, rate: 1.1 },
        kaisel: { pitch: 0.9, rate: 0.85 },
        vera: { pitch: 1.3, rate: 1.0 }
    };
    let cachedVoices = [];
    function loadVoicesForAgents() {
        try {
            cachedVoices = speechSynthesis.getVoices() || [];
        } catch (e) {}
    }
    loadVoicesForAgents();
    if (
        typeof speechSynthesis !== "undefined" &&
        "onvoiceschanged" in speechSynthesis
    ) {
        speechSynthesis.onvoiceschanged = loadVoicesForAgents;
    }
    function pickSystemVoiceForAgent(agentId) {
        if (!cachedVoices.length) return null;
        const idx = AGENTS.findIndex(a => a.id === agentId);
        if (idx < 0) return null;
        return cachedVoices[idx % cachedVoices.length];
    }
    function speakAsAgent(text, agentId) {
        try {
            const u = new SpeechSynthesisUtterance(text);
            u.lang = "hi-IN";
            const profile =
                AGENT_VOICE_PROFILE[agentId] || AGENT_VOICE_PROFILE.vera;
            u.pitch = profile.pitch;
            u.rate = profile.rate;
            const v = pickSystemVoiceForAgent(agentId);
            if (v) u.voice = v;
            speechSynthesis.cancel();
            speechSynthesis.speak(u);
        } catch (e) {}
    }

    function generateAgentPDF(agent, taskText, resultText) {
        try {
            if (!window.jspdf) return null;
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            doc.setFontSize(18);
            doc.text(`${agent.icon}  ${agent.name} — Task Report`, 15, 20);
            doc.setFontSize(11);
            doc.text(`Role: ${agent.role}`, 15, 30);
            doc.text(`Date: ${new Date().toLocaleString()}`, 15, 37);
            doc.text(`Reported to: Vera (Decoder)`, 15, 44);
            doc.setFontSize(13);
            doc.text("Task:", 15, 56);
            doc.setFontSize(11);
            doc.text(doc.splitTextToSize(taskText || "-", 180), 15, 64);
            doc.setFontSize(13);
            doc.text("Result:", 15, 90);
            doc.setFontSize(11);
            doc.text(doc.splitTextToSize(resultText || "-", 180), 15, 98);
            doc.setFontSize(9);
            doc.text("Shadow Army — MERAJ: The Monarch Protocol", 15, 280);
            const fileName = `${agent.name}-report-${Date.now()}.pdf`;
            doc.save(fileName);
            return fileName;
        } catch (e) {
            console.warn("PDF generation failed:", e);
            return null;
        }
    }
    function flyEnvelopeToDecoder(agentId) {
        const wrap = document.getElementById("agentRoomsWrap");
        const from = roomEl(agentId);
        if (!wrap || !from) return;
        const wrapRect = wrap.getBoundingClientRect();
        const fromRect = from.getBoundingClientRect();
        const env = document.createElement("div");
        env.className = "envelope-fly";
        env.innerText = "📩";
        env.style.left =
            fromRect.left - wrapRect.left + fromRect.width / 2 + "px";
        env.style.top =
            fromRect.top - wrapRect.top + fromRect.height / 2 + "px";
        wrap.style.position = "relative";
        wrap.appendChild(env);
        requestAnimationFrame(() => {
            env.style.left = wrapRect.width / 2 + "px";
            env.style.top = "-10px";
            env.style.opacity = "0.2";
        });
        setTimeout(() => env.remove(), 1000);
    }

    function doSleep() {
        if (anyoneWorking) return;
        const idle = SMALL_AGENTS.filter(a => agentState[a.id] === "idle");
        if (!idle.length) return;
        const a = idle[Math.floor(Math.random() * idle.length)];
        setState(a.id, "sleeping", "💤 Araam kar raha hai...");
        setTimeout(
            () => {
                if (agentState[a.id] === "sleeping") setState(a.id, "idle", "");
            },
            8000 + Math.random() * 6000
        );
    }

    function setCorridorLights(on) {
        const corridor = document.getElementById("agentCorridor");
        if (corridor) corridor.classList.toggle("lights-on", on);
    }

    function walkVisit(a, b, onArrive) {
        const corridor = document.getElementById("agentCorridor");
        const roomA = roomEl(a.id),
            roomB = roomEl(b.id);
        if (!corridor || !roomA || !roomB) return;
        setState(a.id, "away", `🚶 ${b.name} se milne gaya`);
        activeTravelers++;
        setCorridorLights(true);
        const corrRect = corridor.getBoundingClientRect();
        const fromRect = roomA.getBoundingClientRect();
        const toRect = roomB.getBoundingClientRect();
        const traveler = document.createElement("div");
        const isCar = a.id === "vera";
        traveler.className = isCar ? "car-travel" : "robot traveling";
        if (!isCar) {
            traveler.style.setProperty("--accent", a.color);
            traveler.innerHTML = robotInnerHTML();
        } else {
            traveler.innerText = "🚗";
        }
        traveler.style.left =
            fromRect.left - corrRect.left + fromRect.width / 2 + "px";
        corridor.appendChild(traveler);
        requestAnimationFrame(() => {
            traveler.style.left =
                toRect.left - corrRect.left + toRect.width / 2 + "px";
        });
        setTimeout(() => {
            const knock = document.createElement("div");
            knock.className = "visit-bubble show";
            knock.innerText = "🚪✊";
            traveler.appendChild(knock);
            setTimeout(() => knock.remove(), 450);
        }, 1350);
        setTimeout(() => {
            const bubble = document.createElement("div");
            bubble.className = "visit-bubble show";
            bubble.innerText = "💬";
            traveler.appendChild(bubble);
            const s = statusEl(b.id);
            if (s && agentState[b.id] === "idle")
                s.innerText = `💬 ${a.name} se baat kar raha hai`;
            if (onArrive) onArrive();
        }, 1600);
        setTimeout(() => {
            traveler.style.left =
                fromRect.left - corrRect.left + fromRect.width / 2 + "px";
            const s = statusEl(b.id);
            if (s && agentState[b.id] === "idle") s.innerText = "";
        }, 3200);
        setTimeout(() => {
            traveler.remove();
            if (agentState[a.id] === "away") setState(a.id, "idle", "");
            activeTravelers = Math.max(0, activeTravelers - 1);
            if (activeTravelers === 0) setCorridorLights(false);
        }, 4700);
    }

    function doVisit() {
        if (anyoneWorking) return;
        const idle = SMALL_AGENTS.filter(a => agentState[a.id] === "idle");
        if (idle.length < 2) return;
        // real jaisa: kabhi 1, kabhi 2, kabhi 3, kabhi 4 log jaate hain — poora group zaroori nahi
        const target = idle[Math.floor(Math.random() * idle.length)];
        const others = idle.filter(x => x.id !== target.id);
        const groupSize = Math.min(
            others.length,
            1 + Math.floor(Math.random() * 4)
        );
        const movers = others
            .sort(() => Math.random() - 0.5)
            .slice(0, groupSize);
        movers.forEach((mover, i) => {
            setTimeout(() => walkVisit(mover, target), i * 400);
        });
    }
    setInterval(() => {
        if (Math.random() < 0.5) doSleep();
        else doVisit();
    }, 22000);

    /* ---------- Proactive Check-ins ---------- */
    const PROACTIVE_MESSAGES = {
        igris: [
            "⚔️ IGRIS: Boss, aaj ka ek course complete kiya kya?",
            "⚔️ IGRIS: Skill seekhne ka sabse achha time abhi hai."
        ],
        beru: [
            "🐜 BERU: Boss, thoda stretch kar lo — body ka khayal rakhna zaroori hai.",
            "🐜 BERU: Paani piya aaj?"
        ],
        bellion: [
            "💀 BELLION: Namaz ka waqt ho gaya ho to yaad rakhna, boss.",
            "💀 BELLION: Ek dua padh lo, dil halka ho jayega."
        ],
        greed: [
            "💰 GREED: Boss, aaj koi income task try kiya?",
            "💰 GREED: Chhota step bhi Empire ki taraf ek step hai."
        ],
        kaisel: [
            "🐉 KAISEL: Waqt nikal raha hai, boss — aaj ka plan yaad hai na?"
        ]
    };
    function proactiveCheckIn() {
        if (anyoneWorking) return;
        if (Math.random() > 0.35) return;
        const idle = SMALL_AGENTS.filter(a => agentState[a.id] === "idle");
        if (!idle.length) return;
        const agent = idle[Math.floor(Math.random() * idle.length)];
        const pool = PROACTIVE_MESSAGES[agent.id];
        if (!pool) return;
        const msgText = pool[Math.floor(Math.random() * pool.length)];
        setState(agent.id, "working", "✍️ Aapko message likh raha hai...");
        setTimeout(() => {
            setState(agent.id, "idle", "");
            const chat = document.getElementById("aiChat");
            if (chat) {
                const el = document.createElement("p");
                el.className = "ai-message";
                el.style.borderLeft = "3px solid #ffd54f";
                el.style.paddingLeft = "6px";
                el.innerText = msgText;
                chat.appendChild(el);
                chat.scrollTop = chat.scrollHeight;
            }
            speakAsAgent(msgText, agent.id);
        }, 1200);
    }
    setInterval(proactiveCheckIn, 100000);

    /* ================= Colony Project — Vera 3 REAL din me naya Shadow banati hai ================= */
    const COLONY_KEY = "shadowColonyProject";
    const COLONY_DAY_MS = 24 * 60 * 60 * 1000;
    const COLONY_POOL = [
        {
            name: "Tusk",
            icon: "🛡️",
            color: "#f97316",
            role: "Discipline & Protection"
        },
        { name: "Noir", icon: "🌙", color: "#8b5cf6", role: "Rest & Recovery" },
        {
            name: "Ashen",
            icon: "🔥",
            color: "#dc2626",
            role: "Courage & Action"
        },
        {
            name: "Vellan",
            icon: "📚",
            color: "#06b6d4",
            role: "Knowledge & Research"
        },
        { name: "Korr", icon: "🧭", color: "#84cc16", role: "Planning & Focus" }
    ];
    function loadColonyProject() {
        try {
            return JSON.parse(localStorage.getItem(COLONY_KEY));
        } catch (e) {
            return null;
        }
    }
    function saveColonyProject(p) {
        localStorage.setItem(COLONY_KEY, JSON.stringify(p));
    }
    function pickColonyRecruit() {
        const usedNames = AGENTS.map(a => a.name);
        const avail = COLONY_POOL.filter(c => !usedNames.includes(c.name));
        return avail.length
            ? avail[Math.floor(Math.random() * avail.length)]
            : COLONY_POOL[Math.floor(Math.random() * COLONY_POOL.length)];
    }
    function startColonyProject() {
        let p = loadColonyProject();
        if (p && !p.completed) return p;
        const recruit = pickColonyRecruit();
        p = { startedAt: Date.now(), recruit, completed: false };
        saveColonyProject(p);
        return p;
    }
    function colonyPhase(p) {
        const elapsed = Date.now() - p.startedAt;
        const day = elapsed / COLONY_DAY_MS;
        if (day < 1)
            return {
                phase: "design",
                label: "🧬 Naye Shadow ko design kar rahi hai...",
                pct: Math.min(100, day * 100)
            };
        if (day < 2)
            return {
                phase: "build",
                label: "🏗️ Uska ghar bana rahi hai...",
                pct: Math.min(100, (day - 1) * 100)
            };
        if (day < 3)
            return {
                phase: "assign",
                label: "📋 Pehla kaam taiyar kar rahi hai...",
                pct: Math.min(100, (day - 2) * 100)
            };
        return { phase: "done", label: "✅ Colony project poora!", pct: 100 };
    }
    function updateColonyWidget() {
        const box = document.getElementById("hqColony");
        const label = document.getElementById("hqColonyLabel");
        const bar = document.getElementById("hqColonyBarFill");
        if (!box || !label || !bar) return;
        const p = loadColonyProject();
        if (!p || p.completed) {
            box.classList.remove("show");
            return;
        }
        const ph = colonyPhase(p);
        box.classList.add("show");
        label.innerText = `${p.recruit.icon} ${p.recruit.name} — ${ph.label}`;
        bar.style.width = Math.round(ph.pct) + "%";
    }
    setInterval(updateColonyWidget, 20000);
    function finishColonyProject(p) {
        const recruit = p.recruit;
        const id = recruit.name.toLowerCase().replace(/[^a-z0-9]/g, "");
        if (AGENTS.some(a => a.id === id)) {
            p.completed = true;
            saveColonyProject(p);
            return;
        }
        const newAgent = {
            id,
            name: recruit.name,
            icon: recruit.icon,
            color: recruit.color,
            role: recruit.role,
            keywords: []
        };
        AGENTS.push(newAgent);
        SMALL_AGENTS = AGENTS.filter(a => a.id !== "vera");
        agentState[id] = "idle";
        const wrap = document.getElementById("agentRoomsWrap");
        if (wrap) {
            const holder = document.createElement("div");
            holder.innerHTML = createRoomElement(newAgent);
            wrap.appendChild(holder.firstElementChild);
            renderBond(id);
            addCctvTile(newAgent);
        }
        p.completed = true;
        saveColonyProject(p);
        updateColonyWidget();
        const chat = document.getElementById("aiChat");
        const msg = `👑 VERA: Meraj-nim, colony ka naya Shadow taiyar hai — ${newAgent.icon} ${newAgent.name} (${newAgent.role}). Maine uska ghar bana diya aur pehla kaam de diya hai: "${taskReply(newAgent)}"`;
        if (chat) {
            const el = document.createElement("p");
            el.className = "ai-message";
            el.innerText = msg;
            chat.appendChild(el);
            chat.scrollTop = chat.scrollHeight;
        }
        speakAsAgent(msg, "vera");
    }
    function checkColonyOnLoad() {
        const p = loadColonyProject();
        if (!p || p.completed) return;
        const ph = colonyPhase(p);
        if (ph.phase === "done") finishColonyProject(p);
        else updateColonyWidget();
    }
    setInterval(checkColonyOnLoad, 60000);
    function colonyStatusReply() {
        let p = loadColonyProject();
        if (!p || p.completed) {
            p = startColonyProject();
            updateColonyWidget();
            return `👑 VERA: Naya colony project shuru kar rahi hoon, Meraj-nim. Poore 3 din lagenge — abhi: ${colonyPhase(p).label}`;
        }
        const ph = colonyPhase(p);
        if (ph.phase === "done") {
            finishColonyProject(p);
            return "👑 VERA: Colony project complete ho gaya, boss! Naye Shadow se milo.";
        }
        updateColonyWidget();
        return `👑 VERA: Colony project chal raha hai, Meraj-nim — ${p.recruit.icon} ${p.recruit.name} taiyar ho raha hai. ${ph.label} (${Math.round(ph.pct)}% — is phase ka)`;
    }

    /* ================= Study-Along Courses — Igris khud saath padhta hai, phir Greed real income roadmap deta hai ================= */
    const COURSES = {
        html: {
            title: "HTML Course",
            lessons: [
                "HTML basics — tags, structure, headings, paragraphs",
                "Links, images aur lists",
                "Forms — input, button, label",
                "Semantic tags — header, nav, section, footer",
                "Mini project — apna ek simple webpage banao"
            ]
        },
        css: {
            title: "CSS Course",
            lessons: [
                "CSS selectors aur basic styling",
                "Box model — margin, padding, border",
                "Flexbox se layout banana",
                "Grid se layout banana",
                "Responsive design — mobile-friendly banana"
            ]
        },
        javascript: {
            title: "JavaScript Course",
            lessons: [
                "Variables, data types aur operators",
                "Functions aur if/else conditions",
                "Loops aur arrays",
                "DOM ko select aur update karna",
                "Events — click/input pe react karna + mini project"
            ]
        }
    };
    const COURSE_TOPIC_KEYWORDS = {
        html: ["html"],
        css: ["css"],
        javascript: ["javascript", "java script", " js "]
    };
    function detectCourseTopic(text) {
        const t = " " + text.toLowerCase() + " ";
        for (const topic in COURSE_TOPIC_KEYWORDS) {
            if (COURSE_TOPIC_KEYWORDS[topic].some(k => t.includes(k)))
                return topic;
        }
        return null;
    }
    function isLessonAdvanceWords(text) {
        return /\bagla\b|\bnext\b|\bdone\b|\bcomplete\b|khatam|ho gaya|\bfinish\b/i.test(
            text
        );
    }
    function courseKey(topic) {
        return "shadowCourse_" + topic;
    }
    function loadCourse(topic) {
        try {
            return JSON.parse(localStorage.getItem(courseKey(topic)));
        } catch (e) {
            return null;
        }
    }
    function saveCourse(c) {
        localStorage.setItem(courseKey(c.topic), JSON.stringify(c));
    }
    function findActiveCourse() {
        for (const topic in COURSES) {
            const c = loadCourse(topic);
            if (c && !c.completed) return c;
        }
        return null;
    }
    const INCOME_ROADMAPS = {
        html: [
            "GitHub par free account banao aur apna webpage wahan upload karo (portfolio ban jayega).",
            "3-4 chhoti practice sites banao — apna kaam dikhane ke liye.",
            "Fiverr ya Upwork par free profile banao aur complete karo.",
            "Roz 5 chhote business dhoondo jinki website nahi hai, unhe simple message bhejo.",
            "Pehla kaam chhota rakho (₹500-₹1000), sirf real client se real paisa lo."
        ],
        css: [
            "Apne HTML projects ko CSS se sundar banao — before/after dikhao.",
            "3 alag design style ki landing pages banao (portfolio ke liye).",
            "Freelance platform par 'landing page design' service list karo.",
            "Local business owners se contact karo jinhe website redesign chahiye.",
            "Pehla real client project lo, kaam poora karke real payment lo."
        ],
        javascript: [
            "Apne portfolio sites me JS se interactivity add karo.",
            "2-3 chhote tools banao (calculator, to-do list) — apna kaam dikhane ke liye.",
            "Freelance platform par 'website + JS functionality' service list karo.",
            "Chhote business ya seniors ko dhoondo jinhe chhota web tool chahiye.",
            "Ek real chhota project lo aur time par deliver karke pehla real income kamao."
        ]
    };
    function incomeRoadmapText(topic) {
        const steps = INCOME_ROADMAPS[topic] || INCOME_ROADMAPS.html;
        return (
            `💰 GREED: Shabaash Meraj-nim, ${COURSES[topic].title} complete! Ab step by step, seedhe tareeke se paisa kamana shuru karo:\n` +
            steps.map((s, i) => `${i + 1}. ${s}`).join("\n") +
            `\nJab bhi real paisa mile, mujhe "income <amount>" bolke batana — main sirf tumhara real kamaya hua paisa count karta hoon, koi fake coin nahi.`
        );
    }
    function startCourseReply(topic) {
        let c = loadCourse(topic);
        if (!c || c.completed) {
            c = {
                topic,
                lessonIndex: 0,
                startedAt: Date.now(),
                completed: false
            };
            saveCourse(c);
        }
        setState(
            "igris",
            "working",
            `📚 ${COURSES[topic].title} — Lesson ${c.lessonIndex + 1}`
        );
        return `⚔️ IGRIS: Meraj-nim, ${COURSES[topic].title} shuru karta hoon — main bhi ye khud kar raha hoon, aap bhi saath saath padhiye!\nLesson ${c.lessonIndex + 1}: ${COURSES[topic].lessons[c.lessonIndex]}\nLesson khatam ho jaye to "done" ya "agla" bolo, main agla lesson bhi saath me karunga.`;
    }
    function advanceCourseReply(c) {
        const course = COURSES[c.topic];
        c.lessonIndex++;
        if (c.lessonIndex >= course.lessons.length) {
            c.completed = true;
            saveCourse(c);
            setState("igris", "done", "✅ Course complete!");
            addBond("igris", 2);
            flyEnvelopeToDecoder("igris");
            setTimeout(() => setState("igris", "idle", ""), 2000);
            setTimeout(() => {
                setState(
                    "greed",
                    "working",
                    "💰 Income roadmap taiyar kar raha hai..."
                );
                setTimeout(() => {
                    setState("greed", "idle", "");
                    const chat = document.getElementById("aiChat");
                    const msg = incomeRoadmapText(c.topic);
                    if (chat) {
                        const el = document.createElement("p");
                        el.className = "ai-message";
                        el.innerText = msg;
                        chat.appendChild(el);
                        chat.scrollTop = chat.scrollHeight;
                    }
                    speakAsAgent(msg, "greed");
                }, 1400);
            }, 900);
            return `⚔️ IGRIS: Meraj-nim, humne ${course.title} poora kar liya — dono ne saath me seekha! 🎉 Ab Greed aapko step-by-step batayega ki isse real paisa kaise kamayein.`;
        }
        saveCourse(c);
        setState(
            "igris",
            "working",
            `📚 Lesson ${c.lessonIndex + 1} kar raha hai`
        );
        return `⚔️ IGRIS: Badhiya Meraj-nim! Ab dono agla lesson karte hain.\nLesson ${c.lessonIndex + 1}: ${course.lessons[c.lessonIndex]}`;
    }

    /* ================= Real Income Tracker — sirf real, khud-bataya hua paisa count hota hai ================= */
    const INCOME_KEY = "shadowRealIncome";
    const INCOME_LOG_KEY = "shadowIncomeLog";
    const GOAL_KEY = "shadowIncomeGoal";
    const INCOME_MILESTONES = [
        1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000
    ];
    function getRealIncome() {
        return Number(localStorage.getItem(INCOME_KEY)) || 0;
    }
    function loadIncomeLog() {
        try {
            return JSON.parse(localStorage.getItem(INCOME_LOG_KEY)) || [];
        } catch (e) {
            return [];
        }
    }
    function saveIncomeLog(log) {
        localStorage.setItem(INCOME_LOG_KEY, JSON.stringify(log));
    }
    function getCrossedMilestones() {
        try {
            return (
                JSON.parse(localStorage.getItem("shadowIncomeMilestones")) || []
            );
        } catch (e) {
            return [];
        }
    }
    function checkNewMilestones(total) {
        const crossed = getCrossedMilestones();
        const newly = INCOME_MILESTONES.filter(
            m => total >= m && !crossed.includes(m)
        );
        if (newly.length)
            localStorage.setItem(
                "shadowIncomeMilestones",
                JSON.stringify(crossed.concat(newly))
            );
        return newly;
    }
    function addRealIncome(amount, source) {
        const v = getRealIncome() + amount;
        localStorage.setItem(INCOME_KEY, v);
        const log = loadIncomeLog();
        log.push({ amount, source: source || "other", ts: Date.now() });
        saveIncomeLog(log);
        return v;
    }
    function getIncomeGoal() {
        return Number(localStorage.getItem(GOAL_KEY)) || 0;
    }
    function setIncomeGoal(amount) {
        localStorage.setItem(GOAL_KEY, amount);
    }
    function isIncomeLog(text) {
        return /\bincome\b\s*\d|kamaya|maine\s*kamay|\bearned\b\s*\d/i.test(
            text
        );
    }
    function isIncomeQuery(text) {
        return /(mera|total|kitna)\s*income|income\s*kitna|income\s*batao/i.test(
            text
        );
    }
    function isGoalSetCommand(text) {
        return (
            /goal\s*set|income\s*goal|mera\s*goal/i.test(text) &&
            extractAmount(text) !== null
        );
    }
    function isGoalQueryCommand(text) {
        return /goal\s*kitna|goal\s*progress|mera\s*goal\s*kya/i.test(text);
    }
    function isWeekIncomeQuery(text) {
        return /hafte.*income|week\s*income|income.*hafte/i.test(text);
    }
    function isMonthIncomeQuery(text) {
        return /mahine.*income|month\s*income|income.*mahine/i.test(text);
    }
    function isTopSourceQuery(text) {
        return /sabse\s*zyada|top\s*source|kaha\s*se\s*zyada/i.test(text);
    }
    function extractAmount(text) {
        const m = text.match(/(\d+(?:[.,]\d+)?)/);
        return m ? parseFloat(m[1].replace(",", "")) : null;
    }
    function extractSource(text) {
        let t = text
            .replace(/\bincome\b|\bkamaya\b|maine\s*kamay(a)?|\bearned\b/gi, "")
            .trim();
        t = t.replace(/(\d+(?:[.,]\d+)?)/, "").trim();
        return t || null;
    }
    function incomeLogReply(text) {
        const amt = extractAmount(text);
        if (amt === null)
            return "💰 GREED: Kitna kamaya, Meraj-nim? Number ke saath batao — jaise 'income 500 freelance'.";
        const source = extractSource(text);
        const total = addRealIncome(amt, source);
        addBond("greed", 1);
        setState("greed", "done", "✅ Income record ho gaya");
        setTimeout(() => setState("greed", "idle", ""), 1800);
        let msg = `💰 GREED: Shabaash! ₹${amt}${source ? ` (${source})` : ""} record kar liya — ye real paisa hai, koi fake coin nahi. Ab tak ka total real income: ₹${total}.`;
        const newly = checkNewMilestones(total);
        if (newly.length)
            msg += `\n🎉 Milestone cross ho gaya: ₹${newly[newly.length - 1]}! Bahut badhiya chal rahe ho, Meraj-nim.`;
        const goal = getIncomeGoal();
        if (goal)
            msg += `\nGoal ₹${goal} ka ${Math.min(100, Math.round((total / goal) * 100))}% ho gaya.`;
        return msg;
    }
    function incomeQueryReply() {
        return `💰 GREED: Ab tak ka total real income: ₹${getRealIncome()}. Sirf wahi jo tumne khud mujhe bataya hai.`;
    }
    function goalSetReply(text) {
        const amt = extractAmount(text);
        setIncomeGoal(amt);
        return `💰 GREED: Theek hai boss, goal set kar diya — ₹${amt}. Jaise-jaise income aayegi, main progress batata rahunga.`;
    }
    function goalProgressReply() {
        const goal = getIncomeGoal();
        if (!goal)
            return "💰 GREED: Abhi koi goal set nahi hai, Meraj-nim. 'goal set 5000' bolke set karo.";
        const total = getRealIncome();
        const pct = Math.min(100, Math.round((total / goal) * 100));
        return `💰 GREED: Goal ₹${goal} me se ₹${total} ho gaya (${pct}%). Baaki ₹${Math.max(0, goal - total)} — chalte raho, Meraj-nim.`;
    }
    function sumIncomeSince(msAgo) {
        const cutoff = Date.now() - msAgo;
        return loadIncomeLog()
            .filter(e => e.ts >= cutoff)
            .reduce((s, e) => s + e.amount, 0);
    }
    function weekIncomeReply() {
        return `💰 GREED: Is hafte tumne ₹${sumIncomeSince(7 * 24 * 60 * 60 * 1000)} kamaya, Meraj-nim.`;
    }
    function monthIncomeReply() {
        return `💰 GREED: Is mahine tumne ₹${sumIncomeSince(30 * 24 * 60 * 60 * 1000)} kamaya, Meraj-nim.`;
    }
    function topSourceReply() {
        const log = loadIncomeLog();
        if (!log.length)
            return "💰 GREED: Abhi koi income log nahi hai, Meraj-nim.";
        const bySource = {};
        log.forEach(e => {
            bySource[e.source] = (bySource[e.source] || 0) + e.amount;
        });
        const [topName, topAmt] = Object.entries(bySource).sort(
            (a, b) => b[1] - a[1]
        )[0];
        return `💰 GREED: Sabse zyada kamaya hai "${topName}" se — ₹${topAmt} tak. Isi pe aur focus karo.`;
    }

    /* ================= Shadow Council — sab agents live milkar bahas karte hain, phir Vera final faisla deti hai ================= */
    function isCouncilQuery(text) {
        return /confused|kya karu\b|kya karoon|kaunsa kaam|help me decide|decide karo|samajh nahi aa raha/i.test(
            text
        );
    }
    const COUNCIL_VOICES = {
        igris: () =>
            "⚔️ IGRIS: Mera vote — pehle skill pe kaam karo, wahi sabse solid foundation hai.",
        beru: () =>
            "🐜 BERU: Mera vote — pehle body/health theek rakho, warna kuch bhi consistent nahi chalega.",
        bellion: () =>
            "💀 BELLION: Sabr se socho — jo dil ko sukoon de aur sahi lage, wahi pehle karo.",
        greed: () =>
            "💰 GREED: Mera vote — jo cheez sabse jaldi real paisa la sakti hai, us par focus karo."
    };
    function runCouncil(done) {
        const order = ["igris", "beru", "bellion", "greed"].filter(
            id => agentState[id] !== undefined
        );
        const chat = document.getElementById("aiChat");
        order.forEach((id, i) => {
            setTimeout(() => {
                setState(
                    id,
                    "working",
                    "🗣️ Council me apni raay de raha hai..."
                );
                setTimeout(() => {
                    setState(id, "idle", "");
                    const line = COUNCIL_VOICES[id] ? COUNCIL_VOICES[id]() : "";
                    if (line && chat) {
                        const el = document.createElement("p");
                        el.className = "ai-message";
                        el.style.borderLeft =
                            "3px solid " + AGENTS.find(a => a.id === id).color;
                        el.style.paddingLeft = "6px";
                        el.innerText = line;
                        chat.appendChild(el);
                        chat.scrollTop = chat.scrollHeight;
                    }
                    if (line) speakAsAgent(line, id);
                }, 900);
            }, i * 1600);
        });
        setTimeout(
            () => {
                const verdict =
                    "👑 VERA: Meraj-nim, sabki baat sun li. Mera final faisla — bada sochne se pehle ek chhota kaam aaj hi shuru karo, chahe wo skill ho ya health; kal se dusra shuru karna.";
                if (chat) {
                    const el = document.createElement("p");
                    el.className = "ai-message";
                    el.style.borderLeft = "3px solid " + VERA.color;
                    el.style.paddingLeft = "6px";
                    el.innerText = verdict;
                    chat.appendChild(el);
                    chat.scrollTop = chat.scrollHeight;
                }
                speakAsAgent(verdict, "vera");
            },
            order.length * 1600 + 1000
        );
        done(
            "👑 VERA: Shadow Council bula rahi hoon, thodi der ruko — sab apni raay de rahe hain...",
            null,
            "vera"
        );
    }

    /* ================= Simple Daily Income Ideas (Greed) — sirf easy, real tareeke ================= */
    const SIMPLE_INCOME_IDEAS = [
        "Apna ek hunar (jo bhi aata hai) social media pe 1 chhota post ke through dikhao — logo ko pata to chale.",
        "5 log dhoondo jinhe tumhari koi skill se help chahiye, unhe direct message karo.",
        "Apne aas-paas kisi se poocho unhe koi chhota kaam (tuition, design, likhna, delivery) chahiye kya.",
        "Purani cheezein jo ghar me pade hain, unhe online bech do — chhota shuru karo.",
        "Ek local shop/business owner se pooch, unhe social media handle karne wala chahiye kya.",
        "Apni skill ka ek chhota sample/demo banao aur 3 logo ko dikhao — free me pehla feedback lo."
    ];
    let incomeIdeaIndex =
        Number(localStorage.getItem("shadowIncomeIdeaIdx")) || 0;
    function todayIncomeIdea() {
        const idea =
            SIMPLE_INCOME_IDEAS[incomeIdeaIndex % SIMPLE_INCOME_IDEAS.length];
        incomeIdeaIndex++;
        localStorage.setItem("shadowIncomeIdeaIdx", incomeIdeaIndex);
        return `Aaj ka simple kaam: ${idea} Jab paisa mile, "income <amount>" bolke batana.`;
    }

    /* ================= Baran — Company Growth ================= */
    function getCompanyName() {
        return localStorage.getItem("shadowCompanyName") || "";
    }
    function setCompanyName(name) {
        localStorage.setItem("shadowCompanyName", name);
    }
    const COMPANY_GROWTH_STEPS = [
        "Is hafte sirf ek cheez pe focus karo: logo ko clearly batao tumhara business kya solve karta hai (1 line).",
        "Is hafte apne 5 mojooda ya purane customers se poocho unhe aur kya chahiye — unki baat suno.",
        "Is hafte apni pricing check karo — kya wo tumhari value ke hisaab se sahi hai?",
        "Is hafte 3 naye log dhoondo jo tumhare customer ban sakte hain, unse baat karo.",
        "Is hafte apne khush customers se poocho — kya wo kisi aur ko refer kar sakte hain?"
    ];
    function isSetCompanyCommand(text) {
        return /meri company\s+(.+)|company ka naam\s+(.+)/i.test(text);
    }
    function extractCompanyName(text) {
        const m = text.match(/meri company\s+(.+)|company ka naam\s+(.+)/i);
        return m ? (m[1] || m[2]).trim() : null;
    }
    function companyGrowthReply() {
        const name = getCompanyName();
        const weekIdx =
            Math.floor(Date.now() / (7 * 24 * 60 * 60 * 1000)) %
            COMPANY_GROWTH_STEPS.length;
        const step = COMPANY_GROWTH_STEPS[weekIdx];
        if (!name)
            return `📈 BARAN: Meraj-nim, pehle "meri company <naam>" bolke company ka naam batao, phir main uska growth plan simple steps me dunga.`;
        return `📈 BARAN: ${name} ke liye — ${step}`;
    }

    /* ================= Diwan — Documents / Notes + PDF ================= */
    const DOC_KEY = "shadowDocuments";
    function loadDocs() {
        try {
            return JSON.parse(localStorage.getItem(DOC_KEY)) || [];
        } catch (e) {
            return [];
        }
    }
    function saveDocs(docs) {
        localStorage.setItem(DOC_KEY, JSON.stringify(docs));
    }
    function isSaveNoteCommand(text) {
        return /^(?:diwan\s+)?note\s*[:\-]/i.test(text.trim());
    }
    function extractNoteText(text) {
        return text.replace(/^(?:diwan\s+)?note\s*[:\-]/i, "").trim();
    }
    function isPdfRequestCommand(text) {
        return /pdf\s*bana|pdf\s*banao|documents?\s*pdf|notes?\s*pdf/i.test(
            text
        );
    }
    function saveNoteReply(text) {
        const note = extractNoteText(text);
        if (!note)
            return "🗂️ DIWAN: Kya save karu, Meraj-nim? 'note: <text>' is tarah bolo.";
        const docs = loadDocs();
        docs.push({ text: note, savedAt: Date.now() });
        saveDocs(docs);
        addBond("diwan", 1);
        setState("diwan", "done", "📥 Note save ho gaya");
        setTimeout(() => setState("diwan", "idle", ""), 1800);
        return `🗂️ DIWAN: Note save kar liya, Meraj-nim. Ab tak ${docs.length} document(s) safe hain. Jab chaho "pdf bana do" bolo.`;
    }
    function generateDocsPDF() {
        const docs = loadDocs();
        if (!docs.length) return null;
        try {
            if (!window.jspdf) return null;
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            doc.setFontSize(18);
            doc.text("🗂️ Diwan — Saved Documents", 15, 20);
            doc.setFontSize(10);
            doc.text(
                `Total: ${docs.length} | Generated: ${new Date().toLocaleString()}`,
                15,
                28
            );
            let y = 40;
            docs.forEach((d, i) => {
                doc.setFontSize(11);
                const lines = doc.splitTextToSize(
                    `${i + 1}. [${new Date(d.savedAt).toLocaleDateString()}] ${d.text}`,
                    180
                );
                if (y + lines.length * 6 > 280) {
                    doc.addPage();
                    y = 20;
                }
                doc.text(lines, 15, y);
                y += lines.length * 6 + 6;
            });
            const fileName = `Diwan-Documents-${Date.now()}.pdf`;
            doc.save(fileName);
            return fileName;
        } catch (e) {
            console.warn("Docs PDF failed:", e);
            return null;
        }
    }
    function pdfRequestReply() {
        setState("diwan", "working", "📄 PDF bana raha hai...");
        const fileName = generateDocsPDF();
        setState(
            "diwan",
            fileName ? "done" : "idle",
            fileName ? "✅ PDF ready" : ""
        );
        setTimeout(() => setState("diwan", "idle", ""), 1800);
        if (!fileName)
            return "🗂️ DIWAN: Abhi koi saved document nahi hai, Meraj-nim. Pehle 'note: <text>' bolke kuch save karo.";
        return `🗂️ DIWAN: PDF bana diya, boss — ${fileName} save ho gayi.`;
    }

    /* ================= Health + Namaz combined streak (Beru + Bellion) ================= */
    const HEALTH_KEY = "shadowHealthLog";
    function loadHealthLog() {
        try {
            return JSON.parse(localStorage.getItem(HEALTH_KEY)) || {};
        } catch (e) {
            return {};
        }
    }
    function saveHealthLog(log) {
        localStorage.setItem(HEALTH_KEY, JSON.stringify(log));
    }
    function todayKey() {
        return new Date().toISOString().slice(0, 10);
    }
    function isWorkoutDoneCommand(text) {
        return /workout\s*(done|kar liya|ho gaya)|gym\s*(done|kar liya)/i.test(
            text
        );
    }
    function isNamazDoneCommand(text) {
        return /namaz\s*(done|padh li|ho gayi|kar li)/i.test(text);
    }
    function computeHealthStreak() {
        const log = loadHealthLog();
        let streak = 0;
        let d = new Date();
        while (true) {
            const key = d.toISOString().slice(0, 10);
            const entry = log[key];
            if (entry && entry.workout && entry.namaz) {
                streak++;
                d.setDate(d.getDate() - 1);
            } else break;
        }
        return streak;
    }
    function logHealth(field) {
        const log = loadHealthLog();
        const key = todayKey();
        if (!log[key]) log[key] = { workout: false, namaz: false };
        log[key][field] = true;
        saveHealthLog(log);
    }
    function workoutDoneReply() {
        logHealth("workout");
        addBond("beru", 1);
        setState("beru", "done", "✅ Workout ho gaya");
        setTimeout(() => setState("beru", "idle", ""), 1800);
        const log = loadHealthLog()[todayKey()];
        const streak = computeHealthStreak();
        return `🐜 BERU: Shabaash Meraj-nim! Workout record ho gaya.${log.namaz ? ` Aaj namaz bhi ho gayi — streak: ${streak} din!` : " Namaz bhi ho jaye to aaj ka din complete."}`;
    }
    function namazDoneReply() {
        logHealth("namaz");
        addBond("bellion", 1);
        setState("bellion", "done", "✅ Namaz ho gayi");
        setTimeout(() => setState("bellion", "idle", ""), 1800);
        const log = loadHealthLog()[todayKey()];
        const streak = computeHealthStreak();
        return `💀 BELLION: Allah kabool kare, Meraj-nim.${log.workout ? ` Workout bhi ho gaya — streak: ${streak} din!` : " Workout bhi kar lo, din complete ho jayega."}`;
    }

    /* ================= Handwritten Notes — upload karke text nikalna aur sunana ================= */
    function loadTesseractIfNeeded() {
        return new Promise((resolve, reject) => {
            if (window.Tesseract) return resolve();
            const s = document.createElement("script");
            s.src =
                "https://cdnjs.cloudflare.com/ajax/libs/tesseract.js/4.1.1/tesseract.min.js";
            s.onload = () => resolve();
            s.onerror = () => reject(new Error("Tesseract load failed"));
            document.head.appendChild(s);
        });
    }
    async function handleNotesFile(file, statusEl2) {
        try {
            if (statusEl2)
                statusEl2.innerText = "📖 Handwriting padh raha hoon...";
            await loadTesseractIfNeeded();
            const result = await window.Tesseract.recognize(file, "eng");
            const text = (
                (result && result.data && result.data.text) ||
                ""
            ).trim();
            localStorage.setItem("shadowHandwrittenNotes", text);
            if (statusEl2)
                statusEl2.innerText = text
                    ? "✅ Notes padh li — 'notes padho' bolo."
                    : "⚠️ Kuch clear nahi mila, saaf photo try karo.";
        } catch (e) {
            if (statusEl2)
                statusEl2.innerText = "❌ Notes padhne me dikkat hui.";
        }
    }
    function isReadNotesCommand(text) {
        return /notes?\s*padho|padh\s*kar\s*sunao|handwritten/i.test(text);
    }
    function readNotesReply() {
        const text = localStorage.getItem("shadowHandwrittenNotes");
        if (!text)
            return "🗂️ DIWAN: Abhi koi handwritten note upload nahi hui, Meraj-nim. Vera HQ me 'Notes Upload' button se photo daalo.";
        setTimeout(() => speak(text), 300);
        return `🗂️ DIWAN: Padh kar suna raha hoon, Meraj-nim:\n${text}`;
    }

    function executeAgent(text, done) {
        const agent = pickAgent(text);
        anyoneWorking = true;
        setState(agent.id, "working", "💻 Kaam kar raha hai...");
        setTimeout(() => {
            const reply = agentReply(agent, text);
            const fileName = generateAgentPDF(agent, text, reply);
            setState(
                agent.id,
                "done",
                fileName ? "📄 Report ready" : "✅ Done"
            );
            addBond(agent.id, 1);
            flyEnvelopeToDecoder(agent.id);
            setTimeout(() => {
                anyoneWorking = false;
                setState(agent.id, "idle", "");
            }, 1800);
            done(reply, fileName, agent.id);
        }, 900);
    }

    function routeMessage(text, done) {
        if (isSalam(text)) {
            const agent =
                pickAgent(text.replace(/assalamu.*?(alaikum)/i, "")) || VERA;
            const reply = `${agent.icon} ${agent.name.toUpperCase()}: Waalaikumussalam warahmatullahi wabarakatuhu, boss! Okkk boss, main kaam karne jaa raha hoon.`;
            addBond(agent.id, 1);
            setState(agent.id, "working", "💻 Kaam karne gaya...");
            setTimeout(() => {
                setState(agent.id, "idle", "");
            }, 3500);
            done(reply, null, agent.id);
            return;
        }
        if (isCameraOn(text)) {
            const btn = document.getElementById("hqCamBtn");
            if (btn) btn.click();
            done("👑 VERA: Camera ON kar rahi hoon, boss.", null, "vera");
            return;
        }
        if (isCameraOff(text)) {
            const hqScreen = document.getElementById("hqScreen");
            if (hqScreen) {
                const video = hqScreen.querySelector("video");
                if (video && video.srcObject) {
                    video.srcObject.getTracks().forEach(t => t.stop());
                }
                hqScreen.innerHTML = `<span style="color:#334155;font-size:11px;">📷 Camera Off</span>`;
            }
            const btn = document.getElementById("hqCamBtn");
            if (btn) btn.innerText = "📷 Camera ON (Vera aapko dekh sake)";
            done("👑 VERA: Camera OFF kar di, boss.", null, "vera");
            return;
        }
        if (isColonyQuery(text)) {
            done(colonyStatusReply(), null, "vera");
            return;
        }
        if (isSetCompanyCommand(text)) {
            const name = extractCompanyName(text);
            if (name) setCompanyName(name);
            done(
                `📈 BARAN: Theek hai boss, "${name}" ke liye ab main har hafte simple growth step dunga.`,
                null,
                "baran"
            );
            return;
        }
        if (isSaveNoteCommand(text)) {
            done(saveNoteReply(text), null, "diwan");
            return;
        }
        if (isPdfRequestCommand(text)) {
            done(pdfRequestReply(), null, "diwan");
            return;
        }
        if (isReadNotesCommand(text)) {
            done(readNotesReply(), null, "diwan");
            return;
        }
        if (isWorkoutDoneCommand(text)) {
            done(workoutDoneReply(), null, "beru");
            return;
        }
        if (isNamazDoneCommand(text)) {
            done(namazDoneReply(), null, "bellion");
            return;
        }
        const courseTopic = detectCourseTopic(text);
        if (courseTopic) {
            const c = loadCourse(courseTopic);
            if (c && !c.completed) {
                if (isLessonAdvanceWords(text))
                    done(advanceCourseReply(c), null, "igris");
                else
                    done(
                        `⚔️ IGRIS: Meraj-nim, hum abhi Lesson ${c.lessonIndex + 1} par hain: ${COURSES[courseTopic].lessons[c.lessonIndex]}. Khatam ho jaye to "done" bolna.`,
                        null,
                        "igris"
                    );
            } else {
                done(startCourseReply(courseTopic), null, "igris");
            }
            return;
        }
        const activeCourse = findActiveCourse();
        if (activeCourse && isLessonAdvanceWords(text)) {
            done(advanceCourseReply(activeCourse), null, "igris");
            return;
        }
        if (isGoalSetCommand(text)) {
            done(goalSetReply(text), null, "greed");
            return;
        }
        if (isGoalQueryCommand(text)) {
            done(goalProgressReply(), null, "greed");
            return;
        }
        if (isWeekIncomeQuery(text)) {
            done(weekIncomeReply(), null, "greed");
            return;
        }
        if (isMonthIncomeQuery(text)) {
            done(monthIncomeReply(), null, "greed");
            return;
        }
        if (isTopSourceQuery(text)) {
            done(topSourceReply(), null, "greed");
            return;
        }
        if (isIncomeLog(text)) {
            done(incomeLogReply(text), null, "greed");
            return;
        }
        if (isIncomeQuery(text)) {
            done(incomeQueryReply(), null, "greed");
            return;
        }
        if (isCouncilQuery(text)) {
            runCouncil(done);
            return;
        }
        const visit = parseDirectVisitCommand(text);
        if (visit) {
            const { mover, target } = visit;
            const reply = `🚶 ${mover.icon} ${mover.name.toUpperCase()}: Theek hai boss, ${target.name} ke paas ja raha hoon.`;
            walkVisit(mover, target);
            done(reply, null, mover.id);
            return;
        }
        const targetAgent = pickAgent(text);

        if (isSleepCommand(text)) {
            if (!targetAgent || targetAgent.id === "vera") {
                done(
                    "👑 VERA: Mujhe directly sleep command nahi diya ja sakta, boss.",
                    null,
                    "vera"
                );
                return;
            }

            setState(targetAgent.id, "sleeping", "💤 Araam kar raha hai...");
            done(
                `${targetAgent.icon} ${targetAgent.name.toUpperCase()}: Theek hai boss, main ab araam kar raha hoon. 😴`,
                null,
                targetAgent.id
            );
            return;
        }

        if (isWakeCommand(text)) {
            if (!targetAgent || targetAgent.id === "vera") {
                done("👑 VERA: Theek hai boss.", null, "vera");
                return;
            }

            setState(targetAgent.id, "idle", "👀 Wapas kaam par hoon");
            done(
                `${targetAgent.icon} ${targetAgent.name.toUpperCase()}: Uth gaya boss. Ab kaam ke liye ready hoon. 💻`,
                null,
                targetAgent.id
            );
            return;
        }

        executeAgent(text, done);
    }
    window.sendToAgentSystem = function (text, chat, input) {
        routeMessage(text, (reply, fileName, agentId) => {
            if (chat) {
                const msg = document.createElement("p");
                msg.className = "ai-message";
                msg.innerText =
                    reply +
                    (fileName
                        ? `\n\n📄 PDF report save ho gayi: ${fileName}`
                        : "");
                chat.appendChild(msg);
                chat.scrollTop = chat.scrollHeight;
            }
            if (input) input.value = "";
            speakAsAgent(reply, agentId);
        });
    };
    window.agentRouteForDecoder = function (text) {
        return new Promise(resolve => {
            routeMessage(text, (reply, fileName, agentId) => {
                speakAsAgent(reply, agentId);
                resolve(
                    reply +
                        (fileName ? ` (PDF report bhi save ho gayi hai.)` : "")
                );
            });
        });
    };

    document.addEventListener("DOMContentLoaded", buildRooms);
    if (document.readyState !== "loading") buildRooms();

    console.log(
        "🖤 agents.js v10 Loaded — Vera 2 rooms (Work/Sleep) + CCTV wall watching all Shadows, income goal tracker, source breakdown, milestones, weekly/monthly income summary, Baran, Diwan, handwritten notes, health+namaz streak, courses, Shadow Council, colony project"
    );
})();
