import streamlit as st
from PIL import Image
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

#image_path = 'logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=240)

st.sidebar.markdown('### Food Delivery & Dining')
st.sidebar.markdown(""" --- """)

st.header('Zomato - Food Delivery & Dining')

st.sidebar.markdown('###### Powered by William Cardoso')

st.markdown(
    """
    A Zomato, fundada em 2008, é uma plataforma tecnológica indiana de entrega de comida e descoberta de restaurantes.
     A empresa cresceu rapidamente e se tornou uma das maiores plataformas de delivery do mundo, operando em diversos países. 
     O modelo de negócio da Zomato funciona como um marketplace, conectando clientes a restaurantes através de seu aplicativo e site, 
     onde os usuários podem visualizar menus, avaliações, fotos e informações detalhadas sobre restaurantes, 
     além de fazer pedidos para entrega ou reservas.

    Esse growth dashboard foi construído para acompanhar as métricas de crescimento da operação Zomato, através de dados públicos disponíveis 
    em [Kaggle.com](https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv).

    ### Como utilizar esse Growth Dashboard?
    - Visão países:
        - Métricas gerais relativas aos países em operação
        - Indicadores de desempenho médio dos restaurantes por país
        - Gráficos de vizualização de indicadores
    - Visão cidades:
        - Métricas gerais relativas as cidades em operação
        - Indicadores de desempenho médio dos restaurantes por cidade
        - Gráficos de vizualização de indicadores
    - Visão Restaurantes:
        - Indicadores de desempenho dos restaurantes
        - Mapa de geolocalização de todos os restaurantes cadastados
        - Gráficos de comparação entre restaurantes com opção delivery e reserva
    - Insights:
        - Percepções geradas a partir da análise dos indicadores, gráficos e mapas
        - Novas análises criadas através de hipóteses de negócio
        - Considerações finais

    ### Ask for Help
    - [👩‍💻 Desenvolvedor](https://github.com/wcardosoecom) = William Cardoso
    
        
        """
)