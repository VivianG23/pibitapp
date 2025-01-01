import streamlit as st
from pymongo import MongoClient
import pandas as pd

# Conexão ao MongoDB
def connect_to_mongo():
    client = MongoClient("mongodb://localhost:27017/")  # Substitua pela URI do MongoDB
    db = client['pibit_app']  # Substitua pelo nome do seu banco de dados
    return db

# Função para buscar amostras do banco de dados
def fetch_samples():
    db = connect_to_mongo()
    collection = db['amostras']
    samples = list(collection.find())
    for sample in samples:
        sample['_id'] = str(sample['_id'])  # Converte ObjectId para string
    return samples

# Página principal
st.title("Registros de Amostras")

# Buscar amostras do banco de dados
samples = fetch_samples()

if samples:
    # Converter dados para DataFrame
    df = pd.DataFrame(samples)

    # Exibir tabela
    st.dataframe(df, use_container_width=True)

    # Opção para exportar como CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar como CSV",
        data=csv,
        file_name="amostras_registradas.csv",
        mime="text/csv"
    )
else:
    st.info("Nenhuma amostra registrada ainda.")
