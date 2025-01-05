import os
import time
from operacoes_json import carregar_json, exportar_json
from operacoes_autor import listar_autores, adicionar_publicacao_ao_autor
from operacoes_publicacao import criar_publicacao, extrair_id_publicacao,atualizar_publicacao,imprimir_publicacao,eliminar_publicacao, publicacoes, dados_fcc, estatisticas
import json
import matplotlib.pyplot as plt

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

comandos = [bcolors.OKGREEN + "\tHelp" + bcolors.ENDC,
            bcolors.OKGREEN + "\tCriar" + bcolors.ENDC + " publicação",
            bcolors.OKBLUE + "\tAtualizar" + bcolors.ENDC + " publicação",
            bcolors.OKBLUE + "\tConsultar" + bcolors.ENDC + " publicação",
            bcolors.OKBLUE + "\tConsultar" + bcolors.ENDC + " publicações",
            bcolors.WARNING + "\tEliminar" + bcolors.ENDC + " publicação",
            bcolors.OKCYAN + "\tEstatisticas" + bcolors.ENDC,
            bcolors.OKCYAN + "\tListar autores" + bcolors.ENDC,
            bcolors.OKBLUE + "\tImportar" + bcolors.ENDC + " publicações",
            bcolors.OKGREEN + "\tGuardar" + bcolors.ENDC + " publicações",
            bcolors.WARNING + "\tQuit" + bcolors.ENDC
            ]

tempo_inicio = time.time()

def help():

    os.system('cls' if os.name == 'nt' else 'clear') # portabilidade mac windows 
    print("Comandos : ")
    for indice, comando in enumerate(comandos):
        print(indice + 1, "-", comando)

def imprimir_publicacoes():
    def filtrar_publicacoes():
        filtrado = fcc_data
        filtro_titulo = input("Filtrar por título (deixe vazio para não filtrar): ").strip().lower()
        if filtro_titulo:
            filtrado = [publicacao for publicacao in filtrado if filtro_titulo in publicacao.get('title', '').lower()]

        filtro_autor = input("Filtrar por autor (deixe vazio para não filtrar): ").strip().lower()
        if filtro_autor:
            filtrado = [publicacao for publicacao in filtrado if any(filtro_autor in autor['name'].lower() for autor in publicacao.get('authors', []))]

        filtro_afiliacao = input("Filtrar por afiliação (deixe vazio para não filtrar): ").strip().lower()
        if filtro_afiliacao:
            filtrado = [publicacao for publicacao in filtrado if any(filtro_afiliacao in autor['affiliation'].lower() for autor in publicacao.get('authors', []))]

        filtro_palavras_chave = input("Filtrar por palavras-chave (deixe vazio para não filtrar): ").strip().lower()
        if filtro_palavras_chave:
            filtrado = [publicacao for publicacao in filtrado if filtro_palavras_chave in publicacao.get('keywords', '').lower()]

        filtro_data = input("Filtrar por data de publicação (deixe vazio para não filtrar): ").strip()
        if filtro_data:
            filtrado = [publicacao for publicacao in filtrado if filtro_data in publicacao.get('publish_date', '')]

        return filtrado

    dados_filtrados = filtrar_publicacoes()
    tamanho_pagina = 10  # Número de publicações por página
    total_paginas = (len(dados_filtrados) + tamanho_pagina - 1) // tamanho_pagina  # Calcular o número total de páginas

    def imprimir_pagina(pagina):
        os.system('cls' if os.name == 'nt' else 'clear')
        inicio = pagina * tamanho_pagina
        fim = inicio + tamanho_pagina
        for publicacao in dados_filtrados[inicio:fim]:
            print(json.dumps(publicacao, indent=4))
            print("\n" + "-"*80 + "\n")
        print(f"\nPágina {pagina + 1} de {total_paginas}")

    pagina_atual = 0
    while True:
        imprimir_pagina(pagina_atual)
        comando = input("Digite 'n' para próxima página, 'p' para página anterior, 'q' para sair, ou 'r' para redefinir filtros: ").strip().lower()
        if comando == 'n':
            if pagina_atual < total_paginas - 1:
                pagina_atual += 1
            else:
                print("Você está na última página.")
        elif comando == 'p':
            if pagina_atual > 0:
                pagina_atual -= 1
            else:
                print("Você está na primeira página.")
        elif comando == 'q':
            break
        elif comando == 'r':
            dados_filtrados = filtrar_publicacoes()
            total_paginas = (len(dados_filtrados) + tamanho_pagina - 1) // tamanho_pagina
            pagina_atual = 0
        else:
            print("Comando inválido. Por favor, digite 'n', 'p', 'q' ou 'r'.")

