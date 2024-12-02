from bokeh.models import Div
from bokeh.layouts import column
import datetime

def create_viz_story(data):
    """
    Create a storytelling visualization with text and a structured timeline.
    """
    start_year = 1984
    current_year = datetime.datetime.now().year
    years_elapsed = current_year - start_year

    unique_countries = data['Country'].nunique()  
    unique_regions = data['Region'].nunique() 
    unique_indicators = data['Indicator'].nunique()  

    # Story 
    title = Div(text=f"""
        <div style="text-align: center;">
            <h1 style="font-size: 36px;">A World United Against Torture</h1>
        </div>
    """)

    intro = Div(text=f"""
        <p style="text-align: left; font-size: 26px; line-height: 1.3;">
            In <span style="font-weight: bold; font-size: 32px; color: #E36360;">{start_year}</span>, 
            the <strong>United Nations</strong> adopted the <strong> Convention against Torture</strong>, a landmark moment that laid the 
            foundation for global efforts to safeguard human dignity and prevent one of the gravest violations 
            of human rights.
        </p>
        <p style="font-size: 26px; line-height: 1.3;">
            Over the past <span style="font-weight: bold; font-size: 32px; color: #E36360;">{years_elapsed}</span> <strong>years</strong>, 
            across <span style="font-weight: bold; font-size: 32px; color: #E36360;">{unique_countries}</span> <strong>countries</strong> spanning 
            <span style="font-weight: bold; font-size: 32px; color: #E36360;">{unique_regions}</span> <strong>regions</strong>, 
            the <strong>Association for the Prevention of Torture (APT)</strong> has worked tirelessly to achieve the foundational 
            <span style="font-weight: bold; font-size: 32px; color: #E36360;">{unique_indicators}</span> <strong>Legal Indicators</strong> 
            that form the backbone of torture prevention. 
            These indicators represent critical milestones in building a world where torture is unlikely to occur.
        </p>
    """)

    # Timeline wired
    timeline = Div(text=f"""
        <div style="display: flex; align-items: center;  font-size: 26px;">
            <div style="margin: 10px">  {start_year}</div>
            <div style="width: 1000px; height: 50px; background: url('assets/wire_pattern.jpg') repeat-x; background-size: contain;"></div>
            <div style="margin: 10px">  {current_year}</div>
        </div>
    """)

    # Layout of the viz
    viz3 = column(title, intro, timeline)

    return viz3