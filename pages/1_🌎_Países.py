### IMPORT LIBRARIES ###
import pandas as pd
import inflection
import streamlit as st
import numpy as np
import plotly.express as px
from pandas.core.internals import concat
from PIL import Image
import plotly.express as px
######################################################################

### FUNÇÕES ###
### função country_name() serve para indentificar o país do restaurante 
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]
##############################

### função create_price_tye() cria coluna com categoria para o tipo de 
# comida baseado no range de valores
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
##############################

### função color_name() cria coluna com o nome das cores baseado em seus códigos
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]
##############################

### função que renomeia as colunas 
def rename_columns(dataframe):
    df1 = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df1.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df1.columns = cols_new
    return df1
##############################

def best_5_countries(df1, coluna):
    """ Essa função cria um gráfico de barras com os 5 países com o melhor desempenho.
    coluna = 'aggregate_rating' (nota média) ou 'votes' (média de avaliações)
    Input = Dataframe
    Output = Gráfico de barras
    """
    nozero = df1[coluna] != 0
    country_mean_best = (df1.loc[nozero, ['country', 'aggregate_rating', 'votes']]
                         .groupby('country')
                         .agg({coluna : 'mean'})
                         .reset_index()
                         .sort_values(coluna, ascending=False)
                         .round(2)
                         .head(5))
    if coluna == 'aggregate_rating':
        y_name = 'Nota média'
    else:
        y_name = 'Média de avaliações recebidas por restaurante'
    fig = px.bar(country_mean_best, 
                x='country', 
                y=coluna,
                labels={'country': 'País', coluna: y_name})
    fig.update_traces(marker=dict(color='red'))
    fig.update_layout(
        xaxis_title='Países',
        yaxis_title=y_name,
        xaxis_tickangle=-45,
        showlegend=False,
        height=600,
        width=500,
        plot_bgcolor='rgb(175, 175, 175)',
        font_color='white')
    fig.update_traces(hovertemplate='País: %{x}<br>Média: %{y}')
    return fig
##############################

def count_biggest(df1, coluna):
    """ Essa função cria um gráfico de barras com o total de cidades e restaurantes por país.
    coluna = 'restaurant_id' (restaurantes) ou 'city' (cidades)
    Input = Dataframe
    Output = Gráfico de barras
    """
    count_b = df1.groupby('country')[coluna].nunique().reset_index()
    count_b.columns = ['country', 't_coluna']
    count_b = count_b.sort_values('t_coluna', ascending=False)
    if coluna == 'city':
        y_name = 'Total de cidades'
    else:
        y_name = 'Total de restaurantes'
    fig = px.bar(count_b, 
                x='country', 
                y='t_coluna',
                labels={'country': 'País', 't_coluna': y_name},
                color='t_coluna',
                color_continuous_scale='rdgy')
    fig.update_layout(
        xaxis_title='Países',
        yaxis_title=y_name,
        xaxis_tickangle=-45,
        showlegend=False,
        height=600,
        width=1000,
        plot_bgcolor='rgb(175, 175, 175)',
        font_color='white')
    fig.update_traces(hovertemplate='País: %{x}<br>Total: %{y}')
    return fig
##############################

############################################################

### IMPORT DATASET + COPY ###
df = pd.read_csv('dataset/zomato.csv')
df1 = df.copy()

######################################################################

