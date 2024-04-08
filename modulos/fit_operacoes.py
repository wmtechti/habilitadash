import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def gera_df_ranking(df):        
    df_treinadores = df.copy()
    df_treinadores = df_treinadores.groupby('treinador').sum(numeric_only=True)
    df_treinadores = df[['treinador', 'aluno']]
    df_aluno_por_treinadores = df_treinadores.drop_duplicates()

    freq_alunos_por_personal = df_aluno_por_treinadores.treinador.value_counts()
    freq_treinos_por_personal = df_treinadores.treinador.value_counts()
    dist_freq = pd.DataFrame(
        {'alunos': freq_alunos_por_personal, 'treinos':  freq_treinos_por_personal }
    )
    dist_freq.rename_axis('treinador', axis = 'columns', inplace = True)
    dist_freq = dist_freq.reset_index()
    dist_freq.columns = ['treinador', 'alunos', 'treinos registrados']
    return dist_freq

def gera_df_qtd_treinos_dia(df):
    df_treinos = df.copy()
    df_treinos = df_treinos[['data', 'treinador', 'aluno']]

    df_treinos = pd.crosstab(index = df_treinos.treinador,
                        columns = df_treinos.data,
                        values = df_treinos.treinador,
                        aggfunc= 'count')
    df_treinos = df_treinos.T

    df_treinos_dia = df_treinos.copy()
    df_treinos_dia.index = pd.to_datetime(df_treinos_dia.index, dayfirst=True)

    df_treinos_dia = df_treinos_dia.reset_index()
    df_media_treinos_dia = df_treinos_dia.groupby(pd.Grouper(key = 'data', freq= 'D')).sum().round()

    return df_media_treinos_dia

def gera_df_nivel_questionario(df_avaliacao_fisica):
    df_nivel_questionario =  df_avaliacao_fisica.copy()
    df_nivel_questionario = df_nivel_questionario[['aluno', 'data', 'treinador',
                                        'pontuacaoTempoTreinoAtual', 
                                        'pontuacao_tempo_de_destreinamento_atual',
                                        'pontuacao_experiencia_previa_de_treinamento',
                                        ]]
    df_nivel_questionario.columns = ['aluno', 'data', 'treinador',
                                'Tempo de treino atual', 
                                'Tempo de destreinamento',
                                'Experiencia prévia',
                                ]
    df_nivel_questionario['data'] = pd.to_datetime(df_nivel_questionario['data'], format="%m/%d/%Y").dt.date
    df_nivel_questionario = df_nivel_questionario.drop_duplicates(keep='last')

    colunas_info = list(df_nivel_questionario.loc[:,'aluno':'treinador'].columns)

    colunas_nivel = list(df_nivel_questionario.loc[:,'Tempo de treino atual':
                                                'Experiencia prévia'].columns)

    df_nivel_questionario = df_nivel_questionario.melt(id_vars = colunas_info,
                                                    value_vars = colunas_nivel,
                                                    var_name = "Variável",
                                                    value_name = "Pontuação")

    df_nivel_questionario = df_nivel_questionario.sort_values("aluno", axis = 0, ascending = True)

    return df_nivel_questionario

def gera_df_nivel_testes_fisicos(df_avaliacao_fisica):
    df_nivel_testes_fisicos = df_avaliacao_fisica.copy()
    df_nivel_testes_fisicos = df_nivel_testes_fisicos[['aluno', 'data','treinador',
                                                        'pontuacao_squat_nivel',
                                                        'pontuacao_supino_nivel',
                                                        'pontuacao_terra_nivel',
                                                    ]]

    df_nivel_testes_fisicos.columns = ['aluno', 'data', 'treinador',
                                    'Agachamento', 'Supino',
                                    'Terra', 
                                    ]
    df_nivel_testes_fisicos['data'] = pd.to_datetime(df_nivel_testes_fisicos['data'], format="%m/%d/%Y").dt.date
    df_nivel_testes_fisicos = df_nivel_testes_fisicos.drop_duplicates(keep='last')

    colunas_info = list(df_nivel_testes_fisicos.loc[:,'aluno':'treinador'].columns)

    colunas_nivel = list(df_nivel_testes_fisicos.loc[:, 'Agachamento':
                                        'Terra'].columns)
    df_nivel_testes_fisicos = df_nivel_testes_fisicos.melt(id_vars = colunas_info,
                                                    value_vars = colunas_nivel,
                                                    var_name = "Variável",
                                                    value_name = "Pontuação")
    df_nivel_testes_fisicos = df_nivel_testes_fisicos.sort_values("aluno", axis = 0, ascending = True)
    return df_nivel_testes_fisicos

def gera_df_antropometria(df_avaliacao_fisica):
    df_antropometria = df_avaliacao_fisica.copy()
    df_antropometria = df_antropometria[['data', 'peso',
                                        'torax', 'cintura',
                                        'abdômen', 'quadril',
                                        'braço(d)', 'braço(e)',
                                        'coxa(d)', 'coxa(e)', 
                                        'panturrilha(d)', 'panturrilha(e)']].round(2)
    df_antropometria['data'] = pd.to_datetime(df_antropometria['data']).dt.date
    df_antropometria = df_antropometria.set_index('data')
    return df_antropometria.T

def gera_df_imc(df_avaliacao_fisica):
    df_imc = df_avaliacao_fisica.copy()
    df_imc = df_imc[['data', 'IMC']]
    df_imc['data'] = pd.to_datetime(df_imc['data']).dt.date
    df_imc = df_imc.set_index('data')
    df_imc['Diferença percentual'] = (df_imc.pct_change() * 100).round(2).astype(float)
    return df_imc.round(1)

def gera_df_antropometria_tronco(df_avaliacao_fisica):
    df_antropometria_tronco = df_avaliacao_fisica.copy()
    df_antropometria_tronco = df_antropometria_tronco[['data',
                                        'torax', 'cintura',
                                        'abdômen', 'quadril',
                                        ]].round(2)
    df_antropometria_tronco['data'] = pd.to_datetime(df_antropometria_tronco['data']).dt.date
    df_antropometria_tronco = df_antropometria_tronco.set_index('data')
    return df_antropometria_tronco

def gera_df_antropometria_membros(df_avaliacao_fisica):
    df_antropometria_membros = df_avaliacao_fisica.copy()
    df_antropometria_membros = df_antropometria_membros[['data',
                                        'braço(d)', 'braço(e)',
                                        'coxa(d)', 'coxa(e)', 
                                        'panturrilha(d)', 'panturrilha(e)'
                                        ]].round(2)
    df_antropometria_membros['data'] = pd.to_datetime(df_antropometria_membros['data']).dt.date
    df_antropometria_membros = df_antropometria_membros.set_index('data')
    return df_antropometria_membros

def gera_df_velocidade_aerobia(df_avaliacao_fisica):
    df_velocida_aerobia = df_avaliacao_fisica.copy()
    df_velocida_aerobia = df_velocida_aerobia[['data',
                                        'VelocidadeAerobiaMaxima'
                                        ]].round(2)
    df_velocida_aerobia['data'] = pd.to_datetime(df_velocida_aerobia['data']).dt.date
    df_velocida_aerobia = df_velocida_aerobia.set_index('data')
    return df_velocida_aerobia

def gera_df_vo2_estimado(df_avaliacao_fisica):
    df_vo2_estimado = df_avaliacao_fisica.copy()
    df_vo2_estimado = df_vo2_estimado[['data',
                                        'vo2_estimado'
                                        ]].round(2)
    df_vo2_estimado['data'] = pd.to_datetime(df_vo2_estimado['data']).dt.date
    df_vo2_estimado = df_vo2_estimado.set_index('data')
    return df_vo2_estimado

