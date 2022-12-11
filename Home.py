import streamlit as st
import pip
pip.main(["install", "openpyxl"])


st.set_page_config(
    page_title="Final Project",
    page_icon="📈",
)


st.markdown(
    """
   ### Final project- Proposal
### The first query:  
Users would like to get information about a type of offence (or multiple type) in a specific month. 

- Present the input of months and type of offence in a sidebar which designed 
with a selection box for month, and offence description in dropdown box. 

- The data will be presented in the map with appropriate latitude and longitude. 

- Generate a pivot table at the same time with data from that month, index is chosen offence (selection box), column is district and value is the quantity for offence happened.
In pivot table, using district name instead of district code, for example, user can see data in District A-1 is for Downtown, A-& is for East Boston.

### The second query:
User would like to know the trend of Violent crimes and Drug-related abuse crimes in 2021
Violent Crimes by BJS are murder, negligent manslaughter, assault, robbery, sexual abuse, kidnapping, threatening communication, and threats against the President.
Drug-related crimes as “The unlawful cultivation, manufacture, distribution, sale, purchase, use, possession, transportation, or importation of any controlled drug or narcotic substance.”

- Since offence codes are missing in dataset, we will finding suitable words from “offense description” to get data for each type of offense. 

- Create a line chart for that two type of offense to display the trend of offences happened during in 2021 and a stacked chart with different colors for involving shooting and not shooting.

- Using seaborn for drawing a scatterplot by date of week (from chosen month in sidebar)

### The third query:
Users would like to know which month of the year have the most shooting offence.
- Using doc-strings to display: “The months in 2021 had most shooting offence are:” and populate the answer under Streamlit markdown formatting. 
-Using slider to choose what date of month, display the data framework which kind of offense happened and quantity in descending order 

### The fourth query: 
The user would like to know the most dangerous districts in 2021 (let the user choose how many districts they want to see, for example, they can select the most three or five dangerous districts). To identify the highest offense, we calculate the total offense, each offense count 1, and if it involved shooting, count 2).
- Using doc-strings to display: “The districts had most shooting offence in 2021 are:” and populate the answer under Streamlit markdown formatting. 
-Generate streamlit table to show the detail of each type of offense in those districts, go with average number of offense happened.

"""
)