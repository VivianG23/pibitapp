import streamlit as st
from pymongo import MongoClient
from widgets import __login__

st.markdown(
    """
    <h1 style='text-align: center; font-size: 32px; margin-top: 10px;'>
        NEPPAS - Laboratório de Vigilância de Epizootias - UFPI
    </h1>
    """,
    unsafe_allow_html=True
)

# Inicialização do objeto de login
__login__obj = __login__(
    company_name = "UFPI",
    width = 200, height = 250,
    logout_button_name = 'Logout', 
    hide_menu_bool = False,
    hide_footer_bool = False,
    lottie_url = 'https://lottie.host/955e400e-8241-40d5-88d5-7b24a65c0e2c/viy1vmGJhi.json'
)

# Construindo a interface de login
LOGGED_IN = __login__obj.build_login_ui()
username = __login__obj.get_username()

def connect_to_mongo():
    # Substitua <username>, <password> e, se necessário, o nome do cluster e banco de dados
    uri = "mongodb+srv://emilianodl:icHkQo4W507qyMMf@cluster0.excq6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    db = client['pibit_app']  # Ou já especificado na URI, se preferir.
    return db

if LOGGED_IN:
    # Armazenando o usuário no estado da sessão
    if 'username' not in st.session_state:
        st.session_state['username'] = username
    
else:
    st.write("Por favor, faça login para acessar a aplicação.")
