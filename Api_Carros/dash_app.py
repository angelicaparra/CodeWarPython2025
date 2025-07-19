# dash_app.py

import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import requests
import random
import dash_bootstrap_components as dbc # Importação crucial para 'dbc'

# URL base da sua API FastAPI
FASTAPI_BASE_URL = "http://127.0.0.1:8000"
CARS_LIST_ENDPOINT = f"{FASTAPI_BASE_URL}/api/v1/carros/"
ETL_IMPORT_ENDPOINT = f"{FASTAPI_BASE_URL}/api/v1/carros/etl/importar_carros"


# Inicializa o aplicativo Dash com o tema CYBORG do Bootstrap
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.CYBORG, # Tema escuro e moderno do Bootstrap
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap',
    '/assets/styles.css' # Seu CSS customizado para complementar o tema
])

# Define o layout do aplicativo usando componentes do Bootstrap
app.layout = dbc.Container( # dbc.Container para o layout principal
    fluid=True, # Ocupa toda a largura disponível
    style={'padding': '20px', 'backgroundColor': '#212121'}, # Fundo ligeiramente mais escuro para contraste
    children=[
        html.H1(
            "Dashboard de Análise de Frotas",
            style={
                'textAlign': 'center',
                'marginBottom': '40px',
                'paddingBottom': '15px',
                'borderBottom': '2px solid #343a40', # Cor da borda ajustada para tema escuro
                'color': '#ffffff', # Título branco para tema escuro
                'textShadow': '2px 2px 4px rgba(0,0,0,0.3)' # Sombra no texto do título
            }
        ),

        dbc.Row( # Linha para os botões
            [
                dbc.Col(
                    html.Button(
                        'Atualizar Dados dos Carros',
                        id='refresh-button',
                        n_clicks=0,
                        className='button-style' # Usa a classe do seu CSS externo
                    ),
                    width={"size": 4, "offset": 2}, # Centraliza o botão
                    className="d-flex justify-content-end" # Alinha à direita na coluna
                ),
                dbc.Col(
                    html.Button(
                        'Executar ETL (Importar Carros)',
                        id='etl-button',
                        n_clicks=0,
                        className='etl-button-style' # Usa a classe do seu CSS externo
                    ),
                    width=4,
                    className="d-flex justify-content-start" # Alinha à esquerda na coluna
                ),
            ],
            justify="center", # Centraliza a linha de botões
            className="mb-5" # Margem inferior aumentada
        ),

        html.Div(
            id='etl-message',
            style={'textAlign': 'center', 'marginTop': '10px', 'marginBottom': '40px', 'fontWeight': 'bold', 'fontSize': '1.1em', 'color': '#ffffff'} # Cor da mensagem ajustada, margem aumentada
        ),

        dcc.Store(id='cars-data-store'),

        dbc.Row( # Linha principal para conteúdo (tabela, sugestões, gráficos)
            [
                dbc.Col( # Coluna para a tabela principal
                    dcc.Loading(type="circle", children=[
                        dbc.Card( # Tabela dentro de um Card Bootstrap
                            dbc.CardBody(
                                html.Div(id="cars-table-container")
                            ),
                            className='mb-5', # Margem inferior para separar da próxima linha
                            style={'backgroundColor': '#2c3e50', 'color': '#ffffff', 'border': '1px solid #444'} # Cor de fundo do card, borda sutil
                        )
                    ]),
                    md=12 # Ocupa a largura total em telas médias e maiores
                ),
            ],
            className="mb-0" # Removendo margem extra aqui
        ),

        dbc.Row( # Linha para as sugestões (Marca Favorita e Sugestão do Dia)
            [
                dbc.Col( # Coluna para Seleção de Comparativo
                    dbc.Card( # Card para o seletor e a sugestão dinâmica
                        dbc.CardBody([
                            html.H3("Comparativo de Carros", style={'color': '#007bff', 'marginBottom': '15px'}),
                            dcc.Dropdown(
                                id='comparison-selector',
                                options=[
                                    {'label': 'Marca Favorita', 'value': 'favorite_make'},
                                    {'label': 'Melhor Carro Esportivo', 'value': 'best_sports_car'},
                                    {'label': 'Carro que Gaste Menos', 'value': 'most_fuel_efficient'}
                                ],
                                value='favorite_make', # Valor inicial
                                clearable=False,
                                style={'backgroundColor': '#34495e', 'color': '#ffffff', 'border': 'none', 'marginBottom': '20px'},
                                className='dbc' # Aplica estilos do dbc para dropdown
                            ),
                            html.Div(id='dynamic-car-suggestion') # Conteúdo dinâmico aqui
                        ]),
                        className='mb-5',
                        style={'backgroundColor': '#2c3e50', 'color': '#ffffff', 'border': '1px solid #444'}
                    ),
                    md=6
                ),
                dbc.Col( # Coluna para Sugestão do Dia
                    dbc.Card( # Sugestão do Dia dentro de um Card Bootstrap
                        dbc.CardBody(
                            html.Div(id='daily-car-suggestion')
                        ),
                        className='mb-5',
                        style={'backgroundColor': '#2c3e50', 'color': '#ffffff', 'border': '1px solid #444'}
                    ),
                    md=6
                ),
            ],
            className="mb-0"
        ),

        dbc.Row( # Linha para os gráficos
            [
                dbc.Col( # Coluna para o gráfico de Carros por Marca
                    dbc.Card( # Gráfico dentro de um Card Bootstrap
                        dbc.CardBody(
                            dcc.Graph(id='cars-by-make-graph')
                        ),
                        className='mb-5',
                        style={'backgroundColor': '#2c3e50', 'color': '#ffffff', 'border': '1px solid #444'}
                    ),
                    md=6
                ),
                dbc.Col( # Coluna para o gráfico de Distribuição de Anos
                    dbc.Card( # Gráfico dentro de um Card Bootstrap
                        dbc.CardBody(
                            dcc.Graph(id='cars-by-year-graph')
                        ),
                        className='mb-5',
                        style={'backgroundColor': '#2c3e50', 'color': '#ffffff', 'border': '1px solid #444'}
                    ),
                    md=6
                ),
            ],
            className="mb-0"
        ),

        html.Div(
            id='error-message',
            style={'color': '#dc3545', 'textAlign': 'center', 'marginTop': '20px', 'fontWeight': 'bold', 'fontSize': '1.1em'}
        ),

        html.Footer(
            html.Div(
                "Dashboard de Análise de Frotas © 2024",
                style={"text-align": "center", "margin-top": "50px", "padding": "20px", "color": "#adb5bd", "font-size": "14px", "border-top": "1px solid #343a40"}
            )
        )
    ]
)

