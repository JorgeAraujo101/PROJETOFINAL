import os

publicacoes_autor = []
autores_ordenados = []

def adicionar_publicacao_ao_autor(nome_autor, id_publicacao):
    for i, (autor, publicacoes) in enumerate(publicacoes_autor):
        if autor == nome_autor:
            publicacoes.append(id_publicacao)
            publicacoes_autor[i] = (autor, publicacoes)
            return
    publicacoes_autor.append((nome_autor, [id_publicacao]))

def remover_publicacao_do_autor(nome_autor, id_publicacao):
    for i, (autor, publicacoes) in enumerate(publicacoes_autor):
        if autor == nome_autor:
            publicacoes.remove(id_publicacao)
            if not publicacoes:
                publicacoes_autor.pop(i)
            else:
                publicacoes_autor[i] = (autor, publicacoes)
            return

def listar_autores(publicacoes, tamanho_pagina=10):
    # Ordenar os autores pelo número de publicações em ordem decrescente
    global autores_ordenados
    if not autores_ordenados :
        autores_ordenados = sorted(publicacoes_autor, key=lambda x: len(x[1]), reverse=True)
        
    total_paginas = (len(autores_ordenados) + tamanho_pagina - 1) // tamanho_pagina

    def imprimir_pagina(pagina):
        os.system('cls' if os.name == 'nt' else 'clear')
        inicio = pagina * tamanho_pagina
        fim = inicio + tamanho_pagina
        for autor, ids_publicacoes in autores_ordenados[inicio:fim]:
            print(f"Autor: {autor}")
            for id_pub in ids_publicacoes:
                titulo = publicacoes[id_pub].get('title', 'Sem título')
                print(f"  - {titulo}")
            print("\n" + "-"*80 + "\n")
        print(f"\nPágina {pagina + 1} de {total_paginas}")

    pagina_atual = 0
    while True:
        imprimir_pagina(pagina_atual)
        comando = input("Digite 'n' para próxima página, 'p' para página anterior, ou 'q' para sair: ").strip().lower()
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
        else:
            print("Comando inválido. Por favor, digite 'n', 'p' ou 'q'.")