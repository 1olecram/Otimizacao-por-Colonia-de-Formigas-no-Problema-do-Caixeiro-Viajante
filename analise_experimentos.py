import aco
import matplotlib.pyplot as plt
import statistics
import time

def executar_aco_teste(qtd_formigas, taxa_evaporacao, matriz_distancias, max_iteracoes=2000):
    """
    Roda uma única execução do ACO com as regras de convergência das Partes 2 e 3.
    """
    n_cidades = len(matriz_distancias)
    matriz_feromonio = [[1.0 for _ in range(n_cidades)] for _ in range(n_cidades)]
    
    menor_distancia_global = float('inf')
    iteracoes_sem_melhoria = 0
    iteracao_convergencia = 0
    
    for iteracao in range(max_iteracoes):
        rotas_e_distancias = []
        melhoria_nesta_iteracao = False
        
        for i in range(qtd_formigas):
            # Se tiver mais formigas que cidades, distribui usando módulo
            cidade_inicial = i % n_cidades 
            
            rota = aco.constroi_rota(cidade_inicial, matriz_distancias, matriz_feromonio, alfa=1.0, beta=5.0)
            distancia = aco.calcula_distancia_rota(rota, matriz_distancias)
            rotas_e_distancias.append((rota, distancia))
            
            if distancia < menor_distancia_global:
                menor_distancia_global = distancia
                iteracao_convergencia = iteracao + 1
                melhoria_nesta_iteracao = True
                
        # Atualiza o feromônio sem elitismo (apenas Q=100)
        matriz_feromonio = aco.atualiza_feromonio(matriz_feromonio, rotas_e_distancias, rho=taxa_evaporacao, Q=100.0)
        
        # Lógica de convergência: estabilizar por 50 iterações
        if melhoria_nesta_iteracao:
            iteracoes_sem_melhoria = 0
        else:
            iteracoes_sem_melhoria += 1
            
        if iteracoes_sem_melhoria >= 50:
            break # Encerra antecipadamente
            
    return menor_distancia_global, iteracao_convergencia

def plotar_graficos_parte(titulo_eixo_x, valores_x, medias_dist, desvios_dist, medias_iter, nome_arquivo_base):
    """
    Gera o Gráfico A (Distância) e o Gráfico B (Iterações) para cada experimento.
    """
    # Gráfico A: Média e Desvio Padrão da Distância Final
    plt.figure(figsize=(10, 5))
    plt.errorbar(valores_x, medias_dist, yerr=desvios_dist, fmt='-o', color='b', capsize=5, capthick=2, ecolor='red')
    plt.title(f"Gráfico A: Distância Final vs {titulo_eixo_x}")
    plt.xlabel(titulo_eixo_x)
    plt.ylabel("Distância Média Convergida")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(valores_x)
    plt.savefig(f"{nome_arquivo_base}_A_distancia.png", bbox_inches='tight')
    plt.close()

    # Gráfico B: Média de Iterações até Convergência
    plt.figure(figsize=(10, 5))
    plt.plot(valores_x, medias_iter, marker='s', color='g', linestyle='-')
    plt.title(f"Gráfico B: Velocidade de Convergência vs {titulo_eixo_x}")
    plt.xlabel(titulo_eixo_x)
    plt.ylabel("Média de Iterações (Estabilização)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(valores_x)
    plt.savefig(f"{nome_arquivo_base}_B_iteracoes.png", bbox_inches='tight')
    plt.close()

def parte2_populacao(matriz_distancias):
    print("\n" + "="*60)
    print("🚀 INICIANDO PARTE 2: ANÁLISE DA POPULAÇÃO (FORMIGAS)")
    print("="*60)
    
    lista_formigas = [3, 5, 10, 20, 40, 80]
    taxa_evaporacao = 0.5
    resultados = []
    
    print(f"{'Formigas':<10} | {'Média Distância':<18} | {'Desvio Padrão':<15} | {'Média Iterações':<15}")
    print("-" * 65)
    
    for f in lista_formigas:
        distancias = []
        iteracoes = []
        
        for rep in range(10):
            dist, it = executar_aco_teste(f, taxa_evaporacao, matriz_distancias)
            distancias.append(dist)
            iteracoes.append(it)
            
        media_dist = statistics.mean(distancias)
        desvio_dist = statistics.stdev(distancias) if len(distancias) > 1 else 0.0
        media_iter = statistics.mean(iteracoes)
        
        resultados.append((f, media_dist, desvio_dist, media_iter))
        print(f"{f:<10} | {media_dist:<18.2f} | {desvio_dist:<15.2f} | {media_iter:<15.2f}")
        
    # Desempacotar dados para o gráfico
    x = [r[0] for r in resultados]
    m_dist = [r[1] for r in resultados]
    d_dist = [r[2] for r in resultados]
    m_it = [r[3] for r in resultados]
    
    plotar_graficos_parte("Número de Formigas", x, m_dist, d_dist, m_it, "assets/Parte2_Populacao")

def parte3_evaporacao(matriz_distancias):
    print("\n" + "="*60)
    print("🚀 INICIANDO PARTE 3: ANÁLISE DA EVAPORAÇÃO")
    print("="*60)
    
    qtd_formigas = 20
    lista_evaporacao = [0.0, 0.25, 0.5, 0.75, 1.0]
    resultados = []
    
    print(f"{'Taxa Evap.':<10} | {'Média Distância':<18} | {'Desvio Padrão':<15} | {'Média Iterações':<15}")
    print("-" * 65)
    
    for taxa in lista_evaporacao:
        distancias = []
        iteracoes = []
        
        for rep in range(10):
            dist, it = executar_aco_teste(qtd_formigas, taxa, matriz_distancias)
            distancias.append(dist)
            iteracoes.append(it)
            
        media_dist = statistics.mean(distancias)
        desvio_dist = statistics.stdev(distancias) if len(distancias) > 1 else 0.0
        media_iter = statistics.mean(iteracoes)
        
        resultados.append((taxa, media_dist, desvio_dist, media_iter))
        print(f"{taxa:<10.2f} | {media_dist:<18.2f} | {desvio_dist:<15.2f} | {media_iter:<15.2f}")
        
    x = [r[0] for r in resultados]
    m_dist = [r[1] for r in resultados]
    d_dist = [r[2] for r in resultados]
    m_it = [r[3] for r in resultados]
    
    plotar_graficos_parte("Taxa de Evaporação (rho)", x, m_dist, d_dist, m_it, "assets/Parte3_Evaporacao")

def main():
    tempo_inicio = time.time()
    matriz_distancias = aco.percorre_distancias()
    
    # Chama a execução dos dois experimentos
    parte2_populacao(matriz_distancias)
    parte3_evaporacao(matriz_distancias)
    
    print("\nAnálises concluídas! Todos os gráficos foram salvos na pasta 'assets/'.")
    print(f"Tempo total de execução dos experimentos: {(time.time() - tempo_inicio)/60:.2f} minutos.")

if __name__ == "__main__":
    main()