def exibir_estatisticas():

    opcoes_stats = [bcolors.OKGREEN + "\tDistribuição de publicações por ano" + bcolors.ENDC,
            bcolors.OKBLUE + "\tDistribuição de publicações por mês de um determinado ano" + bcolors.ENDC,
            bcolors.OKBLUE + "\tNúmero de publicações por autor (top 20 autores)" + bcolors.ENDC,
            bcolors.OKBLUE + "\tDistribuição de publicações de um autor por anos" + bcolors.ENDC,
            bcolors.WARNING + "\tDistribuição de palavras-chave pela sua frequência (top 20 palavras-chave)" + bcolors.ENDC,
            bcolors.OKCYAN + "\tDistribuição de palavras-chave mais frequente por ano" + bcolors.ENDC,
            bcolors.OKCYAN + "\tGráfico" + bcolors.ENDC,
            bcolors.WARNING + "\tQuit" + bcolors.ENDC
            ]

    grafico = False
    flag = True
    while flag:

        for indice, opcao in enumerate(opcoes_stats):
            print(indice + 1, "-", opcao)

        opcao = input("Enter a command: ").strip().lower()
        os.system('cls' if os.name == 'nt' else 'clear')
        
        match opcao:
            case "1":
                if grafico :
                    # Gráfico de publicações por ano
                    anos, counts = zip(*sorted(estatisticas['publicacoes_por_ano'].items(), key=lambda x: x[1], reverse=True))
                    plt.figure(figsize=(10, 5))
                    plt.bar(anos, counts)
                    plt.title('Distribuição de publicações por ano')
                    plt.xlabel('Ano')
                    plt.ylabel('Número de publicações')
                    plt.show()
                else :
                    for ano, count in estatisticas['publicacoes_por_ano'].items():
                        print(f"{ano}: {count}")
                
                
        
            case "2":
                if grafico :
                    # Gráfico de publicações por mês (para o ano mais recente)
                    if estatisticas['publicacoes_por_ano']:
                        ano_mais_recente = max(estatisticas['publicacoes_por_ano'], key=estatisticas['publicacoes_por_ano'].get)
                        publicacoes_por_mes = sorted(estatisticas['publicacoes_por_mes'][ano_mais_recente].items(), key=lambda x: x[1], reverse=True)
                        meses, counts = zip(*publicacoes_por_mes)
                        plt.figure(figsize=(10, 5))
                        plt.bar(meses, counts)
                        plt.title(f'Distribuição de publicações por mês em {ano_mais_recente}')
                        plt.xlabel('Mês')
                        plt.ylabel('Número de publicações')
                        plt.show()
                else :
                    for ano, meses in estatisticas['publicacoes_por_mes'].items():
                        for mes, count in meses.items():
                            print(f"{ano}-{mes}: {count}")
                
            case "3":
                top_autores = sorted(estatisticas['publicacoes_por_autor'].items(), key=lambda x: x[1], reverse=True)[:20]
                if grafico :
                # Gráfico de publicações por autor (top 20 autores)
                    autores, counts = zip(*top_autores)
                    plt.figure(figsize=(10, 5))
                    plt.barh(autores, counts)
                    plt.title('Número de publicações por autor (top 20 autores)')
                    plt.xlabel('Número de publicações')
                    plt.ylabel('Autor')
                    plt.gca().invert_yaxis()
                    plt.show()
                else :
                    for autor, count in top_autores:
                        print(f"{autor}: {count}")
        
            case "4":
                if grafico :
                    # Gráfico de publicações de um autor por anos (para o autor com mais publicações)
                    if estatisticas['publicacoes_por_autor']:
                        autor_mais_publicacoes = max(estatisticas['publicacoes_por_autor'], key=estatisticas['publicacoes_por_autor'].get)
                        publicacoes_por_ano = sorted(estatisticas['publicacoes_por_autor_por_ano'][autor_mais_publicacoes].items(), key=lambda x: x[1], reverse=True)
                        anos, counts = zip(*publicacoes_por_ano)
                        plt.figure(figsize=(10, 5))
                        plt.bar(anos, counts)
                        plt.title(f'Distribuição de publicações por ano para {autor_mais_publicacoes}')
                        plt.xlabel('Ano')
                        plt.ylabel('Número de publicações')
                        plt.show()
                else :
                    for autor, anos in estatisticas['publicacoes_por_autor_por_ano'].items():
                        print(f"{autor}:")
                        for ano, count in anos.items():
                            print(f"  {ano}: {count}")
        
            case "5":
                top_palavras_chave = sorted(estatisticas['palavras_chave_frequencia'].items(), key=lambda x: x[1], reverse=True)[:20]
                if grafico :
                    # Gráfico de palavras-chave pela sua frequência (top 20 palavras-chave)
                    palavras, counts = zip(*top_palavras_chave)
                    plt.figure(figsize=(10, 5))
                    plt.barh(palavras, counts)
                    plt.title('Distribuição de palavras-chave pela sua frequência (top 20 palavras-chave)')
                    plt.xlabel('Frequência')
                    plt.ylabel('Palavra-chave')
                    plt.gca().invert_yaxis()
                    plt.show()
                else :
                    
                    for palavra, count in top_palavras_chave:
                        print(f"{palavra}: {count}")
                
            case "6":
                if grafico :
                    # Perguntar ao usuário o número máximo de palavras-chave a serem exibidas
                    max_palavras = input("Digite o número máximo de palavras-chave a serem exibidas (ou '*' para todas): ").strip()
                    if max_palavras == '*':
                        max_palavras = None
                    else:
                        max_palavras = int(max_palavras)
                    
                    # Gráfico de palavras-chave mais frequente por ano (para o ano mais recente)
                    if estatisticas['publicacoes_por_ano']:
                        ano_mais_recente = max(estatisticas['publicacoes_por_ano'], key=estatisticas['publicacoes_por_ano'].get)
                        palavras_por_ano = sorted(estatisticas['palavras_chave_por_ano'][ano_mais_recente].items(), key=lambda x: x[1], reverse=True)
                        if max_palavras:
                            palavras_por_ano = palavras_por_ano[:max_palavras]
                        palavras, counts = zip(*palavras_por_ano)
                        plt.figure(figsize=(10, 5))
                        plt.barh(palavras, counts)
                        plt.title(f'Distribuição de palavras-chave mais frequente por ano em {ano_mais_recente}')
                        plt.xlabel('Frequência')
                        plt.ylabel('Palavra-chave')
                        plt.gca().invert_yaxis()
                        plt.show()
                else :  
                    for ano, palavras in estatisticas['palavras_chave_por_ano'].items():
                        print(f"{ano}:")
                        for palavra, count in palavras.items():
                            print(f"  {palavra}: {count}")
                
            case "7":
                if grafico :
                    grafico = False
                    print("Gráficos desativados")
                else :
                    grafico = True
                    print("Gráficos ativados")
            case 'quit' | "8" | "q":
                flag_quit = True
                while flag_quit:
                    quit = input("Deseja sair? (Y/N) : ")
                    if quit == "Y" or quit == 'y':
                        flag = False
                        flag_quit = False
                    elif quit == "N" or quit == "n":
                        flag_quit = False
                    else:
                        print("Invalido, escreva Y ou N")
            case _:
                print("Comando inválido.")

