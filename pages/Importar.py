import streamlit as st
from pymongo import MongoClient
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
tipo_planilha = st.radio("Selecione o tipo de planilha a ser importada:", options=["Amostras", "Reagentes"])

if tipo_planilha == "Amostras":
    collection = db["amostras"]
else:
    collection = db["reagentes"]

# Componente para upload do arquivo
uploaded_file = st.file_uploader("Selecione uma planilha (CSV ou Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Verifica o tipo de arquivo e lê com o Pandas
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.subheader("Visualização dos Dados")
        st.dataframe(df.head())

        # Botão para iniciar a importação
        if st.button("Importar dados"):
            # Converte o DataFrame em uma lista de dicionários
            dados = df.to_dict(orient="records")
            resultado = collection.insert_many(dados)
            st.success(f"Foram inseridos {len(resultado.inserted_ids)} documentos na coleção '{tipo_planilha}' do MongoDB!")
            
    except Exception as e:
        st.error(f"Ocorreu um erro ao importar os dados: {e}")