def gera_df_forca_relativaI(df_avaliacao_fisica):
    df_forca_relativa = df_avaliacao_fisica.copy()
    df_forca_relativa = df_forca_relativa[['aluno', 'data','treinador',
                                                'forcaRelativaAgachamento', 
                                                'forcaRelativaSupino',
                                                'forcaRelativaTerra',
                                                'forcaRelativaBarraFixa',
                                            ]]

    df_forca_relativa.columns = ['aluno', 'data', 'treinador',
                                    'Agachamento', 'Supino',
                                    'Terra', 'Barra fixa',
                                    ]
    df_forca_relativa['data'] = pd.to_datetime(df_forca_relativa['data'], format="%m/%d/%Y").dt.date

    colunas_info = list(df_forca_relativa.loc[:,'aluno':'treinador'].columns)

    colunas_nivel = list(df_forca_relativa.loc[:, 'Agachamento':
                                        'Barra fixa'].columns)
    df_forca_relativa = df_forca_relativa.melt(id_vars = colunas_info,
                                                    value_vars = colunas_nivel,
                                                    var_name = "Padrão",
                                                    value_name = "Força relativa")
    df_forca_relativa = df_forca_relativa.sort_values("aluno", axis = 0, ascending = True)
    return df_forca_relativa

def gera_df_forca_relativa_final(df_forca_relativaI):
    df_forca_relativaI = pd.crosstab(index = df_forca_relativaI["Padrão"],
                        columns = df_forca_relativaI.data,
                        values = df_forca_relativaI["Força relativa"],
                        aggfunc= 'sum')
    df_forca_relativaI  = df_forca_relativaI.replace(np.nan, 0)
    df_forca_relativaI = df_forca_relativaI.T

    return df_forca_relativaI

def gera_df_potenciaI(df_avaliacao_fisica):
    df_potencia = df_avaliacao_fisica.copy()
    df_potencia = df_avaliacao_fisica[['aluno', 'data','treinador',
                                            'squatJump1', 'squatJump2',
                                            'squatJump3', 'media_squat_jump'
                                            ]]

    df_potencia.columns = ['aluno', 'data','treinador',
                                        'squat jump 1', 'squat jump 2',
                                        'squat jump 3', 'media squat jump'
                                    ]
    df_potencia['data'] = pd.to_datetime(df_potencia['data'], format="%m/%d/%Y").dt.date

    colunas_info = list(df_potencia.loc[:,'aluno':'treinador'].columns)

    colunas_nivel = list(df_potencia.loc[:, 'squat jump 1':
                                        'media squat jump'].columns)
    df_potencia = df_potencia.melt(id_vars = colunas_info,
                                                    value_vars = colunas_nivel,
                                                    var_name = "Padrão",
                                                    value_name = "potencia")
    df_potencia = df_potencia.sort_values("aluno", axis = 0, ascending = True)
    return df_potencia

def gera_df_potencia_final(df_potenciaI):
    df_potenciaI = pd.crosstab(index = df_potenciaI["Padrão"],
                        columns = df_potenciaI.data,
                        values = df_potenciaI["potencia"],
                        aggfunc= 'sum')
    df_potenciaI  = df_potenciaI.replace(np.nan, 0)
    df_potenciaI = df_potenciaI.T

    return df_potenciaI

def gera_df_classificacao_flexibilidade(df_avaliacao_fisica):
    df_classificacao_flexibilidade = df_avaliacao_fisica.copy()
    df_classificacao_flexibilidade = df_classificacao_flexibilidade[['aluno', 'data','treinador',
                                                'nivel_mob_omb_direito', 'nivel_mob_omb_esquerdo',
                                                'nivel_mob_quadril_direito', 'nivel_mob_quadril_esquerdo',
                                                'nivel_mob_torn_direito', 'nivel_mob_torn_esquerdo',
                                                
                                            ]]

    df_classificacao_flexibilidade.columns = ['aluno', 'data', 'treinador',
                                    'Ombro (d)',
                                    'Ombro (e)',
                                    'Quadril (d)',
                                    'Quadril (e)',
                                    'Tornozelo (d)',
                                    'Tornozelo (e)'
                                    ]
    df_classificacao_flexibilidade['data'] = pd.to_datetime(df_classificacao_flexibilidade['data'], format="%m/%d/%Y").dt.date
    df_classificacao_flexibilidade = df_classificacao_flexibilidade.drop_duplicates(keep='last')

    colunas_info = list(df_classificacao_flexibilidade.loc[:,'aluno':'treinador'].columns)

    colunas_nivel = list(df_classificacao_flexibilidade.loc[:, 'Ombro (d)':
                                        'Tornozelo (e)'].columns)
    df_classificacao_flexibilidade = df_classificacao_flexibilidade.melt(id_vars = colunas_info,
                                                    value_vars = colunas_nivel,
                                                    var_name = "Articulação",
                                                    value_name = "Pontuação")
    df_classificacao_flexibilidade = df_classificacao_flexibilidade.sort_values("aluno", axis = 0, ascending = True)
    return df_classificacao_flexibilidade

def gera_df_classificacao_flexibilidade_final(df_classificacao_flexibilidade):
    df_classificacao_flexibilidadeI = pd.crosstab(index = df_classificacao_flexibilidade["Articulação"],
                        columns = df_classificacao_flexibilidade.data,
                        values = df_classificacao_flexibilidade["Pontuação"],
                        aggfunc= 'sum')
    df_classificacao_flexibilidadeI  = df_classificacao_flexibilidadeI.replace(np.nan, 0)
    df_classificacao_flexibilidadeI = df_classificacao_flexibilidadeI.T

    return df_classificacao_flexibilidadeI

def gera_df_nivel_flexibilidade(df_avaliacao_fisica):
    df_flexibilidade = df_avaliacao_fisica.copy()
    df_flexibilidade = df_flexibilidade[['aluno', 'data','treinador',
                                                'mobilidadeGlenoumeralDireita',
                                                'mobilidadeGlenoumeralEsquerda',
                                                'AmplitudeMovimentoQuadrilDireito',
                                                'AmplitudeMovimentoQuadrilEsquerdo',
                                                'AmplitudeMovimentoTornozeloDireito',
                                                'AmplitudeMovimentoTornozeloEsquerdo',
                                            ]]

    df_flexibilidade.columns = ['aluno', 'data', 'treinador',
                                    'Ombro direito',
                                    'Ombro esquerdo',
                                    'Quadril Direito',
                                    'Quadril Esquerdo',
                                    'Tornozelo Direito',
                                    'Tornozelo Esquerdo'
                                    ]
    df_flexibilidade['data'] = pd.to_datetime(df_flexibilidade['data'], format="%m/%d/%Y").dt.date
    df_flexibilidade = df_flexibilidade.drop_duplicates(keep='last')

    colunas_info = list(df_flexibilidade.loc[:,'aluno':'treinador'].columns)

    colunas_nivel = list(df_flexibilidade.loc[:, 'Ombro direito':
                                        'Tornozelo Esquerdo'].columns)
    df_flexibilidade = df_flexibilidade.melt(id_vars = colunas_info,
                                                    value_vars = colunas_nivel,
                                                    var_name = "Variável",
                                                    value_name = "Pontuação")
    df_flexibilidade = df_flexibilidade.sort_values("aluno", axis = 0, ascending = True)
    return df_flexibilidade

def gera_df_flexibilidade_final(df_flexibilidade):
    df_flexibilidadeI = pd.crosstab(index = df_flexibilidade["Variável"],
                        columns = df_flexibilidade.data,
                        values = df_flexibilidade["Pontuação"],
                        aggfunc= 'sum')
    df_flexibilidadeI  = df_flexibilidadeI.replace(np.nan, 0)
    df_flexibilidadeI = df_flexibilidadeI.T

    return df_flexibilidadeI

