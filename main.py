import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  
        self.h = 0 
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def heuristica(pos_atual, pos_final):
    return abs(pos_atual[0] - pos_final[0]) + abs(pos_atual[1] - pos_final[1])

def encontrar_inicio_fim(matriz):
    inicio = fim = None
    for i, linha in enumerate(matriz):
        for j, valor in enumerate(linha):
            if valor == 'S':
                inicio = (i, j)
            elif valor == 'E':
                fim = (i, j)
    return inicio, fim

def a_star(matriz):
    inicio, fim = encontrar_inicio_fim(matriz)
    if not inicio or not fim:
        return "Ponto S ou E ausente no labirinto"

    open_list = []
    closed_set = set()

    nodo_inicio = Node(inicio)
    nodo_fim = Node(fim)

    heapq.heappush(open_list, nodo_inicio)

    while open_list:
        nodo_atual = heapq.heappop(open_list)
        closed_set.add(nodo_atual.position)

        if nodo_atual.position == nodo_fim.position:
            caminho = []
            while nodo_atual:
                caminho.append(nodo_atual.position)
                nodo_atual = nodo_atual.parent
            return caminho[::-1]

        vizinhos = obter_vizinhos(nodo_atual.position, matriz)
        for pos_vizinho in vizinhos:
            if pos_vizinho in closed_set:
                continue

            vizinho = Node(pos_vizinho, nodo_atual)
            vizinho.g = nodo_atual.g + 1
            vizinho.h = heuristica(vizinho.position, fim)
            vizinho.f = vizinho.g + vizinho.h

            if any(open_node.position == vizinho.position and open_node.f <= vizinho.f for open_node in open_list):
                continue

            heapq.heappush(open_list, vizinho)

    return "Sem solução"

def obter_vizinhos(pos, matriz):
    linhas, colunas = len(matriz), len(matriz[0])
    movimentos = [(-1,0), (1,0), (0,-1), (0,1)]
    vizinhos = []

    for dx, dy in movimentos:
        nx, ny = pos[0] + dx, pos[1] + dy
        if 0 <= nx < linhas and 0 <= ny < colunas and matriz[nx][ny] != '1':
            vizinhos.append((nx, ny))
    return vizinhos

labirinto = [
    ['S', '0', '1', '0', '0'],
    ['0', '0', '1', '0', '1'],
    ['1', '0', '1', '0', '0'],
    ['1', '0', '0', 'E', '1']
]

resultado = a_star(labirinto)
print("Caminho encontrado:", resultado)
