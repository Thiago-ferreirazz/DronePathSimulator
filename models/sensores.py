import random

class SensorTemperatura:
    def __init__(self, limite_critico=45):
        """Inicializa sensor com limite crítico configurável"""
        self.limite = limite_critico

    @staticmethod
    def gerar_temperaturas():
        """Gera 3 temperaturas simuladas com 30% de chance de valor crítico"""
        return [random.randint(25, 39) if random.random() < 0.7 else random.randint(40, 55) for _ in range(3)]

    @staticmethod
    def calcular_media(temperaturas):
        """Calcula média das temperaturas com 2 casas decimais"""
        return round(sum(temperaturas) / len(temperaturas), 2)

    def verificar_alerta(self, temperaturas):
        """Verifica se alguma temperatura atingiu o limite crítico"""
        return any(temp >= self.limite for temp in temperaturas)