def gera_df_coreI(df_avaliacao_fisica):
    df_core = df_avaliacao_fisica.copy()
    df_core = df_avaliacao_fisica[['aluno', 'data','treinador',
                                            'pranchaVentral',
                                            'extensãoColuna', 
                                            'pranchaLateralDireita', 
                                            'pranchaLateralEsquerda'
                                            ]]

    df_core.columns = ['aluno', 'data','treinador',
                                        'Prancha ventral', 'Extensão da coluna',
                                        'Prancha lateral direita', 'Prancha lateral esquerda'
                                    ]
    df_core['data'] = pd.to_datetime(df_core['data'], format="%m/%d/%Y").dt.date

    colunas_info = list(df_core.loc[:,'aluno':'treinador'].columns)

    colunas_nivel = list(df_core.loc[:, 'Prancha ventral':
                                        'Prancha lateral esquerda'].columns)
    df_core = df_core.melt(id_vars = colunas_info,
                                                    value_vars = colunas_nivel,
                                                    var_name = "Padrão",
                                                    value_name = "core")
    df_core = df_core.sort_values("aluno", axis = 0, ascending = True)
    return df_core
def gera_df_core_final(df_coreI):
    df_coreI = pd.crosstab(index = df_coreI["Padrão"],
                        columns = df_coreI.data,
                        values = df_coreI["core"],
                        aggfunc= 'sum')
    df_coreI  = df_coreI.replace(np.nan, 0)
    df_coreI = df_coreI.T

    return df_coreI
def gera_df_nivel_core_pontos(df_avaliacao_fisica):
    df_nivel_core_pontos = df_avaliacao_fisica.copy()
    df_nivel_core_pontos = df_nivel_core_pontos[['aluno', 'data','treinador',
                                                'pontosPranchaVentral',
                                                'pontosPranchaLateralEsquerda',
                                                'pontosExtensaoColuna',
                                                'pontosPranchaLateralDireita',
                                            ]]

    df_nivel_core_pontos.columns = ['aluno', 'data', 'treinador',
                                    'Prancha ventral',
                                    'Prancha lateral (e)',
                                    'Extensão da coluna',
                                    'Prancha lateral (d)',
                                    ]
    df_nivel_core_pontos['data'] = pd.to_datetime(df_nivel_core_pontos['data'], format="%m/%d/%Y").dt.date
    df_nivel_core_pontos = df_nivel_core_pontos.drop_duplicates(keep='last')

    colunas_info = list(df_nivel_core_pontos.loc[:,'aluno':'treinador'].columns)

    colunas_nivel = list(df_nivel_core_pontos.loc[:, 'Prancha ventral':
                                                    'Prancha lateral (d)'].columns)
    df_nivel_core_pontos = df_nivel_core_pontos.melt(id_vars = colunas_info,
                                                    value_vars = colunas_nivel,
                                                    var_name = "Variável",
                                                    value_name = "Pontuação")
    df_nivel_core_pontos = df_nivel_core_pontos.sort_values("aluno", axis = 0, ascending = True)
    return df_nivel_core_pontos
def gera_df_tonelagem_dia(df):
    df_tonelagem = df.copy()
    df_tonelagem = df_tonelagem.query('series != 0')
    df_tonelagem = df_tonelagem[['aluno','data', 'treino', 'tonelagem']]

    df_tonelagem = pd.crosstab(index = df_tonelagem.treino,
                        columns = df_tonelagem.data,
                        values = df_tonelagem.tonelagem,
                        aggfunc= 'sum')
    df_tonelagem  = df_tonelagem.replace(np.nan, 0)
    df_tonelagem = df_tonelagem.T

    df_tonelagem_dia = df_tonelagem.copy()
    df_tonelagem_dia.index = pd.to_datetime(df_tonelagem_dia.index, dayfirst=True)

    df_tonelagem_dia = df_tonelagem_dia.reset_index()
    df_media_tonelagem_dia = df_tonelagem_dia.groupby(pd.Grouper(key = 'data', freq= 'D')).sum().round()
    return df_media_tonelagem_dia
def gera_df_tonelagem_semana(df):
    df_tonelagem = df.copy()
    df_tonelagem = df_tonelagem[['aluno','data', 'tonelagem']]

    df_tonelagem = pd.crosstab(index = df_tonelagem.aluno,
                        columns = df_tonelagem.data,
                        values = df_tonelagem.tonelagem,
                        aggfunc= 'sum')
    df_tonelagem  = df_tonelagem.replace(np.nan, 0)
    df_tonelagem = df_tonelagem.T

    df_tonelagem_semanal = df_tonelagem.copy()
    df_tonelagem_semanal.index = pd.to_datetime(df_tonelagem_semanal.index, dayfirst=True)

    df_tonelagem_semanal = df_tonelagem_semanal.reset_index()
    df_media_tonelagem_semanal = df_tonelagem_semanal.groupby(pd.Grouper(key = 'data', freq= 'W')).sum().round()
    df_media_tonelagem_semanal['Diferença percentual'] = (df_media_tonelagem_semanal.pct_change() * 100).round(2) 
    
    return df_media_tonelagem_semanal
def gera_df_carga_interna_dia(df):
    df_carga_interna_dia = df.copy()
    df_carga_interna_dia = df_carga_interna_dia[['aluno','data', 'treino', 'carga_interna']]

    df_carga_interna_dia = pd.crosstab(index = df_carga_interna_dia.treino,
                        columns = df_carga_interna_dia.data,
                        values = df_carga_interna_dia.carga_interna,
                        aggfunc= 'sum')
    df_carga_interna_dia  = df_carga_interna_dia.replace(np.nan, 0)
    df_carga_interna_dia = df_carga_interna_dia.T

    df_carga_interna_dia = df_carga_interna_dia.copy()
    df_carga_interna_dia.index = pd.to_datetime(df_carga_interna_dia.index, dayfirst=True)

    df_carga_interna_dia = df_carga_interna_dia.reset_index()
    df_carga_interna_dia = df_carga_interna_dia.groupby(pd.Grouper(key = 'data', freq= 'D')).sum().round()
    return df_carga_interna_dia
def gera_df_carga_interna_semana(df):
    df_carga_interna = df.copy()
    df_carga_interna = df_carga_interna[['aluno','data', 'treino', 'carga_interna']]

    df_carga_interna = pd.crosstab(index = df_carga_interna.aluno,
                        columns = df_carga_interna.data,
                        values = df_carga_interna.carga_interna,
                        aggfunc= 'sum')
    df_carga_interna  = df_carga_interna.replace(np.nan, 0)
    df_carga_interna = df_carga_interna.T

    df_carga_interna_semanal = df_carga_interna.copy()
    df_carga_interna_semanal.index = pd.to_datetime(df_carga_interna_semanal.index, dayfirst=True)

    df_carga_interna_semanal = df_carga_interna_semanal.reset_index()
    df_media_carga_interna_semanal = df_carga_interna_semanal.groupby(pd.Grouper(key = 'data', freq= 'W')).sum().round()
    df_media_carga_interna_semanal['Diferença percentual'] = (df_media_carga_interna_semanal.pct_change() * 100).round(2)
    return df_media_carga_interna_semanal
def gera_df_monotonia_strain(df):
    df_monotonia = df.copy()
    df_monotonia = df_monotonia[['aluno','data', 'treino', 'carga_interna']]

    monotonia_sum = pd.crosstab(index = df_monotonia.treino,
                        columns = df_monotonia.data,
                        values = df_monotonia.carga_interna,
                        aggfunc= 'sum')
    monotonia  = monotonia_sum.replace(np.nan, 0)
    monotonia = monotonia.T

    monotonia_semanal = monotonia.copy()
    monotonia_semanal.index = pd.to_datetime(monotonia_semanal.index, dayfirst=True)

    monotonia_semanal = monotonia_semanal.reset_index()
    df_monotonia_semanal_sum = monotonia_semanal.groupby(pd.Grouper(key = 'data', freq= 'W')).sum().round()
    df_monotonia_semanal_std = monotonia_semanal.groupby(pd.Grouper(key = 'data', freq= 'W')).std().round()
    df_monotonia_semanal_mean = monotonia_semanal.groupby(pd.Grouper(key = 'data', freq= 'W')).mean().round()
    
    monotonia = (df_monotonia_semanal_mean / df_monotonia_semanal_std).round(2)
    monotonia = monotonia.fillna(0)
    
    strain = (df_monotonia_semanal_sum * monotonia)

    return monotonia, strain
