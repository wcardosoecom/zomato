### IMPORT LIBRARIES ###
import pandas as pd
import inflection
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pandas.core.internals import concat
from PIL import Image
import plotly.express as px
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
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

def best_5_rests(df1, coluna):
    """ Essa função cria um gráfico de barras com 5 restaurantes com a 
    melhor nota media ou mais avaliações recebidas.
    coluna = 'aggregate_rating' (nota média) ou 'votes' (avaliações recebidas)
    Input = Dataframe
    Output = Gráfico de barras
    """
    if coluna == 'aggregate_rating':
        nozero = (df1['aggregate_rating'] != 0) & (df1['restaurant_name'] != 'tbsp.')
        op = 'mean'
        y_name = 'Nota média'
    else:
        nozero = ':'
        op = 'sum'
        y_name = 'Avaliações recebidas'
    nozero = (df1[coluna] != 0) & (df1['restaurant_name'] != 'tbsp.')
    rest_mean_best = df1.loc[nozero, ['restaurant_name', 'country', coluna]].groupby(['restaurant_name', 'country']).agg({coluna: op}).reset_index().sort_values(coluna, ascending=False).round(2)
    rest_mean_best = rest_mean_best.groupby('country').head(1)
    rest_mean_best = rest_mean_best.head(5)

    colors = ['#FF0000', '#CC0000', '#990000', '#660000', '#330000']

    fig = px.bar(rest_mean_best, 
                x='restaurant_name', 
                y=coluna,
                title='',
                labels={'restaurant_name': 'Restaurante', coluna: 'y_name', 'country': 'País'},
                color='country',
                color_discrete_sequence=colors)
    fig.update_layout(
        xaxis_title='Restaurante',
        yaxis_title=y_name,
        xaxis_tickangle=-45,
        height=600,
        width=500,
        plot_bgcolor='rgb(175, 175, 175)',
        font_color='white')
    fig.update_traces(hovertemplate='Restaurante: %{x}<br>Valor: %{y}')
    return fig
##############################

def pizza_pie_delivery(df1):
    """ Essa função cria um grafico de pizza com a diferença da média 
    de avaliações recebidas para restaurantes com x sem delivery.
    Input = Dataframe
    Output = Gráfico de pizza pie """
    online = (df1['has_online_delivery'] == 1) & (df1['is_delivering_now'] ==1)
    online = df1.loc[online, ['restaurant_name', 'votes']].groupby('restaurant_name').agg({'votes': 'mean'}).reset_index().sort_values('votes', ascending=False)
    t_votes_online = online['votes'].mean().round(0)
    offline = (df1['has_online_delivery'] == 0) & (df1['is_delivering_now'] ==0)
    offline = df1.loc[offline, ['restaurant_name', 'votes']].groupby('restaurant_name').agg({'votes': 'mean'}).reset_index().sort_values('votes', ascending=False)
    t_votes_offline = offline['votes'].mean().round(0)
    delivery = {'total_votes': [t_votes_online, t_votes_offline], 'restaurantes': ['Com delivery', 'Sem delivery']}

    fig = go.Figure(data=[go.Pie(labels=delivery['restaurantes'],
                    values=delivery['total_votes'], pull=[0, 0.1, 0.1])])
    fig.update_traces(
    marker=dict(colors=['#FF0000', '#505050'])
    )
    return fig
##############################

def pizza_pie_booking(df1):
    """ Essa função cria um grafico de pizza com a diferença da média 
    de avaliações recebidas para restaurantes com x sem reservas.
    Input = Dataframe
    Output = Gráfico de pizza pie """
    booking = df1['has_table_booking'] == 1
    booking = df1.loc[booking, ['restaurant_name', 'votes']].groupby('restaurant_name').agg({'votes': 'mean'}).reset_index().sort_values('votes', ascending=False)
    t_votes_booking = booking['votes'].mean().round(0)
    no_booking = df1['has_table_booking'] == 0
    no_booking = df1.loc[no_booking, ['restaurant_name', 'votes']].groupby('restaurant_name').agg({'votes': 'mean'}).reset_index().sort_values('votes', ascending=False)
    t_votes_no_booking = no_booking['votes'].mean().round(0)
    booking = {'total_votes': [t_votes_booking, t_votes_no_booking], 'restaurantes': ['Com reserva', 'Sem reserva']}

    fig = go.Figure(data=[go.Pie(labels=booking['restaurantes'],
                    values=booking['total_votes'], pull=[0, 0.1, 0.1])])
    fig.update_traces(
    marker=dict(colors=['#FF0000', '#505050'])
    )
    return fig
