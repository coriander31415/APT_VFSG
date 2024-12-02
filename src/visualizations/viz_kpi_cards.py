from bokeh.models import Div, ColumnDataSource, HoverTool, Spacer, Legend, LegendItem
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
    p = figure(width=300, height=100, tools="", toolbar_location=None, x_range=(min_year, current_year))
    line_partially = p.line(x="Year", y="Partially", source=source, line_width=3, color="#F1B5B5")
    line_yes = p.line(x="Year", y="Yes", source=source, line_width=3, color="#3F84E6")

    custom_legend = Legend(items=[
      LegendItem(label="Yes", renderers=[line_yes]),
      LegendItem(label="Partially", renderers=[line_partially])
    ], location="top_left")

    p.add_layout(custom_legend)
    custom_legend.label_text_font_size = "9pt"
    custom_legend.label_text_color = "grey"
    custom_legend.background_fill_alpha = 0.1
    custom_legend.border_line_color = None

    hover = HoverTool(tooltips=[
        ("Year", "@Year"),
        ("Yes", "@Yes"),
        ("Partially", "@Partially")
    ])
    p.add_tools(hover)

    p.xaxis.ticker = [min_year, current_year]
    p.xaxis.major_label_overrides = {min_year: str(min_year), current_year: str(current_year)}
    p.xaxis.major_label_text_color = "grey"
    p.xaxis.major_tick_line_color = None
    p.xaxis.axis_line_color = "grey"
    p.xaxis.visible = True
    p.yaxis.visible = False
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.outline_line_color = None

    spacer = Spacer(sizing_mode="stretch_height")

    # Combine the chart and percentage in a Bokeh column layout
    title_div = Div(text=f"<h3 style='font-size: 20px; font-weight: bold; text-align: left; margin: 0; padding: 0;'>{indicator}</h3>", width=300)
    percentage_div = Div(text=f"""<p  style='margin: 0; padding: 0; font-size: 32px; font-weight: bold; color: #3F84E6;'>{percentage}%
                         <span style='font-size: 20px; color: black; font-weight: normal;'>({yes_partially_count} countries)</span></p>""")
    return column(title_div, percentage_div, spacer, p, spacing=1, sizing_mode="stretch_both", margin=(20, 10, 10, 10))


def create_viz_kpi_cards(data):
    """
    Create adaptive KPI cards with charts for all indicators dynamically.
    """

    indicators = data["Indicator"].unique()
    kpi_cards = []

    for indicator in indicators:
        kpi_card = create_kpi_card_with_chart(indicator, data)
        kpi_cards.append(kpi_card)

    viz_kpi_cards = gridplot(kpi_cards, ncols=4, sizing_mode="stretch_width") 

    return viz_kpi_cards