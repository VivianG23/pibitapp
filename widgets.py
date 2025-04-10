import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
import bcrypt
from utils import check_usr_pass
from utils import load_lottieurl
from utils import check_valid_name
from utils import check_valid_email
from streamlit_lottie import option_menu
from utils import check_unique_email
from utils import check_unique_usr
from utils import register_new_usr
from utils import change_password
from pymongo import MongoClient

def connect_to_mongo():
    uri = "mongodb+srv://emilianodl:icHkQo4W507qyMMf@cluster0.excq6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    return client['pibit_app']

class __login__:
    """
    Builds the UI for the Login/ Sign Up page.
    """

    def __init__(self, company_name: str, width, height, logout_button_name: str = 'Logout', hide_menu_bool: bool = False, hide_footer_bool: bool = False, lottie_url: str = "https://assets8.lottiefiles.com/packages/lf20_ktwnwv5m.json"):
        self.company_name = company_name
        self.width = width
        self.height = height
        self.logout_button_name = logout_button_name
        self.hide_menu_bool = hide_menu_bool
        self.hide_footer_bool = hide_footer_bool
        self.lottie_url = lottie_url


        if not self.cookies.ready():
            st.stop()

    def check_auth_json_file_exists(self, auth_filename: str) -> bool:
        file_names = []
        for path in os.listdir('./'):
            if os.path.isfile(os.path.join('./', path)):
                file_names.append(path)

        present_files = []
        for file_name in file_names:
            if auth_filename in file_name:
                present_files.append(file_name)

            present_files = sorted(present_files)
            if len(present_files) > 0:
                return True
        return False

    def get_username(self):
        if st.session_state['LOGOUT_BUTTON_HIT'] == False:
            fetched_cookies = self.cookies
            if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
                username = fetched_cookies['__streamlit_login_signup_ui_username__']
                return username

    def login_widget(self) -> None:
        if st.session_state['LOGGED_IN'] == False:
            if st.session_state['LOGOUT_BUTTON_HIT'] == False:
                fetched_cookies = self.cookies
                if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
                    if fetched_cookies['__streamlit_login_signup_ui_username__'] != '1c9a923f-fb21-4a91-b3f3-5f18e3f01182':
                        st.session_state['LOGGED_IN'] = True

        if st.session_state['LOGGED_IN'] == False:
            st.session_state['LOGOUT_BUTTON_HIT'] = False

            del_login = st.empty()
            with del_login.form("Login Form"):
                username = st.text_input(
                    "Usuário", placeholder='')
                password = st.text_input(
                    "Senha", placeholder='', type='password')

                st.markdown("###")
                login_submit_button = st.form_submit_button(label='Login')

                if login_submit_button == True:
                    authenticate_user_check = check_usr_pass(
                        username, password)

                    if authenticate_user_check == False:
                        st.error("Usuário ou senha inválida")

                    else:
                        st.session_state['LOGGED_IN'] = True
                        self.cookies['__streamlit_login_signup_ui_username__'] = username
                        self.cookies.save()
                        del_login.empty()


    def sign_up_widget(self) -> None:
      with st.form("Registre-se"):
        name_sign_up = st.text_input("Nome *", placeholder='Digite seu nome')
        valid_name_check = check_valid_name(name_sign_up)

        email_sign_up = st.text_input(
            "Email *", placeholder='Digite seu email')
        valid_email_check = check_valid_email(email_sign_up)
        unique_email_check = check_unique_email(email_sign_up)

        username_sign_up = st.text_input(
            "Usuário *", placeholder='Digite um usuário')
        unique_username_check = check_unique_usr(username_sign_up)

        password_sign_up = st.text_input(
            "Senha *", placeholder='Crie sua senha', type='password')

        matricula_sign_up = st.selectbox(
                    "Tipo de Usuário *", 
                    ["Bolsista UFPI", "Bolsista Externo", "Mestrando", "Doutorando", "Professor"]
                    )

        st.markdown("###")
        sign_up_submit_button = st.form_submit_button(label='Registrar')

        if sign_up_submit_button:
            if not valid_name_check:
                st.error("Digite um nome válido")

            elif not valid_email_check:
                st.error("Digite um email válido")

            elif not unique_email_check:
                st.error("Já existe uma conta com esse email")

            elif not unique_username_check:
                st.error(f'O usuário {username_sign_up} já existe')

            elif unique_username_check is None:
                st.error('Digite um nome de usuário')

            if valid_name_check and valid_email_check and unique_email_check and unique_username_check:
                # Adiciona a data de criação no momento do registro
                created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Função de registro que agora também recebe matrícula e created_at
                register_new_usr(name_sign_up, email_sign_up, username_sign_up,
                                 password_sign_up, matricula_sign_up, created_at)
                st.success("Registro realizado com sucesso!")

    def change_pass_widget(self) -> None:
        with st.form('Alterar senha'):
            new_password = st.text_input(
                'Nova senha', placeholder='Digite a nova senha', type='password')
            confirm_new_password = st.text_input(
                "Confirmar nova senha", placeholder='Digite novamente a nova senha', type='password')
            submit_button = st.form_submit_button(label='Mudar senha')

            if submit_button:
                if new_password != confirm_new_password:
                    st.error('As senhas não são iguais')
                    return

                salt = bcrypt.gensalt()
                hashed_new_password = bcrypt.hashpw(
                    new_password.encode('utf-8'), salt)

                email = st.session_state['email']
                self.change_passwd(email, hashed_new_password('utf-8'))


    def show_users_widget(self) -> None:
       db = connect_to_mongo()
       users_collection = db["usuarios"]
       users_data = list(users_collection.find({}, {"_id": 0}))  # Exclui o _id para não exibir

    # Garante que todos os registros tenham as chaves necessárias
       for user in users_data:
           user['matricula'] = user.get('matricula', 'N/A')
           user['created_at'] = user.get('created_at', 'N/A')

    # Converte para DataFrame e exibe
       users_df = pd.DataFrame(users_data)
       if not users_df.empty:
           st.title("Usuários Registrados")
           st.table(users_df[['username', 'name', 'email', 'matricula', 'created_at']])
       else:
           st.info("Nenhum usuário encontrado.")


    def logout_widget(self) -> None:
        if st.session_state['LOGGED_IN'] == True:
            del_logout = st.sidebar.empty()
            del_logout.markdown("#")
            logout_click_check = del_logout.button(self.logout_button_name)

            if logout_click_check == True:
                st.session_state['LOGOUT_BUTTON_HIT'] = True
                st.session_state['LOGGED_IN'] = False
                self.cookies['__streamlit_login_signup_ui_username__'] = '1c9a923f-fb21-4a91-b3f3-5f18e3f01182'
                del_logout.empty()

    def nav_sidebar(self):
        main_page_sidebar = st.sidebar.empty()
        with main_page_sidebar:
            selected_option = option_menu(
                menu_title='Navegação',
                menu_icon='list-columns-reverse',
                icons=['box-arrow-in-right', 'person-plus', 'x-circle',
                       'arrow-counterclockwise', 'file-plus'],
                options=['Autenticação', 'Criar uma conta',
                         'Esqueceu a senha?', 'Usuários'],
                styles={
                    "container": {"padding": "5px"},
                    "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px"}})
        return main_page_sidebar, selected_option
    
    

    def hide_menu(self) -> None:
        st.markdown(""" <style>
        #MainMenu {visibility: hidden;}
        </style> """, unsafe_allow_html=True)

    def hide_footer(self) -> None:
        st.markdown(""" <style>
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)

    def build_login_ui(self):
        if 'LOGGED_IN' not in st.session_state:
            st.session_state['LOGGED_IN'] = False

        if 'LOGOUT_BUTTON_HIT' not in st.session_state:
            st.session_state['LOGOUT_BUTTON_HIT'] = False

        auth_json_exists_bool = self.check_auth_json_file_exists(
            '_secret_auth_.json')

        if auth_json_exists_bool == False:
            with open("_secret_auth_.json", "w") as auth_json:
                json.dump([], auth_json)

        main_page_sidebar, selected_option = self.nav_sidebar()

        if selected_option == 'Autenticação':
            c1, c2 = st.columns([7, 3])
            with c1:
                self.login_widget()
            with c2:
                if st.session_state['LOGGED_IN'] == False:
                    self.animation()

        if selected_option == 'Criar uma conta':
            self.sign_up_widget()

        if selected_option == 'Esqueceu a senha?':
            self.change_pass_widget()

        if selected_option == 'Usuários':
            self.show_users_widget()

        self.logout_widget()


        if self.hide_menu_bool == True:
            self.hide_menu()

        if self.hide_footer_bool == True:
            self.hide_footer()

        return st.session_state['LOGGED_IN']
