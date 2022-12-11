import streamlit as st
import pandas as pd
import pydeck as pdk
import os
from urllib.error import URLError


st.set_page_config(page_title="First Query", page_icon=":one:")
st.markdown("# First Query")
st.sidebar.header(":one: First Query")

list_Day = ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday']
DATA_CSV = os.path.abspath(os.getcwd())+"/BostonCrime2021_7000_sample.xlsx"

@st.experimental_memo
def read_File(sheet="in",nrows=None):
    """
    Function with a default parameter that returns a value
    """
    # Read the excel sheet to pandas dataframe
    data = pd.read_excel(DATA_CSV, sheet_name=sheet,usecols=lambda x: 'OCCURRED_ON_DATE' not in x, na_filter = False,nrows= nrows)
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_dict.html
    result = data.to_dict(orient="records") 
    return result

def offense_DISTRICT(BOSTONCRIME,DISTRICT):
    for b in BOSTONCRIME:
        try:
            b["DISTRICT_NAME"] = DISTRICT[b["DISTRICT"]]
        except:
            b["DISTRICT_NAME"] = "External"
    return BOSTONCRIME


def show_Map(chart_data,init):
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=init["Lat"],
            longitude=init["Long"],
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
               'HexagonLayer',
               data=chart_data,
               get_position='[lon, lat]',
               radius=200,
               elevation_scale=4,
               elevation_range=[0, 1000],
               pickable=True,
               extruded=True,
            )
        ],
    ))


def pivot_Table(BostonCrime):
    tbb = pd.DataFrame(BostonCrime)
    data = pd.pivot_table(tbb,values="INCIDENT_NUMBER", columns=['DAY_OF_WEEK'],
                            index=['DISTRICT_NAME'],aggfunc=len,fill_value=0)
    pivot_table = data.reindex(list_Day, axis=1,fill_value=0)
    st.table(pivot_table)

def main():
    # create dict metadata
    BOSTONCRIME = read_File()
    
    # create dict OFFENSE
    OFFENSE = pd.DataFrame(BOSTONCRIME).set_index('OFFENSE_CODE')['OFFENSE_DESCRIPTION'].drop_duplicates().to_dict()

    # add DISTRICT NAME for metadata
    DISTRICT = read_File("district",None)
    DISTRICT = dict({  d["DISTRICT"]:d["DISTRICT_NAME"] for d in DISTRICT })
    BOSTONCRIME = offense_DISTRICT(BOSTONCRIME,DISTRICT)
    
    try:
        # create list month
        is_Month = st.sidebar.selectbox(
            "Select month",
            tuple(range(1,13))
        )
        # create list Offense
        is_Offense = st.sidebar.multiselect(
            "Select Offense",
            OFFENSE.values(),
            OFFENSE.values()
        )
        
        if is_Month and is_Offense:
            st.write('### Information about offense in {}/2021.'.format(is_Month ))
            OFFENSE_DISTRICT = []
            for row in BOSTONCRIME:
                if row["MONTH"]  == is_Month and row["OFFENSE_DESCRIPTION"] in is_Offense:
                    row["lon"] = row["Long"]
                    row["lat"] = row["Lat"]
                    OFFENSE_DISTRICT.append(row)
            # show map
            if len(OFFENSE_DISTRICT) > 0:
                init = OFFENSE_DISTRICT[0]
            else:
                init = BOSTONCRIME[0]
            show_Map(OFFENSE_DISTRICT,init)
            
            st.write('### Pivot table .....')
            pivot_Table(BOSTONCRIME)
        else:
            st.error("Please choose at least one layer above.")
            
    except URLError as e:
        st.error(
            """
            **This project requires internet access.**
            Connection error: %s
        """
            % e.reason
        )
    
if __name__ == "__main__":
    main()