def main():
    global fcc_data
    fcc_data = carregar_json('dataset/ata_medica_papers.json')
    for publicacao in fcc_data:
        id_publicacao = extrair_id_publicacao(publicacao.get('url', ''))
        if id_publicacao:
            publicacoes[id_publicacao] = publicacao
            for autor in publicacao['authors']:
                adicionar_publicacao_ao_autor(autor['name'], id_publicacao)

    help()
    flag = True
    tempo_decorrido = time.time() - tempo_inicio
    print(f"Tempo desde o início do programa: {tempo_decorrido:.2f} segundos")
    while flag:

        command = input("Enter a command: ").strip().lower()
        os.system('cls' if os.name == 'nt' else 'clear')
        match command:
            #done
            case "help" | "1" : 
                help()
            #done
            case "criar publicacao" | "2" : 
                criar_publicacao(fcc_data)
            #done
            case 'atualizar publicacao' | "3" :
                atualizar_publicacao()
            #done (pode ser melhorado)
            case 'consultar publicacao' | "4" : 
                imprimir_publicacao()
            #done
            case "consultar publicacoes" | "5" : 
                imprimir_publicacoes()
                input("\nContinue...")
                os.system('cls' if os.name == 'nt' else 'clear')
            #done
            case 'eliminar publicacao' | "6" : 
                eliminar_publicacao()
            #done
            case 'estatisticas' | "7" : 
                exibir_estatisticas()
                input("\nContinue...")
            #done (possivelmente diferente do pretendido, a averiguar)
            case 'listar autores' | "8" : 
                listar_autores(publicacoes=publicacoes)
            #done
            case 'importar publicacoes' | "9": 
                path = input("Caminho para o ficheiro a importar: ")
                novos_dados = carregar_json(path)
                fcc_data.extend(novos_dados)
                input("\nContinue...")
            #done (falta exportar automaticamente, e falta dar a possibilidade de exportar com filtros)
            case 'exportar publicacoes' | "10":
                path = input("Caminho para o ficheiro a ser exportado: ")
                exportar_json(path, fcc_data)
                input("\nContinue...")
            case 'quit' | "11" | "q":
                flag_quit = True
                while flag_quit:
                    quit = input("Deseja sair? (Y/N) : ")
                    if quit == "Y" or quit == 'y':
                        flag = False
                        flag_quit = False
                    elif quit == "N" or quit == "n":
                        flag_quit = False
                    else :
                        print("Invalido, escreva Y ou N")
            case default:
                print("Comando invalido (use o comando : help para listar os comandos disponiveis)")
        if flag :
            help()

if __name__ == "__main__":
    main()
