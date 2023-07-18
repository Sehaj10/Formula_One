import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(layout="centered",
                   page_icon="F1-logo-removebg-preview.png")

col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')
with col2:
    image = Image.open("F1-logo-removebg-preview.png")
    resized_image = image.resize((175, 90))
    st.image(resized_image)
with col3:
    st.write(' ')

selected_year = st.slider("Select the Year", 2019, 2023)

# Load the race session
races= ['Bahrain', 'Saudi Arabia', 'Australia', 'Azerbaijan', 
        'United States', 'Monaco', 'Spain', 'Canada',
        'Austria', 'Great Britain', 'Hungary', 'Belgium',
        'Netherlands', 'Italy', 'Singapore', 'Japan',
        'Qatar', 'United States', 'Mexico', 'Brazil',
        'United States', 'Abu Dhabi']
selected_location = st.selectbox("Select the Grand Prix", options=races)

submit_button = st.button("Submit")

if submit_button:
    with st.spinner("Loading data...might take a few seconds"):
        session = fastf1.get_session(selected_year, selected_location, 'R')
        session.load()  # Load the data for the race session

        if selected_year >= 2019:
            laps = session.laps

            # Get the list of driver numbers
            drivers = session.drivers

            # Convert the driver numbers to three-letter abbreviations
            drivers = [session.get_driver(driver)["Abbreviation"] for driver in drivers]

            stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
            stints = stints.groupby(["Driver", "Stint", "Compound"]).size().reset_index(name="StintLength")

            # Now we can plot the strategies for each driver
            fig, ax = plt.subplots(figsize=(5, 8))

            for driver in drivers:
                driver_stints = stints.loc[stints["Driver"] == driver]

                previous_stint_end = 0
                for idx, row in driver_stints.iterrows():
                    # each row contains the compound name and stint length
                    # we can use this information to draw horizontal bars
                    plt.barh(
                        y=driver,
                        width=row["StintLength"],
                        left=previous_stint_end,
                        color=fastf1.plotting.COMPOUND_COLORS[row["Compound"]],
                        edgecolor="black",
                        fill=True
                    )

                    previous_stint_end += row["StintLength"]

            # Make the plot more readable and intuitive
            plt.title(f"{selected_year} {selected_location} Finishing Postions & Tyre Strategies")
            plt.xlabel("Lap Number")
            plt.grid(False)
            # invert the y-axis so drivers that finish higher are closer to the top
            ax.invert_yaxis()

            # Plot aesthetics
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)

            plt.tight_layout()
            st.pyplot(fig)
        else:
            drivers = session.drivers
            drivers = [session.get_driver(driver)["Abbreviation"] for driver in drivers]
            data= pd.DataFrame(drivers)
            st.write(data)

footer = "MADE WITH  \u2764\ufe0f  BY SEHAJ "
# Apply CSS styling to position the footer at the bottom
footer_style = """
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
    padding: 10px;
    font-weight: bold;
    letter-spacing: 1.25px;
    font-size: 13px;
    color: #FC6600;
"""
st.markdown('<p style="{}">{}</p>'.format(footer_style, footer), unsafe_allow_html=True)
