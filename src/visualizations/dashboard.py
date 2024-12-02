from bokeh.layouts import column, row
from bokeh.io import output_file, save, show
from bokeh.models import Div, Spacer
from src.visualizations.viz_kpi_cards import create_viz_kpi_cards
from src.visualizations.viz_breakdown import create_viz_breakdown
from src.visualizations.viz_story import create_viz_story

def create_dashboard(data):
    """
    Assemble all visualizations into a single dashboard layout.
    """
    viz_story = create_viz_story(data)
    viz_kpi_cards = create_viz_kpi_cards(data)
    viz_breakdown = create_viz_breakdown(data)

    apt_logo = Div(
        text="<img src='assets/apt_logo_en_pos_pantone.jpg' style='max-height: 250px;'>",
        width=300, height=300
    )
    vfsg_logo = Div(
        text="<img src='assets/VFSG_logo.png' style='max-height: 120px;'>"
    )

    header = row(
        apt_logo,
        Spacer(sizing_mode="stretch_width"),
        vfsg_logo,
        sizing_mode="stretch_width",
        height=250 
    )

    content = column(
        viz_story,
        viz_kpi_cards,
        viz_breakdown,
        sizing_mode="stretch_width"
    )

    dashboard = column(
        header, 
        content, 
        sizing_mode="stretch_width",
        margin=(10, 10, 10, 10)
    )
    return dashboard

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