from bokeh.layouts import column, row
from bokeh.io import output_file, save
from src.visualizations.viz1 import viz1
from src.visualizations.viz2 import viz2

def create_dashboard(data):
    """
    Assemble all visualizations into a single dashboard layout.
    """
    # Load data for visualizations
    kpi_cards = viz1(data)
    main_viz = viz2(data)

    # Combine into layout
    dashboard_layout = column(
        kpi_cards,
        main_viz,
        sizing_mode="stretch_width"
    )

    return dashboard_layout

def render_dashboard(data_path):
    """
    Render the dashboard to an HTML file.
    """
    import pandas as pd
    data = pd.read_csv(data_path)

    dashboard = create_dashboard(data)

    # Output to HTML
    output_file("APT_VFSG.html")
    save(dashboard)