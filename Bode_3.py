import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# =========================
# Load CSV

# =========================
CSV_PATH = "pvn20.csv"

data = pd.read_csv(CSV_PATH, sep=None, engine="python")
data.columns = data.columns.str.strip().str.lower()

# =========================
# Detect datasets
# =========================
sets = sorted([int(col.split("_")[1]) for col in data.columns if "frequency_" in col])
set_names = [f"Set {i}" for i in sets]

colors = [
"#1f77b4","#ff7f0e","#2ca02c","#d62728",
"#9467bd","#8c564b","#e377c2","#7f7f7f",
"#bcbd22","#17becf",
"#393b79","#637939","#8c6d31","#843c39",
"#7b4173","#3182bd","#e6550d","#31a354",
"#756bb1","#636363"
]

# =========================
# Function to extract data
# =========================
def get_set_data(i):

    freq = data[f"frequency_{i}"].dropna() /1e6
    gain = data[f"gain_{i}"].dropna()

    return freq, gain


# =========================
# Dash App
# =========================
app = Dash(__name__)
app.title = "Gain vs Frequency Dashboard"

app.layout = html.Div(

    style={
        "height": "100vh",
        "display": "flex",
        "flexDirection": "column",
        "margin": "0px"
    },

    children=[

        html.H3(
            "Frequency vs Gain Analysis",
            style={"textAlign": "center", "margin": "5px"}
        ),

        html.Div([

            html.Label("Select Dataset"),

            dcc.Dropdown(
                id="dataset",
                options=[{"label": f"Set {i}", "value": i} for i in sets],
                value=sets[0],
                clearable=False,
                style={"width": "200px"}
            )

        ], style={
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "gap": "10px",
            "marginBottom": "5px"
        }),

        dcc.Graph(
            id="gain-graph",
            style={"flexGrow": "1"}
        )
    ]
)


# =========================
# Callback
# =========================
@app.callback(
    Output("gain-graph", "figure"),
    Input("dataset", "value")
)
def update_graph(selected_set):

    fig = go.Figure()

    # background traces
    for i in sets:

        freq, gain = get_set_data(i)

        fig.add_trace(go.Scatter(
            x=freq,
            y=gain,
            line=dict(color=colors[(i-1) % len(colors)]),
            opacity=0.2,
            showlegend=False
        ))

    # highlight selected
    freq, gain = get_set_data(selected_set)

    fig.add_trace(go.Scatter(
        x=freq,
        y=gain,
        name=f"Set {selected_set}",
        line=dict(width=3, color=colors[(selected_set-1) % len(colors)])
    ))

    fig.update_layout(

        template="plotly_white",

        margin=dict(l=40, r=20, t=20, b=40),

        xaxis=dict(
            title="Frequency (MHz)",
            type="linear"
        ),

        yaxis=dict(
            title="Gain (dB)"
        )
    )

    return fig


# =========================
# Run
# =========================
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port)
