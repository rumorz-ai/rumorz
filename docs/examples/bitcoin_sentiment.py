import os

import plotly.graph_objects as go
import plotly.io as pio

from rumorz.client import RumorzClient
from rumorz.enums import Lookback
from rumorz_data.constants import RMZ_EMOTIONS

rumorz = RumorzClient(api_key=os.environ['RUMORZ_API_KEY'],
                      api_url='http://localhost:8000')

entities = rumorz.graph.search_entities(**{
    "name": "Bitcoin",
    "symbol_search": "BTC",
    "limit": 1
})
assert len(entities) == 1, "Bitcoin entity search returned an unexpected number of results"
bitcoin_node_id = entities[0]['id']
df = rumorz.graph.get_metrics(
    ids=[bitcoin_node_id],
    lookback=Lookback.THREE_MONTHS,
    limit=10000,
    as_df=True
)

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
