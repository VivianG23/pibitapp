import streamlit as st
import pandas as pd
import json
from datetime import datetime

def register_sample():
    """
    Função para registrar uma nova amostra biológica.
    """
    with st.form("Registrar Amostra"):
        sample_id = st.text_input("ID da Amostra", placeholder='Digite o ID da amostra')
        species = st.text_input("Espécie", placeholder='Digite a espécie')
        location = st.text_input("Local de Coleta", placeholder='Digite o local de coleta')
        submit_button = st.form_submit_button(label='Registrar Amostra')

        if submit_button:
            # Salvar os dados no banco ou arquivo
            st.success(f"Amostra {sample_id} registrada com sucesso!")

