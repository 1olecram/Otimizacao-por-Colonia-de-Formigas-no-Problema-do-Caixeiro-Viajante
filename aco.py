import csv
import random

def calcula_probabilidade(cidade_atual, linha_distancias, linha_feromonio, cidades_visitadas, alfa=1.0, beta=5.0):
    """
    Calcula a probabilidade de uma formiga ir para outras cidades
    considerando o feromônio (tau) e a visibilidade (eta = 1 / distância).
    """
    if cidades_visitadas is None:
        cidades_visitadas = set() #sets são coleções não ordenadas de itens únicos
        
    probabilidades = []
    denominador = 0.0
    
    # Calcula o denominador: soma de (tau_il^alfa * eta_il^beta) para as cidades factíveis
    for j, dist in enumerate(linha_distancias):
        if j != cidade_atual and j not in cidades_visitadas and dist > 0:
            tau = linha_feromonio[j]
            eta = 1.0 / dist
            denominador += (tau ** alfa) * (eta ** beta)
            
    # Calcula a probabilidade para cada cidade
    for j, dist in enumerate(linha_distancias):
        if j == cidade_atual or j in cidades_visitadas or dist == 0:
            # A probabilidade de ir para si mesma, cidades já visitadas ou com distância 0 é nula
            probabilidades.append(0.0)
        else:
            tau = linha_feromonio[j]
            eta = 1.0 / dist
            if denominador == 0:
                # Se houver underflow por evaporação extrema, fallback para probabilidade uniforme baseada só em eta
                probabilidade = 1.0 / (len(linha_distancias) - len(cidades_visitadas))
            else:
                probabilidade = ((tau ** alfa) * (eta ** beta)) / denominador
            probabilidades.append(probabilidade)
            
    return probabilidades

def selecao_roleta(probabilidades):
    """
    Seleciona um índice (cidade) baseado na lista de probabilidades usando o método da roleta.
    Valores 0.0 são desconsiderados automaticamente pois não incrementam a soma.
    """
    r = random.random()
    soma = 0.0
    for i, p in enumerate(probabilidades):
        if p > 0.0:
            soma += p #soma as probabilidades equivale a "ocupar um pedaço da roleta"
            if r <= soma:
                return i
                
    # Fallback de segurança para arredondamentos em ponto flutuante
    for i in range(len(probabilidades)-1, -1, -1):
        if probabilidades[i] > 0.0:
            return i
    return -1

def constroi_rota(cidade_inicial, matriz_distancias, matriz_feromonio, alfa=1.0, beta=5.0):
    """
    Constrói a rota completa de uma formiga partindo da 'cidade_inicial'.
    """
    rota = [cidade_inicial]
    cidades_visitadas = {cidade_inicial}
    qtd_cidades = len(matriz_distancias)
    
    while len(rota) < qtd_cidades:
        cidade_atual = rota[-1]
        linha_distancias = matriz_distancias[cidade_atual]
        linha_feromonio = matriz_feromonio[cidade_atual]
        
        # Calcula as probabilidades de ir para as próximas cidades não visitadas
        probabilidades = calcula_probabilidade(cidade_atual, linha_distancias, linha_feromonio, cidades_visitadas, alfa, beta)
        
        # Seleciona a próxima cidade via roleta
        proxima_cidade = selecao_roleta(probabilidades)
        
        rota.append(proxima_cidade)
        cidades_visitadas.add(proxima_cidade)
        
    return rota

def percorre_distancias():
    """
    Lê a matriz de distâncias a partir do arquivo CSV usando o módulo padrão.
    """
    matriz = []
    with open('distancia_matrix.csv', 'r') as arquivo:
        leitor = csv.reader(arquivo)
        for linha in leitor:
            if any(linha): # Verifica se a linha não está vazia
                linha_float = [float(x) for x in linha]
                matriz.append(linha_float)
    return matriz

def calcula_distancia_rota(rota, matriz_distancias):
    """
    Calcula o tamanho total de uma rota, somando as distâncias entre
    cada par de cidades adjacentes na lista.
    """
    distancia_total = 0.0
    for i in range(len(rota) - 1):
        cidade_atual = rota[i]
        proxima_cidade = rota[i+1]
        distancia_total += matriz_distancias[cidade_atual][proxima_cidade]
    return distancia_total

def atualiza_feromonio(matriz_feromonio, rotas_e_distancias, rho=0.5, Q=1.0):
    """
    Atualiza a matriz de feromônios aplicando evaporação e o depósito das formigas.
    
    matriz_feromonio: Matriz quadrada representando o feromônio nas arestas.
    rotas_e_distancias: Lista de tuplas contendo (rota, distancia) de cada formiga k.
    rho: Taxa de evaporação do feromônio (0 < rho <= 1).
    Q: Intensidade do feromônio a ser depositado.
    """
    n_cidades = len(matriz_feromonio)
    
    # Evaporação: Aplica (1 - rho) a TODAS as arestas da matriz
    for i in range(n_cidades):
        for j in range(n_cidades):
            matriz_feromonio[i][j] *= (1.0 - rho)
            
    # Depósito: Adiciona o feromônio deixado por cada formiga nas arestas que ela percorreu
    for rota, distancia in rotas_e_distancias:
        if distancia > 0:
            delta_tau = Q / distancia
            
            # Percorre os pares de cidades adjacentes na rota da formiga
            for i in range(len(rota) - 1):
                cidade_atual = rota[i]
                proxima_cidade = rota[i+1]
                
                # Deposita o feromônio na aresta
                matriz_feromonio[cidade_atual][proxima_cidade] += delta_tau
                # Em problemas do caixeiro viajante simétricos, reforçamos ambos os sentidos da aresta
                matriz_feromonio[proxima_cidade][cidade_atual] += delta_tau
                
    return matriz_feromonio