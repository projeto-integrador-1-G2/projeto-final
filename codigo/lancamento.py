import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from geopy.distance import geodesic
from datetime import timedelta, datetime , time
import json


# Função para salvar os dados dos lançamentos no arquivo JSON
def save_launch_data(launch_data, launch_data_path):
    with open(launch_data_path, 'w') as file:
        json.dump(launch_data, file, indent=4)

# Função para carregar os dados dos lançamentos do arquivo JSON
def load_launch_data(launch_data_path):
    try:
        with open(launch_data_path, 'r') as file:
            launch_data = json.load(file)
    except FileNotFoundError:
        launch_data = []  # Se o arquivo não existir, começamos com uma lista vazia
    return launch_data

def find_last_launch_number(markdown_content):
    
    last_number = 0

    for line in markdown_content:
        if '### Lançamento' in line and 'X' not in line:  # Verifique se 'X' não está na linha
            # Extrair o número do lançamento da linha
            try:
                number = int(line.split(' ')[-1].strip())
                if number > last_number:
                    last_number = number
            except ValueError:
                # Se houver um erro ao converter para int, ignorar a linha
                pass
    return last_number

def time_diff_in_seconds(time1, time2):
    # Adicionando uma data arbitrária para converter para datetime
    dummy_date = datetime(2000, 1, 1)
    datetime1 = datetime.combine(dummy_date, time1)
    datetime2 = datetime.combine(dummy_date, time2)

    # Calculando a diferença e convertendo para segundos
    diff = datetime2 - datetime1
    return diff.total_seconds()



# Função para plotar o gráfico de Velocidade x Tempo
def plot_speed_graph(data, start_time, end_time, launch_number):
    # Filtrando os dados para o intervalo de tempo desejado
    mask = (data['Time'] >= start_time) & (data['Time'] <= end_time)
    filtered_data = data.loc[mask].copy()

    # Ajustando a velocidade com base na margem de erro
    filtered_data['Adjusted Speed'] = filtered_data['Speed'].apply(lambda x: x if x > 0.1 else 0)
    # Converter 'Total Time' de milissegundos para segundos e ajustar para começar do zero
    filtered_data['Total Time'] = (filtered_data['Total Time'] - filtered_data.iloc[0]['Total Time']) / 1000

    all_launch_data = load_launch_data('./../codigo/launch_data.json')
    launch_data = all_launch_data[launch_number - 1]
    # Adicionar os novos dados do lançamento
    velocidade_media = np.mean(filtered_data['Adjusted Speed'])
    launch_data['velocidade_media'] = velocidade_media
    all_launch_data[launch_number - 1] = launch_data

    save_launch_data(all_launch_data, './../codigo/launch_data.json')


    # Gráfico de Velocidade x Tempo
    plt.figure(figsize=(12, 10))
    plt.plot(filtered_data['Total Time'], filtered_data['Adjusted Speed'], label='Velocidade')
    plt.xlabel('Tempo')
    plt.ylabel('Velocidade (m/s)')
    plt.title('Gráfico de Velocidade x Tempo')
    plt.xticks(rotation=45)
    plt.legend()
    plt.savefig(f'./../docs/grafico_velocidade_{launch_number}.png')

# Função para plotar o gráfico de Posição x Tempo
def plot_position_graph(data, start_time, end_time, launch_number):
    # Filtrando os dados para o intervalo de tempo desejado
    mask = (data['Time'] >= start_time) & (data['Time'] <= end_time)
    filtered_data = data.loc[mask].copy()

    # Converter 'Total Time' de milissegundos para segundos e ajustar para começar do zero
    filtered_data['Total Time'] = (filtered_data['Total Time'] - filtered_data.iloc[0]['Total Time']) / 1000

    # Calcular a distância percorrida
    distances = [0]
    for i in range(1, len(filtered_data)):
        point1 = (filtered_data.iloc[0]['Latitude'], filtered_data.iloc[i - 1]['Longitude'])
        point2 = (filtered_data.iloc[0]['Latitude'], filtered_data.iloc[i]['Longitude'])
        distance = geodesic(point1, point2).meters
        distances.append(distances[-1] + distance)

    filtered_data['Distance'] = distances

    # Gráfico de Distância Percorrida x Tempo
    plt.figure(figsize=(12, 8))
    plt.plot(filtered_data['Total Time'], filtered_data['Distance'], label='Distância Percorrida', color='blue')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Distância Percorrida (m)')
    plt.title('Gráfico de Distância Percorrida x Tempo')
    plt.xticks(rotation=45)
    plt.legend()
    plt.savefig(f'./../docs/grafico_distancia_lancamento_{launch_number}.png')


