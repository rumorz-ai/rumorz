import os

import plotly.graph_objects as go
import plotly.io as pio

from rumorz.client import RumorzClient
from rumorz_data.constants import RMZ_EMOTIONS

rumorz = RumorzClient(api_key=os.environ['RUMORZ_API_KEY'])

bitcoin_node_id = '7d8d81b3-0808-47ce-b459-a9fd5f74fd57'

df = rumorz.graph.get_entity_timeseries(**{
    "node_ids": [
        bitcoin_node_id
    ],
    "metrics": [
        "price",
        "sentiment"
    ],
    "lookback": "3M",
    "page": 1,
    "limit": 100
},
                                        as_df=True)

fig = go.Figure()
df = df[bitcoin_node_id]
for score in ['sentiment'] + RMZ_EMOTIONS:
    toplot = df[score].ewm(alpha=0.01, adjust=False).mean()
    fig.add_trace(go.Scatter(x=df.index, y=toplot, mode='lines', name=score, line=dict(width=1)))

fig.update_layout(
    title={
        'text': 'Bitcoin Sentiment and Emotion Scores Over the Last 3 Months',
        'font': {
            'size': 25
        }
    },
    xaxis_title='Date',
    yaxis_title='Score',
    legend_title='Scores',
    template='plotly_dark'
)

report_path = 'bitcoin_sentiment_report.html'
pio.write_html(fig, file=report_path, auto_open=True)