def gera_df_monotonia_strain(df):
    df_monotonia = df.copy()
    df_monotonia = df_monotonia[['aluno','data', 'treino', 'carga_interna']]

    monotonia_sum = pd.crosstab(index = df_monotonia.treino,
                        columns = df_monotonia.data,
                        values = df_monotonia.carga_interna,
                        aggfunc= 'sum')
    monotonia  = monotonia_sum.replace(np.nan, 0)
    monotonia = monotonia.T

    monotonia_semanal = monotonia.copy()
    monotonia_semanal.index = pd.to_datetime(monotonia_semanal.index, dayfirst=True)

    monotonia_semanal = monotonia_semanal.reset_index()
    df_monotonia_semanal_sum = monotonia_semanal.groupby(pd.Grouper(key = 'data', freq= 'W')).sum().round()
    df_monotonia_semanal_std = monotonia_semanal.groupby(pd.Grouper(key = 'data', freq= 'W')).std().round()
    df_monotonia_semanal_mean = monotonia_semanal.groupby(pd.Grouper(key = 'data', freq= 'W')).mean().round()
    
    monotonia = (df_monotonia_semanal_mean / df_monotonia_semanal_std).round(2)
    monotonia = monotonia.fillna(0)
    
    strain = (df_monotonia_semanal_sum * monotonia)

    return monotonia, strain

def monotonia_total(df_monotonia, df_strain): 
    monotonia_total = df_monotonia.copy()
    monotonia_total['Valor'] = df_monotonia.sum(axis=1).round(2)
    monotonia_total['Diferença percentual'] = (monotonia_total['Valor'].pct_change() * 100).round(2) 
    
    strain_total = df_strain.copy()
    strain_total['Valor'] = df_strain.sum(axis=1)
    strain_total['Diferença percentual'] = (strain_total['Valor'].pct_change() * 100).round(2)
    return monotonia_total, strain_total

def gera_df_volume(df):
    df_volume = df.copy()
    df_volume  = df_volume[['aluno','data', 'volume']]
    df_volume  = pd.crosstab(index = df_volume.aluno,
                        columns = df_volume.data,
                        values = df_volume.volume,
                        aggfunc= 'sum')
    df_volume  = df_volume.replace(np.nan, 0)
    df_volume = df_volume.T

    df_volume_semanal = df_volume.copy()
    df_volume_semanal.index = pd.to_datetime(df_volume_semanal.index, dayfirst=True)

    df_volume_semanal = df_volume_semanal.reset_index()
    df_media_volume_semanal = df_volume_semanal.groupby(pd.Grouper(key = 'data', freq= 'W')).mean().round()
    return df_media_volume_semanal

def gera_df_intensidade(df):
    df_intensidade = df.copy()
    df_intensidade  = df_intensidade[['aluno','data', 'intensidade']]

    df_intensidade  = pd.crosstab(index = df_intensidade.aluno,
                        columns = df_intensidade.data,
                        values = df_intensidade.intensidade,
                        aggfunc= 'sum')
    df_intensidade  = df_intensidade.replace(np.nan, 0)
    df_intensidade = df_intensidade.T

    df_intensidade_semanal = df_intensidade.copy()
    df_intensidade_semanal.index = pd.to_datetime(df_intensidade_semanal.index, dayfirst=True)

    df_intensidade_semanal = df_intensidade_semanal.reset_index()
    df_intensidade_semanal = df_intensidade_semanal.groupby(pd.Grouper(key = 'data', freq= 'W')).mean().round()
    return df_intensidade_semanal

def gera_df_series_dia(df):
    df_series = df.copy()
    df_series = df_series.query('series!=0')
    df_series = df_series[['aluno','data', 'treino', 'series']]

    df_series = pd.crosstab(index = df_series.treino,
                        columns = df_series.data,
                        values = df_series.series,
                        aggfunc= 'sum')
    df_series  = df_series.replace(np.nan, 0)
    df_series = df_series.T

    df_series_dia = df_series.copy()
    df_series_dia.index = pd.to_datetime(df_series_dia.index, dayfirst=True)

    df_series_dia = df_series_dia.reset_index()
    df_media_series_dia = df_series_dia.groupby(pd.Grouper(key = 'data', freq= 'D')).sum().round()
    return df_media_series_dia

def gera_df_repeticoes_dia(df):
    df_repeticoes = df.copy()
    df_repeticoes = df_repeticoes.query('repeticoes!=0')
    df_repeticoes = df_repeticoes[['aluno','data', 'treino', 'repeticoes']]

    df_repeticoes = pd.crosstab(index = df_repeticoes.treino,
                        columns = df_repeticoes.data,
                        values = df_repeticoes.repeticoes,
                        aggfunc= 'sum')
    df_repeticoes  = df_repeticoes.replace(np.nan, 0)
    df_repeticoes = df_repeticoes.T

    df_repeticoes_dia = df_repeticoes.copy()
    df_repeticoes_dia.index = pd.to_datetime(df_repeticoes_dia.index, dayfirst=True)

    df_repeticoes_dia = df_repeticoes_dia.reset_index()
    df_media_repeticoes_dia = df_repeticoes_dia.groupby(pd.Grouper(key = 'data', freq= 'D')).sum().round()
    return df_media_repeticoes_dia

def gera_df_tonelagem_dia(df):
    df_tonelagem = df.copy()
    df_tonelagem = df_tonelagem.query('series!=0')
    df_tonelagem = df_tonelagem[['aluno','data', 'treino', 'tonelagem']]

    df_tonelagem = pd.crosstab(index = df_tonelagem.treino,
                        columns = df_tonelagem.data,
                        values = df_tonelagem.tonelagem,
                        aggfunc= 'sum')
    df_tonelagem  = df_tonelagem.replace(np.nan, 0)
    df_tonelagem = df_tonelagem.T

    df_tonelagem_dia = df_tonelagem.copy()
    df_tonelagem_dia.index = pd.to_datetime(df_tonelagem_dia.index, dayfirst=True)

    df_tonelagem_dia = df_tonelagem_dia.reset_index()
    df_media_tonelagem_dia = df_tonelagem_dia.groupby(pd.Grouper(key = 'data', freq= 'D')).sum().round()
    return df_media_tonelagem_dia

def gera_df_repeticoes_semana(df):
    df_repeticoes = df.copy()
    df_repeticoes = df_repeticoes[['aluno','data', 'repeticoes']]

    df_repeticoes = pd.crosstab(index = df_repeticoes.aluno,
                        columns = df_repeticoes.data,
                        values = df_repeticoes.repeticoes,
                        aggfunc= 'sum')
    df_repeticoes  = df_repeticoes.replace(np.nan, 0)
    df_repeticoes = df_repeticoes.T

    df_repeticoes_semanal = df_repeticoes.copy()
    df_repeticoes_semanal.index = pd.to_datetime(df_repeticoes_semanal.index, dayfirst=True)

    df_repeticoes_semanal = df_repeticoes_semanal.reset_index()
    df_media_repeticoes_semanal = df_repeticoes_semanal.groupby(pd.Grouper(key = 'data', freq= 'W')).sum().round()
    return df_media_repeticoes_semanal

def gera_df_series(df, df_intensidade):
    df_series = df.copy()
    df_series  = df_series[['aluno','data', 'series']]

    df_series  = pd.crosstab(index = df_series.aluno,
                        columns = df_series.data,
                        values = df_series.series,
                        aggfunc= 'sum')
    df_series = df_series.replace(np.nan, 0)
    df_series = df_series.T

    df_series_semanal = df_intensidade.copy()
    df_series_semanal.index = pd.to_datetime(df_series_semanal.index, dayfirst=True)

    df_series_semanal = df_series_semanal.reset_index()
    df_series_semanal = df_series_semanal.groupby(pd.Grouper(key = 'data', freq= 'W')).mean().round()
    return df_series_semanal

