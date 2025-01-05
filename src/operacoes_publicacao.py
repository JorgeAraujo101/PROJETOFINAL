from operacoes_autor import adicionar_publicacao_ao_autor, remover_publicacao_do_autor
import re
estatisticas = {
    'publicacoes_por_ano': {},
    'publicacoes_por_mes': {},
    'publicacoes_por_autor': {},
    'publicacoes_por_autor_por_ano': {},
    'palavras_chave_frequencia': {},
    'palavras_chave_por_ano': {}
}
publicacoes = {}

def extrair_id_publicacao(url):
    correspondencia = re.search(r'(\d+)$', url)
    return correspondencia.group(1) if correspondencia else None

def adicionar_publicacao(publicacao,dados_fcc):
    dados_fcc.append(publicacao)
    id_publicacao = extrair_id_publicacao(publicacao.get('url', ''))
    if id_publicacao:
        publicacoes[id_publicacao] = publicacao
        for autor in publicacao['authors']:
            adicionar_publicacao_ao_autor(autor['name'], id_publicacao)

def criar_publicacao(dados_fcc):
    resumo = input("abstract : ")
    palavras_chave = input("keywords : ")
    numero_autores = int(input("numero de autores : "))
    autores = []
    for x in range(numero_autores):
        nome = input("name :")
        afiliacao = input("affiliation : ")
        autor = {
            'name': nome,
            'affiliation': afiliacao
        }
        autores.append(autor)
    doi = input("doi : ")
    pdf = input("pdf : ")
    data_publicacao = input("publish_date : ")
    titulo = input("title : ")
    url = input("url : ")
    nova_publicacao = {
        'abstract': resumo,
        'keywords': palavras_chave,
        'authors': autores,
        'doi': doi,
        'pdf': pdf,
        'publish_date': data_publicacao,
        'title': titulo,
        'url': url
    }
    adicionar_publicacao(nova_publicacao,dados_fcc)

def atualizar_publicacao():
    id_publicacao = input("Digite o ID da publicação que deseja atualizar: ").strip()
    if id_publicacao not in publicacoes:
        print("Publicação não encontrada.")
        return

    publicacao = publicacoes[id_publicacao]
    print("Deixe o campo vazio para não atualizar.")

    resumo = input(f"abstract ({publicacao.get('abstract', '')}): ").strip()
    if resumo:
        publicacao['abstract'] = resumo

    palavras_chave = input(f"keywords ({publicacao.get('keywords', '')}): ").strip()
    if palavras_chave:
        publicacao['keywords'] = palavras_chave

    numero_autores = int(input(f"numero de autores ({len(publicacao.get('authors', []))}): ").strip() or len(publicacao.get('authors', [])))
    autores = []
    for x in range(numero_autores):
        nome = input(f"name ({publicacao['authors'][x]['name'] if x < len(publicacao['authors']) else ''}): ").strip()
        afiliacao = input(f"affiliation ({publicacao['authors'][x]['affiliation'] if x < len(publicacao['authors']) else ''}): ").strip()
        autor = {
            'name': nome or publicacao['authors'][x]['name'],
            'affiliation': afiliacao or publicacao['authors'][x]['affiliation']
        }
        autores.append(autor)
    publicacao['authors'] = autores

    doi = input(f"doi ({publicacao.get('doi', '')}): ").strip()
    if doi:
        publicacao['doi'] = doi

    pdf = input(f"pdf ({publicacao.get('pdf', '')}): ").strip()
    if pdf:
        publicacao['pdf'] = pdf

    data_publicacao = input(f"publish_date ({publicacao.get('publish_date', '')}): ").strip()
    if data_publicacao:
        publicacao['publish_date'] = data_publicacao

    titulo = input(f"title ({publicacao.get('title', '')}): ").strip()
    if titulo:
        publicacao['title'] = titulo

    url = input(f"url ({publicacao.get('url', '')}): ").strip()
    if url:
        publicacao['url'] = url

    publicacoes[id_publicacao] = publicacao
    print("Publicação atualizada com sucesso.")

def atualizar_publicacao_grafica(publicacao,dados_fcc):
    id_publicacao = extrair_id_publicacao(publicacao.get('url', ''))
    if id_publicacao:
        print("Publicação atualizada com sucesso.")
        
        publicacoes[id_publicacao] = publicacao
        for autor in publicacao['authors']:
            adicionar_publicacao_ao_autor(autor['name'], id_publicacao)
        atualizar_estatisticas(publicacao)
        dados_fcc.append(publicacao)

