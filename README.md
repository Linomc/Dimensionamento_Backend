# Dimensionamento Back - End

A energia elétrica é um dos elementos essenciais no desenvolvimento econômico de um país, e as energias oriundas de fontes renováveis são protagonistas na revolução energética deste milênio.

A energia solar tem um imenso potencial e proporciona muitos benefícios para todos setores: iniciativa privada, poderes a união federativa e sociedade civil. Os geradores fotovoltaicos têm maturidade tecnológica, confiabilidade, competitividade 
econômica e o setor em franca expansão. O objetivo deste projeto, inicialmente, é realizar a análise exploratória do vetor (ou vetores) de entrada. 

O vetor de entrada nada mais é do que o consumo do local da futura usina fotovoltaica, para maior precisão dentro da máxima produtividade dentro de cada unidade de área tem-se que definir os grupos de consumo dentro de cada ciclo, que nada mais do que o ano. Os grupos são separados por meio dos quantis, para a partir daí identificar, quando houver, valores atípicos (outliers) e retira-los. 

Identicar também dentro de cada vetor o tipo de distribuição, para categorizar o consumo, avaliando como o conjunto de dados se comporta dentro de cada ciclo. Verificando assim se a gaussiana é: ou simétrica ou assimétrica (superior ou inferior). Após o tratamento inicial do conjunto de dados os códigos seguirão processamentos mais adequados para cada uma das categorias que serão desenvolvidas e ajustadas.

A saída é o dimensionamento do gerador fotovoltaico. 

# OBJETIVOS PRIMÁRIOS

* 1. Desenvolver uma metodologia de dimensionamento fotovoltaico para Unidades Consumidoras (UC) de Baixa Tensão (BT), onde qualquer pessoa jurídica ou especialista possa ter acesso a esse método para dimensionar novas usinas fotovoltaicas, com foco na otimização do GFV.
     
* 2. Contribuir para a mudança da matriz energética mundial, aumentando as ferramentas disponíveis para dimensionar geradores fotovoltaicos (GFV) em residências e comércios de pequeno porte.
     
* 3. Analisar, tratar e informar por meio da estatística e tecnologia da informação a partir de dados brutos, questões úteis, sem que os usuários de tais sistemas (dimensionamento de sistemas de energia solar), sejam especialistas em dimensionamento de sistemas solares ou experientes no setor de energias renováveis.
