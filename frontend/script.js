const API = "http://127.0.0.1:9000";

/* --------------------------
   REGISTER
-------------------------- */
async function register() {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password")?.value;

    if (!email || !password) {
        alert("Please enter email and password");
        return;
    }

    try {
        const response = await fetch(`${API}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.message || "Registration failed");
            return;
        }

        alert("Registered Successfully!");
        window.location.href = "login.html";

    } catch (error) {
        alert("Server not responding.");
    }
}

/* --------------------------
   LOGIN
-------------------------- */
async function login() {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password")?.value;

    if (!email || !password) {
        alert("Please enter email and password");
        return;
    }

    try {
        const response = await fetch(`${API}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.message || "Invalid credentials");
            return;
        }

        localStorage.setItem("user", email);
        window.location.href = "dashboard.html";

    } catch (error) {
        alert("Server not responding.");
    }
}

/* --------------------------
   LOGOUT
-------------------------- */
function logout() {
    localStorage.removeItem("user");
    window.location.href = "index.html";
}

/* --------------------------
   PROTECT DASHBOARD
-------------------------- */
(function protectDashboard() {
    if (window.location.pathname.includes("dashboard.html")) {
        const user = localStorage.getItem("user");
        if (!user) {
            window.location.href = "login.html";
        }
    }
})();

/* --------------------------
   PORTFOLIO GENERATION
-------------------------- */

let allocationChart = null;
let stressChart = null;

async function generate() {

    const profile = {
        age: +age.value,
        income: +income.value,
        years: +years.value,
        loss: +loss.value,
        amount: +amount.value
    };

    if (Object.values(profile).some(v => isNaN(v))) {
        alert("Please fill all fields correctly.");
        return;
    }

    document.getElementById("riskScore").innerText = "Analyzing...";
    document.getElementById("explanation").innerText = "Generating portfolio strategy...";

    try {
        const response = await fetch(`${API}/generate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(profile)
        });

        const data = await response.json();

        if (!response.ok) {
            alert("Error generating portfolio.");
            return;
        }

        updateUI(data);

    } catch (error) {
        alert("Backend server not responding.");
    }
}

/* --------------------------
   UPDATE UI
-------------------------- */

function updateUI(data) {

    document.getElementById("riskScore").innerText =
        "Risk Score: " + data.risk_score;

    document.getElementById("explanation").innerText =
        data.explanation;

    updateAllocationChart(data.allocation);
    updateStressChart(data.stress_test);

    const logList = document.getElementById("logs");
    logList.innerHTML = "";

    data.logs.forEach(log => {
        const li = document.createElement("li");
        li.textContent = log;
        logList.appendChild(li);
    });
}

/* --------------------------
   OPTIMIZED CHART UPDATES
-------------------------- */

function updateAllocationChart(allocation) {

    const labels = Object.keys(allocation);
    const values = Object.values(allocation);

    if (!allocationChart) {
        allocationChart = new Chart(
            document.getElementById("allocationChart"),
            {
                type: "doughnut",
                data: {
                    labels,
                    datasets: [{ data: values }]
                },
                options: {
                    responsive: true,
                    animation: { duration: 800 }
                }
            }
        );
    } else {
        allocationChart.data.labels = labels;
        allocationChart.data.datasets[0].data = values;
        allocationChart.update();
    }
}

function updateStressChart(stress) {

    const labels = Object.keys(stress);
    const values = Object.values(stress);

    if (!stressChart) {
        stressChart = new Chart(
            document.getElementById("stressChart"),
            {
                type: "bar",
                data: {
                    labels,
                    datasets: [{
                        label: "Portfolio Value",
                        data: values
                    }]
                },
                options: {
                    responsive: true,
                    animation: { duration: 800 }
                }
            }
        );
    } else {
        stressChart.data.labels = labels;
        stressChart.data.datasets[0].data = values;
        stressChart.update();
    }
}