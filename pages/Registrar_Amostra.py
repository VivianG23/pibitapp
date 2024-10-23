import streamlit as st
import pandas as pd
import os

# Nome do arquivo CSV onde os dados serão armazenados
csv_file = '/mnt/data/amostras.csv'

# Função para carregar o CSV, ou criar um novo se não existir
def load_data():
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    else:
        # Criar um DataFrame vazio com as colunas necessárias
        df = pd.DataFrame(columns=['ID LAB', 'Número / ID amostra', 'Tipo de amostra', 'Nome do animal', 'Data de coleta'])
        df.to_csv(csv_file, index=False)
        return df

# Função para salvar os dados no CSV
def save_data(df):
    df.to_csv(csv_file, index=False)

# Carregar os dados existentes
df_amostras = load_data()

# Exibindo as colunas principais no CRUD
st.title("Adicionar Nova Amostra")

id_lab = st.text_input("ID LAB")
id_amostra = st.text_input("Número / ID amostra")
tipo_amostra = st.selectbox("Tipo de amostra", ['Swab oral', 'Sangue', 'Outro'])
nome_animal = st.text_input("Nome do animal")
data_coleta = st.date_input("Data de Coleta")

if st.button("Adicionar Amostra"):
    # Criando um novo registro
    new_data = {
        'ID LAB': id_lab,
        'Número / ID amostra': id_amostra,
        'Tipo de amostra': tipo_amostra,
        'Nome do animal': nome_animal,
        'Data de coleta': data_coleta
    }
    
    # Adicionando o novo registro ao DataFrame
    df_amostras = df_amostras.append(new_data, ignore_index=True)
    
    # Salvando no CSV
    save_data(df_amostras)
    
    st.success(f"Amostra {id_amostra} de {nome_animal} adicionada com sucesso!")

# Exibindo as amostras já inseridas
st.subheader("Amostras Registradas")
st.dataframe(df_amostras)
