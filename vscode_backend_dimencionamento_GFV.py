# %% [markdown]
# # Backend do Sistema de Dimensionamento de Micro Usinas Fotovoltaicas a partir do consumo.
# 
# * Início no dia 16/01.
# 

# %% [markdown]
# # Função 01 (1 lista apenas)- tratamento de dados básicos
# 
# 1. Preparando conjunto de dados para quaisquer análise
# 2. Função recebe uma lista com os valores do consumo de energia (kwh/mês), com os valores desordenados.
# 
#     2,1. As saídas serão:        
#         2,1,1. lista ordenada de dados
#         2,1,2. Mínimo (mi) 
#         2,1,3. Quartil 1 (Q1)
#         2,1,4. Quartil 2 (Q2)
#         2,1,5. Quartil 3 (Q3)
#         2,1,6. Máximo (ma)

# %%
# Função que cria os intervalos para os grupos ( preparando assim p/ identificar a distribuição e dados atipicos)
def trata_dados(meses):
    consumo_mensal = sorted(meses)
    # Etapa da separação em Percentis, 4 classes de dados, definição das classes de dados.
    minimo = min(consumo_mensal)
    P25 = round (0.25*len(consumo_mensal))
    P50 = round (0.50*len(consumo_mensal))
    P75 = round (0.75*len(consumo_mensal))
    maximo = max(consumo_mensal)
    #Etapa Quartis
    Q1 = round (((consumo_mensal[(P25-1)]) + (consumo_mensal[(P25)]))/2, 1)
    Q2 = round (((consumo_mensal[(P50-1)]) + (consumo_mensal[(P50)]))/2, 1)
    Q3 = round (((consumo_mensal[(P75-1)]) + consumo_mensal[P75])/2, 1)
    return minimo, Q1, Q2, Q3, maximo, consumo_mensal

# %%
# teste da função
conta_energia = [1532,1472,1553,1479,1486,1206,1454,1552,146,101,1590,1217]
consumo_mensal, minimo, Q1, Q2, Q3, maximo = trata_dados(conta_energia)
print (consumo_mensal, minimo, Q1, Q2, Q3, maximo)

# %% [markdown]
# ## Recriar a Função 01 - Trata dados com as Bibliotecas STATISTICS e NUMPY
# - criada em 09/03

# %%
import statistics as stat
import numpy as np
from pandas import Series, read_excel

def trata_dados_stat(dados):
    vetor = sorted(dados)
    quartis = stat.quantiles(vetor, n=4, method= 'inclusive')
    return quartis, vetor

def trata_dados_np (dados):
    vetor = sorted(dados)
    quartis = list(np.quantile(vetor, [0.25,0.50,0.75]))
    return quartis, vetor

def trata_dados_pd (dados):
    vetor_df = pandas.read_excel(dados, sep = '\t', encoding= 'latin1')
    tamanho, media, std, minimo, um_quarto, metade, tres_quartos, maximo  = Series.describe(vetor_df)
    return minimo, um_quarto, metade, tres_quartos, maximo, vetor_df

# %%
# teste da Função recriada com as bibliotecas Numpy, statistic e pandas
conta_energia = [1532,1472,1553,1479,1486,1206,1454,1552,146,101,1590,1217]
quartis = trata_dados_stat(conta_energia)
Q1 = trata_dados_np(conta_energia)
print (quartis)
print (Q1)

# %% [markdown]
# # Função 02 - Retira quando houver - Outiliers Inferiores
# 
# - atualizada em 01/03

# %%
def retira_outliers(meses):
    consumo_ordenado, minimo, Q1, Q2, Q3, maximo = trata_dados(meses)
    lista_limpa = [
        consumo 
        for consumo in meses 
        if consumo > 180 and consumo > (Q1 - (Q3-Q1)*1.5)
    ]
    return lista_limpa

# %%
# teste da função 2
conta_energia = [1532,1472,1553,1479,1486,1206,1454,1552,146,101,1590,1217]
lista_limpa = retira_outliers(conta_energia)
print (lista_limpa)

# %% [markdown]
# # Funcao 03 - ordena lista limpa de outliers
# 
# - criada em 05/03
# - Quando houver outliers

