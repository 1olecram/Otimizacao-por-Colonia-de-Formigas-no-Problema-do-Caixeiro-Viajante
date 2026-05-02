import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy

def gerar_animacao_feromonios(historico_feromonios, num_cidades, arquivo_saida='assets/animacao_feromonios.gif'):
    """
    Gera uma animação (GIF) do grafo das cidades, mostrando a evolução
    dos feromônios através da cor e espessura das arestas.
    
    :param historico_feromonios: Lista de matrizes de feromônio ao longo do tempo.
    :param num_cidades: Quantidade de cidades no grafo.
    :param arquivo_saida: Caminho onde o arquivo .gif será salvo.
    """
    print(f"\nGerando animação com {len(historico_feromonios)} quadros... Pode levar alguns segundos.")
    
    # Cria a figura e remove os eixos
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_axis_off()
    
    # Cria o grafo completo (todas as cidades conectadas)
    G = nx.complete_graph(num_cidades)
    
    # Define o layout circular para os nós
    pos = nx.circular_layout(G)
    
    # Descobre o valor máximo de feromônio de toda a história para normalizar a espessura/cor
    max_feromonio = 0
    for matriz in historico_feromonios:
        for linha in matriz:
            for val in linha:
                if val > max_feromonio:
                    max_feromonio = val
                    
    # Previne divisão por zero se não houver feromônio
    if max_feromonio == 0:
        max_feromonio = 1
        
    def update(frame_idx):
        ax.clear()
        ax.set_title(f"Concentração de Feromônio (Iteração {frame_idx * 10})", fontsize=14)
        ax.set_axis_off()
        
        matriz_atual = historico_feromonios[frame_idx]
        
        # Desenha os nós (cidades)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue', node_size=300)
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight='bold')
        
        edges = []
        colors = []
        widths = []
        
        # Verifica as arestas (apenas i < j para não duplicar, já que é simétrico)
        for i in range(num_cidades):
            for j in range(i + 1, num_cidades):
                feromonio = matriz_atual[i][j]
                
                if feromonio > 0.001:  # Ignora arestas com feromônio praticamente zerado
                    # Normaliza entre 0 e 1
                    intensidade = feromonio / max_feromonio
                    
                    # Espessura: de 0.1 a 5.0
                    width = 0.1 + (intensidade * 5.0)
                    
                    # Cor: Tons de cinza. 1.0 é branco (invisível), 0.0 é preto.
                    # Vamos mapear de 0.9 (cinza bem claro) até 0.0 (preto) para que fique visível
                    cor_cinza = 0.9 - (intensidade * 0.9)
                    color = str(cor_cinza)  # matplotlib aceita string float para escala de cinza
                    
                    edges.append((i, j))
                    colors.append(color)
                    widths.append(width)
                    
        # Desenha as arestas ativas neste frame
        if edges:
            nx.draw_networkx_edges(G, pos, edgelist=edges, ax=ax, edge_color=colors, width=widths, alpha=0.8)

    # Cria a animação
    anim = animation.FuncAnimation(fig, update, frames=len(historico_feromonios), interval=200, repeat=True)
    
    # Salva como GIF
    anim.save(arquivo_saida, writer='pillow')
    plt.close(fig)
    print(f"Animação salva com sucesso em '{arquivo_saida}'.")
