from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Select, CustomJS
from bokeh.layouts import column
from bokeh.models.widgets import Div

def create_viz2(data):
    """
    Create a dynamic visualization with regions, countries, and detailed data display.
    """
    # Preprocessing data
    data['Date'] = data['Date'].fillna('Unknown')  # Fill missing dates
    regions = data['Region'].unique()

    # Data sources
    region_source = ColumnDataSource(data={'Region': regions})
    country_source = ColumnDataSource(data={'Country': [], 'Indicator': [], 'Input': [], 'Date': []})

    # Widgets
    region_select = Select(title="Select Region:", options=list(regions), value=list(regions)[0])
    country_select = Select(title="Select Country:", options=[], value=None)
    info_div = Div(text="Select a region and a country to view details.", width=600, height=200)

    # Callback for region selection
    region_callback = CustomJS(
        args=dict(
            country_source=country_source,
            data=data.to_dict(orient='list'),
            country_select=country_select,
            region_select=region_select,
            info_div=info_div
        ),
        code="""
        const selectedRegion = region_select.value;
        const filteredCountries = data['Country'].filter((_, i) => data['Region'][i] === selectedRegion);
        const uniqueCountries = [...new Set(filteredCountries)];
        
        country_select.options = uniqueCountries;
        country_select.value = uniqueCountries.length > 0 ? uniqueCountries[0] : null;
        
        country_source.data = {'Country': [], 'Indicator': [], 'Input': [], 'Date': []};
        info_div.text = "Select a country to view details.";
        """
    )

    # Callback for country selection
    country_callback = CustomJS(
        args=dict(
            country_source=country_source,
            data=data.to_dict(orient='list'),
            country_select=country_select,
            info_div=info_div
        ),
        code="""
        const selectedCountry = country_select.value;
        const indices = data['Country'].map((c, i) => c === selectedCountry ? i : null).filter(i => i !== null);
        
        country_source.data = {
            'Country': indices.map(i => data['Country'][i]),
            'Indicator': indices.map(i => data['Indicator'][i]),
            'Input': indices.map(i => data['Input'][i]),
            'Date': indices.map(i => data['Date'][i])
        };
        
        if (indices.length > 0) {
            let details = `<b>Details for ${selectedCountry}</b><br>`;
            details += "<ul>";
            for (let i = 0; i < indices.length; i++) {
                details += `<li>${data['Indicator'][indices[i]]}: ${data['Input'][indices[i]]} (Date: ${data['Date'][indices[i]]})</li>`;
            }
            details += "</ul>";
            info_div.text = details;
        } else {
            info_div.text = "No details available for the selected country.";
        }
        """
    )

    # Link callbacks to widgets
    region_select.js_on_change("value", region_callback)
    country_select.js_on_change("value", country_callback)

    # Layout of the viz
    viz2 = column(region_select, country_select, info_div)

    return viz2