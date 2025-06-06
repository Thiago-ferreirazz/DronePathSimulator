from datetime import datetime
from .sensores import SensorTemperatura
import heapq

class DroneMonitoramento:
    def __init__(self, grafo, pos_inicial="Bunker", limite_critico=45):
        """Inicializa drone com grafo do mapa e sensor de temperatura"""
        self.grafo = grafo
        self.posicao = pos_inicial
        self.sensor = SensorTemperatura(limite_critico)
        self.historico = []

    def registrar_dados(self, destino, temperaturas, media, alerta):
        """Registra todos os dados da zona visitada"""
        self.historico.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "de": self.posicao,
            "para": destino,
            "temperaturas": temperaturas,
            "media": media,
            "alerta": alerta,
            "imagem": f"imagem_{destino}.jpg"
        })

    def voar_para(self, destino):
        """Calcula e executa voo para destino usando Dijkstra"""
        caminho, custo = self.calcular_melhor_caminho(self.posicao, destino)
        print(f"\n✈️ {' → '.join(caminho)} (Custo total: {custo} km)")
        return custo

    def calcular_melhor_caminho(self, origem, destino):
        """Implementa Dijkstra para encontrar caminho mais curto"""
        """Complexidade: O((V + E) log V) onde:
           V = número de vértices (zonas)
           E = número de arestas (conexões)
           Uso de heap mantém a eficiência"""
        predecessores = {}
        distancias = {origem: 0}
        fila = [(0, origem)]

        while fila:
            dist_atual, atual = heapq.heappop(fila)
            if atual == destino:
                break

            for vizinho, peso in self.grafo.vizinhos.get(atual, []):
                distancia = dist_atual + peso
                if vizinho not in distancias or distancia < distancias[vizinho]:
                    distancias[vizinho] = distancia
                    predecessores[vizinho] = atual
                    heapq.heappush(fila, (distancia, vizinho))

        caminho = []
        atual = destino
        while atual in predecessores:
            caminho.append(atual)
            atual = predecessores[atual]
        caminho.append(origem)
        caminho.reverse()

        return caminho, distancias.get(destino, float('inf'))

    def executar_missao_completa(self, zonas):
        """Executa rota passando por todas as zonas do mapa"""
        rota = self.planejar_rota(zonas)
        print(f"\n🗺 Rota otimizada: {' → '.join(rota)}")

        for i in range(len(rota) - 1):
            self.posicao = rota[i]
            destino = rota[i + 1]

            temps = self.sensor.gerar_temperaturas()
            media = self.sensor.calcular_media(temps)
            alerta = self.sensor.verificar_alerta(temps)

            # Simula captura de imagem
            print(f"📸 Capturando imagem em {destino}...")

            # Registra todos os dados, não apenas alertas
            self.registrar_dados(destino, temps, media, alerta)

            # Destaque para temperaturas críticas
            temps_str = [f"{t}°C 🚨" if t >= self.sensor.limite else f"{t}°C" for t in temps]
            print(f"🌡 Temperaturas: {', '.join(temps_str)} | Média: {media}°C")
            print("🚨 ALERTA! Temperatura elevada detectada" if alerta else "✅ Normais")

        return self.historico

    def planejar_rota(self, zonas):
        """Planeja rota visitando todas as zonas usando abordagem gulosa"""
        """Complexidade: O(n * Dijkstra) = O(n*(V log V))
            Onde n = número de zonas a visitar
            Pode ser otimizado para Problema do Caixeiro Viajante"""
        visitados = {self.posicao}
        rota = [self.posicao]
        atual = self.posicao

        while len(visitados) < len(zonas) + 1:
            distancias = self.grafo.dijkstra(atual)
            proximos = {z: d for z, d in distancias.items() if z in zonas and z not in visitados}

            if not proximos:
                break

            proximo = min(proximos, key=proximos.get)
            rota.append(proximo)
            visitados.add(proximo)
            atual = proximo

        return rota
