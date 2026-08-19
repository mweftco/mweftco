const API =
  "https://aurelia-backend-0mfy.onrender.com";


const agentsGrid =
  document.getElementById("agentsGrid");

const connection =
  document.getElementById("connection");


function createAgentCard(agent) {

  const card =
    document.createElement("div");

  card.className = "agent-card";


  const statusClass =
    agent.status === "working"
      ? "working"
      : "";


  card.innerHTML = `

    <div class="desk">

      <div class="monitor">
        ${agent.name}
      </div>

    </div>


    <div class="agent-header">

      <div>

        <div class="agent-title">
          ${agent.name}
        </div>

        <div class="agent-role">
          ${agent.role}
        </div>

      </div>

    </div>


    <div class="agent-status ${statusClass}">
      ● ${agent.status.toUpperCase()}
    </div>


    <div class="agent-task">
      ${agent.task}
    </div>

  `;


  return card;
}


async function loadColony() {

  try {

    connection.textContent =
      "COLONY CONNECTED";

    const response =
      await fetch(
        `${API}/api/aurelia/colony`
      );


    if (!response.ok) {
      throw new Error(
        "Colony API failed"
      );
    }


    const data =
      await response.json();


    agentsGrid.innerHTML = "";


    data.agents
      .filter(
        agent => agent.id !== "vera"
      )
      .forEach(
        agent => {

          agentsGrid.appendChild(
            createAgentCard(agent)
          );

        }
      );


  } catch (error) {

    console.error(error);

    connection.textContent =
      "COLONY OFFLINE";

  }

}


loadColony();


setInterval(
  loadColony,
  10000
);