# --- Funções Auxiliares para os Comparativos ---
def _format_car_details(car_data, title_color):
    """Formata os detalhes de um carro para exibição."""
    if not car_data:
        return html.Div([
            html.H3("N/A", style={'color': title_color}),
            html.P("Nenhum dado disponível para esta categoria.", style={'color': '#adb5bd'})
        ])

    return html.Div([
        html.H3(car_data.get('title', 'Detalhes do Carro'), style={'color': title_color}),
        html.P(["Marca: ", html.Strong(car_data.get('marca', 'N/A'))], style={'marginBottom': '5px', 'color': '#adb5bd'}),
        html.P(["Modelo: ", html.Strong(car_data.get('modelo', 'N/A'))], style={'marginBottom': '5px', 'color': '#adb5bd'}),
        html.P(f"Ano: {car_data.get('ano', 'N/A')}", style={'color': '#adb5bd'}),
        html.P(f"Quilometragem: {car_data.get('quilometragem', 'N/A')} km", style={'color': '#adb5bd'}),
        html.P(f"Cor: {car_data.get('cor', 'N/A')}", style={'color': '#adb5bd'}),
        html.P(f"Combustível: {car_data.get('tipo_combustivel', 'N/A')}", style={'color': '#adb5bd'}),
        html.P(f"Potência (HP): {car_data.get('horsepower', 'N/A')}", style={'color': '#adb5bd'}) # Adiciona potência
    ])

def _get_favorite_make_details(df):
    """Identifica e retorna a marca favorita."""
    if df.empty or 'marca' not in df.columns:
        return None

    favorite_make = df['marca'].mode().iloc[0]
    count = df['marca'].value_counts()[favorite_make]
    return {
        'title': 'Marca Favorita',
        'marca': favorite_make,
        'modelo': f"Total: {count} veículos", # Adapta para mostrar a contagem
        'ano': '', 'quilometragem': '', 'cor': '', 'tipo_combustivel': '', 'horsepower': ''
    }

def _get_best_sports_car_details(df):
    """Identifica e retorna o melhor carro esportivo (maior horsepower)."""
    if df.empty or 'horsepower' not in df.columns:
        return None

    # Converte 'horsepower' para numérico, tratando valores ausentes
    df_temp = df.copy()
    df_temp['horsepower'] = pd.to_numeric(df_temp['horsepower'], errors='coerce')
    df_temp.dropna(subset=['horsepower'], inplace=True)

    if df_temp.empty:
        return None

    # Ordena por horsepower (desc) e ano (desc) para desempate
    best_car = df_temp.sort_values(by=['horsepower', 'ano'], ascending=[False, False]).iloc[0]
    best_car_dict = best_car.to_dict()
    best_car_dict['title'] = 'Melhor Carro Esportivo'
    return best_car_dict

