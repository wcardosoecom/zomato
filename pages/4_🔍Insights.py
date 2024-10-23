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
        return "1_acessivel"
    elif price_range == 2:
        return "2_regular"
    elif price_range == 3:
        return "3_alto"
    else:
        return "4_superior"
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

st.set_page_config(page_title='Insights', page_icon='🔍;', layout='wide')

# colocando a imagem:
image_path = 'logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=240)

st.header('Dashboard Zomato - Insights')


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

### =================================================== ###
#                   layout streamlit                      #
### =================================================== ###

tab1, tab2 = st.tabs(
    ['Propostas para análises adicionais', 'Gráficos adicionais'])

with tab1:  
    with st.container():
        st.markdown('#### Países')
        '''
1. Análise temporal da expansão internacional:
- Mapear detalhadamente a cronologia de expansão da Zomato além do mercado indiano
- Identificar padrões de crescimento e velocidade de penetração em novos mercados
- Avaliar a taxa de sucesso em diferentes regiões geográficas para projetar tendências futuras de expansão

2. Estudo dos fatores de sucesso na Indonésia
- Investigar as características específicas do mercado gastronômico indonésio
- Analisar o perfil dos estabelecimentos mais bem avaliados
- Examinar as políticas de relacionamento com parceiros e estratégias de engajamento com usuários
- Avaliar aspectos culturais e comportamentais que possam influenciar as avaliações positivas

3. Análise comparativa Indonésia-Austrália
- Identificar padrões comuns entre os mercados que contribuem para o alto desempenho
- Estudar as práticas operacionais bem-sucedidas que possam ser replicadas em outros mercados
- Desenvolver um framework de boas práticas baseado nas experiências positivas destes países
- Elaborar recomendações estratégicas para aprimoramento das operações em outros mercados'''
    st.markdown(""" --- """)

with tab1:  
    with st.container():
        st.markdown('#### Cidades')
    '''
    1. Identificar possíveis barreiras para expansão do serviço de entregas em outras localidades

    2. Estudo da diversidade culinária
    - Mapear a distribuição de tipos de culinária por região
    - Analisar a relação entre diversidade culinária e demografia local
    - Identificar oportunidades de expansão do cardápio em mercados específicos

    3. Aprofundamento do caso Londres
    - Examinar os fatores que contribuem para o alto desempenho da cidade
    - Estudar a relação entre diversidade culinária e satisfação dos usuários
    - Aventar a possibilidade de desenvolvimento de benchmarks baseados no modelo londrino para aplicação em outros mercados urbanos
    '''
    st.markdown(""" --- """)

with tab1:  
    with st.container():
        st.markdown('#### Restaurantes')
    '''
    1. Análise aprofundada do serviço de delivery
    - Investigar o perfil e motivação dos usuários que mais avaliam restaurantes com delivery
    - Analisar a relação entre tempo de entrega e satisfação do cliente

    2. Estudo do sistema de reservas
    - Examinar a correlação entre o sistema de reservas e o ticket médio dos estabelecimentos
    - Avaliar o impacto do sistema de reservas em diferentes categorias de restaurantes
    - Identificar fatores que contribuem para a maior satisfação em restaurantes com sistema de reservas

    3. Aprofundamento do caso Domino's Pizza
    - Realizar um benchmark detalhado das práticas operacionais da rede
    - Estudar a evolução temporal das avaliações para identificar melhorias implementadas
    - Investigar a relação entre campanhas promocionais e volume de avaliações
    - Realizar um planejamento para melhoria na satisfação dos clientes com o restaurante
    '''
    st.markdown(""" --- """)


def price_rating(df1, coluna):
    """ Essa função cria um gráfico de barras com os 5 países com o melhor desempenho.
    coluna = 'aggregate_rating' (nota média) ou 'votes' (média de avaliações)
    Input = Dataframe
    Output = Gráfico de barras
    """
    price_plus = (df1[['price_tye', coluna]].groupby('price_tye')[coluna].mean().sort_values(ascending=False).reset_index().round(2))
    if coluna == 'aggregate_rating':
        y_name = 'Nota média'
    else:
        y_name = 'Média de avaliações recebidas por restaurante'
    fig = px.bar(price_plus, 
                x='price_tye', 
                y=coluna,
                labels={'price_tye': 'País', coluna: y_name})
    fig.update_traces(marker=dict(color='red'))
    fig.update_layout(
        xaxis_title='Países',
        yaxis_title=y_name,
        xaxis_tickangle=-45,
        showlegend=False,
        height=600,
        width=500,
        font_color='white')
    fig.update_traces(hovertemplate='País: %{x}<br>Média: %{y}')
    return fig
##############################


with tab2:  
    with st.container():
        st.markdown('#### Gráficos adicionais')
        '''
A partir das análises realizadas, surgiu uma hipótese para análise e verificou-se a necessidade de analisar os possíveis 
impactos da categoria de preços dos restaurantes
em relação as avaliações dos usuários. Para isso, foram realizados os seguintes passos:

Hipótese: a faixa de preço praticada pelo restaurante influencia no desempenho das avaliações?
- Criação de uma nova coluna no dataframe com categorização de preços baseado no range de valores
- Tratamento dos dados relacionados as avaliações dos usuários
- Criação de dois novos gráficos para análise geral da correlação entre preços e avaliações

'''
    with st.container():
        col1, col2 = st.columns(2, gap='large')
        with col1: #grafico de barras 1/2 color = RED
            st.markdown('##### Média de avaliações recebidas por faixa de preço')
            fig = price_rating(df1, 'votes')
            st.plotly_chart(fig)
        ###
        with col2: #grafico de barras 1/2 color = RED
            st.markdown('##### Nota média por faixa de preço')
            fig = price_rating(df1, 'aggregate_rating')
            st.plotly_chart(fig)
        ###


    with st.container():# Análise da page
        expander = st.expander("Análises relevantes e considerações finais")
        expander.write('''
            Pode-se afirmar que a maioria dos restaurantes estão nas categorias de preços Regular e Alto, onde os restaurantes que trabalham
                       com a faixa de preço Alto possuem melhor nota média (4.22) além de receberem um volume muito maior de avaliações. Destaca-se
                       negativamente a categoria Acessível tanto em quantidade de avaliações recebidas quanto em nota média.

            A partir dessa nova análise gráfica, podemos afirmar que o principal fator de desempenho dos restaurantes é a qualidade de sua comida. Além
            disso podem ser definidas novas hipóteses para a sequência desse Dashboard, considerando relacionar diversos indicadores com a categorização de preços
                       para obter respostas aos problemas de negócio da operação Zomato.
        ''')
        st.markdown(""" --- """)