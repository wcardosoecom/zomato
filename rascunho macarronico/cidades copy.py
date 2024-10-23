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

st.set_page_config(page_title='Cidades', page_icon='🌆;', layout='wide')

# colocando a imagem:
image_path = 'logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=240)

st.header('Dashboard Zomato - Cidades')


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

#streamlit run cidades.py

### =================================================== ###
#                   layout streamlit                      #
### =================================================== ###

with st.container():
        st.markdown('#### Métricas gerais')
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            city_on = df1['city'].nunique()
            col1.metric('Total de cidades em operação', city_on)
        with col1:
            city_counts = df1.groupby('city')['restaurant_id'].nunique().reset_index()
            city_counts.columns = ['city', 't_restaurants']
            city_counts = city_counts.sort_values('t_restaurants', ascending=False)
            biggest_city = city_counts.iloc[0]['city']
            col1.metric('Mais restaurantes cadastrados', biggest_city)
        with col2:
            city_w_votes = df1.groupby('city')['votes'].mean().reset_index()
            city_w_votes.columns = ['city', 't_votes']
            city_w_votes = city_w_votes.sort_values('t_votes', ascending=False)
            b_city_w_votes = city_w_votes.iloc[0]['city']
            col2.metric('Maior média de avaliações recebidas', b_city_w_votes)
        with col2:
            city_rest_counts = df1.groupby('city')['cuisines'].nunique().reset_index()
            city_rest_counts.columns = ['city', 't_cuisines']
            city_rest_counts = city_rest_counts.sort_values('t_cuisines', ascending=False)
            b_city_rest_counts = city_rest_counts.iloc[0]['city']
            col2.metric('Maior variedade culinária', b_city_rest_counts)
        with col3:
            online_delivery = (df1['has_online_delivery'] == 1) & (df1['is_delivering_now'] ==1)
            city_online_delivery = df1.loc[online_delivery, ['city', 'restaurant_id']].value_counts('city').reset_index().sort_values('count', ascending=False)
            city_online_delivery = city_online_delivery.iloc[0,0]
            col3.metric('Mais restaurantes com delivery', city_online_delivery)
        with col3:
            city_rest_book = df1['has_table_booking'] == 1
            city_rest_book = df1.loc[city_rest_book, ['city', 'restaurant_id']].value_counts('city').reset_index()
            b_city_rest_book = city_rest_book.iloc[0]['city']
            col3.metric('Mais restaurantes com reserva', b_city_rest_book)
        with col4:
            nozero = df1['aggregate_rating'] != 0
            city_mean_last = df1.loc[nozero, ['city', 'aggregate_rating']].groupby('city').agg({'aggregate_rating': 'mean'}).reset_index().sort_values('aggregate_rating', ascending=True)
            city_mean_last = city_mean_last.iloc[0]['city']
            col4.metric('Pior nota média', city_mean_last)
        with col4:
            nozero = df1['aggregate_rating'] != 0
            city_mean_best = df1.loc[nozero, ['city', 'aggregate_rating']].groupby('city').agg({'aggregate_rating': 'mean'}).reset_index().sort_values('aggregate_rating', ascending=False)
            city_mean_best = city_mean_best.iloc[0]['city']
            col4.metric('Melhor nota média', city_mean_best)
###

st.markdown(""" --- """)

st.markdown('#### Gráficos')

with st.container():# gráfico de barras - COLOR RED-BLACK
    online_delivery = (df1['has_online_delivery'] == 1) & (df1['is_delivering_now'] ==1)
    city_online_delivery = df1.loc[online_delivery, ['city', 'restaurant_id']].value_counts('city').reset_index().sort_values('count', ascending=False).head(25)

    fig = px.bar(city_online_delivery, 
                x='city', 
                y='count',
                title='25 cidades com mais restaurantes que fazem entrega',
                labels={'city': 'Cidade', 'count': 'Total de restaurantes'},
                color='count',
                color_continuous_scale='rdgy')
    fig.update_layout(
        xaxis_title='Cidades',
        yaxis_title='Total de restaurantes',
        xaxis_tickangle=-45,
        showlegend=False,
        height=600,
        width=1000,
        plot_bgcolor='rgb(175, 175, 175)',
        font_color='white')
    fig.update_traces(hovertemplate='Cidade: %{x}<br>Total de restaurantes: %{y}')
    st.plotly_chart(fig, use_container_width=True)
