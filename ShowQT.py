import plotly.offline as pyo
from PyQt5.QtWebEngineWidgets import QWebEngineView

def show_qt(fig):
    raw_html = '<html><head><meta charset="utf-8" />'
    raw_html += '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script></head>'
    raw_html += '<body>'
    raw_html += pyo.plot(fig, include_plotlyjs=False, output_type='div')
    raw_html += '</body></html>'

    fig_view = QWebEngineView()
    # setHtml has a 2MB size limit, need to switch to setUrl on tmp file
    # for large figures.

    fig_view.setHtml(raw_html)

    return fig_view