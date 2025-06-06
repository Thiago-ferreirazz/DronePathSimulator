from models.grafo import Grafo

class Floresta:
    def __init__(self):
        """Inicializa os 3 mapas disponíveis com suas conexões"""
        self.mapas = [
            self._criar_mapa_1(),
            self._criar_mapa_2(),
            self._criar_mapa_3()
        ]

        self.zonas = [
            ["Bunker", "Z1", "Z2", "Z3", "Z4"],
            ["Bunker", "Z5", "Z6", "Z7"],
            ["Bunker", "Z8", "Z9", "Z10", "Z11", "Z12"]
        ]

    @staticmethod
    def _criar_mapa_1():
        g = Grafo()
        g.adicionar_aresta_bidirecional("Bunker", "Z1", 8)
        g.adicionar_aresta_bidirecional("Z1", "Z2", 5)
        g.adicionar_aresta_bidirecional("Z2", "Z3", 9)
        g.adicionar_aresta_bidirecional("Z3", "Z4", 2)
        g.adicionar_aresta_bidirecional("Z4", "Bunker", 3)
        g.adicionar_aresta_bidirecional("Z1", "Z3", 4)
        return g

    @staticmethod
    def _criar_mapa_2():
        g = Grafo()
        g.adicionar_aresta_bidirecional("Bunker", "Z5", 7)
        g.adicionar_aresta_bidirecional("Z5", "Z6", 2)
        g.adicionar_aresta_bidirecional("Z6", "Z7", 4)
        g.adicionar_aresta_bidirecional("Z7", "Bunker", 3)
        return g

    @staticmethod
    def _criar_mapa_3():
        g = Grafo()
        g.adicionar_aresta_bidirecional("Bunker", "Z8", 9)
        g.adicionar_aresta_bidirecional("Z8", "Z9", 8)
        g.adicionar_aresta_bidirecional("Z9", "Z10", 4)
        g.adicionar_aresta_bidirecional("Z10", "Z11", 2)
        g.adicionar_aresta_bidirecional("Z11", "Z12", 5)
        g.adicionar_aresta_bidirecional("Z12", "Bunker", 2)
        g.adicionar_aresta_bidirecional("Z9", "Z12", 1)
        return g

    def obter_mapa(self, idx):
        """Retorna o grafo correspondente ao índice"""
        if 0 <= idx < len(self.mapas):
            return self.mapas[idx]
        return None

    def zonas_por_mapa(self, idx):
        """Retorna as zonas de um mapa pelo índice"""
        if 0 <= idx < len(self.zonas):
            return self.zonas[idx]
        return []