def imprimir_publicacao():
    id_publicacao = input("Digite o ID da publicação que deseja atualizar: ").strip()
    if id_publicacao not in publicacoes:
        print("Publicação não encontrada.")
        return
    
    publicacao = publicacoes[id_publicacao]
    print("\nInformações da Publicação:")
    print(f"ID: {id_publicacao}")
    print(f"Título: {publicacao.get('title', 'Sem título')}")
    print(f"Resumo: {publicacao.get('abstract', 'Sem resumo')}")
    print(f"Palavras-chave: {publicacao.get('keywords', 'Sem palavras-chave')}")
    print(f"DOI: {publicacao.get('doi', 'Sem DOI')}")
    print(f"PDF: {publicacao.get('pdf', 'Sem PDF')}")
    print(f"Data de Publicação: {publicacao.get('publish_date', 'Sem data de publicação')}")
    print(f"URL: {publicacao.get('url', 'Sem URL')}")
    print("Autores:")
    for autor in publicacao.get('authors', []):
        print(f"  - Nome: {autor.get('name', 'Sem nome')}, Afiliação: {autor.get('affiliation', 'Sem afiliação')}")
    input("\nPressione Enter para continuar...")

def eliminar_publicacao():
    id_publicacao = input("Digite o ID da publicação que deseja eliminar: ").strip()
    if id_publicacao not in publicacoes:
        print("Publicação não encontrada.")
        return

    publicacao = publicacoes.pop(id_publicacao)
    for autor in publicacao.get('authors', []):
        remover_publicacao_do_autor(autor['name'], id_publicacao)
    print("Publicação eliminada")
    input("\nPressione Enter para continuar...")

def eliminar_publicacao_grafica(id_publicacao,dados_fcc):
    if id_publicacao in publicacoes:
        publicacao = publicacoes.pop(id_publicacao)
    try :
        dados_fcc.remove(publicacao)
    except:
        pass

    for autor in publicacao.get('authors', []):
        remover_publicacao_do_autor(autor['name'], id_publicacao)

def atualizar_estatisticas(publicacao):
    if 'publish_date' in publicacao and isinstance(publicacao['publish_date'], str):
        ano = publicacao['publish_date'][:4]
        mes = publicacao['publish_date'][5:7]
        
        # Distribuição de publicações por ano
        if ano not in estatisticas['publicacoes_por_ano']:
            estatisticas['publicacoes_por_ano'][ano] = 0
        estatisticas['publicacoes_por_ano'][ano] += 1
        
        # Distribuição de publicações por mês de um determinado ano
        if ano not in estatisticas['publicacoes_por_mes']:
            estatisticas['publicacoes_por_mes'][ano] = {}
        if mes not in estatisticas['publicacoes_por_mes'][ano]:
            estatisticas['publicacoes_por_mes'][ano][mes] = 0
        estatisticas['publicacoes_por_mes'][ano][mes] += 1
        
        # Número de publicações por autor
        for autor in publicacao['authors']:
            nome_autor = autor['name']
            if nome_autor not in estatisticas['publicacoes_por_autor']:
                estatisticas['publicacoes_por_autor'][nome_autor] = 0
            estatisticas['publicacoes_por_autor'][nome_autor] += 1
            
            # Distribuição de publicações de um autor por anos
            if nome_autor not in estatisticas['publicacoes_por_autor_por_ano']:
                estatisticas['publicacoes_por_autor_por_ano'][nome_autor] = {}
            if ano not in estatisticas['publicacoes_por_autor_por_ano'][nome_autor]:
                estatisticas['publicacoes_por_autor_por_ano'][nome_autor][ano] = 0
            estatisticas['publicacoes_por_autor_por_ano'][nome_autor][ano] += 1
        
        # Distribuição de palavras-chave pela sua frequência
        if 'keywords' in publicacao and isinstance(publicacao['keywords'], str):
            palavras_chave = publicacao['keywords'].split(',')
            for palavra in palavras_chave:
                palavra = palavra.strip()
                if palavra not in estatisticas['palavras_chave_frequencia']:
                    estatisticas['palavras_chave_frequencia'][palavra] = 0
                estatisticas['palavras_chave_frequencia'][palavra] += 1
                
                # Distribuição de palavras-chave mais frequente por ano
                if ano not in estatisticas['palavras_chave_por_ano']:
                    estatisticas['palavras_chave_por_ano'][ano] = {}
                if palavra not in estatisticas['palavras_chave_por_ano'][ano]:
                    estatisticas['palavras_chave_por_ano'][ano][palavra] = 0
                estatisticas['palavras_chave_por_ano'][ano][palavra] += 1