# %%
def lista_limpa_ordenada(meses):
    consumo_limpo = retira_outliers(meses)
    consumo_limpo.sort()
    return consumo_limpo

# %%
# teste da função 3
conta_energia = [1532,1472,1553,1479,1486,1206,1454,1552,146,101,1590,1217]
lista_ordenada = lista_limpa_ordenada(conta_energia)
print (lista_ordenada)

# %% [markdown]
# # Função 04 - Distribuição do conjunto
# 
# - atualizada em 06/03
# 
# * Essa função faz a distribuição normal (gaussiana) dos dados:    
#     1.Retorna duas saídas:
#         * dicionario com o valor entre quartis, potencial total do conjunto
#     

# %%
def distribuicao (meses):
    meses_limpos = lista_limpa_ordenada(meses)
    consumo_ordenado, minimo, Q1, Q2, Q3, maximo = trata_dados(meses_limpos)
    interquartis = ((Q1,Q3), (minimo,Q1), (Q1,Q2), (Q2,Q3), (Q3,maximo))
    grupamentos = ('simetrica','25%', '50%', '75%', '100%')
    potencial_total = sum(meses_limpos)
    distribuicao = {}
    for i, grupo in enumerate(interquartis):
        distribuicao[grupamentos[i]] = round((sum(mes for mes in meses_limpos if grupo[0] <= mes < grupo[1])/potencial_total),2) 
    return distribuicao

# %%
# teste da função 04
conta_energia = [1532,1472,1553,1479,1486,1206,1454,1552,1146,101,1590,1217]
gaussiana = distribuicao(conta_energia)
print (gaussiana)

# %% [markdown]
# # Funcao 05 - histograma da Distribuição do Conjunto
# 
# - criado 06/03

# %%
# essa função ta conceitualmente errada.. 24/03. ainda não repensei essa saída
import matplotlib.pyplot as plt
def histograma(meses):
    resumo_conjunto = distribuicao(meses)
    chaves_dados = list(resumo_conjunto)
    valores_dados = list(resumo_conjunto.values())
    # falta criar a parte gráfica.

# %% [markdown]
# # Função 06 - Qualifica a distribuição do conjunto
# 
# * Essa função verificará a distribuição normal (gaussiana) dos dados e seus percentuais:    
#     1.Simétrica;    
#     2.Assimétrica:
#         * inferior
#         * superior

# %%
def peso_distribuicao(meses):
    distribuicoes = distribuicao(meses)
    qualifica_conjunto = [chave for chave, valor in distribuicoes.items() if valor >= 50]
    return qualifica_conjunto

# testando função

conta_energia = [1532,1472,1553,1479,1486,1206,1454,1552,146,101,1590,1217]
gaussiana = peso_distribuicao(conta_energia)

# Verificando resultados da Função: Saídas 
print (gaussiana)

# %% [markdown]
# # Função 07 (01 lista apenas) - Resumo de um conjunto de dados
# ## Tem a centralidade e a dispersão de dados.
# 
# 1. usa os dados de saída (return) da função 01 (trata_dados)
# 2. Essa função pegará os dados tratados da função 01 e terá como saída:
#     1. média aritmética **(X)** do consumo (potência anual)
#     2. Desvio Padrão **(DP)** do consumo (potência anual)
#     3. A função (trata_dados) possui 5 saídas **(Q1, Q3, AIQ, Consumo normalizados, outliers quando houver)**

# %%
# 24/03 - vou refazer essa função se necessario, usando os metodos de uma das bibliotecas: Numpy, Pandas ou Statistic
# obs. Na epoca que criei essa função não conhecia os metodos
def medidas_centralidade (meses):
    consumo_anual_limpo = retira_outliers(meses)
    potencia_total = float(sum(consumo_anual_limpo))
    media = (potencia_total/(len(consumo_anual_limpo)))
    variacao_mensal = sum((mes-media)**2 for mes in consumo_anual_limpo) # variância do consumo mensal
    dm = sum(abs(mes-media) for mes in consumo_anual_limpo) # desvio medio dos dados
    variacao_mensal = variacao_mensal/(len(consumo_anual_limpo)-1) # dados amostrais, por isso a população -1.
    dm = round(dm/(len(consumo_anual_limpo)-1),2) # dados amostrais, por isso a população -1.
    dp_consumo = round((variacao_mensal)**(0.5),2)    
    return (media, dm, dp_consumo)

