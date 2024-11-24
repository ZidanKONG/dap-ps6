from shiny import App, ui, reactive, render
import pandas as pd 
import matplotlib.pyplot as plt
import json
import altair as alt
import geopandas as gpd

app_ui = ui.page_fluid(
    ui.input_select(
        id="select",
        label="Select Type and Subtype",
        choices=[
            'Jam - Heavy traffic', 'Accident - Major', 'Accident - Minor',
            'Hazard - On road', 'Hazard - On road car stopped', 
            'Hazard - On road construction', 'Hazard - On road emergency vehicle', 
            'Hazard - On road ice', 'Hazard - On road object', 
            'Hazard - On road pot hole', 'Hazard - On road traffic light fault', 
            'Hazard - On shoulder', 'Hazard - On shoulder car stopped', 
            'Hazard - Weather', 'Hazard - Weather flood', 
            'Jam - Moderate traffic', 'Jam - Stand still traffic', 
            'Road_closed - Event', 'Hazard - On road lane closed', 
            'Hazard - Weather fog', 'Road_closed - Construction', 
            'Hazard - On road road kill', 'Hazard - On shoulder animals', 
            'Hazard - On shoulder missing sign', 'Jam - Light traffic', 
            'Hazard - Weather heavy snow', 'Road_closed - Hazard', 
            'Hazard - Weather hail'
        ]
    ),
    ui.output_plot("scatter_plot")
)

def server(input, output, session):
    @reactive.calc
    def full_data():
        return pd.read_csv("sorted_type_bin.csv")
    
    @reactive.calc
    def filtered_data():
        df = full_data()
        selected_type, selected_subtype = input.select().split(" - ")
        selected_df = df[(df['updated_type'] == selected_type) 
                  & (df['updated_subtype'] == selected_subtype)]
        return selected_df.head(10)
    
    @render.plot
    def scatter_plot():
        file_path = "/Users/kongzidan/Documents/GitHub/DAP-PS6/top_alerts_map/Boundaries - Neighborhoods.geojson"
        geo_data = gpd.read_file(file_path)
        
        data = filtered_data()
        scale_factor = 200
        base_size = 10
        data['scaled_size'] = (data['counts'] - data['counts'].min()) / \
            (data['counts'].max() - data['counts'].min()) * scale_factor + base_size
        
        fig, ax = plt.subplots()

        # Plot the map (neighborhood boundaries)
        geo_data.plot(ax=ax, color='lightgray', edgecolor='white')

        sc = ax.scatter(data['lonBin'], data['latBin'],  
                        s=data['scaled_size'],
                        c=data['counts'],
                        cmap='plasma',
                        alpha=0.6,
                        edgecolor='black')
        
        ax.set_title("Top 10 Area of Selected Alert Alerts in Chicago", fontsize=14)
        ax.set_xlabel("Longitude", fontsize=12)
        ax.set_ylabel("Latitude", fontsize=12)

        return fig

        

app = App(app_ui, server)