def gera_df_pse_dia(df):
    df_pse_dia = df.copy()
    df_pse_dia = df_pse_dia.query('series!=0')
    df_pse_dia = df_pse_dia[['aluno','data', 'treino', 'pse_quantitativa']]

    df_pse_dia = pd.crosstab(index = df_pse_dia.treino,
                        columns = df_pse_dia.data,
                        values = df_pse_dia.pse_quantitativa,
                        aggfunc= 'sum')
    df_pse_dia  = df_pse_dia.replace(np.nan, 0)
    df_pse_dia = df_pse_dia.T

    df_pse_dia = df_pse_dia.copy()
    df_pse_dia.index = pd.to_datetime(df_pse_dia.index, dayfirst=True)

    df_pse_dia = df_pse_dia.reset_index()
    df_pse_dia = df_pse_dia.groupby(pd.Grouper(key = 'data', freq= 'D')).sum().round()
    return df_pse_dia

def gera_df_prs_dia(df):
    df_prs_dia = df.copy()
    df_prs_dia = df_prs_dia.query('series!=0')
    df_prs_dia = df_prs_dia[['aluno','data', 'treino', 'prs_quantitativa']]

    df_prs_dia = pd.crosstab(index = df_prs_dia.treino,
                        columns = df_prs_dia.data,
                        values = df_prs_dia.prs_quantitativa,
                        aggfunc= 'sum')
    df_prs_dia  = df_prs_dia.replace(np.nan, 0)
    df_prs_dia = df_prs_dia.T

    df_prs_dia = df_prs_dia.copy()
    df_prs_dia.index = pd.to_datetime(df_prs_dia.index, dayfirst=True)

    df_prs_dia = df_prs_dia.reset_index()
    df_prs_dia = df_prs_dia.groupby(pd.Grouper(key = 'data', freq= 'D')).sum().round()
    return df_prs_dia

def gera_df_prs_dia_se(df):
    df_prs_dia = df.copy()
    df_prs_dia = df_prs_dia.query('series==0')
    df_prs_dia = df_prs_dia[['aluno','data', 'treino', 'prs_quantitativa']]

    df_prs_dia = pd.crosstab(index = df_prs_dia.treino,
                        columns = df_prs_dia.data,
                        values = df_prs_dia.prs_quantitativa,
                        aggfunc= 'sum')
    df_prs_dia  = df_prs_dia.replace(np.nan, 0)
    df_prs_dia = df_prs_dia.T

    df_prs_dia = df_prs_dia.copy()
    df_prs_dia.index = pd.to_datetime(df_prs_dia.index, dayfirst=True)

    df_prs_dia = df_prs_dia.reset_index()
    df_prs_dia = df_prs_dia.groupby(pd.Grouper(key = 'data', freq= 'D')).sum().round()
    return df_prs_dia

def gera_df_pse_dia_se(df):
    df_pse_dia = df.copy()
    df_pse_dia = df_pse_dia.query('series==0')
    df_pse_dia = df_pse_dia[['aluno','data', 'treino', 'pse_quantitativa']]

    df_pse_dia = pd.crosstab(index = df_pse_dia.treino,
                        columns = df_pse_dia.data,
                        values = df_pse_dia.pse_quantitativa,
                        aggfunc= 'sum')
    df_pse_dia  = df_pse_dia.replace(np.nan, 0)
    df_pse_dia = df_pse_dia.T

    df_pse_dia = df_pse_dia.copy()
    df_pse_dia.index = pd.to_datetime(df_pse_dia.index, dayfirst=True)

    df_pse_dia = df_pse_dia.reset_index()
    df_pse_dia = df_pse_dia.groupby(pd.Grouper(key = 'data', freq= 'D')).sum().round()
    return df_pse_dia

def gera_df_densidade(df):
    df_densidade = df.copy()
    df_densidade = df_densidade.query('densidade!=0')
    df_densidade = df_densidade[['aluno','data', 'treino', 'densidade']]

    df_densidade = pd.crosstab(index = df_densidade.treino,
                        columns = df_densidade.data,
                        values = df_densidade.densidade,
                        aggfunc= 'sum')
    df_densidade  = df_densidade.replace(np.nan, 0)
    df_densidade = df_densidade.T

    df_densidade = df_densidade.copy()
    df_densidade.index = pd.to_datetime(df_densidade.index, dayfirst=True)

    df_densidade = df_densidade.reset_index()
    df_densidade = df_densidade.groupby(pd.Grouper(key = 'data', freq= 'D')).sum().round()
    return df_densidade

def gera_df_intervalo_dia(df):
    df_intervalo = df.copy()
    df_intervalo = df_intervalo.query('series!=0')
    df_intervalo = df_intervalo[['aluno','data', 'treino', 'intervalo']]

    df_intervalo = pd.crosstab(index = df_intervalo.treino,
                        columns = df_intervalo.data,
                        values = df_intervalo.intervalo,
                        aggfunc= 'sum')
    df_intervalo  = df_intervalo.replace(np.nan, 0)
    df_intervalo = df_intervalo.T

    df_intervalo_dia = df_intervalo.copy()
    df_intervalo_dia.index = pd.to_datetime(df_intervalo_dia.index, dayfirst=True)

    df_intervalo_dia = df_intervalo_dia.reset_index()
    df_media_intervalo_dia = df_intervalo_dia.groupby(pd.Grouper(key = 'data', freq= 'D')).sum().round()
    return df_media_intervalo_dia

def gera_df_gasto(df):
    df_gasto = df.copy()
    
    #df_carga_interna_dia = df_carga_interna_dia.query('series!=0')
    df_gasto = df_gasto[['aluno', 'data', 'treino', 'Gasto_Calorico']]

    df_gasto = pd.crosstab(index = df_gasto.treino,
                        columns = df_gasto.data,
                        values = df_gasto.Gasto_Calorico,
                        aggfunc= 'sum')
    df_gasto  = df_gasto.replace(np.nan, 0)
    df_gasto = df_gasto.T

    df_gasto = df_gasto.copy()
    df_gasto.index = pd.to_datetime(df_gasto.index, dayfirst=True)

    df_gasto = df_gasto.reset_index()
    df_gasto = df_gasto.groupby(pd.Grouper(key = 'data', freq= 'D')).sum().round()
    return df_gasto

def gera_df_Gasto_Calorico_semana(df):
    df_Gasto_Calorico = df.copy()
    df_Gasto_Calorico = df_Gasto_Calorico[['aluno','data', 'treino', 'Gasto_Calorico']]

    df_Gasto_Calorico = pd.crosstab(index = df_Gasto_Calorico.aluno,
                        columns = df_Gasto_Calorico.data,
                        values = df_Gasto_Calorico.Gasto_Calorico,
                        aggfunc= 'sum')
    df_Gasto_Calorico  = df_Gasto_Calorico.replace(np.nan, 0)
    df_Gasto_Calorico = df_Gasto_Calorico.T

    df_Gasto_Calorico_semanal = df_Gasto_Calorico.copy()
    df_Gasto_Calorico_semanal.index = pd.to_datetime(df_Gasto_Calorico_semanal.index, dayfirst=True)

    df_Gasto_Calorico_semanal = df_Gasto_Calorico_semanal.reset_index()
    df_media_Gasto_Calorico_semanal = df_Gasto_Calorico_semanal.groupby(pd.Grouper(key = 'data', freq= 'W')).sum().round()
    df_media_Gasto_Calorico_semanal['Diferença percentual'] = (df_media_Gasto_Calorico_semanal.pct_change() * 100).round(2)
    return df_media_Gasto_Calorico_semanal

