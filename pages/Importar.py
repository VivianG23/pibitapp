import streamlit as st
from pymongo import MongoClient
import datetime
import os
import pandas as pd

# Conexão ao MongoDB
def connect_to_mongo():
    uri = ("mongodb+srv://emiliods79:uD5A2J4o38dpk0hX@cluster0.ufpae.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    client = MongoClient(uri)
    db = client['pibit_app']  # Ou já especificado na URI, se preferir.
    return db


db = connect_to_mongo()

st.title("Importação de Dados para MongoDB")

# Seleção do tipo de planilha para definir a coleção
tipo_planilha = st.radio(
    "Selecione o tipo de planilha a ser importada:",
    options=["Amostras", "Reagentes"]
)

collection = db["amostras"] if tipo_planilha == "Amostras" else db["reagentes"]

# Upload do arquivo
uploaded_file = st.file_uploader(
    "Selecione uma planilha (CSV ou Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        # Leitura com pandas
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, parse_dates=['Data de Coleta'])
        else:
            df = pd.read_excel(uploaded_file, parse_dates=['Data de Coleta'])
        
        # 1) Converter coluna 'Hora' (datetime.time) para string ISO:
        if 'Hora' in df.columns:
            df['Hora'] = df['Hora'].apply(
                lambda x: x.isoformat() if isinstance(x, datetime.time) else x
            )

        st.subheader("Visualização dos Dados")
        st.dataframe(df.head())

        if st.button("Importar dados"):
            # transformar em lista de dicts e inserir
            dados = df.to_dict(orient="records")
            resultado = collection.insert_many(dados)
            st.success(
                f"Foram inseridos {len(resultado.inserted_ids)} "
                f"documentos na coleção '{tipo_planilha}'!"
            )

    except Exception as e:
        st.error(f"Ocorreu um erro ao importar os dados: {e}")