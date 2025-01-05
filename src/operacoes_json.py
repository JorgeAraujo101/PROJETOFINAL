import json
from operacoes_publicacao import atualizar_estatisticas

def carregar_json(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo_fcc:
        dados = json.load(arquivo_fcc)
        for publicacao in dados:
            atualizar_estatisticas(publicacao)
        return dados

def exportar_json(caminho_arquivo, dados):
    with open(caminho_arquivo, 'w') as arquivo_fcc:
        json.dump(dados, arquivo_fcc, indent=4)