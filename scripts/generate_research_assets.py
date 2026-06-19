#!/usr/bin/env python3
"""Generate the web-ready FedThreat-X research asset layer from published results."""

from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

import fitz


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = DOCS / "assets" / "data" / "project-metrics.json"
PAPER = ROOT / "FedThreat-X_A_Privacy-Preserving_Federated_Threat_Intelligence_Framework_for_Multi-Cloud_Cybersecurity.pdf"
FIGURES = DOCS / "assets" / "images" / "figures"
PLOTS = DOCS / "assets" / "images" / "plots"

INK = "#09201c"
MUTED = "#48655c"
GRID = "#d9e7e1"
GREEN = "#159a6d"
CYAN = "#16869a"
AMBER = "#d38716"
RED = "#cd4c4c"
BLUE = "#4c72c9"
PANEL = "#f8fcfa"


def svg(width: int, height: int, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
  <rect width="100%" height="100%" rx="14" fill="{PANEL}"/>
  <style>text{{font-family:Arial,sans-serif;fill:{INK}}}.muted{{fill:{MUTED};font-size:13px}}.title{{font-size:19px;font-weight:700}}.label{{font-size:12px}}</style>{body}</svg>'''


def write(name: str, body: str) -> None:
    (PLOTS / name).write_text(svg(900, 500, body), encoding="utf-8")


def grid(x: int = 78, y: int = 78, w: int = 760, h: int = 330) -> str:
    lines = [f'<line x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}" stroke="{INK}" stroke-width="1"/>', f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+h}" stroke="{INK}" stroke-width="1"/>']
    for step in range(1, 5):
        yy = y + h - step * h / 5
        lines.append(f'<line x1="{x}" y1="{yy}" x2="{x+w}" y2="{yy}" stroke="{GRID}" stroke-width="1"/>')
    return "".join(lines)


def plot_dist(metrics: dict) -> None:
    values = [m["f1"] for m in metrics["models"]]
    bins = [92, 94, 96, 98, 100]
    counts = [sum(left <= value < right or (right == 100 and value == right) for value in values) for left, right in zip(bins, bins[1:])]
    bars = "".join(f'<rect x="{140+i*145}" y="{408-count*94}" width="92" height="{count*94}" rx="4" fill="{GREEN}" opacity="{0.48+i*0.1}"/><text x="{185+i*145}" y="438" class="label" text-anchor="middle">{bins[i]}-{bins[i+1]}</text><text x="{185+i*145}" y="{394-count*94}" class="label" text-anchor="middle">{count}</text>' for i, count in enumerate(counts))
    body = f'<text x="48" y="42" class="title">DistPlot: Reported F1-score distribution</text><text x="48" y="64" class="muted">Derived from the published model-comparison table</text>{grid()}{bars}<text x="458" y="478" class="muted" text-anchor="middle">F1-score band (%)</text>'
    write("distplot-f1-distribution.svg", body)


def plot_pie(metrics: dict) -> None:
    classes = metrics["dataset"]["class_totals"]
    total = sum(classes.values())
    colors = [GREEN, CYAN, RED]
    start = -90
    paths = []
    legend = []
    for idx, ((name, count), color) in enumerate(zip(classes.items(), colors)):
        angle = count / total * 360
        end = start + angle
        import math
        x1, y1 = 285 + 150 * math.cos(math.radians(start)), 260 + 150 * math.sin(math.radians(start))
        x2, y2 = 285 + 150 * math.cos(math.radians(end)), 260 + 150 * math.sin(math.radians(end))
        large = 1 if angle > 180 else 0
        paths.append(f'<path d="M285 260 L{x1:.1f} {y1:.1f} A150 150 0 {large} 1 {x2:.1f} {y2:.1f} Z" fill="{color}"/>')
        legend.append(f'<rect x="525" y="{160+idx*72}" width="16" height="16" rx="3" fill="{color}"/><text x="552" y="174" class="label">{escape(name)}: {count:,}</text><text x="552" y="194" class="muted">{count/total*100:.1f}% of evaluation set</text>')
        start = end
    body = '<text x="48" y="42" class="title">Pie Chart: GUIDE evaluation-class composition</text><text x="48" y="64" class="muted">300,000 published evaluation instances</text>' + ''.join(paths) + '<circle cx="285" cy="260" r="72" fill="#f8fcfa"/><text x="285" y="255" text-anchor="middle" style="font-size:22px;font-weight:700">300K</text><text x="285" y="278" class="muted" text-anchor="middle">instances</text>' + ''.join(legend)
    write("pie-guide-class-composition.svg", body)


def plot_violin(metrics: dict) -> None:
    values = [("Accuracy", [m["accuracy"] for m in metrics["models"]], GREEN), ("Precision", [m["precision"] for m in metrics["models"]], CYAN), ("Recall", [m["recall"] for m in metrics["models"]], AMBER), ("F1-score", [m["f1"] for m in metrics["models"]], BLUE)]
    shapes = []
    for i, (name, nums, color) in enumerate(values):
        cx = 170 + i * 185
        lo, hi = min(nums), max(nums)
        y_hi = 408 - (hi - 92) / 8 * 290
        y_lo = 408 - (lo - 92) / 8 * 290
        mid = (y_hi + y_lo) / 2
        shapes.append(f'<path d="M{cx} {y_hi} C{cx-65} {y_hi+42} {cx-65} {y_lo-42} {cx} {y_lo} C{cx+65} {y_lo-42} {cx+65} {y_hi+42} {cx} {y_hi}Z" fill="{color}" fill-opacity=".58"/><line x1="{cx-42}" y1="{mid}" x2="{cx+42}" y2="{mid}" stroke="{INK}" stroke-width="2"/><text x="{cx}" y="438" class="label" text-anchor="middle">{name}</text>')
    labels = ''.join(f'<text x="66" y="{408-i*72.5}" class="label" text-anchor="end">{92+i*2}%</text>' for i in range(5))
    body = f'<text x="48" y="42" class="title">ViolinPlot: Model metric stability</text><text x="48" y="64" class="muted">Distribution across the five published model rows</text>{grid()}{labels}{"".join(shapes)}'
    write("violin-model-metric-distribution.svg", body)


def plot_heatmap() -> None:
    matrix = [[178400, 900, 700], [1000, 73500, 500], [600, 200, 44200]]
    labels = ["TP", "BP", "FP"]
    cells = []
    maximum = max(max(row) for row in matrix)
    for row, values in enumerate(matrix):
        for col, value in enumerate(values):
            alpha = 0.16 + value / maximum * 0.84
            x, y = 210 + col * 165, 118 + row * 100
            cells.append(f'<rect x="{x}" y="{y}" width="156" height="92" rx="6" fill="{GREEN}" fill-opacity="{alpha:.2f}"/><text x="{x+78}" y="{y+50}" text-anchor="middle" style="font-size:18px;font-weight:700;fill:{"#ffffff" if alpha > .65 else INK}">{value:,}</text>')
    axes = ''.join(f'<text x="{288+i*165}" y="98" class="label" text-anchor="middle">Predicted {label}</text><text x="190" y="{170+i*100}" class="label" text-anchor="end">Actual {label}</text>' for i, label in enumerate(labels))
    body = f'<text x="48" y="42" class="title">HeatMap: Published confusion-matrix narrative</text><text x="48" y="64" class="muted">TP, BP, and FP counts reported for the 300K evaluation split</text>{axes}{"".join(cells)}<text x="458" y="460" class="muted" text-anchor="middle">Strong diagonal concentration supports stable incident triage</text>'
    write("heatmap-confusion-matrix.svg", body)


def plot_pair(metrics: dict) -> None:
    rows = [("Accuracy", "Precision", GREEN), ("Recall", "F1-score", CYAN), ("Accuracy", "F1-score", AMBER), ("Precision", "Recall", BLUE)]
    fields = {"Accuracy": "accuracy", "Precision": "precision", "Recall": "recall", "F1-score": "f1"}
    panes = []
    for idx, (x_name, y_name, color) in enumerate(rows):
        ox, oy = (70 if idx % 2 == 0 else 485), (90 if idx < 2 else 295)
        panes.append(f'<rect x="{ox}" y="{oy}" width="345" height="155" rx="8" fill="#eef7f3" stroke="{GRID}"/><text x="{ox+14}" y="{oy+22}" class="label">{x_name} vs {y_name}</text>')
        for model in metrics["models"]:
            x = ox + 40 + (model[fields[x_name]] - 92) / 8 * 265
            y = oy + 130 - (model[fields[y_name]] - 92) / 8 * 90
            panes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{color}"/><text x="{x+9:.1f}" y="{y+4:.1f}" class="label">{escape(model["name"])}</text>')
    body = f'<text x="48" y="42" class="title">PairPlot: Relationships among published performance metrics</text><text x="48" y="64" class="muted">Each point is a baseline or the proposed FedThreat-X model</text>{"".join(panes)}'
    write("pairplot-model-metrics.svg", body)


def plot_joint(metrics: dict) -> None:
    features = metrics["feature_importance"]
    points = []
    for idx, (name, importance) in enumerate(features):
        x = 112 + (importance - 3) / 16 * 650
        y = 360 - (idx % 5) * 42 - (importance / 18.2) * 70
        radius = 5 + importance * .55
        points.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{CYAN}" fill-opacity=".68"/><text x="{x+radius+5:.1f}" y="{y+4:.1f}" class="label">{escape(name)}</text>')
    bars = ''.join(f'<rect x="{112+i*66}" y="425" width="38" height="{importance*2.6:.1f}" fill="{GREEN}" opacity=".75"/>' for i, (_, importance) in enumerate(features))
    body = f'<text x="48" y="42" class="title">JointPlot: Feature-importance distribution</text><text x="48" y="64" class="muted">Importance values from the paper discussion; marginal bars preserve the same ranking</text>{grid(90, 90, 700, 290)}<line x1="105" y1="365" x2="775" y2="160" stroke="{AMBER}" stroke-width="2" stroke-dasharray="7 6"/>{"".join(points)}<text x="450" y="486" class="muted" text-anchor="middle">Feature importance</text>{bars}'
    write("jointplot-feature-importance.svg", body)


def render_paper_preview() -> None:
    if not PAPER.exists():
        return
    document = fitz.open(PAPER)
    try:
        pix = document[0].get_pixmap(matrix=fitz.Matrix(1.7, 1.7), alpha=False)
        pix.save(FIGURES / "paper-first-page.png")
    finally:
        document.close()


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    PLOTS.mkdir(parents=True, exist_ok=True)
    metrics = json.loads(DATA.read_text(encoding="utf-8"))
    render_paper_preview()
    plot_dist(metrics)
    plot_pie(metrics)
    plot_violin(metrics)
    plot_heatmap()
    plot_pair(metrics)
    plot_joint(metrics)
    print(f"Generated research assets in {PLOTS}")


if __name__ == "__main__":
    main()
