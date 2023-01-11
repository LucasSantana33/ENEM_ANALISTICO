
from dash import Dash, html, dcc,Input, Output
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

app = Dash(__name__)
server = app.server
app.head = [html.Link(rel='stylesheet', href='style.css')]

dfAtt = pd.read_parquet("ENEM_2017_2021.parquet")
# grafico de linha estático
sexo = 'M'
estado = 'SP'
raca = 1
escola=3
sexo2 = 'F'
estado2 = 'BA'
raca2 = 2
escola2=2
materia = 'NU_NOTA_MT'
if (materia =='NU_NOTA_MT'):
    disciplina = 'Matemática'
grupo1_anos = dfAtt.query("SG_UF_PROVA == @estado & TP_SEXO == @sexo & TP_ESCOLA_ATT == @escola & TP_COR_RACA == @raca")
AGRUPADOS_1 = grupo1_anos.groupby(['NU_ANO']).mean().round(2)
AGRUPADOS_1.rename({materia : 'grupo_1'},axis=1,inplace=True)
grupo2_anos = dfAtt.query("SG_UF_PROVA == @estado2 & TP_SEXO == @sexo2 & TP_ESCOLA_ATT == @escola2 & TP_COR_RACA == @raca2")
AGRUPADOS_2 = grupo2_anos.groupby(['NU_ANO']).mean().round(2)
AGRUPADOS_2.rename({materia : 'grupo_2'},axis=1,inplace=True)
geral= pd.concat([AGRUPADOS_1,AGRUPADOS_2],axis=1)
df = geral[['grupo_1','grupo_2']]
df.reset_index(inplace=True)

figura = make_subplots(rows=1, cols=1)

figura.add_trace(
    go.Scatter(x=df['NU_ANO'],y=df['grupo_1'],name = 'Grupo 1'),
    row=1, col=1
)

figura.add_trace(
    go.Scatter(x=df['NU_ANO'],y=df['grupo_2'],name = 'Grupo 2'),
    row=1, col=1
)

figura.update_layout(title={
    'text' :f'Médias de {disciplina} por ano<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><sup>N° de alunos do grupo 1: {grupo1_anos.shape[0]} X</sup><sup> N° de alunos do grupo 2: {grupo2_anos.shape[0]}</sup>',
    'y': 0.93,
    'x': 0.5
},
yaxis_title='nota',
plot_bgcolor = '#efefef',
font = {'family': 'Arial','size': 14.55,'color': 'black'},
colorway=['#32A69D', "#18524D", "#5B696B"], legend_orientation="h",
legend=dict(x = 0.222, y=1.2), height = 455, width = 505)
figura.update_xaxes( showgrid=True, gridwidth=1, gridcolor='lightgray',showline=True, linewidth=1, linecolor='black',dtick=1)
figura.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray',showline=True, linewidth=1, linecolor='black')
################################################################################################################################
# boxplot estático
opcoes_uf = list(dfAtt['SG_UF_PROVA'].unique())
sexo = 'M'
estado = 'SP'
raca = 1
escola= 3
ano = 2021
sexo2 = 'F'
estado2 = 'BA'
raca2 = 2
escola2=2
grupo1 = dfAtt.query("NU_ANO == @ano & SG_UF_PROVA == @estado & TP_SEXO == @sexo & TP_ESCOLA_ATT == @escola & TP_COR_RACA == @raca")
grupo2 = dfAtt.query("NU_ANO == @ano & SG_UF_PROVA == @estado2 & TP_SEXO == @sexo2 & TP_ESCOLA_ATT == @escola2 & TP_COR_RACA == @raca2")

fig = make_subplots(rows=1, cols=1)
fig.add_trace(
    go.Box(y=grupo1[materia],name = 'Grupo 1'),
    row=1, col=1
)

