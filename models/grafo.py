import heapq

class Grafo:
    def __init__(self):
        """Inicializa grafo vazio"""
        self.vizinhos = {}

    def adicionar_aresta(self, origem, destino, peso):
        """Adiciona aresta direcionada ao grafo"""
        self.vizinhos.setdefault(origem, []).append((destino, peso))

    def adicionar_aresta_bidirecional(self, origem, destino, peso):
        """Adiciona aresta nos dois sentidos"""
        self.adicionar_aresta(origem, destino, peso)
        self.adicionar_aresta(destino, origem, peso)

    def dijkstra(self, inicio):
        """Implementa Dijkstra para encontrar menores caminhos a partir de um ponto"""
        """Complexidade padrão do Dijkstra com heap:
           O((V + E) log V) para grafo esparso"""
        distancias = {inicio: 0}
        fila = [(0, inicio)]
        visitados = set()

        while fila:
            dist_atual, atual = heapq.heappop(fila)
            if atual in visitados:
                continue
            visitados.add(atual)

            for vizinho, peso in self.vizinhos.get(atual, []):
                distancia = dist_atual + peso
                if vizinho not in distancias or distancia < distancias[vizinho]:
                    distancias[vizinho] = distancia
                    heapq.heappush(fila, (distancia, vizinho))

        return distancias