def plota_ranking(ranking):
    fig_ranking = px.scatter(ranking,
                    x= 'alunos',
                    y= 'treinos registrados',
                    color = 'treinador',
                    size='treinos registrados',
                    title="Quantidade de alunos e treinos registrados por treinador")
    return fig_ranking

def plota_treinos_dia(treinos_dia):
    fig_treinos_dia = px.line(treinos_dia,
                    #x= 'alunos',
                    #y= 'treinos registrados',
                    color = 'treinador',
                    #bargroup = False,
                    #size='treinos registrados',
                    #title="Quantidade de alunos e treinos registrados por treinador"
                    )
    return fig_treinos_dia
def plota_medidas_imc(df_imc):
    df_imcx = df_imc.drop('Diferença percentual', axis = 1)
    #fig_medidas_imc = px.bar( df_imcx,
                                #markers= True,
    #                            title='Evolução do IMC')
    
    fig_imc = px.bar(df_imcx,
                    x=df_imcx.index,
                    y=df_imcx.columns, 
                    title='Evolução do IMC') 
    
    for i, col in enumerate(df_imcx.columns):
        fig_imc.update_traces(text=df_imcx[col].values,
                                            selector=dict(name=col))
    
    fig_imc.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Data',
                                yaxis_title='')
    fig_imc.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_imc
def plota_medidas_tronco(df_antropometria_tronco):
    fig_medidas_tronco = px.line( df_antropometria_tronco,
                                markers= True,
                                title='Evolução da perimetria do tronco') 
    
    fig_medidas_tronco.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Semana',
                                yaxis_title='')
    fig_medidas_tronco.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_medidas_tronco
def plota_medidas_membros(df_antropometria_membros):
    fig_medidas_membros = px.line( df_antropometria_membros,
                                markers= True,
                                title='Evolução da perimetria de membros superiores e inferiores') 
    
    fig_medidas_membros.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Semana',
                                yaxis_title='')
    fig_medidas_membros.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_medidas_membros

def plota_ranking(ranking):
    fig_ranking = px.scatter(ranking,
                    x= 'alunos',
                    y= 'treinos registrados',
                    color = 'treinador',
                    size='treinos registrados',
                    title="Quantidade de alunos e treinos registrados por treinador"
                    )
    return fig_ranking

def info_gerais(df_anamnese, ranking):
    fig_info_gerais = px.scatter(ranking,
                    x= 'alunos',
                    y= 'treinos registrados',
                    color = 'treinador',
                    size='treinos registrados',
                    title="Quantidade de alunos e treinos registrados por treinador"
                    )
    return fig_info_gerais

def plota_nivel_questionario(df_nivel_questionario): 
    fig_nivel_testes_fisicos = px.line_polar(df_nivel_questionario, r='Pontuação',
                                            theta='Variável', color="data",
                                            line_close=True, template="plotly_dark",
                                            title='Nível de treinamento de acordo com questionário',)
    fig_nivel_testes_fisicos.add_annotation(
        text="Legenda: 1 = Iniciante. 2 = Intermediário. 3 = Avançado. 4 = Altamente Avançado",
        x=0.5,
        y=-0.15,  # Ajuste o valor de y para mais ou menos espaço
        showarrow=False,
        font=dict(size=14, color="white")
    )
    
    fig_nivel_testes_fisicos.update_layout(
                                            polar=dict(
                                            radialaxis=dict(
                                            visible=True,
                                            tickmode='linear',  # Definir o modo de escala linear
                                            tick0=0,            # Valor inicial do eixo
                                            dtick=1,            # Intervalo entre os ticks
                                            range=[0, 4],        # Ajuste aqui os valores mínimos e máximos do eixo radial
        )
    ),
    polar_bgcolor='#0E1117')
    
    return fig_nivel_testes_fisicos

def plota_nivel_testes(df_nivel_testes_fisicos): 
    fig_nivel_testes_fisicosx = px.line_polar(df_nivel_testes_fisicos, r='Pontuação',
                                            theta='Variável', color="data",
                                            line_close=True, template="plotly_dark",
                                            title='Nível de treinamento de acordo com testes físicos')
    
    fig_nivel_testes_fisicosx.add_annotation(
        text="Legenda: 1 = Iniciante, 2 = Intermediário, 3 = Avançado, 4 = Altamente Avançado",
        x=0.5,
        y=-0.15,  # Ajuste o valor de y para mais ou menos espaço
        showarrow=False,
        font=dict(size=14, color="white")
    )
    
    fig_nivel_testes_fisicosx.update_layout(
                                            polar=dict(
                                            radialaxis=dict(
                                            visible=True,
                                            tickmode='linear',  # Definir o modo de escala linear
                                            tick0=0,            # Valor inicial do eixo
                                            dtick=1,            # Intervalo entre os ticks
                                            range=[0, 4]        # Ajuste aqui os valores mínimos e máximos do eixo radial
        )
    ),
    polar_bgcolor='#0E1117',)
    
    return fig_nivel_testes_fisicosx

def plota_forca_relativa_final(forca_relativa_final):
    fig_forca_relativa_final = px.bar(forca_relativa_final,
                                        x=forca_relativa_final.index,
                                        y=forca_relativa_final.columns, 
                                        color='Padrão',
                                        title='Valores de força relativa agrupados por avaliação')
    
    for i, col in enumerate(forca_relativa_final.columns):
        fig_forca_relativa_final.update_traces(text=forca_relativa_final[col].values,
                                            selector=dict(name=col))
    
    fig_forca_relativa_final.update_layout(
        xaxis={'tickangle': 0, 'title': '', 'showticklabels': False, 'showgrid': False},  # Remover o título e os rótulos do eixo x
        yaxis={'title': '', 'title_text': '', 'showticklabels': False, 'showgrid': False},  # Remover o título e os rótulos do eixo y
        barmode='group',
        font=dict(size=14)
    )
    fig_forca_relativa_final.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    
    return fig_forca_relativa_final

def plota_potencia_final(potencia_final):
    fig_potencia_final = px.bar(potencia_final,
                                    x=potencia_final.index,
                                    y=potencia_final.columns, 
                                    color='Padrão',
                                    title='Potência de membros inferiores agrupados por avaliação')
    
    for i, col in enumerate(potencia_final.columns):
        fig_potencia_final.update_traces(text=potencia_final[col].values,
                                            selector=dict(name=col))
    
    fig_potencia_final.update_layout(
        xaxis={'tickangle': 0, 'title': '', 'showticklabels': False, 'showgrid': False},  # Remover o título e os rótulos do eixo x
        yaxis={'title': '', 'title_text': '', 'showticklabels': False, 'showgrid': False},  # Remover o título e os rótulos do eixo y
        barmode='group',
        font=dict(size=14),
        #showlegend=False  # Remover a legenda dos eixos
    )
    fig_potencia_final.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    
    return fig_potencia_final

def plota_velocidade_aerobia(velocidade_aerobia):
    fig_velocidade_aerobia = px.bar(velocidade_aerobia,
                                    x=velocidade_aerobia.index,
                                    y=velocidade_aerobia.columns, 
                                    title='Evolução da velocidade aeróbia máxima (km/h)')
    
    for i, col in enumerate(velocidade_aerobia.columns):
        fig_velocidade_aerobia.update_traces(text=velocidade_aerobia[col].values,
                                            selector=dict(name=col))
    
    fig_velocidade_aerobia.update_layout(
        xaxis={'tickangle': 0, 'title': '', 'showticklabels': False, 'showgrid': False},  # Remover o título e os rótulos do eixo x
        yaxis={'title': '', 'title_text': '', 'showticklabels': False, 'showgrid': False},  # Remover o título e os rótulos do eixo y
        barmode='group',
        font=dict(size=14),
        #showlegend=False  # Remover a legenda dos eixos
    )
    fig_velocidade_aerobia.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    
    return fig_velocidade_aerobia

