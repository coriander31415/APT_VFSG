from bokeh.layouts import column
from bokeh.io import output_file, save, show
from src.visualizations.viz1 import viz1
from src.visualizations.viz2 import viz2

def create_dashboard(data):
    """
    Assemble all visualizations into a single dashboard layout.
    """
    kpi_cards = viz1(data)
    main_viz = viz2(data)

    return column(
        kpi_cards,
        main_viz,
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