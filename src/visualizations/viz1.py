from bokeh.models import Div, ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.layouts import column, gridplot
import pandas as pd
import datetime


def create_kpi_card_with_chart(indicator, data):
    """
    Create a single adaptive KPI card with a chart.
    """
    filtered_data = data[data["Indicator"] == indicator].copy()

    # Calculate percentage of "Yes" and "Partially"
    total_count = len(filtered_data)
    yes_partially_count = ((filtered_data["Input"] == 1) | (filtered_data["Input"] == 0.5)).sum()
    percentage = round((yes_partially_count / total_count) * 100) if total_count > 0 else 0

    # Determine the dynamic timeline (min date to current year)
    # min_year = int(pd.to_datetime(filtered_data["Date"]).dt.year.min())
    min_year = 1984
    current_year = datetime.datetime.now().year
    years = list(range(min_year, current_year + 1))

    # Prepare data for the line chart
    filtered_data["Year"] = pd.to_datetime(filtered_data["Date"]).dt.year
    timeline_data = (
        filtered_data.groupby("Year")["Input"]
        .value_counts()
        .unstack(fill_value=0)
        .reindex(columns=[1, 0.5], fill_value=0)
        .reindex(years, fill_value=0)
        .cumsum()
    )

    source = ColumnDataSource(data={
        "Year": timeline_data.index,
        "Yes": timeline_data[1],
        "Partially": timeline_data[0.5]
    })

    # Create the line chart
    p = figure(width=250, height=80, tools="", toolbar_location=None, x_range=(min_year, current_year))
    p.line(x="Year", y="Yes", source=source, line_width=3, color="#3F84E6", legend_label="Yes")
    p.line(x="Year", y="Partially", source=source, line_width=2, color="#F1B5B5", legend_label="Partially")

    # Add hover tooltips
    hover = HoverTool(tooltips=[
        ("Year", "@Year"),
        ("Yes", "@Yes"),
        ("Partially", "@Partially")
    ])
    p.add_tools(hover)

    p.xaxis.ticker = [min_year, current_year]
    p.xaxis.major_label_overrides = {min_year: str(min_year), current_year: str(current_year)}
    p.yaxis.visible = False
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.outline_line_color = None
    p.legend.visible = False

    # Combine the chart and percentage in a Bokeh column layout
    title_div = Div(text=f"<h3 style='font-size: 18px; font-weight: bold; text-align: left;'>{indicator}</h3>")
    percentage_div = Div(text=f"<p style='font-size: 24px; font-weight: bold; margin: 10px 0; '>{percentage}%</p>")
    return column(title_div, percentage_div, p, sizing_mode="stretch_width")


def viz1(data):
    """
    Create adaptive KPI cards with charts for all indicators dynamically.
    """

    indicators = data["Indicator"].unique()
    kpi_cards = []

    for indicator in indicators:
        kpi_card = create_kpi_card_with_chart(indicator, data)
        kpi_cards.append(kpi_card)

    grid = gridplot(kpi_cards, ncols=4, sizing_mode="stretch_width") 


    return grid