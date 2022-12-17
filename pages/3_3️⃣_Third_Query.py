import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime
import calendar 


sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
st.set_page_config(page_title="Third Query", page_icon=":three:")
st.markdown("# Third Query")
st.sidebar.header(":three: Third Query")

list_Month = ['January', 'February', 'March', 'April', 'May','Jun']
list_MonthN= [i for i in range(1,7)]

DATA_CSV = "BostonCrime2021_7000_sample.xlsx"

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

def most_Shooting(BOSTONCRIME):
    Offense = dict({key: 0 for key in list_Month} ) # {'January': 0, 'February': 0, 'March': 0, 'April': 0, 'May': 0, 'Jun': 0}
    is_Max = 0
    for m in list_MonthN:
        count = 0
        for b in BOSTONCRIME:
            if b["MONTH"] == m:
                count = count + 1
        if is_Max < count:
            is_Max = count
        Offense[ list_Month[m - 1] ] = count
    MOST_SHOOTING = ""
    for key, value in Offense.items():
        if value == is_Max:
            MOST_SHOOTING = MOST_SHOOTING + key + ", "
    return  MOST_SHOOTING[:-2] + " ("+str(is_Max)+")"

def Find_Date_Month(Select_Date):
    d = datetime.strptime(Select_Date, '%Y-%m-%d %H:%M:%S')
    return d.day,d.month
   
def kind_OFFENSE(BOSTONCRIME,Select_Date):
    ROW = []
    for b in BOSTONCRIME:
        d = b["OCCURRED_ON_DATE"].day
        m = b["OCCURRED_ON_DATE"].month
        if d == Select_Date.day and m == Select_Date.month:
            ROW.append(b["OFFENSE_DESCRIPTION"])
    res = {i:ROW.count(i) for i in ROW}
    df = pd.DataFrame({
        "Offense": np.array([key for key,value in res.items()]),
        "Total": np.array([value for key,value in res.items()])
        })
    df.sort_values(by='Total', ascending=False, inplace=True)
    df.index = np.arange(1, len(df) + 1) # set index =1
    st.table(df)

def main():
    # create dict metadata
    BOSTONCRIME = read_File()
    # count most shooting
    MOST_SHOOTING = most_Shooting(BOSTONCRIME)
    
  
    st.markdown('### The months in 2021 had most shooting offence are: **_{}_**.'.format(MOST_SHOOTING))
    
    # select date of month
    st.write("#### Choose date of month")
    select_Month = st.selectbox(
        "Select month",
        tuple(range(1,13))
    )
    
    if select_Month:
        Start,End = calendar.monthrange(2002, select_Month)
        Select_Date = st.slider(
            "Select date",
            value=datetime(2021, select_Month, 1),
            min_value = datetime(2021, select_Month, 1),
            max_value = datetime(2021, select_Month, End),
            format="MM/DD/YY")
        if Select_Date:
            kind_OFFENSE(BOSTONCRIME,Select_Date)
    else:
        st.error("Please choose at least one layer above.")

    
if __name__ == "__main__":
    main()