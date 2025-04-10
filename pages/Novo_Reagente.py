import streamlit as st
from pymongo import MongoClient

# Conexão ao MongoDB
def connect_to_mongo():
    # Substitua <username>, <password> e, se necessário, o nome do cluster e banco de dados
    uri = "mongodb+srv://emilianodl:icHkQo4W507qyMMf@cluster0.excq6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    db = client['pibit_app']  # Ou especifique o banco de dados desejado
    return db

# Verificação de login
if not st.session_state.get("LOGGED_IN"):
    st.warning("Você precisa fazer login para acessar esta página.")
    st.stop()

st.title("Registrar Novo Reagente")

with st.form("form_registro_reagente"):
    # Campos do formulário sem sugestões
    nome = st.text_input("Nome do Reagente", placeholder="Digite o nome do reagente")
    fabricante = st.text_input("Fabricante", placeholder="Digite o fabricante")
    categoria = st.text_input("Categoria", placeholder="Digite a categoria")
    lote = st.text_input("Número do Lote", placeholder="Ex: 12345")
    data_validade = st.date_input("Data de Validade")
    quantidade = st.number_input("Quantidade", min_value=0.0, format="%.2f", step=0.01)
    unidade = st.text_input("Unidade de Medida", placeholder="Ex: ml, g, etc.")
    local_armazenamento = st.text_input("Local de Armazenamento", placeholder="Digite o local de armazenamento")
    observacoes = st.text_area("Observações (opcional)")

    submit_button = st.form_submit_button("Registrar Reagente")

if submit_button:
    db = connect_to_mongo()
    collection = db['reagentes']  # Coleção para reagentes

    reagent_data = {
        "nome": nome,
        "fabricante": fabricante,
        "categoria": categoria,
        "lote": lote,
        "data_validade": str(data_validade),
        "quantidade": quantidade,
        "unidade": unidade,
        "local_armazenamento": local_armazenamento,
        "observacoes": observacoes
    }

    try:
        collection.insert_one(reagent_data)
        st.success("Reagente registrado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao registrar o reagente: {e}")
