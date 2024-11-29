from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

def viz2(data):
    """
    Create a bar chart visualization as the second visualization.
    """
    grouped_data = data.groupby('Region')['Input'].mean().reset_index()
    source = ColumnDataSource(grouped_data)

    p = figure(x_range=grouped_data['Region'], title="Average Input by Region",
               toolbar_location=None, tools="")

    p.vbar(x='Region', top='Input', width=0.5, source=source, color="skyblue")

    return p