###

with st.container():# gráfico de barras - COLOR RED-BLACK
    city_rest_counts = df1.groupby('city')['cuisines'].nunique().reset_index()
    city_rest_counts.columns = ['city', 't_cuisines']
    city_rest_counts = city_rest_counts.sort_values('t_cuisines', ascending=False).head(25)

    fig = px.bar(city_rest_counts, 
                x='city', 
                y='t_cuisines',
                title='25 cidades com maior variedade culinária',
                labels={'city': 'Cidade', 't_cuisines': 'Tipos de culinária'},
                color='t_cuisines',
                color_continuous_scale='rdgy')
    fig.update_layout(
        xaxis_title='Cidade',
        yaxis_title='Tipos de culinária',
        xaxis_tickangle=-45,
        showlegend=False,
        height=600,
        width=1000,
        plot_bgcolor='rgb(175, 175, 175)',
        font_color='white')
    fig.update_traces(hovertemplate='Cidade: %{x}<br>Tipos de culinária: %{y}')
    st.plotly_chart(fig, use_container_width=True)
###

with st.container():
    col1, col2 = st.columns(2, gap='large')
    with col1: #grafico de barras 1/2 color = RED
        nozero = df1['votes'] != 0
        city_mean_best = df1.loc[:, ['country', 'city', 'votes']].groupby(['country','city']).agg({'votes': 'mean'}).reset_index().sort_values('votes', ascending=False).round(0)
        city_mean_best = city_mean_best.groupby('country').head(1)
        city_mean_best = city_mean_best.head(5)
        colors = ['#FF0000', '#CC0000', '#990000', '#660000', '#330000']

        fig = px.bar(city_mean_best, 
                    x='city', 
                    y='votes',
                    title='5 cidades com a maior média de avaliações recebidas (por país)',
                    labels={'city': 'Cidade', 'votes': 'Média de avaliações recebidas', 'country': 'País'},
                    color='country',
                    color_discrete_sequence=colors)
        fig.update_layout(
            xaxis_title='Cidades',
            yaxis_title='Média de avaliações recebidas',
            xaxis_tickangle=-45,
            height=600,
            width=500,
            plot_bgcolor='rgb(175, 175, 175)',
            font_color='white')
        fig.update_traces(hovertemplate='Cidade: %{x}<br>Média de avaliações recebidas: %{y}')
        st.plotly_chart(fig, use_container_width=True)
###

    with col2: #grafico de barras 1/2 color = RED
        nozero = df1['aggregate_rating'] != 0
        city_mean_best = df1.loc[nozero, ['city', 'country', 'aggregate_rating']].groupby(['city', 'country']).agg({'aggregate_rating': 'mean'}).reset_index().sort_values('aggregate_rating', ascending=False).round(2)
        city_mean_best = city_mean_best.groupby('country').head(1)
        city_mean_best = city_mean_best.head(5)

        colors = ['#FF0000', '#CC0000', '#990000', '#660000', '#330000']

        fig = px.bar(city_mean_best, 
                    x='city', 
                    y='aggregate_rating',
                    title='5 cidades com a melhor nota média (por país)',
                    labels={'city': 'Cidade', 'aggregate_rating': 'Nota média', 'country': 'País'},
                    color='country',
                    color_discrete_sequence=colors)
        fig.update_layout(
            xaxis_title='Cidades',
            yaxis_title='Nota média',
            xaxis_tickangle=-45,
            height=600,
            width=500,
            plot_bgcolor='rgb(175, 175, 175)',
            font_color='white')
        fig.update_traces(hovertemplate='Cidade: %{x}<br>Nota média: %{y}')
        st.plotly_chart(fig, use_container_width=True)
###