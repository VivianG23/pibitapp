import streamlit as st
from pymongo import MongoClient
import pandas as pd
import altair as alt

# Conexão ao MongoDB Atlas
def connect_to_mongo():
    uri = "mongodb+srv://emilianodl:icHkQo4W507qyMMf@cluster0.excq6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    db = client['pibit_app']
    return db

# Função para buscar amostras do banco de dados
def fetch_samples():
    db = connect_to_mongo()
    collection = db['amostras']
    samples = list(collection.find())
    for sample in samples:
        sample['_id'] = str(sample['_id'])  # Converte ObjectId para string
    return samples

# Função para filtrar pelo nome do animal
def filter_by_animal_name(df, column_name='Nome do animal'):
    """
    Cria um campo de pesquisa na sidebar para filtrar a coluna 'Nome do animal'.
    Se nada for digitado, retorna o DataFrame original.
    """
    pesquisa = st.sidebar.text_input("Pesquisar pelo nome do animal:")
    if pesquisa:
        df = df[df[column_name].str.contains(pesquisa, case=False, na=False)]
    return df

# Injetar CSS customizado para ajustar o container do multiselect (se necessário)
st.markdown(
    """
    <style>
    /* Ajusta o container do multiselect para ter altura máxima e scroll vertical */
    div[data-baseweb="select"] > div {
        max-height: 150px;
        overflow-y: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Página principal
st.title("Amostras")

# Carrega as amostras e converte para DataFrame
samples = fetch_samples()
if samples:
    df = pd.DataFrame(samples)
else:
    st.info("Nenhuma amostra registrada ainda.")
    st.stop()

# Cria abas para 'Registros' e 'Relatório'
tabs = st.tabs(["Registros", "Relatório"])

with tabs[0]:
    st.header("Lista de Registros")

    # --- Filtros na sidebar ---
    st.sidebar.header("Filtros")
    
    # Filtro por Data de coleta (se existir a coluna)
    if 'Data de coleta' in df.columns:
        df['Data de coleta'] = pd.to_datetime(df['Data de coleta'], errors='coerce')
        data_min = df['Data de coleta'].min()
        data_max = df['Data de coleta'].max()
        data_selecionada = st.sidebar.date_input("Selecione o intervalo de datas:",
                                                  value=(data_min, data_max))
        if isinstance(data_selecionada, tuple) and len(data_selecionada) == 2:
            inicio, fim = data_selecionada
            df = df[(df['Data de coleta'] >= pd.to_datetime(inicio)) & 
                    (df['Data de coleta'] <= pd.to_datetime(fim))]
    
    # Filtro pelo Nome do animal
    if 'Nome do animal' in df.columns:
        df = filter_by_animal_name(df, 'Nome do animal')
    
    # Exibe a tabela filtrada
    st.dataframe(df, use_container_width=True)
    
    # Opção para exportar como CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar como CSV",
        data=csv,
        file_name="amostras_registradas.csv",
        mime="text/csv"
    )

with tabs[1]:
    st.header("Relatório de Amostras")
    
    # Exemplo de gráfico: distribuição das espécies (ou Nome do animal)
    if 'Nome do animal' in df.columns:
        # Cria uma contagem por espécie
        especies = df['Nome do animal'].value_counts().reset_index()
        especies.columns = ['Nome do animal', 'Quantidade']
        
        # Gráfico de barras usando Altair
        grafico = alt.Chart(especies).mark_bar().encode(
            x=alt.X("Nome do animal:N", sort='-y', title="Nome do animal"),
            y=alt.Y("Quantidade:Q", title="Quantidade"),
            tooltip=["Nome do animal", "Quantidade"]
        ).properties(
            width=600,
            height=400,
            title="Distribuição de Espécies"
        )
        st.altair_chart(grafico, use_container_width=True)
    
