# 🌿 Sistema de Monitoramento Ambiental com Drones

Este projeto simula um sistema de **monitoramento ambiental** utilizando **drones autônomos** para inspecionar diferentes zonas de uma floresta virtual. O sistema foi desenvolvido em Python e conta com estruturas de grafos para representar os mapas da floresta, sensores de temperatura simulados, algoritmos para otimização de rotas e registro completo de missões.

---

##  😎 Integrantes

    - Gabriel Gouvea - 555528.
    - Miguel Kapicius Caires - 556198.
    - Thiago Ferreira Oliveira - 555608
---
## 🎯 Objetivo do Projeto

Monitorar automaticamente diferentes regiões de uma floresta utilizando um drone que:
- Planeja uma rota eficiente para visitar zonas.
- Coleta temperaturas em cada região.
- Detecta possíveis riscos ambientais (como incêndios).
- Armazena e exibe o histórico completo das missões realizadas.

---


## 🧠 Funcionalidades Principais

### ✈️ Execução de Missões
- O usuário escolhe um dos **3 mapas disponíveis**, cada um com zonas e conexões diferentes.
- O **drone parte do "Bunker"**, visita cada zona seguindo uma **rota otimizada**, coleta dados de temperatura e simula a captura de imagens.
- Cada visita registra:
  - Horário
  - Zona de origem e destino
  - Temperaturas medidas
  - Média
  - Alerta de temperatura crítica (acima de 45°C)
  - Nome da imagem simulada capturada

### 📦 Armazenamento das Missões
- Após cada missão, os dados são salvos automaticamente em um arquivo `missoes.json`.
- As informações são persistidas entre execuções do programa.
- A data é avançada automaticamente a cada missão.

### 🔍 Consulta ao Histórico
- O sistema permite:
  - **Visualizar todas as missões registradas**
  - **Buscar missões por temperatura média** usando **busca binária**
  - **Ver detalhes completos** de cada missão
  - **Deletar missões anteriores**, se desejado

### 📊 Visualização Gráfica dos Mapas
- Cada mapa pode ser visualizado em um grafo usando a biblioteca `matplotlib` com `networkx`.
- Os grafos mostram as zonas (nós), conexões (arestas) e distâncias (pesos).
- O bunker é destacado na cor vermelha.

---

## 🗺️ Estrutura dos Mapas

- **Mapa 1**: Bunker e zonas Z1 a Z4 com caminhos circulares e conexões alternativas.
- **Mapa 2**: Bunker e zonas Z5 a Z7, mais compacto e linear.
- **Mapa 3**: Bunker e zonas Z8 a Z12 com múltiplas rotas e atalhos (Z9 → Z12).

---

## ⚙️ Algoritmos Utilizados

- **Dijkstra**: Para encontrar os caminhos mais curtos entre zonas.
- **Busca Binária**: Para encontrar missões com temperatura média aproximada de forma eficiente.
- **Planejamento Guloso de Rotas**: O drone escolhe a próxima zona mais próxima ainda não visitada, baseado em Dijkstra.

---

## 💡 Tecnologias e Bibliotecas

- Python 3.x
- `matplotlib` – Visualização de mapas
- `networkx` – Representação gráfica de grafos
- `json`, `datetime`, `heapq`, `random` – Bibliotecas padrão do Python

---