def _get_most_fuel_efficient_car_details(df):
    """Identifica e retorna o carro que gasta menos (baseado em tipo_combustivel)."""
    if df.empty or 'tipo_combustivel' not in df.columns:
        return None

    # Define uma ordem de eficiência (exemplo simplificado)
    fuel_efficiency_order = {
        'electric': 1,
        'hybrid': 2,
        'gasoline': 3,
        'petrol': 3, # Assumindo petrol é o mesmo que gasoline
        'diesel': 4,
        'flex': 3, # Flex pode ser considerado como gasoline/petrol para esta simplificação
        None: 99, # Coloca None por último
        'N/A': 99 # Coloca N/A por último
    }

    df_temp = df.copy()
    df_temp['efficiency_rank'] = df_temp['tipo_combustivel'].apply(lambda x: fuel_efficiency_order.get(str(x).lower(), 99))
    df_temp.dropna(subset=['efficiency_rank'], inplace=True)

    if df_temp.empty:
        return None

    # Ordena por rank de eficiência (asc) e ano (desc) para desempate
    most_efficient_car = df_temp.sort_values(by=['efficiency_rank', 'ano'], ascending=[True, False]).iloc[0]
    most_efficient_car_dict = most_efficient_car.to_dict()
    most_efficient_car_dict['title'] = 'Carro que Gaste Menos'
    return most_efficient_car_dict

# --- Callbacks ---

# Callback para buscar dados da API e armazená-los no dcc.Store
@app.callback(
    Output('cars-data-store', 'data'),
    Output('error-message', 'children'),
    Input('refresh-button', 'n_clicks')
)
def fetch_cars_data(n_clicks):
    """
    Função de callback para buscar dados da API e armazená-los no dcc.Store.
    """
    try:
        response = requests.get(CARS_LIST_ENDPOINT)
        response.raise_for_status()
        cars_data_response = response.json()
        cars_data = cars_data_response.get('cars', [])
        return cars_data, ""
    except requests.exceptions.ConnectionError:
        return [], "Erro: Não foi possível conectar à API FastAPI. Certifique-se de que ela está rodando."
    except requests.exceptions.RequestException as e:
        return [], f"Erro ao buscar dados da API: {e}"
    except Exception as e:
        return [], f"Ocorreu um erro inesperado ao buscar dados: {e}"

# Callback para atualizar a tabela com base nos dados do dcc.Store
@app.callback(
    Output('cars-table-container', 'children'),
    Input('cars-data-store', 'data')
)
def update_cars_table(data):
    """
    Função de callback para renderizar a tabela com base nos dados armazenados.
    """
    if not data:
        return html.Div("Nenhum dado de carro encontrado na API. Tente executar o ETL para importar alguns.",
                        style={'textAlign': 'center', 'marginTop': '20px', 'color': '#adb5bd'})

    df = pd.DataFrame(data)

    table_fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(df.columns),
            fill_color='#007bff', # Cor de cabeçalho da tabela
            align='left',
            font=dict(color='white', size=14),
            height=40
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            fill_color='#495057', # Cor de fundo das células ajustada para tema escuro
            align='left',
            font=dict(color='#ffffff', size=12), # Cor do texto da célula ajustada
            height=30
        )
    )])

    table_fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    return dcc.Graph(figure=table_fig)

