import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from geopy.distance import geodesic
#from scipy.signal import savgol_filter

# Carregando os dados de GPS do arquivo
gps_data = pd.read_csv('./gps_data_constante.csv')

# Supondo que as colunas sejam 'latitude' e 'longitude'
latitudes = gps_data['latitude']
longitudes = gps_data['longitude']

# Intervalo de tempo fixo entre cada ponto (em segundos)
dt = 2  # 20 milissegundos

# Calcular velocidade
velocidades = [0]
velocidade_anterior = 0
aceleracoes = [0]
distancias = [0]
distancia_total = 0
for i in range(1, len(latitudes)):

    #pegando a distancia entre dois pontos somente em relação ao eixo X (distância)
    distancia = geodesic((latitudes[0], longitudes[i-1]), (latitudes[0], longitudes[i])).meters
    distancia_total += distancia
    distancias.append(distancia_total)

    velocidade = distancia / dt
    aceleracao = (velocidade - velocidade_anterior) / dt
    velocidades.append(velocidade)
    aceleracoes.append(aceleracao)
    velocidade_anterior = velocidade

# Aplicar o filtro de Savitzky-Golay para suavizar os dados de velocidade
#velocidades_suavizadas = savgol_filter(velocidades, window_length=5, polyorder=2)  # Ajuste a janela e a ordem conforme necessário

# Criar uma série de tempo para plotagem
tempo = np.arange(0, len(latitudes) * dt, dt)

plt.figure(figsize=(18, 5))
# Plotando o gráfico de aceleração
plt.plot(tempo, aceleracoes)  # O índice de tempo para acelerações começa do segundo ponto
plt.xlabel('Tempo (s)')
plt.ylabel('Aceleração (m/s²)')
plt.title('Aceleração x Tempo')
plt.grid(True)
plt.savefig('grafico_aceleracao.png')

plt.figure(figsize=(18, 5))
# Plotando o gráfico de velocidade
plt.plot(tempo, velocidades)
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.title('Velocidade x Tempo')
plt.grid(True)
plt.savefig('grafico_velocidade.png')

tempo = np.arange(0, len(distancias) * dt, dt)
plt.figure(figsize=(18, 5))

# Plotando o gráfico de posicao
plt.plot(tempo, distancias, label='Posição X')
plt.xlabel('Tempo (s)')
plt.ylabel('Posicao (m)')
plt.title('Posicao x Tempo')
plt.grid(True)
plt.legend()
plt.savefig('grafico_posicao.png')
