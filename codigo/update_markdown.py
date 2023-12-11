import json

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

# Função para adicionar novos dados de lançamento e gráficos no arquivo Markdown
def add_new_launch_data(markdown_path, launch_data, graph_paths, last_launch_number):
    # Carregar o conteúdo do arquivo Markdown
    with open(markdown_path, 'r') as md_file:
        markdown_content = md_file.readlines()

    # Incrementar o último número de lançamento
    new_launch_number = last_launch_number + 1

    # Adicionar a seção do novo lançamento
    new_launch_section = [
        f'\n### Lançamento {new_launch_number}\n',
        '<div style="text-align: center; display: flex; justify-content: space-around;">\n'
    ]

    # Adicionar os caminhos dos gráficos ao novo lançamento
    for graph_path in graph_paths:
        graph_name = os.path.basename(graph_path)
        new_launch_section.append(f'    <img src="./docs/{graph_name}" alt="{graph_name.split(".")[0]}" width="200"/>\n')
    new_launch_section.append('</div>\n\n')

    # Adicionar os dados do novo lançamento
    new_launch_section += [
        '#### Dados do Lançamento:\n',
        f'    - Pressão:  {launch_data["pressure"]} Pa\n',
        f'    - Volume d’água: {launch_data["water_volume"]} L\n',
        f'    - Massa do Foguete: {launch_data["rocket_mass"]} kg\n',
        '\n'
    ]

    # Anexar a nova seção ao conteúdo existente do arquivo Markdown
    markdown_content += new_launch_section

    # Salvar as alterações no arquivo Markdown
    with open(markdown_path, 'w') as md_file:
        md_file.writelines(markdown_content)

# Caminho do arquivo Markdown
markdown_template_path = './../docs/template_lancamentoX.md'

# Carregar os dados existentes
all_launch_data = load_launch_data('./../codigo/launch_data.json')

# Acessar o segundo lançamento (índice 1, pois os índices começam em 0)


# Exemplo de caminhos dos gráficos (assumindo que eles já foram criados e salvos na pasta 'docs')
graph_paths_example = [
    './../docs/grafico_velocidade_2.png',
    './../docs/grafico_distancia_2.png',
    './../docs/grafico_aceleracao_2.png'
]

# Depois de encontrar o último número de lançamento, se for 0, definir para 1 (primeiro lançamento)
for i in range(3):
    with open(markdown_template_path, 'r') as md_file:
        markdown_content = md_file.readlines()

    last_launch_number = find_last_launch_number(markdown_content)
    if last_launch_number == 0:
        last_launch_number = 1  # Definir para 1 se for o primeiro lançamento
    launch_data = all_launch_data[last_launch_number-1] if len(all_launch_data) > 1 else None

    # Agora você pode chamar `add_new_launch_data` com `last_launch_number`

    # Chamada da função para adicionar novos dados de lançamento
    # Isso é apenas um exemplo e não será executado neste ambiente.
    # Você deve executar isso em seu ambiente local após gerar os gráficos com o código fornecido anteriormente.
    add_new_launch_data(markdown_template_path, launch_data, graph_paths_example, last_launch_number)

# NOTA: O código acima é um exemplo e não será executado aqui.