def plota_vo2_estimado(vo2_estimado, df_vo2_estimado):
    fig_vo2_estimado = px.bar(df_vo2_estimado,
                                    x=df_vo2_estimado.index,
                                    y=df_vo2_estimado.columns, 
                                    title='Evolução do Vo2 máximo estimado')
    
    for i, col in enumerate(vo2_estimado.columns):
        fig_vo2_estimado.update_traces(text=vo2_estimado[col].values,
                                            selector=dict(name=col))
    
    fig_vo2_estimado.update_layout(
        xaxis={'tickangle': 0, 'title': '', 'showticklabels': False, 'showgrid': False},  # Remover o título e os rótulos do eixo x
        yaxis={'title': '', 'title_text': '', 'showticklabels': False, 'showgrid': False},  # Remover o título e os rótulos do eixo y
        barmode='group',
        font=dict(size=14),
        #showlegend=False  # Remover a legenda dos eixos
    )
    fig_vo2_estimado.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    
    return fig_vo2_estimado
def plota_flexibilidade_tabela(flexibilidade_classificacao_final):
    flexibilidade_final_ombro = flexibilidade_classificacao_final.copy()
    fig_flexibilidade_tabela = flexibilidade_classificacao_final.style
    
    return fig_flexibilidade_tabela
def plota_antropometria_tabela(df_antropometria):
    df_antropometria = df_antropometria.copy()
    fig_antropometria_tabela = df_antropometria
    
    return fig_antropometria_tabela
def plota_flexibilidade_ombro(flexibilidade_final):
    flexibilidade_final_ombro = flexibilidade_final.copy()
    flexibilidade_final_ombro = flexibilidade_final_ombro[[ 'Ombro direito', 'Ombro esquerdo' ]]
    
    fig_flexibilidade_ombro = px.bar(flexibilidade_final_ombro,
                                    x=flexibilidade_final_ombro.index,
                                    y=flexibilidade_final_ombro.columns, 
                                    title='Amplitude de movimento do ombro')
    
    
    for i, col in enumerate(flexibilidade_final_ombro.columns):
        fig_flexibilidade_ombro.update_traces(text=flexibilidade_final_ombro[col].values,
                                            selector=dict(name=col))
    
    fig_flexibilidade_ombro.update_layout(
        xaxis={'tickangle': 0, 'title': '', 'showticklabels': False, 'showgrid': False},  # Remover o título e os rótulos do eixo x
        yaxis={'title': '', 'title_text': '', 'showticklabels': False, 'showgrid': False},  # Remover o título e os rótulos do eixo y
        barmode='group',
        font=dict(size=14),
    )
    fig_flexibilidade_ombro.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    ) 
    legenda_texto = "Legenda: são considerados ideais valores menores que 25 cm ."
    fig_flexibilidade_ombro.add_annotation(
        text=legenda_texto,
        x=0,
        y=-0.5,  # Ajuste o valor de y para mais ou menos espaço
        xref="paper",  # Posição relativa ao eixo x do gráfico
        yref="paper",  # Posição relativa ao eixo y do gráfico
        showarrow=False,
        font=dict(size=14)
    )
    
    return fig_flexibilidade_ombro
def plota_flexibilidade_quadril(flexibilidade_final):
    flexibilidade_final_quadril = flexibilidade_final.copy()
    flexibilidade_final_quadril = flexibilidade_final_quadril[[ 'Quadril Direito', 'Quadril Esquerdo' ]]
    fig_flexibilidade_quadril = px.bar(flexibilidade_final_quadril,
                                    x=flexibilidade_final_quadril.index,
                                    y=flexibilidade_final_quadril.columns, 
                                    title='Amplitude de movimento do quadril')
    
    for i, col in enumerate(flexibilidade_final_quadril.columns):
        fig_flexibilidade_quadril.update_traces(text=flexibilidade_final_quadril[col].values,
                                            selector=dict(name=col))
    
    fig_flexibilidade_quadril.update_layout(
        xaxis={'tickangle': 0, 'title': '', 'showticklabels': False, 'showgrid': False},  # Remover o título e os rótulos do eixo x
        yaxis={'title': '', 'title_text': '', 'showticklabels': False, 'showgrid': False},  # Remover o título e os rótulos do eixo y
        barmode='group',
        font=dict(size=14),
    )
    fig_flexibilidade_quadril.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    
    legenda_texto = "Legenda: são considerados ideais valores acima de 65 graus ."
    fig_flexibilidade_quadril.add_annotation(
        text=legenda_texto,
        x=0,
        y=-0.5,  # Ajuste o valor de y para mais ou menos espaço
        xref="paper",  # Posição relativa ao eixo x do gráfico
        yref="paper",  # Posição relativa ao eixo y do gráfico
        showarrow=False,
        font=dict(size=14)
    )
    
    return fig_flexibilidade_quadril
def plota_flexibilidade_tornozelo(flexibilidade_final):
    flexibilidade_final_tornozelo = flexibilidade_final.copy()
    flexibilidade_final_tornozelo = flexibilidade_final_tornozelo[[ 'Tornozelo Direito', 'Tornozelo Esquerdo' ]]
    fig_flexibilidade_tornozelo = px.bar(flexibilidade_final_tornozelo,
                                    x=flexibilidade_final_tornozelo.index,
                                    y=flexibilidade_final_tornozelo.columns, 
                                    title='Amplitude de movimento do tornozelo')
    
    for i, col in enumerate(flexibilidade_final_tornozelo.columns):
        fig_flexibilidade_tornozelo.update_traces(text=flexibilidade_final_tornozelo[col].values,
                                            selector=dict(name=col))
    
    fig_flexibilidade_tornozelo.update_layout(
        xaxis={'tickangle': 0, 'title': '', 'showticklabels': False, 'showgrid': False},  # Remover o título e os rótulos do eixo x
        yaxis={'title': '', 'title_text': '', 'showticklabels': False, 'showgrid': False},  # Remover o título e os rótulos do eixo y
        barmode='group',
        font=dict(size=14),
    )
    fig_flexibilidade_tornozelo.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    
    legenda_texto = "Legenda: são considerados ideais valores acima de 45 graus."
    fig_flexibilidade_tornozelo.add_annotation(
        text=legenda_texto,
        x=0,
        y=-0.5,  # Ajuste o valor de y para mais ou menos espaço
        xref="paper",  # Posição relativa ao eixo x do gráfico
        yref="paper",  # Posição relativa ao eixo y do gráfico
        showarrow=False,
        font=dict(size=14)
    )
    
    return fig_flexibilidade_tornozelo
def plota_core_final(core_final):
    fig_core_final = px.bar(core_final,
                                    x=core_final.index,
                                    y=core_final.columns, 
                                    color='Padrão',
                                    title='Performance em segundos nos testes do core')
    
    for i, col in enumerate(core_final.columns):
        fig_core_final.update_traces(text=core_final[col].values,
                                            selector=dict(name=col))
    
    fig_core_final.update_layout(
        xaxis={'tickangle': 0, 'title': '', 'showticklabels': False, 'showgrid': False},  # Remover o título e os rótulos do eixo x
        yaxis={'title': '', 'title_text': '', 'showticklabels': False, 'showgrid': False},  # Remover o título e os rótulos do eixo y
        barmode='group',
        font=dict(size=14),
    )
    
    
    fig_core_final.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    
    return fig_core_final
def plota_nivel_core(df_nivel_core_pontos):
    fig_nivel_core = px.line_polar(df_nivel_core_pontos, r='Pontuação',
                                            theta='Variável', color="data",
                                            line_close=True, template="plotly_dark",
                                            title='Níveis de treinamento do core')
    fig_nivel_core.update_layout(
                                            polar=dict(
                                            radialaxis=dict(
                                            visible=True,
                                            tickmode='linear',  # Definir o modo de escala linear
                                            tick0=0,            # Valor inicial do eixo
                                            dtick=1,            # Intervalo entre os ticks
                                            range=[0, 5]        # Ajuste aqui os valores mínimos e máximos do eixo radial
        )
    ),
    polar_bgcolor='#0E1117',)
    
    fig_nivel_core.add_annotation(
        text="Legenda: 1 = Fraco.  2 = Regular.  3 = Bom.  4 = Muito bom.  5 = Excelente",
        x=0.5,
        y=-0.20,  # Ajuste o valor de y para mais ou menos espaço
        showarrow=False,
        font=dict(size=14, color="white")
    )
    
    return fig_nivel_core