fig.add_trace(
    go.Box(y=grupo2[materia],name = 'Grupo 2'),
    row=1, col=1
)
fig.update_layout(title={
    'text' :f'Análise das notas de {disciplina} do ano de {ano}<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><sup>N° de alunos do grupo 1: {grupo1.shape[0]} X</sup><sup> N° de alunos do grupo 2: {grupo2.shape[0]}</sup>',
    'y': 0.93,
    'x': 0.5
},
yaxis_title='nota',
plot_bgcolor = '#efefef',
font = {'family': 'Arial','size': 14.55,'color': 'black'},
colorway=['#32A69D', "#18524D", "#5B696B"], legend_orientation="h",
legend=dict(x = 0.222, y=1.2), height = 455, width = 505)
fig.update_xaxes( showgrid=True, gridwidth=1, gridcolor='lightgray',showline=True, linewidth=1, linecolor='black')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray',showline=True, linewidth=1, linecolor='black')
################################################################################################################################
# HTML do dashboard
app.layout = html.Div(
        [
            html.Header(
                html.H1('ENEM')
            ),
            html.Div(
                id = "menu",
                children=[
                    html.Div(
                        id = "menu1",
                        children=[
                            html.Label('Escolha um Ano:'),
                            html.Br(),
                            dcc.Dropdown(
                                id="ano_1",
                                options=[
                                    {'label': 2017, 'value': 2017},
                                    {'label': 2018, 'value': 2018},
                                    {'label': 2019, 'value': 2019},
                                    {'label': 2020, 'value': 2020},
                                    {'label': 2021, 'value': 2021}
                                ],
                                value=2021
                            ),
                            html.Br(),
                            html.Label('Escolha uma matéria:'),
                            dcc.Dropdown(
                                id="dropdown",
                                options=[
                                    {'label': 'Matemática', 'value': 'NU_NOTA_MT'},
                                    {'label': 'Linguagens', 'value': 'NU_NOTA_LC'},
                                    {'label': 'Humanas', 'value': 'NU_NOTA_CH'},
                                    {'label': 'Naturezas', 'value': 'NU_NOTA_CN'},
                                    {'label': 'Redação', 'value': 'NU_NOTA_REDACAO'}
                                ],
                                value='NU_NOTA_MT'
                            ),
                            html.Br(),
                            html.H2('Grupo 1'),
                            html.Br(),
                            html.Label('Selecione o Estado do grupo 1:'),
                            html.Br(),
                            dcc.Dropdown(
                                opcoes_uf,
                                value='SP',
                                id='lista_uf'
                            ),
                            html.Br(),
                            html.Label('Selecione a etnia do grupo 1:'),
                            html.Br(),
                            dcc.Checklist(
                                id="tip_raca",
                                options=[
                                    {'label': 'Branca', 'value': 1},
                                    {'label': 'Preta', 'value': 2},
                                    {'label': 'Parda', 'value': 3},
                                    {'label': 'Amarela', 'value': 4},
                                    {'label': 'Indígena', 'value': 5}
                                ],
                                value= [1],
                              
                            ),
                            html.Br(),
                            html.Label('Selecione o sexo do grupo 1:'),
                            html.Br(),
                            dcc.RadioItems(
                                id="dropdown_gen",
                                options=[
                                    {'label': 'Masculino', 'value': 'M'},
                                    {'label': 'Feminino', 'value': 'F'},
                                    {'label': 'Todos', 'value': 'MF'}
                                ],
                                value='M'
                            ),
                            html.Br(),
                            html.Label('Selecione o tipo de escola do grupo 1:'),
                            html.Br(),
                            dcc.RadioItems(
                                id="tip_escola",
                                options=[
                                    {'label': 'Pública', 'value': 2},
                                    {'label': 'Privada', 'value': 3},
                                    {'label': 'Todas', 'value': 14}
                                ],
                                value= 3
                            ),
                        ]
                    ),
                    html.Div(
                        id = "menu2",
                        children=[
                            html.H2('Grupo 2'),
                            html.Br(),
                            html.Label('Selecione o Estado do grupo 2:'),
                            html.Br(),
                            dcc.Dropdown(
                                opcoes_uf,
                                value='BA',
                                id='lista_uff'
                            ),
                            html.Br(),
                            html.Label('Selecione a etnia do grupo 2:'),
                            dcc.Checklist(
                                id="tip_racaa",
                                options=[
                                    {'label': 'Branca', 'value': 1},
                                    {'label': 'Preta', 'value': 2},
                                    {'label': 'Parda', 'value': 3},
                                    {'label': 'Amarela', 'value': 4},
                                    {'label': 'Indígena', 'value': 5}
                                ],
                                value=[2,3]
                            ),
                            html.Br(),
                            html.Label('Selecione o sexo do grupo 2:'),
                            html.Br(),
                            dcc.RadioItems(
                                id="dropdown_genn",
                                options=[
                                    {'label': 'Masculino', 'value': 'M'},
                                    {'label': 'Feminino', 'value': 'F'},
                                    {'label': 'Todos', 'value': 'MF'}
                                ],
                                value='F'
                            ),
                            html.Br(),
                            html.Label('Selecione o tipo de escola do grupo 2:'),
                            html.Br(),
                            dcc.RadioItems(
                                id="tip_escolaa",
                                options=[
                                    {'label': 'Pública', 'value': 2},
                                    {'label': 'Privada', 'value': 3},
                                    {'label': 'Todas', 'value': 14},
                                    
                                    
                                ],
                                value= 2
                            )
                        ]
                    ),
                ]
            ),
            html.Div(
                id = "graficos",
                children=[
                    html.Div(
                        dcc.Graph(
                            id='example_graph',
                            figure=fig
                        ),
                        id = "grafico1"
                    ),
                    html.Div(
                        dcc.Graph(
                            id='example_graphh',
                            figure=figura
                        ),
                        id = "grafico2"
                    )
                ]
            ),
            html.Footer(
                html.P('Desenvolvido pela turma de Probabilidade e Estatística do curso de Sistemas de Informação do CEFET/RJ Maria da Graça no período de 2022.2')
            )
        ],
        id = "tudo"
    )