# %%
# testa funcao 07
conta_energia = [1532,1472,1553,1479,1486,1206,1454,1552,146,101,590,617]
media, dm, dp = medidas_centralidade(conta_energia)
print (media, dm, dp)


# %% [markdown]
# # Função 08 (1 lista de dados apenas de consumo e uma da estação) - kWp 
# ***
# ### Dimensiona a potência pico cheia, a partir dos dados de entrada ( consumo e estação climática)
# 
# - **IMPORTANTE**
# 
# > Essa função 03, **retorna a POTÊNCIA PICO Cheia**, a partir da soma das medidas de **Centralidade + Dispersão**

# %%
# 25/03 - Obs. recebera os dataframes de um banco de dados, a partir do database das estacoes meteorologicas, sera criada a funcao que definirá o estação. 
def pot_pico (meses, estacao):
    X,dm,dp = medidas_centralidade(meses)
    media_estacao = round(sum(estacao)/len(estacao),2)
    W_X_diaria = round((X+dp)/30,2) # usando a referência d tamanho de mês o menor mês do ano bissexto.
    Wp_media = round((W_X_diaria/media_estacao)/0.75,2)
    return Wp_media

# %%
# teste da funcao
# referencia d dados, estação: jan, fev, mar, abr, mai, jun, jul, ago, set, out, nov, dez, media aritmetica
estacao_caxias = [5.86,6.05,4.96,4.36,3.60,3.38,3.37,4.17,4.35,4.86,4.87,5.61]
conta_energia = [1532,1472,1553,1479,1486,1206,1454,1552,146,101,590,617]
# executando a função:
print (pot_pico(conta_energia,estacao_caxias))

# %% [markdown]
# # Função 8.1 (1 lista de dados apenas de consumo e uma da estação) - kWp 
# ***
# ### Dimensiona a potência pico ajustada, a partir dos dados de entrada ( consumo, estação climática, percentual)
# 
# - **IMPORTANTE**
# 
# > Essa função 3.1, **retorna a POTÊNCIA PICO ajustada**, a partir das medidas de **Centralidade + (% * Dispersão)**
# > Essa **(% * DP)** é uma correção sobre o necessário, assim pode variar dimensionamento a partir da necessidade que o lead solicita e é incorporado no dimensionamento diretamente. 

# %%
def pot_pico_ajustada (consumo, estacao, pdp = 10): # Será usado por padrão apenas 10% da potência do DP.
    X,dm,dp = medidas_centralidade(consumo)
    perc_dp_X = round((dp/X)*100,2)
    media_estacao = round(sum(estacao)/len(estacao), 2)
# Nessa etapa estou refletindo, sobre qual caminho seguir. coloco o peso do DP de acordo com o resultado da Distribuição
    W_X_diaria = round((X+(round(pdp/100,2)*dp))/30,2) # usando a referência d tamanho de mês o menor mês do ano bissexto.
    Wp_media = round((W_X_diaria/media_estacao)/0.75,2)
    return Wp_media, perc_dp_X

# %%
#import matplotlib.pyplot as grf
# referencia d dados, estação: jan, fev, mar, abr, mai, jun, jul, ago, set, out, nov, dez, media aritmetica
estacao_caxias = [5.86,6.05,4.96,4.36,3.60,3.38,3.37,4.17,4.35,4.86,4.87,5.61]
conta_energia = [1532,1472,1553,1479,1486,1206,1454,1552,146,101,590,617]
# executando a função:
kWp, DP = pot_pico_ajustada(conta_energia,estacao_caxias)
print ('Potência pico, {} KWp da conta de energia, e o Desvio Padrão da conta é de, {}%'.format(kWp, DP))

# %% [markdown]
# # Função 09- Ajusta Pot. do GFV a partir da escolha dos módulos 
# 
# - ainda não foi atualizado
# - Essa função se encaixa melhor se for acoplado um Banco de dados, assim que for aprendido por mim irei atualizar.
# ---

