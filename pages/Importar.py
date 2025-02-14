import streamlit as st
from pymongo import MongoClient
import pandas as pd

uri = "mongodb+srv://emilianodl:icHkQo4W507qyMMf@cluster0.excq6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['pibit_app']  # Ou já especificado na URI, se preferir.
collection = db["amostras"]

st.title("Importação de Dados para MongoDB")

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
            st.success(f"Foram inseridos {len(resultado.inserted_ids)} documentos no MongoDB!")
            
    except Exception as e:
        st.error(f"Ocorreu um erro ao importar os dados: {e}")