@app.callback(
    Output('example_graph', 'figure'),
    Output('example_graphh', 'figure'),
    Input('dropdown', 'value'),
    Input('dropdown_gen', 'value'),
    Input('tip_escola', 'value'),
    Input('ano_1', 'value'),
    Input('lista_uf', 'value'),
    Input('tip_raca', 'value'),
    Input('lista_uff','value'),
    Input('dropdown_genn', 'value'),
    Input('tip_escolaa', 'value'),
    Input('tip_racaa', 'value'),
    
)
#Função que faz os filtros conforme o usuário interage no dashboard
def pegavalorBox(dropdown,dropdown_gen,tip_escola,ano_1,lista_uf,tip_raca,lista_uff,dropdown_genn,tip_escolaa,tip_racaa):  
    while (tip_escolaa ==14 and dropdown_genn == 'MF'):
        grupo2 = dfAtt.query("NU_ANO == @ano_1 & SG_UF_PROVA == @lista_uff & TP_COR_RACA  == @tip_racaa")
        break     
    while (tip_escolaa ==14 and dropdown_genn!='MF'):
        grupo2 = dfAtt.query("NU_ANO == @ano_1 & SG_UF_PROVA == @lista_uff & TP_SEXO == @dropdown_genn & TP_COR_RACA == @tip_racaa")
        break   
    while (tip_escolaa !=14 and dropdown_genn!='MF'):
        grupo2 = dfAtt.query("NU_ANO == @ano_1 & SG_UF_PROVA == @lista_uff & TP_SEXO == @dropdown_genn & TP_ESCOLA_ATT == @tip_escolaa & TP_COR_RACA == @tip_racaa")
        break
    while (tip_escolaa !=14 and dropdown_genn == 'MF'):
        grupo2 = dfAtt.query("NU_ANO == @ano_1 & SG_UF_PROVA == @lista_uff & TP_ESCOLA_ATT == @tip_escolaa & TP_COR_RACA == @tip_racaa")
        break
    ######################################################################################################################################################################################################### 
    while (tip_escola ==14 and dropdown_gen == 'MF'):
        grupo1 = dfAtt.query("NU_ANO == @ano_1 & SG_UF_PROVA == @lista_uf & TP_COR_RACA  == @tip_raca") 
        break
    while (tip_escola ==14 and dropdown_gen!='MF'):
        grupo1 = dfAtt.query("NU_ANO == @ano_1 & SG_UF_PROVA == @lista_uf & TP_SEXO == @dropdown_gen & TP_COR_RACA == @tip_raca")
        break
    while (tip_escola !=14 and dropdown_gen!='MF'):
        grupo1 = dfAtt.query("NU_ANO == @ano_1 & SG_UF_PROVA == @lista_uf & TP_SEXO == @dropdown_gen & TP_ESCOLA_ATT == @tip_escola & TP_COR_RACA == @tip_raca")
        break
    while (tip_escola !=14 and dropdown_gen == 'MF'):
        grupo1 = dfAtt.query("NU_ANO == @ano_1 & SG_UF_PROVA == @lista_uf & TP_ESCOLA_ATT == @tip_escola & TP_COR_RACA == @tip_raca")
        break
    if (dropdown =='NU_NOTA_REDACAO'):
        disciplina = 'Redação'
    elif (dropdown =='NU_NOTA_MT'):
        disciplina = 'Matemática'
    elif (dropdown =='NU_NOTA_CH'):
        disciplina = 'Humanas'
    elif (dropdown =='NU_NOTA_CN'):
        disciplina = 'Naturezas'
    else:
        disciplina = 'Linguagens'
        
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(
        go.Box(y=grupo1[dropdown],name = 'Grupo 1'),
        row=1, col=1
    )

    fig.add_trace(
        go.Box(y=grupo2[dropdown],name = 'Grupo 2'),
        row=1, col=1
    )
    fig.update_layout(title={
    'text' :f'Análise das notas de {disciplina} do ano de {ano_1}<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><sup>N° de alunos do grupo 1: {grupo1.shape[0]} X</sup><sup> N° de alunos do grupo 2: {grupo2.shape[0]}</sup>',
    'y': 0.93,
    'x': 0.5
},
    yaxis_title='nota',
    plot_bgcolor = '#efefef',
    font = {'family': 'Poppins','size': 14.55,'color': 'black'},
    colorway=['#32A69D', "#18524D", "#5B696B"], legend_orientation="h",
    legend=dict(x = 0.222, y=1.2), height = 455, width = 505)
    fig.update_xaxes( showgrid=True, gridwidth=1, gridcolor='lightgray',showline=True, linewidth=1, linecolor='black')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray',showline=True, linewidth=1, linecolor='black')
    
    while (tip_escolaa ==14 and dropdown_genn == 'MF'):
        grupo2_anos = dfAtt.query("SG_UF_PROVA == @lista_uff & TP_COR_RACA  == @tip_racaa") 
        break
    while (tip_escolaa ==14 and dropdown_genn!='MF'):
        grupo2_anos = dfAtt.query("SG_UF_PROVA == @lista_uff & TP_SEXO == @dropdown_genn & TP_COR_RACA == @tip_racaa")
        break
    while (tip_escolaa !=14 and dropdown_genn!='MF'):
        grupo2_anos = dfAtt.query("SG_UF_PROVA == @lista_uff & TP_SEXO == @dropdown_genn & TP_ESCOLA_ATT == @tip_escolaa & TP_COR_RACA == @tip_racaa")
        break
    while (tip_escolaa !=14 and dropdown_genn == 'MF'):
        grupo2_anos = dfAtt.query("SG_UF_PROVA == @lista_uff & TP_ESCOLA_ATT == @tip_escolaa & TP_COR_RACA == @tip_racaa")
        break
    ##################################################################################################################################################
    while (tip_escola ==14 and dropdown_gen == 'MF'):
        grupo1_anos = dfAtt.query("SG_UF_PROVA == @lista_uf & TP_COR_RACA  == @tip_raca") 
        break
    while (tip_escola ==14 and dropdown_gen!='MF'):
        grupo1_anos = dfAtt.query("SG_UF_PROVA == @lista_uf & TP_SEXO == @dropdown_gen & TP_COR_RACA == @tip_raca")
        break
    while (tip_escola !=14 and dropdown_gen!='MF'):
        grupo1_anos = dfAtt.query("SG_UF_PROVA == @lista_uf & TP_SEXO == @dropdown_gen & TP_ESCOLA_ATT == @tip_escola & TP_COR_RACA == @tip_raca")
        break
    while (tip_escola !=14 and dropdown_gen == 'MF'):
        grupo1_anos = dfAtt.query("SG_UF_PROVA == @lista_uf & TP_ESCOLA_ATT == @tip_escola & TP_COR_RACA == @tip_raca")
        break
    AGRUPADOS_1 = grupo1_anos.groupby(['NU_ANO']).mean().round(2)
    AGRUPADOS_1.rename({dropdown : 'grupo_1'},axis=1,inplace=True)
    AGRUPADOS_2 = grupo2_anos.groupby(['NU_ANO']).mean().round(2)
    AGRUPADOS_2.rename({dropdown : 'grupo_2'},axis=1,inplace=True)
    geral= pd.concat([AGRUPADOS_1,AGRUPADOS_2],axis=1)
    df = geral[['grupo_1','grupo_2']]
    df.reset_index(inplace=True)
    figura = make_subplots(rows=1, cols=1)
    figura.add_trace(
        go.Scatter(x=df['NU_ANO'],y=df['grupo_1'],name = 'Grupo 1'),
        row=1, col=1
    )

    figura.add_trace(
        go.Scatter(x=df['NU_ANO'],y=df['grupo_2'],name = 'Grupo 2'),
        row=1, col=1
    )
    figura.update_layout(title={
    'text' :f'Médias de {disciplina} por ano<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><sup>N° de alunos do grupo 1: {grupo1_anos.shape[0]} X</sup><sup> N° de alunos do grupo 2: {grupo2_anos.shape[0]}</sup>',
    'y': 0.93,
    'x': 0.5
},
    #xaxis_title='ano',
    yaxis_title='nota',
    plot_bgcolor = '#efefef',
    font = {'family': 'Poppins','size': 14.55,'color': 'black'},
    colorway=['#32A69D', "#18524D", "#5B696B"], legend_orientation="h",
    legend=dict(x = 0.222, y=1.2), height = 455, width = 505)
    figura.update_xaxes( showgrid=True, gridwidth=1, gridcolor='lightgray',showline=True, linewidth=1, linecolor='black',dtick=1)
    figura.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray',showline=True, linewidth=1, linecolor='black')
    return fig,figura
if __name__ == '__main__':
    app.run_server(debug=False)
