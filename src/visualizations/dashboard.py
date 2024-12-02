from bokeh.layouts import column
from bokeh.io import output_file, save, show
from src.visualizations.viz_kpi_cards import create_viz_kpi_cards
from src.visualizations.viz2 import create_viz2
from src.visualizations.viz_story import create_viz_story

def create_dashboard(data):
    """
    Assemble all visualizations into a single dashboard layout.
    """
    viz_story = create_viz_story(data)
    viz_kpi_cards = create_viz_kpi_cards(data)
    viz2 = create_viz2(data)

    return column(
        viz_story,
        viz_kpi_cards,
        viz2,
        sizing_mode="stretch_width"
    )

def render_dashboard(data_path):
    """
    Render the dashboard to an HTML file and open it in the browser.
    """
    import pandas as pd
    data = pd.read_csv(data_path)
    dashboard = create_dashboard(data)

    output_file("index.html")
    save(dashboard)
    show(dashboard)