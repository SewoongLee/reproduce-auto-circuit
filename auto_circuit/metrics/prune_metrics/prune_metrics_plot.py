from typing import Any, Dict, List, Optional

import plotly.express as px
import plotly.graph_objects as go

from auto_circuit.prune_algos.prune_algos import PRUNE_ALGO_DICT
from auto_circuit.types import TaskMeasurements


def edge_patching_plot(
    data: List[Dict[str, Any]],
    task_measurements: TaskMeasurements,
    metric_name: str,
    log_x: bool,
    log_y: bool,
    y_axes_match: bool,
    token_circuit: bool,
    y_max: Optional[float],
    y_min: Optional[float],
) -> go.Figure:
    data = sorted(data, key=lambda x: (x["Algorithm"], x["Task"]))
    fig = px.line(
        data,
        x="X",
        y="Y",
        facet_col="Task",
        color="Algorithm",
        log_x=log_x,
        log_y=log_y,
        range_y=None if y_max is None else [y_min, y_max * 0.8],
        # range_y=[-45, 120],
        facet_col_spacing=0.03 if y_axes_match else 0.06,
        markers=True,
    )
    fig.update_layout(
        # title=f"{main_title}: {metric_name} vs. Patched Edges",
        yaxis_title=metric_name,
        template="plotly",
        # width=335 * len(set([d["Task"] for d in data])) + 280,
        width=365 * len(set([d["Task"] for d in data])) - 10,
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.7,
            xanchor="left",
            x=0.0,
            entrywidthmode="fraction",
            entrywidth=0.25,
        ),
    )
    task_measurements = dict(sorted(task_measurements.items(), key=lambda x: x[0]))
    for task_idx, algo_measurements in enumerate(task_measurements.values()):
        for algo_key, measurements in algo_measurements.items():
            algo = PRUNE_ALGO_DICT[algo_key]
            pos = "middle right" if algo.short_name == "GT" else "middle left"
            if len(measurements) == 1:
                x, y = measurements[0]
                fig.add_scattergl(
                    row=1,
                    col=task_idx + 1,
                    x=[x],
                    y=[y],
                    mode="markers+text",
                    text=algo.short_name if algo.short_name else algo.name,
                    textposition=pos,
                    showlegend=task_idx == 0,
                    marker=dict(color="black", size=10, symbol="x-thin"),
                    marker_line_width=2,
                    name=algo.short_name,
                )

    fig.update_yaxes(matches=None, showticklabels=True) if not y_axes_match else None
    fig.update_xaxes(matches=None, title="Circuit Edges")
    return fig
