import streamlit as st
from pymongo import MongoClient

# Verificação de login
if not st.session_state.get("logged_in"):
    st.warning("Você precisa fazer login para acessar esta página.")
    st.stop()  # Interrompe a execução do restante da página se o usuário não estiver logado

# Conexão ao MongoDB
def connect_to_mongo():
    client = MongoClient("mongodb://localhost:27017/")  # Substitua pela URI do MongoDB
    db = client['pibit_app']  # Substitua pelo nome do seu banco de dados
    return db

# Função de registro da amostra
def register_sample(
    sample_id=None, especie=None, nome_comum=None, local_coleta=None, data_coleta=None, 
    nome_coletor=None, metodo_coleta=None, condicao_amostra=None, destino_amostra=None, 
    codigo_barras=None, identificacao_molecular=None, resultado_exame=None, observacoes=None
):
    db = connect_to_mongo()
    collection = db['amostras']  # Substitua pelo nome da coleção desejada

    sample_data = {
        "sample_id": sample_id,
        "especie": especie,
        "nome_comum": nome_comum,
        "local_coleta": local_coleta,
        "data_coleta": data_coleta,
        "nome_coletor": nome_coletor,
        "metodo_coleta": metodo_coleta,
        "condicao_amostra": condicao_amostra,
        "destino_amostra": destino_amostra,
        "codigo_barras": codigo_barras,
        "identificacao_molecular": identificacao_molecular,
        "resultado_exame": resultado_exame,
        "observacoes": observacoes
    }
    
    sample_data = {k: v for k, v in sample_data.items() if v is not None}
    
    try:
        collection.insert_one(sample_data)
        return True
    except Exception as e:
        st.error(f"Erro ao registrar a amostra: {e}")
        return False

# Formulário de registro da amostra
st.title("Registrar Nova Amostra")

with st.form("form_registro_amostra"):
    sample_id = st.text_input("ID da Amostra")
    especie = st.text_input("Espécie (Nome Científico)")
    nome_comum = st.text_input("Nome Comum")
    local_coleta = st.text_input("Local de Coleta")
    data_coleta = st.date_input("Data da Coleta")
    nome_coletor = st.text_input("Nome do Coletor")
    metodo_coleta = st.text_input("Método de Coleta")
    condicao_amostra = st.text_input("Condição da Amostra")
    destino_amostra = st.text_input("Destino da Amostra")
    codigo_barras = st.text_input("Código de Barras")
    identificacao_molecular = st.text_input("Identificação Molecular (opcional)")
    resultado_exame = st.text_input("Resultado do Exame (opcional)")
    observacoes = st.text_area("Observações (opcional)")

    submit_button = st.form_submit_button("Registrar Amostra")

if submit_button:
    registro_sucesso = register_sample(
        sample_id=sample_id,
        especie=especie,
        nome_comum=nome_comum,
        local_coleta=local_coleta,
        data_coleta=str(data_coleta),
        nome_coletor=nome_coletor,
        metodo_coleta=metodo_coleta,
        condicao_amostra=condicao_amostra,
        destino_amostra=destino_amostra,
        codigo_barras=codigo_barras,
        identificacao_molecular=identificacao_molecular,
        resultado_exame=resultado_exame,
        observacoes=observacoes
    )
    if registro_sucesso:
        st.success("Amostra registrada com sucesso!")
    else:
        st.error("Erro ao registrar a amostra.")