def plota_tonelagem_dia(tonelagem_dia):
    fig_tonelagem_dia = px.bar( tonelagem_dia,
                                title='Tonelagem do treinamento por sessão',
                                )
                                
    fig_tonelagem_dia.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Sessão',
                                yaxis_title='kg')
    
    fig_tonelagem_dia.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_tonelagem_dia
def plota_carga_interna_dia(carga_interna_dia):
    fig_carga_interna_dia = px.bar( carga_interna_dia,
                                title='Carga interna do treinamento por sessão')
                                
    fig_carga_interna_dia.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Sessão',
                                yaxis_title='UA')
    fig_carga_interna_dia.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_carga_interna_dia
def plota_tonelagem_semana(tonelagem_semana):
    tonelagem_semanax = tonelagem_semana.copy()
    tonelagem_semanax = tonelagem_semanax.drop('Diferença percentual', axis = 1)
    fig_tonelagem_semana = px.line( tonelagem_semanax,
                                markers= True,
                                title='Tonelagem do treinamento por semana') 
    
    fig_tonelagem_semana.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Semana',
                                yaxis_title='')
    fig_tonelagem_semana.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_tonelagem_semana
def plota_carga_interna_semana(carga_interna_semana):
    carga_interna_semanax = carga_interna_semana.copy()
    carga_interna_semanax = carga_interna_semanax.drop('Diferença percentual', axis = 1)
    fig_carga_interna_semana = px.line( carga_interna_semanax,
                                markers= True,
                                title='Carga interna do treinamento por semana') 
    fig_carga_interna_semana.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Semana',
                                yaxis_title='UA')
    fig_carga_interna_semana.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_carga_interna_semana
def plota_monotonia(df_monotonia):
    fig_monotonia = px.bar( df_monotonia,
                                title='Monotonia do treinamento por semana') 
    fig_monotonia.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Semana',
                                yaxis_title='UA')
    fig_monotonia.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_monotonia
def plota_strain(df_strain):
    fig_strain = px.bar( df_strain,
                                title='Strain do treinamento por semana') 
    fig_strain.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Semana',
                                yaxis_title='UA')
    fig_strain.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_strain
def plota_volume_semana(df_volume):
    fig_volume_semanal = px.line( df_volume,
                                markers= True,
                                title='Volume do treinamento por semana') 
    fig_volume_semanal.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Semana',
                                yaxis_title='kg')
    fig_volume_semanal.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_volume_semanal
def plota_intensidade_semana(df_intensidade):
    fig_intensidade_semanal = px.line( df_intensidade,
                                markers= True,
                                title='Intensidade do treinamento por semana') 
    fig_intensidade_semanal.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Semana',
                                yaxis_title='kg')
    fig_intensidade_semanal.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_intensidade_semanal
def plota_densidade_semana(df_densidade):
    fig_densidade_semanal = px.line( df_densidade,
                                markers= True,
                                title='Densidade do treinamento por semana') 
    fig_densidade_semanal.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Semana',
                                yaxis_title='kg')
    fig_densidade_semanal.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_densidade_semanal
def plota_series_semana(df_series):
    fig_series_semanal = px.line( df_series,
                                markers= True,
                                title='Séries do treinamento por semana') 
    fig_series_semanal.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Semana',
                                yaxis_title='kg')
    fig_series_semanal.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_series_semanal
def plota_series_dia(df_series_dia):
    fig_series_dia = px.bar( df_series_dia,
                                title='Séries por sessão de treinamento')
                                
    fig_series_dia.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Sessão',
                                yaxis_title='kg')
    fig_series_dia.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_series_dia
def plota_repeticoes_dia(df_repeticoes_dia):
    fig_repeticoes_dia = px.bar( df_repeticoes_dia,
                                title='Repetições por sessão de treinamento')
                                
    fig_repeticoes_dia.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Sessão',
                                yaxis_title='kg')
    fig_repeticoes_dia.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_repeticoes_dia
def plota_repeticoes_semana(df_repeticoes_semana):
    fig_repeticoes_semanal = px.line( df_repeticoes_semana,
                                markers= True,
                                title='Repetições do treinamento por semana') 
    fig_repeticoes_semanal.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Semana',
                                yaxis_title='kg')
    fig_repeticoes_semanal.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_repeticoes_semanal
def plota_pse_dia(pse_dia):
    fig_pse_dia = px.bar( pse_dia,
                                title='Percepção de esforço por sessão de treinamento')
                                
    fig_pse_dia.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Sessão',
                                yaxis_title='UA')
    fig_pse_dia.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_pse_dia
def plota_prs_dia_tr(prs_dia):
    fig_prs_dia = px.bar( prs_dia,
                                title='Percepção de recovery por sessão de treinamento de força')
                                
    fig_prs_dia.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Sessão',
                                yaxis_title='UA')
    fig_prs_dia.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_prs_dia
def plota_prs_dia_se(prs_dia_se):
    fig_prs_dia = px.bar( prs_dia_se,
                                title='Percepção de recovery por sessão de modalidade específica')
                                
    fig_prs_dia.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Sessão',
                                yaxis_title='UA')
    fig_prs_dia.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_prs_dia
def plota_pse_dia_se(pse_dia_se):
    fig_pse_dia = px.bar( pse_dia_se,
                                title='Percepção de esforço por sessão de modalidade específica')
                                
    fig_pse_dia.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Sessão',
                                yaxis_title='UA')
    fig_pse_dia.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_pse_dia
def plota_intervalo_dia(df_intervalo_dia):
    fig_intervalo_dia = px.bar( df_intervalo_dia,
                                title='Intervalo total por sessão de treinamento')
                                
    fig_intervalo_dia.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Sessão',
                                yaxis_title='kg')
    fig_intervalo_dia.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_intervalo_dia
def plota_densidade(densidade):
    fig_densidade = px.bar( densidade,
                                title='Densidade por sessão de treinamento')
                                
    fig_densidade.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Sessão',
                                yaxis_title='UA')
    fig_densidade.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_densidade
def plota_treinos_dia(treinos_dia):
    fig_treinos_dia = px.line( treinos_dia,
                                title='Treinos registrados por dia',
                                )
                                
    fig_treinos_dia.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Dia',
                                yaxis_title='',)
    fig_treinos_dia.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_treinos_dia
def plota_gasto_energetico_dia(df_gasto):
    fig_gasto_energetico_dia = px.bar( df_gasto,
                                title='Gasto calórico do exercício por dia')
                                
    fig_gasto_energetico_dia.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Sessão',
                                yaxis_title='UA')
    fig_gasto_energetico_dia.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_gasto_energetico_dia
def plota_gasto_energetico_semana(gasto_Calorico_semana):
    fig_gasto_energetico_semanal = px.line( gasto_Calorico_semana,
                                markers= True,
                                title='Gasto calórico total do treinamento por semana') 
    fig_gasto_energetico_semanal.update_layout(
                                xaxis={'tickangle': 0},
                                xaxis_title='Semana',
                                yaxis_title='kg')
    fig_gasto_energetico_semanal.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1 mês",
                        step="month",
                        stepmode="backward"),
                    dict(count=3,
                        label="3 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6 meses",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="1 ano",
                        step="year",
                        stepmode="backward"),
                    dict(step="all",
                        label="Tudo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_gasto_energetico_semanal
def highlight_diff(val):
            color = 'background-color: #286DC1' if val > 0 else 'background-color: red' if val < 0 else ''
            return color
