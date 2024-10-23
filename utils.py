import streamlit as st
import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets
import requests
import bcrypt
from bcrypt import gensalt
import regex as re

encriptar = gensalt()

import bcrypt
import json

def check_usr_pass(username: str, password: str) -> bool:
    """
    Autentica o usuário e a senha
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_user_data = json.load(auth_json)

    for registered_user in authorized_user_data:
        if registered_user['username'] == username:
            try:
                # A senha no arquivo JSON está como string, então precisa ser convertida de volta para bytes
                stored_hashed_password = registered_user['password'].encode('utf-8')

                # A senha fornecida pelo usuário também precisa ser convertida em bytes
                password_bytes = password.encode('utf-8')

                # Agora verifica se a senha fornecida corresponde ao hash armazenado
                if bcrypt.checkpw(password_bytes, stored_hashed_password):
                    return True
            except Exception as e:
                print(f"Erro ao verificar a senha: {e}")
                pass
    return False


def load_lottieurl(url: str) -> str:
    """
    Carrega a animação
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        pass

def check_valid_name(name_sign_up: str) -> bool:
    """
    Checa se o nome é válido
    """
    name_regex = (r'^[A-Za-z_][A-Za-z0-9_]*')

    if re.search(name_regex, name_sign_up):
        return True
    return False

def check_valid_email(email_sign_up: str) -> bool:
    """
    Checa se o email é válido
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email_sign_up):
        return True
    return False


def check_unique_email(email_sign_up: str) -> bool:
    """
    Checa se o email já existe
    """
    authorized_user_data_master = list()
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            authorized_user_data_master.append(user['email'])

    if email_sign_up in authorized_user_data_master:
        return False
    return True


def non_empty_str_check(username_sign_up: str) -> bool:
    """
    Checha por nomes vazios
    """
    empty_count = 0
    for i in username_sign_up:
        if i == ' ':
            empty_count = empty_count + 1
            if empty_count == len(username_sign_up):
                return False

    if not username_sign_up:
        return False
    return True


def check_unique_usr(username_sign_up: str):
    """
    Checa se o usuário ja existe
    """
    authorized_user_data_master = list()
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            authorized_user_data_master.append(user['username'])

    if username_sign_up in authorized_user_data_master:
        return False
    
    non_empty_check = non_empty_str_check(username_sign_up)

    if non_empty_check == False:
        return None
    return True


def register_new_usr(name_sign_up, email_sign_up, username_sign_up, password_sign_up, matricula, created_at):

    """
    Registra o novo usuário em um JSON
    """
    # Gera o salt. O valor de rounds (custo) padrão é 12, mas você pode usar outro valor inteiro.
    salt = bcrypt.gensalt()  # rounds padrão é 12
    # Se você quiser um valor personalizado, passe um número, por exemplo: bcrypt.gensalt(rounds=10)

    # Faz o hash da senha
    hashed_password = bcrypt.hashpw(password_sign_up.encode('utf-8'), salt)
    
    new_usr_data = {
        'username': username_sign_up,
        'name': name_sign_up,
        'email': email_sign_up,
        'password': hashed_password.decode('utf-8'),  # Converte de bytes para string para salvar no JSON
        'matricula': matricula,
        'created_at': created_at
    }

    # Abrir o arquivo de autenticação para ler os dados existentes
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_user_data = json.load(auth_json)

    # Escrever o novo usuário no arquivo
    with open("_secret_auth_.json", "w") as auth_json_write:
        authorized_user_data.append(new_usr_data)
        json.dump(authorized_user_data, auth_json_write, indent=4)


def check_username_exists(user_name: str) -> bool:
    """
    Checha se o usuário já existe no json
    """
    authorized_user_data_master = list()
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            authorized_user_data_master.append(user['username'])
        
    if user_name in authorized_user_data_master:
        return True
    return False
        

def check_email_exists(email_forgot_passwd: str):
    """
    Checa se o email já existe no json
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            if user['email'] == email_forgot_passwd:
                    return True, user['username']
    return False, None

def change_password(user_name: str, new_password: str):
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

    with open("_secret_auth_.json", "w") as auth_json_:
        for user in authorized_users_data:
            if user['user_name'] == user_name:
                user['password'] = bcrypt.checkpw(new_password)
        json.dump(authorized_users_data, auth_json_)
    