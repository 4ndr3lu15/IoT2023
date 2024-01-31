import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

import pickle
import sklearn

THRESHOLD = 50

st.set_page_config(
    page_title="Massagem sem Mãozinha",
    page_icon="❤️",
)

modelo = pickle.load(open('model/modelo_logistico.pkl', 'rb'))

# read csv from a github repo
dataset_url = "data/inference.csv"


# creating a single-element container
placeholder = st.empty()

def infer_model(df):

  threshold = 50
  colunas_a_normalizar = ['peso', 'velz', 'dist']
  df[colunas_a_normalizar] =df[colunas_a_normalizar].astype(float)

  # Substitua valores acima do threshold por NaN usando np.where
  df['peso'] = df['peso'].apply(lambda x: np.where(np.abs(x) > threshold, np.nan, x))
  df['peso'].interpolate(inplace = True)

  colunas_a_normalizar = ['peso', 'velz', 'dist']
  subsequencia = df[colunas_a_normalizar].iloc[:].values.flatten()

  # Faça previsões nos dados de teste
  previsoes = modelo.predict(subsequencia.reshape(1, -1))

  return  np.argmax(np.bincount(previsoes.astype(int)))


# near real-time / live feed simulation
while True:

    with placeholder.container():

        df = pd.read_csv(dataset_url)
        
        to_infer = df.tail(10)

        msg = infer_model(to_infer)

        msg = "MASSAGEM RUIM!" if msg == 0 else "MASSAGEM BOA!"
        # dashboard title
        st.title(f"{msg}")
        st.markdown("Massagem sem Mãozinha")

        # create a container for each chart
        fig_container1 = st.container()
        fig_container2 = st.container()
        fig_container3 = st.container()

        with fig_container1:
            st.markdown("### Velz")
            fig1 = px.line(
                data_frame=df, y="velz", x="timestamp"
            )
            st.write(fig1)

    
        with fig_container2:
            st.markdown("### Dist")
            fig2 = px.line(
                data_frame=df, y="dist", x="timestamp"
            )
            st.write(fig2)


        with fig_container3:
            st.markdown("### Peso")
            fig3 = px.line(
                data_frame=df, y="peso", x="timestamp"
            )
            st.write(fig3)


        st.markdown("### Inference Data")
        st.dataframe(to_infer)
        time.sleep(1)