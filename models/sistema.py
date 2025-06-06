import matplotlib.pyplot as plt
import networkx as nx
import json
import os
from datetime import datetime, timedelta
from .drone import DroneMonitoramento
from .floresta import Floresta


class Sistema:
    def __init__(self):
        self.floresta = Floresta()
        self.historico_missoes = []
        self.data_atual = datetime.now().date()
        self.carregar_dados()  # Carrega dados do JSON ao iniciar

    def carregar_dados(self):
        if os.path.exists('missoes.json'):
            with open('missoes.json', 'r') as f:
                dados = json.load(f)
                self.historico_missoes = [{
                    'data': datetime.strptime(m['data'], '%Y-%m-%d').date(),
                    'mapa': m['mapa'],
                    'resultados': m['resultados'],
                    'imagens': m['imagens']
                } for m in dados]
                if self.historico_missoes:
                    self.data_atual = max(m['data'] for m in self.historico_missoes)  # Mantém última data

    def salvar_dados(self):
        with open('missoes.json', 'w') as f:
            json.dump([{
                'data': m['data'].strftime('%Y-%m-%d'),
                'mapa': m['mapa'],
                'resultados': m['resultados'],
                'imagens': m['imagens']
            } for m in self.historico_missoes], f, indent=2)

    def avancar_dia(self):
        self.data_atual += timedelta(days=1)
        print(f"\n⏰ Data atualizada para: {self.data_atual.strftime('%d/%m/%Y')}")

    def executar_missao(self, mapa_idx):
        grafo = self.floresta.obter_mapa(mapa_idx)
        if not grafo:
            print("Mapa inválido!")
            return

        zonas = self.floresta.zonas_por_mapa(mapa_idx)[1:]
        drone = DroneMonitoramento(grafo)
        print(f"\n📅 Missão do dia {self.data_atual.strftime('%d/%m/%Y')}")

        resultados = drone.executar_missao_completa(zonas)

        self.historico_missoes.append({
            'data': self.data_atual,
            'mapa': mapa_idx,
            'resultados': resultados,
            'imagens': [f"imagem_{zona}_{self.data_atual}.jpg" for zona in zonas]
        })

        self.historico_missoes.sort(key=lambda x: x['data'])
        self.salvar_dados()  # Salva após cada missão

    def buscar_missao_por_temperatura(self, temperatura_alvo):
        # Ordena as missões por temperatura média (para busca binária)
        """Complexidade: O(log n) para busca + O(n log n) para ordenação inicial
            Melhor caso: O(log n) se já estiver ordenado"""
        missoes_ordenadas = sorted(self.historico_missoes,
                                   key=lambda x: sum(r['media'] for r in x['resultados']) / len(x['resultados']))

        esquerda, direita = 0, len(missoes_ordenadas) - 1

        while esquerda <= direita:
            meio = (esquerda + direita) // 2
            # Calcula a média geral da missão
            medias = [r['media'] for r in missoes_ordenadas[meio]['resultados']]
            media_atual = sum(medias) / len(medias)

            if abs(media_atual - temperatura_alvo) < 0.1:  # Margem de erro pequena
                # Encontrou uma missão com a temperatura exata
                return [missoes_ordenadas[meio]]
            elif media_atual < temperatura_alvo:
                esquerda = meio + 1
            else:
                direita = meio - 1

        # Se não encontrou exato, retorna as mais próximas
        if len(missoes_ordenadas) > 0:
            # Encontra a missão com temperatura mais próxima
            missao_mais_proxima = min(missoes_ordenadas,
                                      key=lambda m: abs(sum(r['media'] for r in m['resultados']) / len(
                                          m['resultados']) - temperatura_alvo))
            return [missao_mais_proxima]

        return []

    def listar_todas_missoes(self):
        print("\n📋 Histórico de Missões:")
        for i, missao in enumerate(self.historico_missoes, 1):
            medias = [r['media'] for r in missao['resultados']]
            media_geral = round(sum(medias) / len(medias), 2)
            print(
                f"{i}. Data: {missao['data'].strftime('%d/%m/%Y')} | Mapa: {missao['mapa'] + 1} | Média geral: {media_geral}°C")

        try:
            escolha = int(input("Selecione uma missão para visualizar (número) ou 0 para cancelar: ")) - 1
            if escolha == -1:
                return None
            if 0 <= escolha < len(self.historico_missoes):
                return self.historico_missoes[escolha]
            print("Missão inválida!")
        except ValueError:
            print("Entrada inválida!")
        return None

    def listar_missoes(self):
        if not self.historico_missoes:
            print("Nenhuma missão registrada!")
            return None

        temp_str = input("Digite a temperatura média para buscar ou deixe em branco para listar tudo: ").strip()

        if temp_str:
            try:
                temp_alvo = float(temp_str)
                missoes = self.buscar_missao_por_temperatura(temp_alvo)

                if missoes:
                    print("\n🔍 Missões encontradas:")
                    for i, missao in enumerate(missoes, 1):
                        medias = [r['media'] for r in missao['resultados']]
                        media_geral = round(sum(medias) / len(medias), 2)
                        print(
                            f"{i}. Data: {missao['data'].strftime('%d/%m/%Y')} | Mapa: {missao['mapa'] + 1} | Média: {media_geral}°C")

                    escolha = int(input("Selecione uma missão para detalhes (número) ou 0 para cancelar: ")) - 1
                    if 0 <= escolha < len(missoes):
                        return missoes[escolha]
                else:
                    print("Nenhuma missão encontrada com essa temperatura média.")
                return None
            except ValueError:
                print("Temperatura inválida! Use números (ex: 38.5)")
                return None
        else:
            return self.listar_todas_missoes()

    def deletar_missao(self):
        missao = self.listar_missoes()
        if missao:
            confirmacao = input(
                f"\nTem certeza que deseja deletar a missão de {missao['data'].strftime('%d/%m/%Y')}? (s/n): ")
            if confirmacao.lower() == 's':
                self.historico_missoes.remove(missao)
                self.salvar_dados()
                print("Missão deletada com sucesso!")

    @staticmethod
    def exibir_detalhes_missao(missao):
        print(f"\n📅 Missão do dia {missao['data'].strftime('%d/%m/%Y')}")
        print(f"🗸 Mapa: {missao['mapa'] + 1}")
        for r in missao['resultados']:
            print(f"\n✈️ {r['de']} → {r['para']} (Horário: {r['timestamp']})")
            print(f"📸 Capturando imagem em {r['para']}...")
            temps_str = [f"{t}°C 🚨" if t >= 45 else f"{t}°C" for t in r['temperaturas']]
            print(f"🌡 Temperaturas: {', '.join(temps_str)} | Média: {r['media']}°C")
            print("🚨 ALERTA! Temperatura elevada detectada" if r['alerta'] else "✅ Normais")

    def mostrar_mapas(self):
        print("\n🗺 Mapas Disponíveis:")
        for i in range(3):
            zonas = self.floresta.zonas_por_mapa(i)
            print(f"{i + 1}. Mapa {i + 1} (Zonas: {', '.join(zonas)})")

    def desenhar_mapas(self):
        plt.figure(figsize=(15, 10))

        for i, grafo in enumerate(self.floresta.mapas, 1):
            plt.subplot(1, 3, i)
            G = nx.DiGraph()

            node_colors = []
            for node in grafo.vizinhos.keys():
                if node == "Bunker":
                    node_colors.append("red")
                else:
                    node_colors.append("skyblue")

            for origem, vizinhos in grafo.vizinhos.items():
                for destino, peso in vizinhos:
                    G.add_edge(origem, destino, weight=peso)

            pos = nx.spring_layout(G, seed=42)

            nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors, edgecolors='black')
            nx.draw_networkx_edges(G, pos, width=2, edge_color='gray', arrows=True, arrowstyle='->')
            nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

            plt.title(f"Mapa {i}\nZonas: {', '.join(self.floresta.zonas[i - 1])}", pad=20)
            plt.axis('off')

        plt.tight_layout()
        plt.show()

    @staticmethod
    def selecionar_mapa():
        try:
            mapa_idx = int(input("Escolha o mapa (1-3): ")) - 1
            if mapa_idx in {0, 1, 2}:
                return mapa_idx
            print("Mapa inválido!")
        except ValueError:
            print("Entrada inválida!")
        return None

    def executar(self):
        while True:
            print("\n=== MENU PRINCIPAL ===")
            print(f"⏰ Data atual: {self.data_atual.strftime('%d/%m/%Y')}")
            print("1. Iniciar nova missão")
            print("2. Ver/Deletar missões anteriores")
            print("3. Visualizar mapas")
            print("4. Avançar dia")
            print("5. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.mostrar_mapas()
                idx = self.selecionar_mapa()
                if idx is not None:
                    self.executar_missao(idx)
            elif opcao == "2":
                print("\n1. Visualizar missão")
                print("2. Deletar missão")
                sub_opcao = input("Escolha: ")
                if sub_opcao == "1":
                    missao = self.listar_missoes()
                    if missao:
                        self.exibir_detalhes_missao(missao)
                elif sub_opcao == "2":
                    self.deletar_missao()
            elif opcao == "3":
                self.desenhar_mapas()
            elif opcao == "4":
                self.avancar_dia()
            elif opcao == "5":
                print("Encerrando sistema...")
                break
            else:
                print("Opção inválida!")