### LIMPEZA DE DADOS ###
### aplicação da função country_name 
df1['Country'] = df1['Country Code'].apply(country_name)
### aplicação da função create_price_tye
df1['Price Tye'] = df1['Price range'].apply(create_price_tye)
### aplicação da função color_name
df1['Color'] = df1['Rating color'].apply(color_name)
### aplicação da função rename_columns
df1 = rename_columns(df1)
### definindo o tipo de culinária principal do restaurante
df1["cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: str(x).split(",")[0])
######################################################################


### =================================================== ###
#                   Index                         #
### =================================================== ###

st.set_page_config(page_title='Países', page_icon='🌎;', layout='wide')

# colocando a imagem:
image_path = 'logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=240)

st.header('Dashboard Zomato - Países')



### =================================================== ###
#                   Barra lateral                         #
### =================================================== ###


# informações da barra lateral
#st.sidebar.markdown('## Zomato')
st.sidebar.markdown('### Food Delivery & Dining')
st.sidebar.markdown(""" --- """)
# multipla seleção de países
st.sidebar.markdown('#### Filtro')
traffic_options = st.sidebar.multiselect(
    'Selecione os países',
    ['Philippines','Brazil','Australia', 'Canada', 'England', 'India', 'Indonesia', 'New Zeland', 'Qatar', 'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates', 'United States of America'],
    default=['Philippines','Brazil','Australia', 'Canada', 'England', 'India', 'Indonesia', 'New Zeland', 'Qatar', 'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates', 'United States of America'])
# aplicando o filtro de países
linhas_selecionadas = df1['country'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]
# testar se o filtro funcionou
#st.dataframe(df1.head())

st.sidebar.markdown('#### Dados tratados')
st.sidebar.download_button(
label="Download",
data=df1.to_csv(),
file_name='zomato.csv',
mime='text/csv')

st.sidebar.markdown(""" --- """)
st.sidebar.markdown('###### Powered by William Cardoso')

#streamlit run paises.py

### =================================================== ###
#                   layout streamlit                      #
### =================================================== ###

with st.container():
        st.markdown('#### Métricas gerais')
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            country_on = df1['country'].nunique()
            col1.metric('Total de países em operação', country_on)
        with col1:
            city_on = df1['city'].nunique()
            col1.metric('Total de cidades em operação', city_on)
        with col2:
            rest_counts = df1.groupby('country')['restaurant_id'].nunique().reset_index()
            rest_counts.columns = ['country', 't_restaurants']
            rest_counts = rest_counts.sort_values('t_restaurants', ascending=False)
            biggest_country = rest_counts.iloc[0]['country']
            col2.metric('Mais restaurantes cadastrados', biggest_country)
        with col2:
            country_rest_counts = df1.groupby('country')['cuisines'].nunique().reset_index()
            country_rest_counts.columns = ['country', 't_cuisines']
            country_rest_counts = country_rest_counts.sort_values('t_cuisines', ascending=False)
            b_country_rest_counts = country_rest_counts.iloc[0]['country']
            col2.metric('Maior variedade culinária', b_country_rest_counts)
        with col3:
            hrange = df1['price_range'] >= 4
            country_hrange = df1.loc[hrange, ['country', 'restaurant_id']].value_counts('country').reset_index()
            country_hrange = country_hrange.sort_values('count', ascending=False)
            biggest_country_hrange = country_hrange.iloc[0]['country']
            col3.metric('País com restaurantes mais caros', biggest_country_hrange)
        with col3:
            country_w_votes = df1.groupby('country')['votes'].mean().reset_index()
            country_w_votes.columns = ['country', 't_votes']
            country_w_votes = country_w_votes.sort_values('t_votes', ascending=False)
            b_country_w_votes = country_w_votes.iloc[0]['country']
            col3.metric('A maior média avaliações recebidas', b_country_w_votes)
        with col4:
            nozero = df1['aggregate_rating'] != 0
            country_mean_last = df1.loc[nozero, ['country', 'aggregate_rating']].groupby('country').agg({'aggregate_rating': 'mean'}).reset_index().sort_values('aggregate_rating', ascending=True)
            b_country_mean_last = country_mean_last.iloc[0]['country']
            col4.metric('Pior nota média', b_country_mean_last)
        with col4:
            nozero = df1['aggregate_rating'] != 0
            country_mean_best = df1.loc[nozero, ['country', 'aggregate_rating']].groupby('country').agg({'aggregate_rating': 'mean'}).reset_index().sort_values('aggregate_rating', ascending=False)
            b_country_mean_best = country_mean_best.iloc[0]['country']
            col4.metric('Melhor nota média', b_country_mean_best)
###

st.markdown(""" --- """)

st.markdown('#### Gráficos')

with st.container():# gráfico de barras - COLOR RED-BLACK
    st.markdown('##### Total de cidades por país')
    fig = count_biggest(df1, 'city')
    st.plotly_chart(fig, use_container_width=True)
###

with st.container():# gráfico de barras - COLOR RED-BLACK
    st.markdown('##### Total de restaurantes por país')
    fig = count_biggest(df1, 'restaurant_id')
    st.plotly_chart(fig, use_container_width=True)
###

with st.container():
    col1, col2 = st.columns(2, gap='large')
    with col1: #grafico de barras 1/2 - TOP 5 - color = RED 
        st.markdown('##### 5 países com melhor média de avaliações recebidas')
        fig = best_5_countries(df1, 'votes')
        st.plotly_chart(fig, use_container_width=True)
###

    with col2: #grafico de barras 1/2 - TOP 5 - color = RED 
        st.markdown('##### 5 países com melhor nota média')
        fig = best_5_countries(df1, 'aggregate_rating')
        st.plotly_chart(fig, use_container_width=True)
###