# Callback para gerar o gráfico de carros por marca
@app.callback(
    Output('cars-by-make-graph', 'figure'),
    Input('cars-data-store', 'data')
)
def update_cars_by_make_graph(data):
    """
    Gera um gráfico de barras mostrando a contagem de carros por marca.
    """
    if not data:
        return go.Figure(layout=go.Layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'))

    df = pd.DataFrame(data)
    if 'marca' not in df.columns:
        return go.Figure(layout=go.Layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'))

    make_counts = df['marca'].value_counts().reset_index()
    make_counts.columns = ['Marca', 'Quantidade']
    fig = px.bar(
        make_counts,
        x='Marca',
        y='Quantidade',
        title='Carros por Marca',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template="plotly_dark"
    )
    return fig

# Callback para gerar o gráfico de distribuição de anos
@app.callback(
    Output('cars-by-year-graph', 'figure'),
    Input('cars-data-store', 'data')
)
def update_cars_by_year_graph(data):
    """
    Gera um histograma mostrando a distribuição de anos dos carros.
    """
    if not data:
        return go.Figure(layout=go.Layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'))

    df = pd.DataFrame(data)
    if 'ano' not in df.columns:
        return go.Figure(layout=go.Layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'))

    fig = px.histogram(
        df,
        x='ano',
        nbins=len(df['ano'].unique()) if len(df['ano'].unique()) < 20 else 20,
        title='Distribuição de Carros por Ano',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Número de Carros",
        margin={"r":0,"t":40,"l":0,"b":0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template="plotly_dark"
    )
    return fig


# Callback para exibir a sugestão dinâmica (Marca Favorita, Esportivo, Econômico)
@app.callback(
    Output('dynamic-car-suggestion', 'children'), # Onde a sugestão será exibida
    Input('cars-data-store', 'data'),
    Input('comparison-selector', 'value') # Nova entrada do dropdown
)
def display_dynamic_car_suggestion(data, selected_comparison):
    """
    Exibe a sugestão de carro baseada na seleção do dropdown.
    """
    if not data:
        return html.Div([
            html.H3("Comparativo", style={'color': '#007bff'}),
            html.P("Nenhum dado disponível para comparativos.", style={'color': '#adb5bd'})
        ])

    df = pd.DataFrame(data)
    if df.empty:
        return html.Div([
            html.H3("Comparativo", style={'color': '#007bff'}),
            html.P("Nenhum carro disponível para comparativos.", style={'color': '#adb5bd'})
        ])

    car_details = None
    title_color = '#007bff' # Cor padrão para o título do card

    if selected_comparison == 'favorite_make':
        car_details = _get_favorite_make_details(df)
        title_color = '#007bff'
    elif selected_comparison == 'best_sports_car':
        car_details = _get_best_sports_car_details(df)
        title_color = '#ffc107' # Amarelo para esportivo
    elif selected_comparison == 'most_fuel_efficient':
        car_details = _get_most_fuel_efficient_car_details(df)
        title_color = '#17a2b8' # Azul ciano para econômico

    return _format_car_details(car_details, title_color)


# Callback para exibir a "Sugestão do Dia" (carro aleatório)
@app.callback(
    Output('daily-car-suggestion', 'children'),
    Input('cars-data-store', 'data')
)
def display_daily_car_suggestion(data):
    """
    Seleciona e exibe uma "Sugestão do Dia" (carro aleatório).
    """
    if not data:
        return html.Div([
            html.H3("Sugestão do Dia", style={'color': '#28a745'}),
            html.P("Nenhum dado disponível para sugestão.", style={'color': '#adb5bd'})
        ])

    df = pd.DataFrame(data)
    if df.empty:
        return html.Div([
            html.H3("Sugestão do Dia", style={'color': '#28a745'}),
            html.P("Nenhum carro disponível para sugestão.", style={'color': '#adb5bd'})
        ])

    random_car = df.sample(1).iloc[0]
    random_car_dict = random_car.to_dict()
    random_car_dict['title'] = 'Sugestão do Dia' # Adiciona um título para a função de formatação

    return _format_car_details(random_car_dict, '#28a745')


# Callback para executar a função ETL
@app.callback(
    Output('etl-message', 'children'),
    Output('refresh-button', 'n_clicks'),
    Input('etl-button', 'n_clicks'),
    State('refresh-button', 'n_clicks')
)
def run_etl_process(etl_clicks, current_refresh_clicks):
    """
    Função de callback que é acionada quando o botão 'Executar ETL' é clicado.
    Ela faz uma requisição POST para o endpoint ETL da sua API.
    """
    if etl_clicks > 0:
        try:
            response = requests.post(ETL_IMPORT_ENDPOINT)
            response.raise_for_status()

            etl_result = response.json()
            imported_count = etl_result.get('importados', 0)
            imported_models = etl_result.get('modelos', [])

            message = f"ETL concluído! {imported_count} carros importados. Modelos: {', '.join(imported_models) if imported_models else 'Nenhum novo carro importado.'}"
            message_style = {'color': '#28a745'} # Cor verde para tema escuro

            return html.Div(message, style=message_style), current_refresh_clicks + 1

        except requests.exceptions.ConnectionError:
            return html.Div("Erro ETL: Não foi possível conectar à API FastAPI.", style={'color': '#dc3545'}), current_refresh_clicks # Cor vermelha para tema escuro
        except requests.exceptions.RequestException as e:
            error_detail = e.response.json().get('detail', str(e)) if e.response else str(e)
            return html.Div(f"Erro ETL ao importar dados: {error_detail}", style={'color': '#dc3545'}), current_refresh_clicks
        except Exception as e:
            return html.Div(f"Ocorreu um erro inesperado durante o ETL: {e}", style={'color': '#dc3545'}), current_refresh_clicks
    return "", current_refresh_clicks


# Executa o servidor Dash
if __name__ == '__main__':
    app.run(debug=True)
