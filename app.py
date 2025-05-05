import streamlit as st
from pymongo import MongoClient
import os
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
)

# Construindo a interface de login
LOGGED_IN = __login__obj.build_login_ui()
username = __login__obj.get_username()

def connect_to_mongo():
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")  # força a conexão
        return client["pibit_app"]
    except Exception as e:
        st.error("Não foi possível conectar ao MongoDB Atlas:")
        # exibe a mensagem real do erro
        st.text(str(e))
        # exibe o traceback completo
        st.text(traceback.format_exc())
        return None

if LOGGED_IN:
    # Armazenando o usuário no estado da sessão
    if 'username' not in st.session_state:
        st.session_state['username'] = username
    
else:
    st.write("Por favor, faça login para acessar a aplicação.")
