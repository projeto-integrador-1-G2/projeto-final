import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import g
import json

# Caminho para o arquivo JSON onde os dados dos lançamentos serão armazenados
launch_data_json_path = './../codigo/launch_data.json'

# Função para carregar os dados dos lançamentos do arquivo JSON
def load_launch_data(launch_data_path):
    try:
        with open(launch_data_path, 'r') as file:
            launch_data = json.load(file)
    except FileNotFoundError:
        # Se o arquivo não existir, começamos com uma lista vazia
        launch_data = []
    return launch_data

# Função para salvar os dados dos lançamentos no arquivo JSON
def save_launch_data(launch_data, launch_data_path):
    with open(launch_data_path, 'w') as file:
        json.dump(launch_data, file, indent=4)


# Solicitando entradas do usuário
# Simulando dados do lançamento como entrada do usuário
dados_lancamento = {
    'pressao': float(input()),
    'volume_agua': float(input()),
    'massa_foguete': float(input()),
    'angulo_lancamento': float(input())
}

pressao_inicial_psi = dados_lancamento["pressao"]
quantidade_agua_ml = dados_lancamento["volume_agua"]
massa_garrafa = dados_lancamento["massa_foguete"]
angulo_lancamento = dados_lancamento["angulo_lancamento"]

all_launch_data = load_launch_data(launch_data_json_path)

# Adicionar os novos dados do lançamento
all_launch_data.append(dados_lancamento)

# Salvar todos os dados de lançamento atualizados
save_launch_data(all_launch_data, launch_data_json_path)

# Conversões e cálculos
pressao_inicial = pressao_inicial_psi * 6894.76  # Convertendo para pascals
massa_agua = quantidade_agua_ml / 1000  # Convertendo ml de água para kg (1ml de água = 1g)
massa_total = massa_agua + massa_garrafa  # Massa total
diametro_abertura = 0.02  # diâmetro da abertura em metros (estimado)
densidade_agua = 1000  # densidade da água em kg/m³
area_abertura = np.pi * (diametro_abertura / 2)**2  # área em m²
altura_coluna_agua = 0.3  # altura em metros (estimativa)
vazao = area_abertura * np.sqrt(2 * g * altura_coluna_agua + 2 * pressao_inicial / densidade_agua)  # vazão em m³/s
volume_agua = massa_agua / densidade_agua  # volume em m³
tempo_expulsao = volume_agua / vazao  # tempo em segundos

# Convertendo o ângulo para radianos
angulo_radianos = np.radians(angulo_lancamento)

# Inicializações para a simulação
tempo = 0  # tempo inicial
dt = 0.01  # intervalo de tempo entre os pontos
posicao_x = 0
posicao_y = 0
velocidade_x = 0
velocidade_y = 0

# Listas para armazenar os resultados
posicoes_x = []
posicoes_y = []
tempos = []

# Loop de simulação
while posicao_y >= 0:
    if tempo < tempo_expulsao:
        pressao_atual = pressao_inicial * (1 - tempo / tempo_expulsao)
        forca_propulsao = pressao_atual * area_abertura
        massa_atual = massa_garrafa + massa_agua * (1 - tempo / tempo_expulsao)

        # Dividindo a força de propulsão em componentes horizontal e vertical
        forca_horizontal = forca_propulsao * np.cos(angulo_radianos)
        forca_vertical = forca_propulsao * np.sin(angulo_radianos)

        acel_atual_x = forca_horizontal / massa_atual
        acel_atual_y = (forca_vertical / massa_atual) - g
    else:
        acel_atual_x = 0
        acel_atual_y = -g

    velocidade_x += acel_atual_x * dt
    velocidade_y += acel_atual_y * dt
    posicao_x += velocidade_x * dt
    posicao_y += velocidade_y * dt

    posicoes_x.append(posicao_x)
    posicoes_y.append(posicao_y)
    tempos.append(tempo)

    tempo += dt

# Plotando os gráficos
plt.figure(figsize=(12, 4))


plt.plot(tempos, posicoes_x)
plt.xlabel('Tempo (s)')
plt.ylabel('Altura (m)')
plt.title('Altura x Tempo')
plt.grid(True)
plt.savefig('./../docs/grafico_simulacao_h.png')
plt.close()

plt.plot(tempos, posicoes_x)
plt.xlabel('Tempo (s)')
plt.ylabel('Distância Horizontal (m)')
plt.title('Distância Horizontal x Tempo')
plt.grid(True)
plt.savefig('./../docs/grafico_simulacao_dh.png')
