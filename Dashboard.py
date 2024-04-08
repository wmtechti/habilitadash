import streamlit as st 
import pandas as pd
from PIL import Image
import logging
import modulos.fit_operacoes as fitoper
import sys

# Configuração básica do logging
# Configuração do logging para incluir data e hora
logging.basicConfig(level=logging.ERROR,
                    filename='app.log',
                    filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

try:

    st.set_page_config(layout='wide')

    image = Image.open('logo.png') 
    st.image(image, width= 500)  

    st.title("DASHBOARD DE PERFORMANCE")

    #dados 

    df = pd.read_csv('df_controle_de_carga.csv')
    df['data'] = pd.to_datetime(df['data'], format = 'mixed') 

    df_anamnese = pd.read_csv('dados_nivel_anamnese.csv')
    df_anamnese['data'] = pd.to_datetime(df_anamnese['data'], format = 'mixed')

    df_avaliacao_fisica = pd.read_csv('df_avaliacao_fisica.csv')
    df_avaliacao_fisica['data'] = pd.to_datetime(df_avaliacao_fisica['data'], format = 'mixed')

    ranking = fitoper.gera_df_ranking(df)

    treinos_dia = fitoper.gera_df_qtd_treinos_dia(df)

    processar = False
    # Filtros
    try:
        treinador = [df["treinador"].unique()]
        treinador_default = treinador[0]

        filtro_treinadores = st.sidebar.multiselect('Treinador', df['treinador'].unique(), max_selections=1)
        if filtro_treinadores:
            df = df[df['treinador'].isin(filtro_treinadores)]
            processar = True
        else:
            # logging.error('value error - selecione um treinador', exc_info=True)
            processar = False
            raise ValueError("Selecione um treinador.")

        alunos = [df["aluno"].unique()]
        aluno_default = alunos[0]

        filtro_alunos = st.sidebar.multiselect('Aluno', df['aluno'].unique(), max_selections=1)
        if filtro_alunos:
            df = df[df['aluno'].isin(filtro_alunos)]
            # Suponha que df_anamnese e df_avaliacao_fisica também precisam ser filtrados
            df_anamnese = df_anamnese[df_anamnese['aluno'].isin(filtro_alunos)]
            df_avaliacao_fisica = df_avaliacao_fisica[df_avaliacao_fisica['aluno'].isin(filtro_alunos)]
            processar = processar and True
        else:
            # logging.error('value error - selecione um aluno', exc_info=True)
            processar = False
            raise ValueError("Selecione um aluno.")

    except ValueError as ve:
        # logging.error(ve, exc_info=True)
        # Exibir a mensagem de erro do primeiro ValueError e continuar em caso de segundo ValueError
        st.error(str(ve))
        
    except Exception as e:
        # logging.error(e, exc_info=True)
        st.error(str(e))
        if isinstance(e, ValueError):
            # Ignorar outros ValueErrors
            pass
        else:
            # Lidar com outros tipos de exceção
            pass

    if not processar: 
        # logging.error('Aluno ou professor não selecionado. Saindo da execução!', exc_info=True)                
        sys.exit()
                
    # 1. Tabelas      
    # logging.error('Seguindo na execução!', exc_info=True)        
    df_nivel_questionario = fitoper.gera_df_nivel_questionario(df_avaliacao_fisica)

    df_nivel_testes_fisicos = fitoper.gera_df_nivel_testes_fisicos(df_avaliacao_fisica)

    df_antropometria = fitoper.gera_df_antropometria(df_avaliacao_fisica)

    df_imc = fitoper.gera_df_imc(df_avaliacao_fisica)

    df_antropometria_tronco = fitoper.gera_df_antropometria_tronco(df_avaliacao_fisica)

    df_antropometria_membros = fitoper.gera_df_antropometria_membros(df_avaliacao_fisica)

    df_velocidade_aerobia = fitoper.gera_df_velocidade_aerobia(df_avaliacao_fisica)

    df_vo2_estimado = fitoper.gera_df_vo2_estimado(df_avaliacao_fisica)

    df_forca_relativaI = fitoper.gera_df_forca_relativaI(df_avaliacao_fisica)

    forca_relativa_final = fitoper.gera_df_forca_relativa_final(df_forca_relativaI)

    df_potenciaI = fitoper.gera_df_potenciaI(df_avaliacao_fisica)

    potencia_final = fitoper.gera_df_potencia_final(df_potenciaI)

    df_classificacao_flexibilidade = fitoper.gera_df_classificacao_flexibilidade(df_avaliacao_fisica)

    flexibilidade_classificacao_final = fitoper.gera_df_classificacao_flexibilidade_final(df_classificacao_flexibilidade)

    df_flexibilidade = fitoper.gera_df_nivel_flexibilidade(df_avaliacao_fisica)

    flexibilidade_final = fitoper.gera_df_flexibilidade_final(df_flexibilidade)

    df_coreI = fitoper.gera_df_coreI(df_avaliacao_fisica)

    core_final = fitoper.gera_df_core_final(df_coreI)

    df_nivel_core_pontos = fitoper.gera_df_nivel_core_pontos(df_avaliacao_fisica)

    tonelagem_dia = fitoper.gera_df_tonelagem_dia(df)

    tonelagem_semana = fitoper.gera_df_tonelagem_semana(df)

    carga_interna_dia = fitoper.gera_df_carga_interna_dia(df)

    carga_interna_semana = fitoper.gera_df_carga_interna_semana(df)

    df_monotonia, df_strain = fitoper.gera_df_monotonia_strain(df)

    df_monotonia, df_strain = fitoper.gera_df_monotonia_strain(df)

    df_monotonia_total, strain_total = fitoper.monotonia_total(df_monotonia, df_strain)

    df_volume = fitoper.gera_df_volume(df)

    df_intensidade = fitoper.gera_df_intensidade(df)

    df_series_dia = fitoper.gera_df_series_dia(df)

    df_repeticoes_dia = fitoper.gera_df_repeticoes_dia(df)

    tonelagem_dia = fitoper.gera_df_tonelagem_dia(df)

    df_repeticoes_semana = fitoper.gera_df_repeticoes_semana(df)

    df_series = fitoper.gera_df_series(df, df_intensidade)

    pse_dia = fitoper.gera_df_pse_dia(df)

    prs_dia = fitoper.gera_df_prs_dia(df)

    prs_dia_se = fitoper.gera_df_prs_dia_se(df)

    pse_dia_se = fitoper.gera_df_pse_dia_se(df)

    df_densidade = fitoper.gera_df_densidade(df)

    df_intervalo_dia = fitoper.gera_df_intervalo_dia(df)

    df_gasto = fitoper.gera_df_gasto(df)

    gasto_Calorico_semana = fitoper.gera_df_Gasto_Calorico_semana(df)

    # 2. Figuras
    fig_ranking = fitoper.plota_ranking(ranking)

    fig_treinos_dia = fitoper.plota_treinos_dia(treinos_dia)

    fig_medidas_imc = fitoper.plota_medidas_imc(df_imc)

    fig_medidas_tronco = fitoper.plota_medidas_tronco(df_antropometria_tronco)

    fig_medidas_membros = fitoper.plota_medidas_membros(df_antropometria_membros)

    fig_ranking = fitoper.plota_ranking(ranking) 

    fig_ranking = fitoper.plota_ranking(ranking)

    fig_nivel_questionario = fitoper.plota_nivel_questionario(df_nivel_questionario)

    fig_nivel_testes_fisicos = fitoper.plota_nivel_testes(df_nivel_testes_fisicos)

    fig_forca_relativa_final = fitoper.plota_forca_relativa_final(forca_relativa_final)

    fig_potencia_final = fitoper.plota_potencia_final(potencia_final)

    fig_velocidade_aerobia = fitoper.plota_velocidade_aerobia(df_velocidade_aerobia)

    fig_vo2_estimado = fitoper.plota_vo2_estimado(df_vo2_estimado, df_vo2_estimado)

    fig_classificacao_flexibilidade = fitoper.plota_flexibilidade_tabela(flexibilidade_classificacao_final)

    fig_classificacao_antropometria = fitoper.plota_antropometria_tabela(df_antropometria)

    fig_flexibilidade_ombro = fitoper.plota_flexibilidade_ombro(flexibilidade_final)

    fig_flexibilidade_quadril = fitoper.plota_flexibilidade_quadril(flexibilidade_final)

    fig_flexibilidade_tornozelo = fitoper.plota_flexibilidade_tornozelo(flexibilidade_final)

    fig_core_final = fitoper.plota_core_final(core_final)

    fig_nivel_core = fitoper.plota_nivel_core(df_nivel_core_pontos)

    fig_tonelagem_dia = fitoper.plota_tonelagem_dia(tonelagem_dia)

    fig_carga_interna_dia = fitoper.plota_carga_interna_dia(carga_interna_dia)

    fig_tonelagem = fitoper.plota_tonelagem_semana(tonelagem_semana)

    fig_carga_interna_semana = fitoper.plota_carga_interna_semana(carga_interna_semana)

    fig_monotonia = fitoper.plota_monotonia(df_monotonia)

    fig_strain = fitoper.plota_strain(df_strain)

    fig_volume = fitoper.plota_volume_semana(df_volume)

    fig_intensidade = fitoper.plota_intensidade_semana(df_intensidade)

    fig_densidade = fitoper.plota_densidade_semana(df_densidade)

    fig_series = fitoper.plota_series_semana(df_series)

    fig_series_dia = fitoper.plota_series_dia(df_series_dia)

    fig_repeticoes_dia = fitoper.plota_repeticoes_dia(df_repeticoes_dia)

    fig_repeticoes_semana = fitoper.plota_repeticoes_semana(df_repeticoes_semana)

    fig_pse_dia = fitoper.plota_pse_dia(pse_dia)

    fig_prs_dia_tr = fitoper.plota_prs_dia_tr(prs_dia)

    fig_prs_dia_se = fitoper.plota_prs_dia_se(prs_dia_se)

    fig_pse_dia_se = fitoper.plota_pse_dia_se(pse_dia_se)

    fig_intervalo_dia = fitoper.plota_intervalo_dia(df_intervalo_dia)

    fig_densidade = fitoper.plota_densidade(df_densidade)

    fig_treinos_dia = fitoper.plota_treinos_dia(treinos_dia)

    fig_gasto_energetico_dia = fitoper.plota_gasto_energetico_dia(df_gasto)

    fig_gasto_energetico_semana = fitoper.plota_gasto_energetico_semana(gasto_Calorico_semana)

    # 3. Streamlit
    aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs(["Ranking", "Perfil e medidas", "Overview de performance", "Controle de carga", "Controle de variáveis", "Perfil calórico"])

    with aba1:
        coluna1, coluna2 = st.columns(2)
        with coluna1:
            #st.header("Ranking")
            st.plotly_chart( fig_ranking, use_container_width = True )
            
        with coluna2:
            #st.header("Treinos dia")
            st.plotly_chart( fig_treinos_dia, use_container_width = True )

    with aba2:
        coluna1, coluna2 = st.columns(2)
        with coluna1:
            nome = filtro_alunos[0]
            modalidade_especifica = df_avaliacao_fisica['modalidadeExtra'].unique()
            modalidade_especifica = modalidade_especifica.item()
            st.metric('Nome', nome)
            st.metric('Modalidade específica', modalidade_especifica)
            st.header("Composição corporal")
            
            #IMC
            imc = df_imc
            last_row = (imc.iloc[-1]).round(2)
            delta_color = 'inverse' if last_row['Diferença percentual'] < 0 else 'normal'
            st.metric(label='IMC atual',
                        value=last_row['IMC'],
                        delta=f'{last_row["Diferença percentual"]:.2f}%',
                        delta_color=delta_color)
            classificacao_imc = df_avaliacao_fisica.ClassificacaoIMC.iloc[-1]
            st.metric('Classificação do IMC', classificacao_imc)
            st.plotly_chart( fig_medidas_imc, use_container_width = True )
            
            #Massa magra
            massa_magra = 'nan'
            st.metric('Massa magra', massa_magra)
            st.plotly_chart( fig_medidas_imc, use_container_width = True )
            
            #Antropometria
            st.header("Antropometria")
            st.plotly_chart( fig_medidas_tronco, use_container_width = True )
            
        with coluna2:
            objetivo = df_avaliacao_fisica.Objetivo.unique()
            objetivo = objetivo.item()
            st.metric('Objetivo', objetivo)
            parq = 'negativo'
            st.metric('PAR-Q', parq)
            #st.plotly_chart( fig_treinos_dia, use_container_width = True)
            st.header(".")
            
            #Massa gorda
            imc = df_imc #atualizar para massa gorda
            last_row = (imc.iloc[-1]).round(2) #atualizar para massa gorda
            delta_color = 'inverse' if last_row['Diferença percentual'] < 0 else 'normal' #atualizar para massa gorda
            st.metric(label='Percentual de gordura', #atualizar para massa gorda
                        value=last_row['IMC'], #atualizar para massa gorda
                        delta=f'{last_row["Diferença percentual"]:.2f}%', #atualizar para massa gorda
                        delta_color=delta_color) #atualizar para massa gorda
            classificacao_imc = df_avaliacao_fisica.ClassificacaoIMC.iloc[-1] #atualizar para massa gorda
            classificacao_massa_magra = 'nan'
            st.metric('Classificação da massa magra', classificacao_massa_magra) #atualizar para massa gorda
            st.plotly_chart( fig_medidas_imc, use_container_width = True ) #atualizar para massa gorda
            classificacao_massa_gorda = 'nan'
            st.metric('Classificação da massa massa', classificacao_massa_gorda)
            st.plotly_chart( fig_medidas_imc, use_container_width = True )
            st.header(".")
            st.plotly_chart( fig_medidas_membros, use_container_width = True )
            
            # Crie um DataFrame de diferenças para destacar
            #diffs_df = df_antropometria.diff(axis=1)
            # Crie um DataFrame de estilos
            #styles_df = diffs_df.applymap(highlight_diff)
            # Exibir o DataFrame estilizado usando Streamlit
            #st.dataframe(df_antropometria.style.format({"Data": "{:%Y-%m-%d}"}).format("{:.1f}").apply(lambda _: styles_df, axis=None))

    with aba3:
        coluna1, coluna2 = st.columns(2)
        with coluna1:
            modalidade_especifica = df_avaliacao_fisica['modalidadeExtra'].unique()
            modalidade_especifica = modalidade_especifica.item()
            st.metric('Nome', nome)
            objetivo = df_avaliacao_fisica.Objetivo.unique()
            objetivo = objetivo.item()
            st.metric('Objetivo', objetivo)
            
            st.header("Níveis de treinamento")
            st.plotly_chart( fig_nivel_questionario, use_container_width = True )
            st.header("Performance neuromuscular")
            st.plotly_chart( fig_forca_relativa_final, use_container_width = True )
            st.header("Performance Cardiorrespirória")
            vo2_estimado = df_avaliacao_fisica.vo2_estimado.iloc[-1]
            st.metric('VO2 máximo estimado (mL / kg / min)', vo2_estimado)
            st.plotly_chart( fig_velocidade_aerobia, use_container_width = True )
            st.header("Core")
            st.plotly_chart( fig_nivel_core, use_container_width = True )
            st.header("Mobilidade e flexibilidade")
            st.plotly_chart( fig_flexibilidade_tornozelo, use_container_width = True )
            st.plotly_chart( fig_flexibilidade_quadril, use_container_width = True )
            
        with coluna2:
            #st.header(".")
            st.metric('Modalidade específica', modalidade_especifica)
            
            #nivel_vo2 = nivel_vo2.item()
            st.metric('Treinos registrados', df.shape[0])
            #st.metric('Treinos registrados', df.shape[0])
            st.header(".")
            st.plotly_chart( fig_nivel_testes_fisicos, use_container_width = True  )
            st.header(".")
            st.plotly_chart( fig_potencia_final, use_container_width = True )
            st.header(".")
            nivel_vo2 = df_avaliacao_fisica.nivel_vo2.iloc[-1]
            st.metric('Capacidade aeróbia', nivel_vo2)
            st.plotly_chart( fig_vo2_estimado, use_container_width = True )
            st.header(".")
            st.plotly_chart( fig_core_final, use_container_width = True )
            st.header(".")
            st.plotly_chart( fig_flexibilidade_ombro, use_container_width = True )
            st.header("")
            st.write('**Classificação de acordo com valores de amplitude de movimento por articulação**')
            def color_vowel(value):
                return f"background-color: red;" if value in ["reduzida"] else None
            st.dataframe(flexibilidade_classificacao_final.style.applymap(color_vowel))
            
    with aba4:
        coluna1, coluna2 = st.columns(2)
        with coluna1:
            last_row = tonelagem_semana.iloc[-1]
            delta_color = 'inverse' if last_row['Diferença percentual'] < 0 else 'normal'
            st.metric(label='Tonelagem',
                        value=last_row[0]/1000,
                        delta=f'{last_row["Diferença percentual"]:.2f}%',
                        delta_color=delta_color)
            st.plotly_chart( fig_tonelagem, use_container_width = True )
            
            last_row = df_monotonia_total.iloc[-1]
            delta_color = 'inverse' if last_row['Diferença percentual'] < 0 else 'normal'
            st.metric(label='Monotonia',
                        value=last_row['Valor'],
                        delta=f'{last_row["Diferença percentual"]:.2f}%',
                        delta_color=delta_color)
            st.plotly_chart( fig_monotonia, use_container_width = True )
            st.plotly_chart( fig_tonelagem_dia, use_container_width = True )
            st.plotly_chart( fig_densidade, use_container_width = True )
            st.plotly_chart( fig_prs_dia_se, use_container_width = True )
            
        with coluna2:
            last_row = carga_interna_semana.iloc[-1]
            delta_color = 'inverse' if last_row['Diferença percentual'] < 0 else 'normal'
            st.metric(label='Carga Interna',
                        value=last_row[0],
                        delta=f'{last_row["Diferença percentual"]:.2f}%',
                        delta_color=delta_color)
            st.plotly_chart( fig_carga_interna_semana, use_container_width = True)
            
            last_row = (strain_total.iloc[-1]).round(2)
            delta_color = 'inverse' if last_row['Diferença percentual'] < 0 else 'normal'
            st.metric(label='Strain',
                        value=last_row['Valor'],
                        delta=f'{last_row["Diferença percentual"]:.2f}%',
                        delta_color=delta_color)
            st.plotly_chart( fig_strain, use_container_width = True )
            st.plotly_chart( fig_carga_interna_dia, use_container_width = True )
            st.plotly_chart( fig_prs_dia_tr, use_container_width = True )
            st.plotly_chart( fig_pse_dia_se, use_container_width = True )
            
    with aba5:
        coluna1, coluna2 = st.columns(2)
        with coluna1:
            st.plotly_chart( fig_volume, use_container_width = True )
            st.plotly_chart( fig_series, use_container_width = True )
            st.plotly_chart( fig_repeticoes_semana, use_container_width = True )
            st.plotly_chart( fig_intervalo_dia, use_container_width = True )
            
        with coluna2:
            st.plotly_chart( fig_intensidade, use_container_width = True )
            st.plotly_chart( fig_series_dia, use_container_width = True )
            st.plotly_chart( fig_repeticoes_dia, use_container_width = True )
            st.plotly_chart( fig_pse_dia, use_container_width = True )

    with aba6: 
        last_row = gasto_Calorico_semana.iloc[-1]
        delta_color = 'inverse' if last_row['Diferença percentual'] < 0 else 'normal'
        st.metric(label='Gasto calórico da semana atual',
                        value=last_row[0],#/1000,
                        delta=f'{last_row["Diferença percentual"]:.2f}%',
                        delta_color=delta_color)
            
        st.plotly_chart( fig_gasto_energetico_semana, use_container_width = True )
        st.plotly_chart( fig_gasto_energetico_dia, use_container_width = True )

  
finally:
    print("finalizou por exceção!")    
