const apiBase = "/api";

async function loadMetrics() {
    const res = await fetch(`${apiBase}/metrics`);
    const data = await res.json();
    const metricSelect = document.getElementById("metric");
    metricSelect.innerHTML = "";
    data.metrics.forEach(m => {
        const opt = document.createElement("option");
        opt.value = m;
        opt.text = m;
        metricSelect.add(opt);
    });
    return data.metrics[0];
}

async function loadWindows(metric) {
    const res = await fetch(`${apiBase}/metrics/${metric}/windows`);
    const data = await res.json();
    const windowSelect = document.getElementById("window");
    windowSelect.innerHTML = "";
    data.windows.forEach(w => {
        const opt = document.createElement("option");
        opt.value = w;
        opt.text = w;
        windowSelect.add(opt);
    });
    return data.windows[0];
}

async function updateChart() {
    const metric = document.getElementById("metric").value;
    const window = document.getElementById("window").value;
    const n = document.getElementById("n").value;

    const res = await fetch(`${apiBase}/top?metric=${metric}&window=${window}&n=${n}`);
    const data = await res.json();

    const tickers = data.map(d => d.ticker);
    const values = data.map(d => d.value);

    Plotly.newPlot("chart", [
        {
            x: tickers,
            y: values,
            type: "bar"
        }
    ], {
        title: `Top ${n} stocks by ${metric} (${window})`,
        margin: { t: 40 }
    });
}

function updateGraph() {
    const metric = document.getElementById("metricSelect").value;
    const window = document.getElementById("windowSelect").value || "1y";
    const n = document.getElementById("nInput").value || 5;

    console.log("Requesting:", metric, window, n);

    const url = `/api/graph?metric=${encodeURIComponent(metric)}&window=${encodeURIComponent(window)}&n=${n}`;

    document.getElementById("graphFrame").src = url;
}

// Load default graph on page load
window.onload = updateGraph;

(async function init() {
    const firstMetric = await loadMetrics();
    await loadWindows(firstMetric);
    await updateChart();
})();