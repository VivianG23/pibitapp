import streamlit as st
from pymongo import MongoClient
import os
import pandas as pd

# Conexão ao MongoDB Atlas
def connect_to_mongo():
    uri = os.getenv("MONGODB_URI")
    client = MongoClient(uri)
    db = client['pibit_app']
    return db

# Conecta ao banco e seleciona a coleção de amostras
db = connect_to_mongo()
collection = db['amostras']

st.title("Editar Amostra")

# Busca todas as amostras e cria um dicionário para facilitar a seleção
samples = list(collection.find())
sample_dict = {sample['_id']: sample for sample in samples}

if not sample_dict:
    st.info("Nenhuma amostra cadastrada para editar.")
    st.stop()

# Seleção da amostra (usando o _id, mas pode ser outro identificador)
sample_ids = list(sample_dict.keys())
sample_id = st.selectbox("Selecione a amostra para editar:", options=sample_ids)

if sample_id:
    # Recupera a amostra selecionada
    sample = sample_dict[sample_id]

    st.subheader("Dados atuais da Amostra")
    st.write(sample)  # Exibe os dados atuais para conferência

    st.subheader("Editar dados da Amostra")
    with st.form("form_editar_amostra"):
        update_data = {}

        # Sempre exibe o campo Status (pode ser adaptado conforme necessário)
        status_atual = sample.get("status", "Pendente")
        opcoes_status = ["Pendente", "Transferida", "Recebida"]
        # Caso o status atual não esteja entre as opções, define o primeiro como padrão
        indice_status = opcoes_status.index(status_atual) if status_atual in opcoes_status else 0
        novo_status = st.selectbox("Status", options=opcoes_status, index=indice_status)
        update_data["status"] = novo_status

        # Exibe o campo Laboratório somente se o valor atual não for NaN
        laboratorio_valor = sample.get("laboratorio", "")
        if pd.notna(laboratorio_valor):
            novo_laboratorio = st.text_input("Laboratório", value=laboratorio_valor)
            update_data["laboratorio"] = novo_laboratorio

        # Você pode adicionar outros campos, condicionando sua exibição
        # Exemplo para um campo "Observacoes"
        observacoes_valor = sample.get("observacoes", "")
        if pd.notna(observacoes_valor):
            nova_observacao = st.text_area("Observações", value=observacoes_valor)
            update_data["observacoes"] = nova_observacao

        submit = st.form_submit_button("Salvar alterações")

        if submit:
            # Atualiza a amostra no MongoDB (filtrando pelo _id)
            result = collection.update_one({"_id": sample['_id']}, {"$set": update_data})
            if result.modified_count:
                st.success("Amostra atualizada com sucesso!")
            else:
                st.warning("Nenhuma alteração realizada ou ocorreu um problema na atualização.")