##############################

def bar_delivery (df1):
    """ Essa função cria um grafico de barras simples com a diferença da média 
    de avaliações recebidas para restaurantes com x sem delivery.
    Input = Dataframe
    Output = Gráfico de barras simples """
    online = (df1['has_online_delivery'] == 1) & (df1['is_delivering_now'] ==1)
    online = df1.loc[online, ['restaurant_name', 'aggregate_rating']].groupby('restaurant_name').agg({'aggregate_rating': 'mean'}).reset_index().sort_values('aggregate_rating', ascending=False)
    nota_online = online['aggregate_rating'].mean().round(2)
    offline = (df1['has_online_delivery'] == 0) & (df1['is_delivering_now'] ==0)
    offline = df1.loc[offline, ['restaurant_name', 'aggregate_rating']].groupby('restaurant_name').agg({'aggregate_rating': 'mean'}).reset_index().sort_values('aggregate_rating', ascending=False)
    nota_offline = offline['aggregate_rating'].mean().round(2)
    delivery = {'nota_media': [nota_online, nota_offline], 'restaurantes': ['Com delivery', 'Sem delivery']}

    fig = px.bar(delivery, 
                x='restaurantes', 
                y='nota_media',
                labels={'restaurantes': 'Restaurantes', 'nota_media': 'Nota média'},
                color_discrete_sequence=['#FF0000'])
    fig.update_layout(
        xaxis_title='Restaurantes',
        yaxis_title='Nota média',
        xaxis_tickangle=-45,
        showlegend=False,
        height=600,
        width=500,
        plot_bgcolor='rgb(175, 175, 175)',
        font_color='white')
    return fig
##############################

def bar_reservas (df1):
    """ Essa função cria um grafico de barras simples com a diferença da 
    nota média para restaurantes com x sem delivery.
    Input = Dataframe
    Output = Gráfico de barras simples """
    booking = df1['has_table_booking'] == 1
    booking = df1.loc[booking, ['restaurant_name', 'aggregate_rating']].groupby('restaurant_name').agg({'aggregate_rating': 'mean'}).reset_index().sort_values('aggregate_rating', ascending=False)
    nota_booking = booking['aggregate_rating'].mean().round(2)
    no_booking = df1['has_table_booking'] == 0
    no_booking = df1.loc[no_booking, ['restaurant_name', 'aggregate_rating']].groupby('restaurant_name').agg({'aggregate_rating': 'mean'}).reset_index().sort_values('aggregate_rating', ascending=False)
    nota_no_booking = no_booking['aggregate_rating'].mean().round(2)
    bookingt = {'nota_media': [nota_booking, nota_no_booking], 'restaurantes': ['Com reserva', 'Sem reserva']}

    fig = px.bar(bookingt, 
                x='restaurantes', 
                y='nota_media',
                labels={'restaurantes': 'Restaurantes', 'nota_media': 'Nota média'},
                color_discrete_sequence=['#FF0000'])
    fig.update_layout(
        xaxis_title='Restaurantes',
        yaxis_title='Nota média',
        xaxis_tickangle=-45,
        showlegend=False,
        height=600,
        width=500,
        plot_bgcolor='rgb(175, 175, 175)',
        font_color='white')
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

st.set_page_config(page_title='Restaurantes', page_icon='🍽;', layout='wide')

# colocando a imagem:
image_path = 'logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=240)

st.header('Dashboard Zomato - Restaurantes')


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

#streamlit run restaurantes.py

### =================================================== ###
#                   layout streamlit                      #
### =================================================== ###

