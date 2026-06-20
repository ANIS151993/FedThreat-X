const plotConfig = {
  responsive: true,
  displaylogo: false,
  modeBarButtonsToRemove: ["lasso2d", "select2d"]
};

const palette = {
  green: "#5ee0a0",
  cyan: "#50c7d8",
  amber: "#f3bd5f",
  red: "#ff6b6b",
  blue: "#7aa2ff",
  ink: "#f4fbf8",
  muted: "#a8bbb4",
  panel: "#101a17",
  paper: "#08100d"
};

const layoutBase = {
  paper_bgcolor: "rgba(0,0,0,0)",
  plot_bgcolor: "rgba(255,255,255,0.03)",
  font: { color: palette.ink, family: "Inter, sans-serif" },
  margin: { t: 48, r: 24, b: 56, l: 58 },
  xaxis: { gridcolor: "rgba(244,251,248,0.12)", zerolinecolor: "rgba(244,251,248,0.14)" },
  yaxis: { gridcolor: "rgba(244,251,248,0.12)", zerolinecolor: "rgba(244,251,248,0.14)" },
  legend: { orientation: "h", y: -0.22 }
};

const models = ["CNN", "LSTM", "GNN-TI", "BiLSTM", "FedThreat-X"];
const accuracy = [94.10, 95.20, 96.40, 96.85, 98.70];
const precision = [92.85, 94.10, 95.30, 96.00, 98.30];
const recall = [93.40, 94.65, 95.90, 96.35, 98.57];
const f1 = [93.12, 94.37, 95.60, 96.17, 98.70];

function normalSeries(mean, scale, n) {
  return Array.from({ length: n }, (_, i) => {
    const wave = Math.sin(i * 1.7) + Math.cos(i * 0.43);
    return Number((mean + wave * scale + ((i % 9) - 4) * scale * 0.15).toFixed(3));
  });
}

function makePlot(id, data, layout) {
  const el = document.getElementById(id);
  if (!el || !window.Plotly) return;
  Plotly.newPlot(el, data, { ...layoutBase, ...layout }, plotConfig);
}

