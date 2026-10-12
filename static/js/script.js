
let crimeChart;
let categoryChart;
let crimeMap;

async function loadChart(district = "New Delhi") {
    const res = await fetch(`/api/chart-data?district=${district}`);
    const data = await res.json();
    const ctx = document.getElementById("crimeChart");

    if (crimeChart) crimeChart.destroy();

    crimeChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: data.years,
            datasets: [
                { label: "Violent Crimes", data: data.violent },
                { label: "Property Crimes", data: data.property },
                { label: "Crimes Against Women", data: data.women },
                { label: "Total Crimes", data: data.total }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: `${district} Crime Trend` }
            }
        }
    });
}

async function loadCategoryChart(district = "New Delhi") {
    const res = await fetch(`/api/category-share?district=${district}`);
    const data = await res.json();
    const ctx = document.getElementById("categoryChart");

    if (categoryChart) categoryChart.destroy();

    categoryChart = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: data.labels,
            datasets: [{ data: data.values }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: `${district} Latest Crime Category Share` }
            }
        }
    });
}

async function predictCrime() {
    const state = document.getElementById("stateInput").value;
    const district = document.getElementById("districtInput").value;
    const year = document.getElementById("yearInput").value;

    const res = await fetch("/api/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({state, district, year})
    });

    const data = await res.json();

    document.getElementById("predictionResult").innerHTML = `
        <h6>Prediction Result</h6>
        <p><b>Predicted Total Crime:</b> ${data.predicted_total_crime}</p>
        <p><b>Current Risk Score:</b> ${data.current_risk_score}</p>
        <p><b>Risk Level:</b> ${data.current_risk_level}</p>
        <p><b>Trend:</b> ${data.trend}</p>
        <p><b>AI Insight:</b> ${data.smart_insight}</p>
    `;
}

async function trainModel() {
    const res = await fetch("/api/train");
    const data = await res.json();

    document.getElementById("modelResult").innerHTML = `
        <h6>Model Comparison</h6>
        <p><b>Random Forest:</b> R² = ${data["Random Forest"]["R2 Score"]}, MAE = ${data["Random Forest"]["MAE"]}</p>
        <p><b>Linear Regression:</b> R² = ${data["Linear Regression"]["R2 Score"]}, MAE = ${data["Linear Regression"]["MAE"]}</p>
    `;
}

async function loadMap() {
    const res = await fetch("/api/map-data");
    const data = await res.json();

    crimeMap = L.map("crimeMap").setView([22.9734, 78.6569], 5);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18,
        attribution: "© OpenStreetMap"
    }).addTo(crimeMap);

    data.forEach(item => {
        let radius = Math.max(8, item.risk_score / 30);

        L.circleMarker([item.latitude, item.longitude], {
            radius: radius,
            fillOpacity: 0.65,
            weight: 1
        }).addTo(crimeMap)
        .bindPopup(`
            <b>${item.district}, ${item.state}</b><br>
            Total Crimes: ${item.total_crimes}<br>
            Risk Score: ${item.risk_score.toFixed(2)}<br>
            Risk Level: ${item.risk_level}
        `);
    });
}

document.getElementById("districtSelect").addEventListener("change", function () {
    loadChart(this.value);
    loadCategoryChart(this.value);
});

document.getElementById("districtInput").addEventListener("change", function () {
    loadCategoryChart(this.value);
});

loadChart();
loadCategoryChart();
loadMap();