with st.container():
        st.markdown('#### Métricas gerais')
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            rest_on = df1['restaurant_name'].nunique()
            col1.metric('Total de restaurantes cadastrados', rest_on)
        with col2:
            rest_w_votes = df1.groupby('restaurant_name')['votes'].mean().reset_index()
            rest_w_votes.columns = ['restaurant_name', 't_votes']
            rest_w_votes = rest_w_votes.sort_values('t_votes', ascending=False)
            b_rest_w_votes = rest_w_votes.iloc[0]['restaurant_name']
            col2.metric('Mais avaliações recebidas', b_rest_w_votes)
        with col3:
            nozero = df1['aggregate_rating'] != 0
            rest_mean_last = df1.loc[nozero, ['restaurant_name', 'aggregate_rating']].groupby('restaurant_name').agg({'aggregate_rating': 'mean'}).reset_index().sort_values('aggregate_rating', ascending=True)
            rest_mean_last = rest_mean_last.iloc[0]['restaurant_name']
            col3.metric('Pior nota média', rest_mean_last)
        with col4:
            nozero = df1['aggregate_rating'] != 0
            rest_mean_best = df1.loc[nozero, ['restaurant_name', 'aggregate_rating']].groupby('restaurant_name').agg({'aggregate_rating': 'mean'}).reset_index().sort_values('aggregate_rating', ascending=False)
            rest_mean_best = rest_mean_best.iloc[0]['restaurant_name']
            col4.metric('Melhor nota média', rest_mean_best)
###

tab1, tab2 = st.tabs(
    ['Gráficos', 'Mapa de geolocalização'])



with tab1:  # Gráficos
    with st.container():
        st.markdown('#### Gráficos')

        with st.container():# 2 gráficos
            col1, col2 = st.columns(2, gap='large')
            with col1:
                st.markdown('###### Média de avaliações recebidas por restaurantes com X sem delivery')
                fig = pizza_pie_delivery(df1)
                st.plotly_chart(fig, use_container_width=True)
            ###
            with col2: #Gráfico de barras simples
                st.markdown('###### Nota média por restaurantes com X sem delivery')
                fig = bar_delivery (df1)
                st.plotly_chart(fig)
        ###

        with st.container():# 2 gráficos
                    col1, col2 = st.columns(2, gap='large')
        with col1:
            with col1:
                st.markdown('###### Média de avaliações recebidas por restaurantes com X sem reserva')
                fig = pizza_pie_booking(df1)
                st.plotly_chart(fig)
        ###

            with col2:
                st.markdown('###### Nota média por restaurantes com X sem reserva')
                fig = bar_reservas (df1)
                st.plotly_chart(fig)
        ###

        with st.container():
            col1, col2 = st.columns(2, gap='large')
            with col1: #grafico de barras 1/2 color = HOT 
                st.markdown('###### 5 restaurantes com a mais avaliações recebidas (por país)')
                fig = best_5_rests(df1, 'votes')
                st.plotly_chart(fig)
        ###

            with col2: #grafico de barras 1/2 color = HOT
                st.markdown('###### 5 restaurantes com a melhor nota média (por país)')
                fig = best_5_rests(df1, 'aggregate_rating')
                st.plotly_chart(fig)
        ###

with tab2:  # Mapa de geolocalização
    with st.container():# mapa de geolocalização com agrupamento e cores
        st.markdown('#### Geolocalização')
        df_aux = (df1.loc[:, ['restaurant_name', 'aggregate_rating', 'latitude',
                'longitude']]
                .drop_duplicates()  # Remove duplicatas se houver
                .groupby(['restaurant_name', 'aggregate_rating']).mean().reset_index())

        color_map = {
        0: 'gray',
        1: 'red',
        2: 'orange',
        3: 'orange',
        4: 'green'
        }

        map = folium.Map(
            prefer_canvas=True, # Usar canvas renderer para melhor performance
            ) 
        marker_cluster = MarkerCluster(
            name="Restaurantes",
            overlay=True,
            control=True,
            show=True
        ).add_to(map)

        for index, location_info in df_aux.iterrows():
            rating = location_info['aggregate_rating']
            color = color_map.get(int(rating))  # Cor padrão para notas não mapeadas
        
            folium.Marker([location_info['latitude'],
                        location_info['longitude']],
                        popup=location_info[['restaurant_name', 'aggregate_rating']],icon=folium.Icon(color=color)).add_to(marker_cluster)

        folium_static(map, width=1024, height=400)
    ###
    st.markdown(""" --- """)