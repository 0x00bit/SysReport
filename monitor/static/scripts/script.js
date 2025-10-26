const lastUpdate = document.getElementById("last-update");

async function updatePanels() {
    try {
        const response = await fetch("/api/status");
        const result = await response.json();
        const data = result.data;
        const timestamp = result.timestamp;

        for (const [category, hosts] of Object.entries(data)) {
            const panel = document.querySelector(`.panel[data-category="${category}"]`);
            if (!panel) continue;

            hosts.forEach(host => {
                const card = panel.querySelector(`.host-card[data-host="${host.hostname}"]`);

                if (card) {
                    // Atualiza IP
                    const ipElem = card.querySelector("p");
                    if (ipElem.textContent !== host.ip) {
                        ipElem.textContent = host.ip;
                    }

                    // Atualiza status suavemente
                    const isOnline = host.status === 1;
                    if (isOnline && card.classList.contains("offline")) {
                        card.classList.remove("offline");
                        card.classList.add("online");
                    } else if (!isOnline && card.classList.contains("online")) {
                        card.classList.remove("online");
                        card.classList.add("offline");
                    }
                } else {
                    // Se novo host aparecer, adiciona
                    const grid = panel.querySelector(".hosts-grid");
                    const newCard = document.createElement("div");
                    newCard.classList.add("host-card", host.status === 1 ? "online" : "offline");
                    newCard.dataset.host = host.hostname;

                    const h3 = document.createElement("h3");
                    h3.textContent = host.hostname;
                    const p = document.createElement("p");
                    p.textContent = host.ip;

                    newCard.appendChild(h3);
                    newCard.appendChild(p);
                    grid.appendChild(newCard);
                }
            });
        }

        // Atualiza horário
        lastUpdate.textContent = `Última atualização: ${timestamp}`;
    } catch (err) {
        console.error("Erro ao atualizar:", err);
    }
}

setInterval(updatePanels, 10000);
updatePanels();

// ===== MODO NOTURNO =====
const toggleBtn = document.getElementById("toggle-theme");
toggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    toggleBtn.textContent = document.body.classList.contains("dark") ? "☀️" : "🌙";
});
