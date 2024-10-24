README

Apresentação da operação Zomato:
A Zomato, fundada em 2008, é uma plataforma tecnológica indiana de entrega de comida e descoberta de restaurantes. A empresa cresceu rapidamente e se tornou uma das maiores plataformas de delivery do mundo, operando em diversos países. O modelo de negócio da Zomato funciona como um marketplace, conectando clientes a restaurantes através de seu aplicativo e site, onde os usuários podem visualizar menus, avaliações, fotos e informações detalhadas sobre restaurantes, além de fazer pedidos para entrega ou reservas.

Problema de negócio:
Um novo profissional foi contratado para o cargo de CEO da empresa e precisa vizualizar alguns pontos chave da operação atual da empresa para entender melhor quais decisões estratégicas precisam ser tomadas de forma breve. Para isso ele necessita que seja elaborada uma analise de dados da Zomato através de dashboards, para que, a partir dessas análises, as seguintes perguntas possam ser respondidas de forma segmentada:

Países:
- Quantos países estão em operação?
- Como as cidades e restaurantes estão distribuidos nos países em operação?
- Qual o desempenho médio dos restaurantes por país, de acordo com a avaliação dos clientes?
- Gráficos de vizualização de indicadores

Cidades:
- Quantas cidades estão em operação?
- Qual a cidade com mais restaurantes cadastrados?
- Quais as cidades com melhor e pior avaliação?
- Quais são as cidades que possui maior variedade gastronômica?

Restaurantes:
- De qual forma os restaurantes estão distribuidos mundialmente?
- Quantos restaurantes estão cadastrados?
- Quais restaurantes se destacam de forma positiva e negativa de acordo com as avaliações?
- Como o serviço de entregas influencia nas avaliações?
- Como o serviço de reservas influencia nas avaliações?
- Quais restaurantes, por país, se destacam de acordo com as notas recebidas?

Premissas do Negócio:
1. A análise foi realizada com dados disponibilizados (de forma pública em https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv) até 04/10/2024.
2. Marketplace foi o modelo de negócio assumido.
3. Os 3 principais visões do negócio foram: Visão global (Países), visão local (Cidades) e visão conveniados (Restaurantes).

Estratégias da solução:
Visão países:
- Métricas gerais relativas aos países em operação
- Indicadores de desempenho médio dos restaurantes por país
- Gráficos de vizualização de indicadores

Visão cidades:
- Métricas gerais relativas as cidades em operação
- Indicadores de desempenho médio dos restaurantes por cidade
- Gráficos de vizualização de indicadores

Visão restaurantes:
- Indicadores de desempenho dos restaurantes
- Mapa de geolocalização de todos os restaurantes cadastados
- Gráficos de comparação entre restaurantes com opção delivery e reserva

Top 3 análises observadas no dashboard:
Países:
1. Dominância da Índia e Expansão Global
2. Destaque para Indonésia nos indicadores de avaliação
3. Diversidade de países em relação aos indices de avaliação

Cidades:
1. Concentração geográfica e diversidade culinária
2. Qualidade e volume de avaliações
3. Mercado amadurecido e oportunidades

Restaurantes:
1. Impacto dos serviços adicionais
2. Liderança da Domino´s Pizza e concentração geográfica
3. Correlação entre os serviços adicionais e qualidade percebida

Top 3 insights de dados para cada visão:
Países:
1. Análise temporal da expansão internacional:
2.Estudo dos fatores de sucesso na Indonésia
3. Análise comparativa Indonésia-Austrália

Cidades:
1. Identificar possíveis barreiras para expansão do serviço de entregas em outras localidades
2. Estudo da diversidade culinária
3. Aprofundamento do caso Londres

Restaurantes:
1. Análise aprofundada do serviço de delivery
2. Estudo do sistema de reservas
3. Aprofundamento do caso Domino's Pizza

O Produto Final do Projeto:
Um dashboard interativo que permite analisar as métricas de crescimento da Zomato em diferentes níveis (países, cidades e restaurantes). O dashboard oferece visualizações intuitivas, como mapas, gráficos de linha e barras, facilitando a identificação de padrões e tendências. Painel online hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet. O dashboard pode ser acessado através do link: https://dashboardzomato.streamlit.app

Conclusão:
A análise dos dados da Zomato permitiu obter insights valiosos sobre o crescimento da empresa e identificar oportunidades de melhoria. O dashboard desenvolvido é uma ferramenta poderosa para acompanhar o desempenho da empresa e tomar decisões estratégicas. Além disso, a partir das novas análises realizadas de forma adicional, é possível afirmar que o principal fator de desempenho dos restaurantes é a qualidade de sua comida. 

Próximos Passos:
- Aprofundar a análise: Realizar análises mais detalhadas sobre os fatores que influenciam a satisfação do cliente, como a qualidade da comida, o tempo de entrega e o atendimento.
- Incorporar novos dados: Integrar dados de outros banco de dados da empresa, como redes sociais e pesquisas de satisfação do cliente, para enriquecer a análise.
- Desenvolver modelos preditivos: Utilizar técnicas de machine learning para prever o desempenho futuro da empresa e identificar novas oportunidades de negócios.
- Monitoramento contínuo: Implementar um processo de monitoramento contínuo do dashboard para acompanhar as mudanças nas métricas e identificar desvios em relação aos objetivos.