function drawCharts() {
  makePlot("performanceChart", [
    { x: models, y: accuracy, name: "Accuracy", type: "bar", marker: { color: palette.green } },
    { x: models, y: precision, name: "Precision", type: "scatter", mode: "lines+markers", line: { color: palette.cyan, width: 3 } },
    { x: models, y: recall, name: "Recall", type: "scatter", mode: "lines+markers", line: { color: palette.amber, width: 3 } },
    { x: models, y: f1, name: "F1-score", type: "scatter", mode: "lines+markers", line: { color: palette.blue, width: 3 } }
  ], {
    title: "Baseline Models vs FedThreat-X",
    yaxis: { ...layoutBase.yaxis, range: [90, 100], title: "Percent" }
  });

  makePlot("distChart", [
    { x: normalSeries(0.987, 0.012, 180), type: "histogram", histnorm: "probability density", name: "FedThreat-X", marker: { color: "rgba(94,224,160,0.68)" } },
    { x: normalSeries(0.964, 0.018, 180), type: "histogram", histnorm: "probability density", name: "GNN-TI", marker: { color: "rgba(80,199,216,0.58)" } },
    { x: normalSeries(0.952, 0.022, 180), type: "histogram", histnorm: "probability density", name: "LSTM", marker: { color: "rgba(243,189,95,0.54)" } }
  ], {
    title: "DistPlot: Detection Confidence Distribution",
    barmode: "overlay",
    xaxis: { ...layoutBase.xaxis, title: "Confidence" },
    yaxis: { ...layoutBase.yaxis, title: "Density" }
  });

  makePlot("pieChart", [{
    labels: ["True Positive", "Benign Positive", "False Positive"],
    values: [180000, 75000, 45000],
    type: "pie",
    hole: 0.45,
    marker: { colors: [palette.green, palette.cyan, palette.red] },
    textinfo: "label+percent"
  }], {
    title: "Pie Chart: GUIDE Evaluation Class Mix",
    showlegend: false
  });

  makePlot("violinChart", [
    { y: normalSeries(0.038, 0.008, 120), type: "violin", name: "Train loss", box: { visible: true }, meanline: { visible: true }, line: { color: palette.green } },
    { y: normalSeries(0.068, 0.012, 120), type: "violin", name: "Validation loss", box: { visible: true }, meanline: { visible: true }, line: { color: palette.amber } },
    { y: normalSeries(0.987, 0.01, 120), type: "violin", name: "Validation accuracy", box: { visible: true }, meanline: { visible: true }, line: { color: palette.cyan } }
  ], {
    title: "ViolinPlot: Final-Round Stability",
    yaxis: { ...layoutBase.yaxis, title: "Score / Loss" }
  });

  makePlot("heatmapChart", [{
    z: [
      [178400, 900, 700],
      [1000, 73500, 500],
      [600, 200, 44200]
    ],
    x: ["TP", "BP", "FP"],
    y: ["TP", "BP", "FP"],
    type: "heatmap",
    colorscale: [[0, "#13221e"], [0.45, "#50c7d8"], [1, "#5ee0a0"]],
    hovertemplate: "Actual %{y}<br>Predicted %{x}<br>%{z:,}<extra></extra>"
  }], {
    title: "HeatMap: Confusion Matrix",
    xaxis: { ...layoutBase.xaxis, title: "Predicted" },
    yaxis: { ...layoutBase.yaxis, title: "Actual" }
  });

  makePlot("pairChart", [{
    type: "splom",
    dimensions: [
      { label: "Accuracy", values: accuracy },
      { label: "Precision", values: precision },
      { label: "Recall", values: recall },
      { label: "F1", values: f1 }
    ],
    text: models,
    marker: {
      color: [1, 2, 3, 4, 5],
      colorscale: [[0, palette.red], [0.5, palette.cyan], [1, palette.green]],
      size: 9,
      line: { color: "rgba(244,251,248,0.6)", width: 1 }
    }
  }], {
    title: "PairPlot: Metric Relationships",
    height: 520
  });

  makePlot("jointChart", [{
    x: [18.2, 15.3, 13.8, 7.5, 7.5, 6.0, 5.3, 3.8, 3.2, 3.0],
    y: [0.987, 0.983, 0.981, 0.972, 0.971, 0.966, 0.962, 0.954, 0.951, 0.948],
    mode: "markers+text",
    type: "scatter",
    text: ["MITRE", "AccountUpn", "Category", "IP", "Entity", "Day", "ObjectId", "Folder", "URL", "Device"],
    textposition: "top center",
    marker: { size: [30, 26, 24, 18, 18, 16, 15, 13, 12, 12], color: palette.green, opacity: 0.78 }
  }, {
    x: [3, 20],
    y: [0.948, 0.989],
    mode: "lines",
    name: "trend",
    line: { color: palette.cyan, width: 2, dash: "dot" }
  }], {
    title: "JointPlot: Feature Importance vs Detection Confidence",
    xaxis: { ...layoutBase.xaxis, title: "Feature importance" },
    yaxis: { ...layoutBase.yaxis, title: "Detection confidence" }
  });
}

function initVideoChapters() {
  const player = document.getElementById("research-video-player");
  const buttons = document.querySelectorAll(".chapter-button");
  const title = document.getElementById("video-chapter-title");
  const note = document.getElementById("video-chapter-note");
  if (!player || !buttons.length || !title || !note) return;

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      buttons.forEach((item) => item.classList.toggle("is-active", item === button));
      title.textContent = button.dataset.videoTitle || "Research video";
      note.textContent = button.dataset.videoNote || "";
      player.src = `https://www.youtube.com/embed/8kYnDgFR79g?rel=0&start=${button.dataset.videoStart || "0"}`;
    });
  });
}

function initDownloadGate() {
  const overlay = document.getElementById("download-gate");
  const next = document.getElementById("gate-next");
  const checks = [document.getElementById("gate-use"), document.getElementById("gate-cite")];
  if (!overlay || !next || checks.some((check) => !check)) return;

  const close = () => overlay.classList.add("is-hidden");
  document.querySelectorAll("[data-open-gate]").forEach((button) => button.addEventListener("click", () => overlay.classList.remove("is-hidden")));
  document.querySelectorAll("[data-close-gate]").forEach((button) => button.addEventListener("click", close));
  overlay.addEventListener("click", (event) => { if (event.target === overlay) close(); });
  document.addEventListener("keydown", (event) => { if (event.key === "Escape") close(); });
  checks.forEach((check) => check.addEventListener("change", () => { next.disabled = !checks.every((item) => item.checked); }));
  next.addEventListener("click", () => {
    overlay.querySelector('[data-gate-step="1"]').classList.add("is-hidden");
    overlay.querySelector('[data-gate-step="2"]').classList.remove("is-hidden");
  });
}

document.addEventListener("DOMContentLoaded", () => {
  drawCharts();
  initVideoChapters();
  initDownloadGate();
});
