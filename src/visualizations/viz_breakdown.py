from bokeh.models import Select, CustomJS
from bokeh.layouts import column, row
from bokeh.models.widgets import Div
import pandas as pd

def create_viz_breakdown(data):
    """
    Create a dynamic visualization with regions, countries, and detailed data display.
    """
    # Preprocessing:
    data['FormattedDate'] = data['Date'].apply(
        lambda x: f"({pd.to_datetime(x).year})" if pd.notnull(x) else ''
    )
    data['Year'] = pd.to_datetime(data['Date'], errors='coerce').dt.year  # Extract year for sorting

    # Widgets
    regions = data['Region'].unique()
    default_region = "Europe" if "Europe" in regions else regions[0]
    countries_by_region = {
        region: data[data['Region'] == region]['Country'].unique().tolist()
        for region in regions
    }

    default_country = "Austria" if "Austria" in countries_by_region.get(default_region, []) else countries_by_region[default_region][0]
    filtered_data = data[(data['Region'] == default_region) & (data['Country'] == default_country)]

    details = {
        'Adopted': [],
        'Partially': [],
        'Awaiting': []
    }

    # Sorting by year
    for _, row_data in filtered_data.sort_values(by='Year').iterrows():
        if row_data['Input'] == 1.0:
            details['Adopted'].append(f"<li>{row_data['Indicator']} {row_data['FormattedDate']}</li>")
        elif row_data['Input'] == 0.5:
            details['Partially'].append(f"<li>{row_data['Indicator']} {row_data['FormattedDate']}</li>")
        else:
            details['Awaiting'].append(f"<li>{row_data['Indicator']}</li>")

    initial_html = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.5; padding: 10px;">
        <h3 style="font-size: 32px;">{default_country}</h3>
    """
    if details['Adopted']:
        initial_html += f"""
        <div style="margin-bottom: 10px;">
            <b style="color: #3F84E6; font-size: 26px;">Adopted:</b>
            <ul style="margin-left: 20px; font-size: 20px">{''.join(details['Adopted'])}</ul>
        </div>
        """
    if details['Partially']:
        initial_html += f"""
        <div style="margin-bottom: 10px;">
            <b style="color: #F1B5B5; font-size: 26px;">Partially:</b>
            <ul style="margin-left: 20px; font-size: 20px">{''.join(details['Partially'])}</ul>
        </div>
        """
    if details['Awaiting']:
        initial_html += f"""
        <div style="margin-bottom: 10px;">
            <b style="color: #8CB5F0; font-size: 26px;">Awaiting:</b>
            <ul style="margin-left: 20px; font-size: 20px">{''.join(details['Awaiting'])}</ul>
        </div>
        """
    initial_html += "</div>"

    # Widgets
    region_select = Select(title="Select Region:", options=list(regions), value=default_region)
    country_select = Select(title="Select Country:", options=countries_by_region[default_region], value=default_country)
    info_div = Div(text=initial_html, width=None, height=None)

    # Callback for region selection
    region_callback = CustomJS(
        args=dict(
            data=data.to_dict(orient='list'),
            country_select=country_select,
            region_select=region_select
        ),
        code="""
        const selectedRegion = region_select.value;
        const filteredCountries = data['Country'].filter((_, i) => data['Region'][i] === selectedRegion);
        const uniqueCountries = [...new Set(filteredCountries)];
        
        country_select.options = uniqueCountries;
        country_select.value = uniqueCountries.includes("Austria") ? "Austria" : uniqueCountries[0];
        """
    )

    # Callback for country selection
    country_callback = CustomJS(
        args=dict(
            data=data.to_dict(orient='list'),
            country_select=country_select,
            info_div=info_div
        ),
        code="""
        const selectedCountry = country_select.value;
        const indices = data['Country'].map((c, i) => c === selectedCountry ? i : null).filter(i => i !== null);

        const details = {
            'Adopted': [],
            'Partially': [],
            'Awaiting': []
        };

        indices.sort((a, b) => {
            const yearA = data['Year'][a] || 9999; // Sort Unknown to the end
            const yearB = data['Year'][b] || 9999;
            return yearA - yearB;
        }).forEach(i => {
            const input = data['Input'][i];
            const indicator = data['Indicator'][i];
            const date = data['FormattedDate'][i];
            if (input === 1.0) {
                details['Adopted'].push(`<li>${indicator} ${date}</li>`);
            } else if (input === 0.5) {
                details['Partially'].push(`<li>${indicator} ${date}</li>`);
            } else {
                details['Awaiting'].push(`<li>${indicator}</li>`);
            }
        });

        let html = `
        <div style="font-family: Arial, sans-serif; line-height: 1.5; padding: 10px;">
            <h3 style=" font-size: 32px; ">${selectedCountry}</h3>
        `;
        if (details['Adopted'].length > 0) {
            html += `
            <div style="margin-bottom: 10px;">
                <b style="color: #3F84E6; font-size: 26px;">Adopted:</b>
                <ul style="margin-left: 20px; font-size: 20px">${details['Adopted'].join("")}</ul>
            </div>
            `;
        }
        if (details['Partially'].length > 0) {
            html += `
            <div style="margin-bottom: 10px;">
                <b style="color: #F1B5B5; font-size: 26px;">Partially:</b>
                <ul style="margin-left: 20px; font-size: 20px">${details['Partially'].join("")}</ul>
            </div>
            `;
        }
        if (details['Awaiting'].length > 0) {
            html += `
            <div style="margin-bottom: 10px;">
                <b style="color: #8CB5F0; font-size: 26px;">Awaiting:</b>
                <ul style="margin-left: 20px; font-size: 20px">${details['Awaiting'].join("")}</ul>
            </div>
            `;
        }
        html += "</div>";

        info_div.text = html;
        """
    )

    # Link callbacks to widgets
    region_select.js_on_change("value", region_callback)
    country_select.js_on_change("value", country_callback)

    # Layout of the viz
    selectors = row(region_select, country_select, sizing_mode="stretch_width", spacing=15, margin=(40, 10, 10, 10))  
    viz_breakdown = column(selectors, info_div) 

    return viz_breakdown