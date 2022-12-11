import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from urllib.error import URLError

sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
st.set_page_config(page_title="Second Query", page_icon=":two:")
st.markdown("# Second Query")
st.sidebar.header(":two: Second Query")

list_Month = ['Jan', 'Feb', 'Mar', 'Apr', 'May','Jun']
list_Day = ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday']
Violent_Key  = ['murder', 'manslaughter', 'assault', 'robbery', 'abuse', 'kidnapping', 'threats']
Drug_Key = ['manufacture', 'distribution', 'sale', 'purchase', 'use', 'possession', 'transportation', 'drug']

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

def trend_Violent(BOSTONCRIME,MONTH=None):
    Violent  = [ 0 for i in range(0,6)]
    Drug = [ 0 for i in range(0,6)]
    Shooting = [ 0 for i in range(0,6)]
    Trend = []
    
    for b in BOSTONCRIME:
        for v in Violent_Key:
            if v.upper() in b["OFFENSE_DESCRIPTION"]:
                m = int(b["MONTH"]) -1 
                Violent[m] = Violent[m] + 1
                Shooting[m] = Shooting[m] + b["SHOOTING"]
                b["OFFENSE_CODE_GROUP"] = 1
                Trend.append(b)
                break
        for d in Drug_Key:
            if d.upper() in b["OFFENSE_DESCRIPTION"]:
                m = int(b["MONTH"]) -1 
                Drug[m] = Drug[m] + 1
                Shooting[m] = Shooting[m] + b["SHOOTING"]
                b["OFFENSE_CODE_GROUP"] = 2
                Trend.append(b)
                break
    return Violent,Drug,Shooting,Trend

def plot_LineChart(Violent,Drug):
    data_plot = pd.DataFrame({
            'Violent': Violent,
            'Drug': Drug
            },index=list_Month)
    fig = plt.figure()
    sns.lineplot(data=data_plot,estimator=sum, ci=None,  color='lightblue')
    st.pyplot(fig)

def plot_StackedChart(NO_SHOOTING,SHOOTING):
    fig = plt.figure()
    plt.bar(list_Month,NO_SHOOTING, color='r')
    plt.bar(list_Month,SHOOTING, bottom=NO_SHOOTING)
    plt.legend(["No Shooting", "Shooting"])
    st.pyplot(fig)
    
def main():
    # create dict metadata
    BOSTONCRIME = read_File()
    
    # create dict trend Violent
    Violent,Drug,Shooting,Trend = trend_Violent(BOSTONCRIME)
    NO_SHOOTING = np.array(Violent) + np.array(Drug) - np.array(Shooting)
    SHOOTING = np.array(Shooting)
    
    
    try:
        st.write('### The trend of offences happened during in 2021.')
        plot_LineChart(Violent,Drug)
        
        st.write('### The trend of offences involving shooting happened during in 2021.')
        plot_StackedChart(NO_SHOOTING,SHOOTING)
        
        # select month
        st.write('### Scatterplot')
        is_Month = st.selectbox(
            "Select month",
            tuple(range(1,7))
        )
        if is_Month:
            # create dict BOSTONCRIME by month
            p = pd.Period('2022-{}'.format(is_Month))
            num = p.days_in_month
            idx = pd.date_range(start='2022-12', freq='D', periods=num)
            Day_Of_Month = np.array(idx.day_name())
            Date_Of_Month = [i for i in range(1,num+1)]
            ToTal = [0 for i in range(0,num)]
            Shooting = [0 for i in range(0,num)]
            
            for row in Date_Of_Month:
                for b in Trend:
                    p = pd.Period(b["OCCURRED_ON_DATE"], freq="H")
                    d = p.date
                    m = p.month
                    if m == is_Month and d == row:
                        ToTal[row-1] = ToTal[row-1] + 1
                        Shooting[row-1] = Shooting[row-1] + b["SHOOTING"]
            data_plot = pd.DataFrame({
                    'ToTal': ToTal,
                    'Shooting': Shooting,
                    'Day': Day_Of_Month,
                    })
            # sns.scatterplot(data=data_plot, x="ToTal", y="Shooting", hue="Day")        
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