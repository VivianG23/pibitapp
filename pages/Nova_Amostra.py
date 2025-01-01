import streamlit as st
from pymongo import MongoClient

# Conexão ao MongoDB
def connect_to_mongo():
    client = MongoClient("mongodb://localhost:27017/")  # Substitua pela URI do MongoDB
    db = client['pibit_app']  # Substitua pelo nome do seu banco de dados
    return db

# Função para buscar sugestões do MongoDB
def get_suggestions(field_name):
    db = connect_to_mongo()
    collection = db['amostras']  # Substitua pelo nome da coleção desejada
    suggestions = collection.distinct(field_name)
    return suggestions

# Verificação de login
if not st.session_state.get("LOGGED_IN"):
    st.warning("Você precisa fazer login para acessar esta página.")
    st.stop()

# Formulário de registro da amostra
st.title("Registrar Nova Amostra")

with st.form("form_registro_amostra"):
    # Buscar sugestões do MongoDB
    especie_suggestions = get_suggestions("especie")
    nome_comum_suggestions = get_suggestions("nome_comum")

    # Campo com sugestões e texto livre para 'Espécie'
    especie_input = st.text_input(
        "Espécie (Nome Científico)", 
        placeholder="Digite ou selecione uma espécie"
    )
    especie = st.selectbox(
        "Sugestões de Espécie",
        options=[""] + especie_suggestions,
        format_func=lambda x: x if x else "Selecione uma sugestão"
    )
    if especie:  # Se o usuário selecionar uma sugestão, substitui o valor digitado
        especie_input = especie

    # Campo com sugestões e texto livre para 'Nome Comum'
    nome_comum_input = st.text_input(
        "Nome Comum", 
        placeholder="Digite ou selecione um nome comum"
    )
    nome_comum = st.selectbox(
        "Sugestões de Nome Comum",
        options=[""] + nome_comum_suggestions,
        format_func=lambda x: x if x else "Selecione uma sugestão"
    )
    if nome_comum:  # Se o usuário selecionar uma sugestão, substitui o valor digitado
        nome_comum_input = nome_comum

    # Outros campos do formulário
    local_coleta = st.text_input("Local de Coleta")
    data_coleta = st.date_input("Data da Coleta")
    nome_coletor = st.text_input("Nome do Coletor")
    metodo_coleta = st.selectbox(
        "Selecione o método de coleta:",  
        ["Swab nasal", "Swab oral", "Swab cloacal", "Swab anal", "Sangue", "Sangue edta", "Sangue PBS", "Necrópsia"]
    )
    condicao_amostra = st.selectbox(
        "Selecione a condição da amostra:",
        ["Temperatura ambiente", "Refrigerada", "Sem identificação", "Coagulada"]
    )
    destino_amostra = st.text_input("Destino da Amostra")
    resultado_exame = st.text_input("Resultado do Exame (opcional)")
    observacoes = st.text_area("Observações (opcional)")

    submit_button = st.form_submit_button("Registrar Amostra")

if submit_button:
    # Registro da amostra
    db = connect_to_mongo()
    collection = db['amostras']
    sample_data = {
        "especie": especie_input,  # Usa o valor digitado ou a sugestão selecionada
        "nome_comum": nome_comum_input,  # Usa o valor digitado ou a sugestão selecionada
        "local_coleta": local_coleta,
        "data_coleta": str(data_coleta),
        "nome_coletor": nome_coletor,
        "metodo_coleta": metodo_coleta,
        "condicao_amostra": condicao_amostra,
        "destino_amostra": destino_amostra,
        "resultado_exame": resultado_exame,
        "observacoes": observacoes
    }
    sample_data = {k: v for k, v in sample_data.items() if v is not None}
    try:
        collection.insert_one(sample_data)
        st.success("Amostra registrada com sucesso!")
    except Exception as e:
        st.error(f"Erro ao registrar a amostra: {e}")
