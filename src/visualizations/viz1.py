from bokeh.models import Div
from bokeh.layouts import row

def viz1(data):
    """
    Generate KPI cards as the first visualization.
    """
    kpi_values = {
        'Regions': data['Region'].nunique(),
        'Countries': data['Country'].nunique(),
        'Indicators': data['Indicator'].nunique(),
        'Yes Status': (data['Input'] == 1).sum()
    }

    # Create KPI cards as HTML divs
    kpi_cards = []
    for key, value in kpi_values.items():
        kpi_cards.append(Div(text=f"<h3>{key}</h3><p>{value}</p>", width=200, height=100))

    return row(*kpi_cards)