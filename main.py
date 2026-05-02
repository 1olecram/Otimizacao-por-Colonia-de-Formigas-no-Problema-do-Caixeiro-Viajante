import aco
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def main():
    # Carrega a matriz de distâncias
    matriz_distancias = aco.percorre_distancias()
    qtd_formigas = len(matriz_distancias) # Como há 20 cidades, teremos 20 formigas (uma em cada)
    
    # Inicializa a matriz de feromônios com um pequeno valor positivo (ex: 1.0)
    matriz_feromonio = [[1.0 for _ in range(qtd_formigas)] for _ in range(qtd_formigas)]
    
    melhor_rota_global = None
    menor_distancia_global = float('inf')
    formiga_vencedora_global = -1
    
    max_iteracoes = 2000
    iteracao_convergencia = 0
    historico_distancias = [] # Guarda a melhor distância ao fim de cada iteração
    
    print("Iniciando otimização com colônia de formigas...")
    for iteracao in range(max_iteracoes):
        rotas_e_distancias = []
        melhoria_nesta_iteracao = False
        
        # Cada formiga constrói sua rota
        for i in range(qtd_formigas):
            # A formiga i inicia na cidade i
            cidade_inicial = i
            
            # Constrói a rota passando alfa e beta
            rota = aco.constroi_rota(cidade_inicial, matriz_distancias, matriz_feromonio, alfa=1.0, beta=5.0)
            
            # Calcula a distância total dessa rota
            distancia = aco.calcula_distancia_rota(rota, matriz_distancias)
            rotas_e_distancias.append((rota, distancia))
            
            # Verifica se é a menor distância global encontrada
            if distancia < menor_distancia_global:
                menor_distancia_global = distancia
                melhor_rota_global = rota
                formiga_vencedora_global = i + 1
                melhoria_nesta_iteracao = True
        
        # Atualiza a matriz de feromônio com o que foi percorrido na rodada
        matriz_feromonio = aco.atualiza_feromonio(matriz_feromonio, rotas_e_distancias, rho=0.5, Q=100.0)
        
        # Controle de convergência e logs
        if melhoria_nesta_iteracao:
            iteracao_convergencia = iteracao + 1
            print(f"Iteração {iteracao+1}: Nova melhor distância encontrada: {menor_distancia_global:.2f}")
            
        # Registra a distância da melhor rota para plotagem no gráfico
        historico_distancias.append(menor_distancia_global)
            
    # Exibe a melhor rota global ao final
    melhor_rota_exibicao = [cidade + 1 for cidade in melhor_rota_global]
    print("\n" + "="*50)
    print("🏆 RESULTADO FINAL - MELHOR ROTA")
    print("="*50)
    print(f"Iterações executadas: {max_iteracoes}")
    print(f"Convergência atingida na iteração: {iteracao_convergencia}")
    print(f"Formiga com o melhor caminho: {formiga_vencedora_global}")
    print(f"Rota percorrida: {melhor_rota_exibicao}")
    print(f"Menor distância encontrada: {menor_distancia_global:.2f}")
    print("="*50)
    
    # Plotagem do Gráfico
    print("\nGerando gráfico de convergência...")
    plt.figure(figsize=(12, 6))
    ax = plt.gca()
    
    plt.plot(range(1, max_iteracoes + 1), historico_distancias, color='b', linewidth=2)
    plt.title('Evolução da Melhor Distância - ACO')
    plt.xlabel('Iterações')
    plt.ylabel('Melhor Distância Global')
    
    # Define um espaçamento menor para os eixos (grid mais detalhado)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100)) # Marcações a cada 100 iterações no eixo X
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))  # Marcações a cada 10 unidades de distância no eixo Y
    
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    
    # Salva e mostra o gráfico
    plt.savefig('grafico_convergencia.png', dpi=300, bbox_inches='tight')
    print("Gráfico salvo como 'grafico_convergencia.png'.")
    try:
        plt.show()
    except Exception as e:
        print("Não foi possível exibir a janela do gráfico. Verifique o arquivo salvo.")

if __name__ == "__main__":
    main()