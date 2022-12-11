import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from urllib.error import URLError

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
st.set_page_config(page_title="Fouth Query", page_icon=":four:")
st.markdown("# Fouth Query")
st.sidebar.header(":three: Fouth Query")

DATA_CSV = "../BostonCrime2021_7000_sample.xlsx"

@st.experimental_memo
def read_File(sheet="in",nrows=None):
    """
    Function with a default parameter that returns a value
    """
    # Read the excel sheet to pandas dataframe
    data = pd.read_excel(DATA_CSV, sheet_name=sheet, na_filter = False,nrows= nrows)
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

def most_Dangerous(BOSTONCRIME, DISTRICT):
    MOST_DANGEROUS = ""
    is_Max = 0
    for d in DISTRICT:
        d["TOTAL"] = 0
        for b in BOSTONCRIME:
            if d["DISTRICT"] == b["DISTRICT"]:
                d["TOTAL"] = d["TOTAL"] + 1 + b["SHOOTING"]
        if is_Max < d["TOTAL"]:
            is_Max = d["TOTAL"]
      
    for d in DISTRICT:
        if d["TOTAL"] == is_Max:
            MOST_DANGEROUS = MOST_DANGEROUS + d["DISTRICT_NAME"] + ", "
    return  MOST_DANGEROUS[:-2] + " ("+str(is_Max)+")"

def show_Table(BOSTONCRIME,is_District):
    data_Table = dict()
    total = 0
    for o in is_District:
        row = [ b["OFFENSE_DESCRIPTION"] for b in BOSTONCRIME if b["DISTRICT_NAME"] == o  ]
        total = total + len(row)
        data_Table[str(o)] = len(row)
    data_Table["Proportion"] =  round(total/len(BOSTONCRIME), 2)
    
    df = pd.DataFrame({
         'key':np.array([k for k,v in data_Table.items()]),
         'value':np.array([v for k,v in data_Table.items()])
        })
    table = pd.pivot_table(df, values='value',columns=['key'])
    hide_table_row_index = """
    <style>
    thead tr th:first-child {display:none}
    tbody th {display:none}
    </style>
    """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    # Display a static table
    st.table(table)

def main():
    # create dict metadata
    BOSTONCRIME = read_File()
       
    # add DISTRICT NAME for metadata
    DISTRICT = read_File("district",None)
    DIST = dict({  d["DISTRICT"]:d["DISTRICT_NAME"] for d in DISTRICT })
    BOSTONCRIME = offense_DISTRICT(BOSTONCRIME,DIST)
    
    # find most dangerous
    MOST_DANGEROUS = most_Dangerous(BOSTONCRIME,DISTRICT)
    
    
    try:
        st.markdown('### The districts had most shooting offence in 2021 are: **_{}_**.'.format(MOST_DANGEROUS))
        
        # create list District
        dist = pd.DataFrame(DISTRICT)
        dist.sort_values(by='DISTRICT_NAME', ascending=True, inplace=True)
        is_District = st.multiselect(
            "Select District",
            dist["DISTRICT_NAME"].unique(),
            dist["DISTRICT_NAME"].unique()[0]
        )
        
        if is_District:
            show_Table(BOSTONCRIME,is_District)
        else:
            st.error("Please choose at least one layer above.")
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )
        
if __name__ == "__main__":
    main()