# %%
def dimUFV (energia, estacao, percentual = 100): # ainda não me organizei para ajustar o dimensionamento para < 100%.
    modulos = {
    'empalux 605':(605, 2.83, 1.3, 2.17, 35, 18.39, 41.80, 17.35, 34.88, 14.63, 31.79, 30),
    'empalux 690':(690,3.11, 1.3, 2.38, 30, 18.90, 46.62, 17.75, 38.88, 14.46, 43.91, 30),
    'elgin 590':(590, 2.77, 1.13, 2.28, 35, 13.94, 53.70, 25),
    'elgin 550':(550, 2,58, 1,13, 2.28, 35, 14.04, 49.60, 25)
    }
    kwp, dp = pot_pico_ajustada(energia, estacao)
    pot_ufv = int(kwp * 1000)
    escolha = 'n'
    modelo = list(modulos)
    contador = 0
    while escolha != 's':
        if contador <= 3 and escolha != 's':
            escolha = input ('s- sim para escolha, n- para recusa. Para o {}: '.format(modelo [contador]))
            contador += 1
        else:
            contador = 0
    # daqui para baixo é construido o dimensionamento a partir da marca e modelo de módulos que estão no dicionário.        
    valores = modulos [modelo[contador - 1]]
    if (pot_ufv%valores[0] != 0): # valores[0] é a potencia do modelo escolhido de módulo. Se a divisão tiver resto, soma 1.
        kwp_ajustado = round(((int(pot_ufv/valores[0]) + 1) * valores [0]) / 1000, 2)
        numero_modulos = int(pot_ufv/valores[0]) + 1
    else:
        kwp_ajustado = round(((pot_ufv/valores[0]) * valores [0]) / 1000, 2)
        numero_modulos = int(pot_ufv/valores[0])
    # saída será a potência ajustada ao menor número unitário de módulos possível.
    return kwp_ajustado, numero_modulos, modelo[contador -1]    

# %%
estacao_caxias = [5.86,6.05,4.96,4.36,3.60,3.38,3.37,4.17,4.35,4.86,4.87,5.61,4.62]
conta_energia = [1532,1472,1553,1479,1486,1206,1454,1552,146,101,590,617]
# executando a função:
kWp, qtde_modulos, modelo = dimUFV(conta_energia,estacao_caxias, 50)
print ('Potência pico, {} KWp da conta de energia, e {} módulos, modelo {}.'.format(kWp, qtde_modulos, modelo))

# %% [markdown]
# #  Função 09.1 - Desmembrando Função 07 em 2 funções.
# 
# ## Parte 01:
# 
# - criado em 03/03/2023
# - Escolha do módulo.

# %%
def Modulos ():    
    modelos = ('empalux 605','empalux 690','elgin 590','elgin 550') # no futuro será um BD atualizado de produtos.
    escolha,contador = 'n', 0     
    while escolha != 's':
        escolha = input ('s- sim para escolha, n- para recusa. Para o {}: '.format(modelos [contador]))
        if contador == 3 and escolha != 's':            
            contador = -1
        contador += 1
    return modelos[contador -1]    

# %%
modulo = Modulos()
print (modulo)


# %% [markdown]
# #  Função 09.2 - Desmembrando Função 07 em 2 funções.
# 
# ## Parte 02:
# 
# - criado em 03/03/2023
# - Potência do sistema ajustada a partir da escolha do modelo do módulo.

