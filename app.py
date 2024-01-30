import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

st.set_page_config(
    page_title="Massagem sem Mãozinha",
    page_icon="✅",
    layout="wide",
)

# read csv from a github repo
dataset_url = "data/data_0.csv"

# read csv from a URL
@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

df = get_data()

# dashboard title
st.title("Massagem sem Mãozinha")

# top-level filters
job_filter = st.selectbox("Select the Job", pd.unique(df["job"]))

# creating a single-element container
placeholder = st.empty()

# dataframe filter
df = df[df["job"] == job_filter]

# near real-time / live feed simulation
for seconds in range(200):

    df["age_new"] = df["age"] * np.random.choice(range(1, 5))
    df["balance_new"] = df["balance"] * np.random.choice(range(1, 5))

    # creating KPIs
    avg_age = np.mean(df["age_new"])

    count_married = int(
        df[(df["marital"] == "married")]["marital"].count()
        + np.random.choice(range(1, 30))
    )

    balance = np.mean(df["balance_new"])

    with placeholder.container():

        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(
            label="Velz",
            value=round(avg_age),
            delta=round(avg_age) - 10,
        )
        
        kpi2.metric(
            label="Dist",
            value=int(count_married),
            delta=-10 + count_married,
        )
        
        kpi3.metric(
            label="Peso",
            value=f"$ {round(balance,2)} ",
            delta=-round(balance / count_married) * 100,
        )

        # create two columns for charts
        fig_col1, fig_col2, fig_col3 = st.columns(3)

        with fig_col1:
            st.markdown("### Dist")
            fig1 = px.line(
                data_frame=df, y="velz", x="timestamp"
            )
            st.write(fig1)
            
        with fig_col2:
            st.markdown("### Velz")
            fig2 = px.line(
                data_frame=df, y="velz", x="timestamp"
            )
            st.write(fig2)

        with fig_col3:
            st.markdown("### Peso")
            fig3 = px.line(
                data_frame=df, y="velz", x="timestamp"
            )
            st.write(fig3)

        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)