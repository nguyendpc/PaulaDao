import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
st.set_page_config(page_title="Second Query", page_icon=":two:")
st.markdown("# Second Query")
st.sidebar.header(":two: Second Query")

list_Month = ['Jan', 'Feb', 'Mar', 'Apr', 'May','Jun']
list_Day = ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday']
Violent_Key  = ['murder', 'manslaughter', 'assault', 'robbery', 'abuse', 'kidnapping', 'threats']
Drug_Key = ['manufacture', 'distribution', 'sale', 'purchase', 'use', 'possession', 'transportation', 'drug']

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

def trend_Violent(BOSTONCRIME,MONTH=None):
    Violent  = [ 0 for i in range(0,6)] 
    Drug = [ 0 for i in range(0,6)] 
    Shooting = [ 0 for i in range(0,6)]
    Trend = [] # dùng cho ý sau, BOSTONCRIME là toàn bộ dữ liệu, Trend chỉ giữ lại dòng nào thuộc 2 type offense
    for b in BOSTONCRIME:
        # dò từng keyword của loại Violent để kiểm tra b có chứa keyword type Violent k
        for v in Violent_Key: 
            # v.upper() là biến chữ thành viết hoa, do mảng tạo ở trên là chữ thường, excel là hoa
            if v.upper() in b["OFFENSE_DESCRIPTION"]: # kiểm tra xem giá trị của v.upper() có nằm trong b["OFFENSE_DESCRIPTION"] 
                # ý tưởng tìm m là tương tự q1 offense_DISTRICT(BOSTONCRIME,DISTRICT) chỗ DISTRICT[b["DISTRICT"]]
                m = int(b["MONTH"]) -1  # int(b["MONTH"]) để đảm bảo value của b["MONTH"] là 1 con số
                Violent[m] = Violent[m] + 1 
                Shooting[m] = Shooting[m] + b["SHOOTING"] # chỗ này b["SHOOTING"] chỉ nhận giá trị 0,1
                b["OFFENSE_CODE_GROUP"] = 1 # excel k có OFFENSE_CODE_GROUP nên mình tự gán Violent là loại 1, dùng về sau
                Trend.append(b)
                break # break vì mỗi dòng b mình chỉ cần dò xem chỉ cần có 1 key của Violent nằm trong OFFENSE_DESCRIPTION là dừng
        # dò từng keyword của loại Violent để kiểm tra b có chứa keyword type Drug k, tương tự khúc trên
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
            })
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
        p = pd.Period('2022-{}'.format(is_Month)) # khi chọn tháng = 1 nó sẽ tạo ra p='2022-1'
        num = p.days_in_month # là số ngày của tháng đó = 31
        idx = pd.date_range(start='2022-12', freq='D', periods=num) # tạo ra cái list 31 ngày từ '2022-12-01' ->'2022-12-31'
        Day_Of_Month = np.array(idx.day_name()) # ngày của tháng dạng chữ tính từ ngày đầu tháng, k phải từ thứ 2
        Date_Of_Month = [i for i in range(1,num+1)]  
        ToTal = [0 for i in range(0,num)]
        Shooting = [0 for i in range(0,num)]
        for row in Date_Of_Month:
            for b in Trend:
                p = pd.Period(b["OCCURRED_ON_DATE"], freq="H") # định dạng lại kiểu dữ liệu thời gian cho OCCURRED_ON_DATE
                d = p.day
                m = p.month
                if m == is_Month and d == row:
                    ToTal[row-1] = ToTal[row-1] + 1
                    Shooting[row-1] = Shooting[row-1] + b["SHOOTING"]
        data_plot = pd.DataFrame({
                'Offense': ToTal,
                'Shooting': Shooting,
                'No Shooting': np.array(ToTal) - np.array(Shooting),
                'Day': Day_Of_Month,
                })
        fig = plt.figure()
        sns.scatterplot(data=data_plot, x="Offense", y="No Shooting", hue="Day")        
        st.pyplot(fig)
    else:
        st.error("Please choose at least one layer above.")

        
if __name__ == "__main__":
    main()