def plot_acceleration_graph(data, start_time, end_time,launch_number):
    # Filtrando os dados e calculando Time_diff e Acceleration usando encadeamento de métodos
    filtered_data = (
        data.loc[(data['Time'] >= start_time) & (data['Time'] <= end_time)]
        .copy()
        .assign(
            Time_diff=lambda df: df['Time'].apply(lambda x: time_diff_in_seconds(x, df['Time'].iloc[0])),
            Acceleration=lambda df: df['Speed'].diff() / df['Time_diff']
        )
    )

    # Converter 'Total Time' de milissegundos para segundos e ajustar para começar do zero
    filtered_data['Total Time'] = (filtered_data['Total Time'] - filtered_data.iloc[0]['Total Time']) / 1000

    all_launch_data = load_launch_data('./../codigo/launch_data.json')
    launch_data = all_launch_data[launch_number - 1]
    # Adicionar os novos dados do lançamento
    aceleracao_media = np.mean(filtered_data['Acceleration'])
    launch_data['aceleracao_media'] = aceleracao_media
    all_launch_data[launch_number - 1] = launch_data

    save_launch_data(all_launch_data, './../codigo/launch_data.json')

    # Gráfico de Aceleração x Tempo
    plt.figure(figsize=(12, 8))
    plt.plot(filtered_data['Total Time'], filtered_data['Acceleration'], label='Aceleração', color='orange')
    plt.xlabel('Tempo')
    plt.ylabel('Aceleração (m/s²)')
    plt.title('Gráfico de Aceleração x Tempo')
    plt.xticks(rotation=45)
    plt.legend()
    plt.savefig(f'./../docs/grafico_aceleracao_lancamento_{launch_number}.png')

# Inicializando listas para armazenar os horários de início e fim
start_times = []
end_times = []

# Recebendo três pares de horários de início e fim
for i in range(3):
    start_time_input = input()
    end_time_input = input()
    
    # Convertendo e ajustando os horários
    start_time = pd.to_datetime(start_time_input, format='%H:%M:%S').time()
    end_time = pd.to_datetime(end_time_input, format='%H:%M:%S').time()

    dummy_date = datetime(2000, 1, 1)  # A data pode ser qualquer uma
    start_datetime = datetime.combine(dummy_date, start_time) + timedelta(hours=3)
    end_datetime = datetime.combine(dummy_date, end_time) + timedelta(hours=3)

    start_times.append(start_datetime.time())
    end_times.append(end_datetime.time())

# Carregando o arquivo CSV
file_path = './GPS.CSV'
gps_data = pd.read_csv(file_path, sep=';', skiprows=lambda x: str(x).startswith('***'))
# Removendo espaços desnecessários das strings de tempo
gps_data['Time'] = gps_data['Time'].str.strip()
# Tentando a conversão para datetime novamente
gps_data['Time'] = pd.to_datetime(gps_data['Time'].str.strip(),format='%H:%M:%S.%f', errors='coerce').dt.time
gps_data['Speed'] = pd.to_numeric(gps_data['Speed'], errors='coerce')
gps_data["Total Time"] = pd.to_numeric(gps_data["Total Time"], errors='coerce')
gps_data.dropna(subset=['Time', 'Speed', 'Total Time'], inplace=True)

markdown_template_path = './../docs/lancamentos.md'

with open(markdown_template_path, 'r') as md_file:
    markdown_content = md_file.readlines()

last_launch_number = find_last_launch_number(markdown_content)


# Processando cada par de horários
for i, (start_time, end_time) in enumerate(zip(start_times, end_times)):
    plot_acceleration_graph(gps_data, start_time, end_time, last_launch_number+i+1)
    plot_position_graph(gps_data, start_time, end_time, last_launch_number+i+1)
    plot_speed_graph(gps_data, start_time, end_time, last_launch_number+i+1)