# %%
def GFV_Modulo (energia, estacao):
    modulos = {
    'empalux 605':(605, 2.83, 1.3, 2.17, 35, 18.39, 41.80, 17.35, 34.88, 14.63, 31.79, 30),
    'empalux 690':(690,3.11, 1.3, 2.38, 30, 18.90, 46.62, 17.75, 38.88, 14.46, 43.91, 30),
    'elgin 590':(590, 2.77, 1.13, 2.28, 35, 13.94, 53.70, 25),
    'elgin 550':(550, 2,58, 1,13, 2.28, 35, 14.04, 49.60, 25)
    }
    modelo = Modulos()
    kwp, dp = pot_pico_ajustada(energia, estacao)
    pot_ufv, valores = int(kwp * 1000), modulos[modelo]
    if (pot_ufv%valores[0] != 0): # valores[0] é a potencia do modelo escolhido de módulo. Se a divisão tiver resto, soma 1.
        kwp_ajustado = round(((int(pot_ufv/valores[0]) + 1) * valores [0]) / 1000, 2)
        numero_modulos = int(pot_ufv/valores[0]) + 1
    else:
        kwp_ajustado = round(((pot_ufv/valores[0]) * valores [0]) / 1000, 2)
        numero_modulos = int(pot_ufv/valores[0])
    area_modulos = int(numero_modulos*valores[1]) + 1
    return kwp_ajustado, numero_modulos, area_modulos, modelo

# %%
estacao_caxias = [5.86,6.05,4.96,4.36,3.60,3.38,3.37,4.17,4.35,4.86,4.87,5.61]
conta_energia = [1532,1472,1553,1479,1486,1206,1454,1552,146,101,590,617]
kwp, total_modulos, area, modelo = GFV_Modulo(conta_energia, estacao_caxias)
print ('\n', kwp, 'kwp')
print (total_modulos, 'módulos')
print ('area em módulos', area)

# %% [markdown]
# # Função 10 - Geração mensal de energia.
# 
# * Início dia 25/01.

# %%

def grf_kwh_kwp (conta, estacao):    
    kwp, numero_modulos, potencia_modulo = dimUFV(conta, estacao)
    numero_dias_mes= (31,27,31,30,31,30,31,31,30,31,30,31)
    meses = ('jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez')
    Ger_UFV = []
    for i, dia in enumerate(estacao): # esse loop precisa acessar duas listas
        kwh_mes = round ((dia * kwp * numero_dias_mes[i]),1) # escrevi essa linha para deixar explicito o cálculo da 
        Ger_UFV.append(kwh_mes)
    kwh_ano = round(sum(Ger_UFV),1)
    
    return Ger_UFV, kwh_ano    

# %% [markdown]
# 
# # Teste do resultado algébrico e vetorial da Função 05
# 
# ### Estou revendo a potência de dimensionamento de GFV, está ótima margem de segurança, mas fora da potência que a concorrência oferece, para essa média de consumo.
# 
# # Preciso refletir, qual caminho tomar

# %%
estacao_caxias = [5.86,6.05,4.96,4.36,3.60,3.38,3.37,4.17,4.35,4.86,4.87,5.61]
conta_energia = [1532,1472,1553,1479,1486,1206,1454,1552,1046,1201,1590,1217]
consumo_ano = sum(conta_energia)
kwh_mes, kwh_ano = grf_kwh_kwp(conta_energia , estacao_caxias)
print (kwh_ano, consumo_ano)
print(kwh_mes)
#

# %%
import locale
import calendar as clnd
locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')
localizacao = locale.setlocale(locale.LC_ALL,'pt_BR')
#print (locale.currency(43223.2, grouping=True))

ano = clnd.monthrange(2023,3)[1]
print (ano)

# %% [markdown]
# # F.10.1 - Função 10 ajustada - 
# 
# * início 26/01.

# %%
import locale
from calendar import month_abbr, monthrange
def grf_kwh_kwp (conta, estacao):
    locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')
    kwp, numero_modulos, potencia_modulo = dimUFV(conta, estacao)
    meses = tuple(month_abbr[1:1+12])
    Ger_UFV = [
        round((dia * kwp * (monthrange(2023,(i+1))[1])),1) 
        for i, dia in enumerate(estacao)
    ]
    kwh_ano = round(sum(Ger_UFV),1)    
    return Ger_UFV, kwh_ano

# %% [markdown]
# # Teste da Função 05 ajustada - F.5.1 

# %%
estacao_caxias = [5.86,6.05,4.96,4.36,3.60,3.38,3.37,4.17,4.35,4.86,4.87,5.61]
conta_energia = [1532,1472,1553,1479,1486,1206,1454,1552,1046,1201,1590,1217]
ger_mensal, ger_anual = grf_kwh_kwp(conta_energia, estacao_caxias)

print (ger_anual)


