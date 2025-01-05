import PySimpleGUI as sg # For the UI
import sys # For the resource path function
from operacoes_json import carregar_json, exportar_json # For the JSON operations
from operacoes_autor import adicionar_publicacao_ao_autor, autores_ordenados, publicacoes_autor # For the author operations
from operacoes_publicacao import extrair_id_publicacao,eliminar_publicacao,atualizar_publicacao_grafica,eliminar_publicacao_grafica, publicacoes, estatisticas # For the publication operations
import json # Needed for the JSON operations
import matplotlib.pyplot as plt # Needed for the statistics

# Define theme and font
sg.theme('DarkAmber')

background = sg.LOOK_AND_FEEL_TABLE['DarkAmber']['BACKGROUND']
font = ("calibri bold", 14)

version = "v1.0"

trademark = " © 2024 Jorge Araujo - ATP"

global fcc_data
fcc_data = carregar_json('dataset/ata_medica_papers.json')
for publicacao in fcc_data:
    id_publicacao = extrair_id_publicacao(publicacao.get('url', ''))
    if id_publicacao:
        publicacoes[id_publicacao] = publicacao
        for autor in publicacao['authors']:
            adicionar_publicacao_ao_autor(autor['name'], id_publicacao)

def mostrar_publicacao(publicao):

    layout = []
    if publicao.get('abstract', ''):
        layout.append([sg.Text(f"Abstract: {publicao['abstract']}", font=font)])

    if publicao.get('keywords', ''):
        layout.append([sg.Text(f"Keywords: {publicao['keywords']}", font=font)])

    if publicao.get('authors', ''):
        layout.append([sg.Text("Autores:", font=font)])
        for autor in publicao['authors']:
            layout.append([sg.Text(f"  - {autor['name']} ({autor['affiliation']})", font=font)])
    if publicao.get('doi', ''):
        layout.append([sg.Text(f"DOI: {publicao['doi']}", font=font)])
    if publicao.get('pdf', ''):
        layout.append([sg.Text(f"PDF: {publicao['pdf']}", font=font)])
    if publicao.get('publish_date', ''):
        layout.append([sg.Text(f"Data de Publicação: {publicao['publish_date']}", font=font)])
    if publicao.get('title', ''):
        layout.append([sg.Text(f"Título: {publicao['title']}", font=font)])
    if publicao.get('url', ''):
        layout.append([sg.Text(f"URL: {publicao['url']}", font=font)])
    layout.append([sg.Button('Back',k='-BACK-', font=font)])  
    layout.append([sg.Text(version+trademark, text_color= '#7C615C')])  
    

    window = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layout,finalize=True,element_justification='c',size=(750,300 + len(publicao['authors'])*25))
    window.bind('<Escape>','-BACK-')

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        match event:
            case '-BACK-':
                break
    window.close()

def editar_publicacao(publicacao):
    autores = []
    layout = [
        [sg.Text('Editar Publicação', font=font)],
        [sg.Input(publicacao.get('abstract', ''),key='-ABS-',font=font,s=(40))],
        [sg.Input(publicacao.get('keywords', ''),key='-KEYW-',font=font,s=(40))],
        [sg.Button('Adicionar Autor',k='-ADD-', font=font)],
        [sg.Input(publicacao.get('doi', ''),key='-DOI-',font=font,s=(40))],
        [sg.Input(publicacao.get('pdf', ''),key='-PDF-',font=font,s=(40))],
        [sg.Input(publicacao.get('publish_date', ''),key='-PD-',font=font,s=(40))],
        [sg.Input(publicacao.get('title', ''),key='-TITLE-',font=font,s=(40))],
        [sg.Input(publicacao.get('url', ''),key='-URL-',font=font,s=(40))],
        [sg.Button('Atualizar',k='-ATUALIZAR-', font=font,s=(40))],
        [sg.Button('Back',k='-BACK-', font=font)],
        [sg.Text(version+trademark, text_color= '#7C615C')]
    ]
    window = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layout,finalize=True,element_justification='c',size=(750,350))
    window.bind('<Escape>','-BACK-')

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        autores = []

        match event:
            case '-ADD-':
                layoutMiniMenuAutor = [
                    [sg.Input("Nome",key='-NOME-',font=font,s=(20))],
                    [sg.Input("Afiliação",key='-AFIL-',font=font,s=(20))],
                    [sg.Button('Adicionar',k='-ADDA-', font=font,s=(20))],
                    [sg.Button('Back',k='-BACKA-', font=font,s=(20))],
                    [sg.Text(version+trademark, text_color= '#7C615C'),sg.Push()]
                ]
                mini1 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMiniMenuAutor,finalize=True,element_justification='c')   
                mini1.bind('<Escape>','-BACKA-')

                while True:
                    window.hide()
                    eventMini1, valuesMini1 = mini1.read()

                    if eventMini1 == sg.WINDOW_CLOSED:
                        break

                    match eventMini1:
                        case '-ADDA-':
                            autor = {
                                'name': valuesMini1['-NOME-'],
                                'affiliation': valuesMini1['-AFIL-']
                            }
                            autores.append(autor)
                            sg.popup("Autor adicionado com sucesso")
                        case '-BACKA-':
                            break
                mini1.close()
                window.un_hide()

            case '-ATUALIZAR-':
                publicacao2 = {
                    'abstract': values['-ABS-'],
                    'keywords': values['-KEYW-'],
                    'authors': autores,
                    'doi': values['-DOI-'],
                    'pdf': values['-PDF-'],
                    'publish_date': values['-PD-'],
                    'title': values['-TITLE-'],
                    'url': values['-URL-']
                }
                atualizar_publicacao_grafica(publicacao2,fcc_data)
                sg.popup("Publicação atualizada com sucesso")
                break
            case '-BACK-':
                break
    window.close()



# Layout for the license menu
layout = [[sg.Button("Criar Publicacao",key = '-CP-', font=font,s=(17)),sg.Push(),
        sg.Button("Atualizar Publicação",key='-AP-', font=font,s=(17)),
        sg.Button("Consultar Publicação",key = '-CONP-', font=font,s=(17)),sg.Push()],
        [sg.Button("Consultar Publicações",key= '-CONPS-', font=font,s=(17)),sg.Push(),
        sg.Button("Eliminar Publicação", key = '-ES-',font=font,s=(17)),
        sg.Button("Estatísticas", key='-EST-' ,font=font,s=(17)),sg.Push()],
        [sg.Button("Listar Autores",key= '-LA-', font=font,s=(17)),sg.Push(),
        sg.Button("Importar Publicações",key= '-IP-', font=font,s=(17)),
        sg.Push(),sg.Button("Exportar Publicações",key= '-EP-', font=font,s=(17)),sg.Push()]
    ,
    [sg.Column([[sg.T(s=15)]])],
    [sg.Text(version+trademark, text_color= '#7C615C'),sg.Push(), sg.Button("Close",key = '-CLOSE-',font=font)]
]

window = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout, return_keyboard_events=True,finalize=True,element_justification='c')

window.bind('<Escape>','-CLOSE-')

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    # Behaviour of Central Menu
    match event:
        case '-CP-': # Create Publication
            window.hide()

            layoutMenu1 = [
                [sg.Text('Criar Publicação', font=font)],
                [sg.Input("Abstract",key='-ABS-',font=font,s=(20))],
                [sg.Input("Keywords",key='-KEYW-',font=font,s=(20))],
                [sg.Button('Adicionar Autor',k='-ADD-', font=font)],
                [sg.Input("Doi",key='-DOI-',font=font,s=(20))],
                [sg.Input("PDF",key='-PDF-',font=font,s=(20))],
                [sg.Input("PublishDate",key='-PD-',font=font,s=(20))],
                [sg.Input("Title",key='-TITLE-',font=font,s=(20))],
                [sg.Input("URL",key='-URL-',font=font,s=(20))],
                [sg.Button('Criar',k='-CRIAR-', font=font,s=(20))],
                [sg.Button('Back',k='-BACK-', font=font)],
                [sg.Text(version+trademark, text_color= '#7C615C')]
            ]
            # Create new menu1 window
            m1 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMenu1,finalize=True,element_justification='c')
            m1.bind('<Escape>','-BACK-')

            # Behaviour of Menu Covers
            while True:
                eventMenu1, valuesMenu1 = m1.read()

                if eventMenu1 == sg.WINDOW_CLOSED:
                    break

                autores = []

                match eventMenu1:
                    case '-ADD-':

                        layoutMiniMenuAutor = [
                            [sg.Input("Nome",key='-NOME-',font=font,s=(20))],
                            [sg.Input("Afiliação",key='-AFIL-',font=font,s=(20))],
                            [sg.Button('Adicionar',k='-ADDA-', font=font,s=(20))],
                            [sg.Button('Back',k='-BACKA-', font=font,s=(20))],
                            [sg.Text(version+trademark, text_color= '#7C615C'),sg.Push()]
                        ]

                        mini1 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMiniMenuAutor,finalize=True,element_justification='c')

                        mini1.bind('<Escape>','-BACKA-')
                        m1.hide()
                        while True:
                            
                            eventMini1, valuesMini1 = mini1.read()

                            if eventMini1 == sg.WINDOW_CLOSED:
                                break

                            match eventMini1:
                                case '-ADDA-':
                                    autor = {
                                        'name': valuesMini1['-NOME-'],
                                        'affiliation': valuesMini1['-AFIL-']
                                    }
                                    autores.append(autor)
                                    sg.popup("Autor adicionado com sucesso")
                                    break
                                case '-BACKA-':
                                    break
                        mini1.close()
                        m1.un_hide()


                    case '-CRIAR-':
                        publicacao = {
                            'abstract': valuesMenu1['-ABS-'],
                            'keywords': valuesMenu1['-KEYW-'],
                            'authors': autores,
                            'doi': valuesMenu1['-DOI-'],
                            'pdf': valuesMenu1['-PDF-'],
                            'publish_date': valuesMenu1['-PD-'],
                            'title': valuesMenu1['-TITLE-'],
                            'url': valuesMenu1['-URL-']
                        }
                        id_publicacao = extrair_id_publicacao(publicacao['url'])
                        if id_publicacao:
                            publicacoes[id_publicacao] = publicacao
                            for autor in publicacao['authors']:
                                adicionar_publicacao_ao_autor(autor['name'], id_publicacao)
                            sg.popup("Publicação criada com sucesso")
                        else :
                            sg.popup("URL inválida")
                    case '-BACK-':
                        break

            m1.close()
            window.un_hide()
        case '-AP-': # Update Publication
            window.hide()

            layoutMenu2 = [
                [sg.Text('Editar Publicação', font=font)],
                [sg.Input("ID",key='-ID-',font=font,s=(20)),sg.Button('ID',k='-IDB-', font=font)],
                [sg.Button('Back',k='-BACK-', font=font)],
                [sg.Text(version+trademark, text_color= '#7C615C')]
            ]

            m2 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMenu2,finalize=True,element_justification='c')

            m2.bind('<Escape>','-BACK-')

            while True:
                eventMenu2, valuesMenu2 = m2.read()

                if eventMenu2 == sg.WINDOW_CLOSED:
                    break

                match eventMenu2:
                    case '-IDB-':
                        try:
                            publicacao = publicacoes[valuesMenu2['-ID-']]
                            m2.hide()
                            editar_publicacao(publicacao)
                            m2.un_hide()
                        except:
                            sg.popup("Publicação não encontrada")
                    case '-BACK-':
                        break
            m2.close()
            window.un_hide()
        case '-CONP-': # Consult Publication
            window.hide()

            layoutMenu3 = [
                [sg.Text('Consultar Publicação', font=font)],
                [sg.Input("ID",key='-ID-',font=font,s=(20)),sg.Button('ID',k='-IDB-', font=font)],
                [sg.Button('Back',k='-BACK-', font=font)],
                [sg.Text(version+trademark, text_color= '#7C615C')]
            ]

            m3 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMenu3,finalize=True,element_justification='c')

            m3.bind('<Escape>','-BACK-')

            while True:
                eventMenu3, valuesMenu3 = m3.read()

                if eventMenu3 == sg.WINDOW_CLOSED:
                    break

                match eventMenu3:
                    case '-IDB-':
                        try:
                            publicacao = publicacoes[valuesMenu3['-ID-']]
                            mostrar_publicacao(publicacao)
                        except:
                            sg.popup("Publicação não encontrada")
                    case '-BACK-':
                        break
            m3.close()
            window.un_hide()
        case '-CONPS-': # List Publications
            window.hide()

            layoutMenu4 = [
                [sg.Text('Consultar Publicações', font=font)],
                [sg.Input("Filtrar por titulo (vazio para não filtrar)",key='-TITLE-',font=font,s=(40))],
                [sg.Input("Filtrar por autor (vazio para não filtrar)",key='-AUTOR-',font=font,s=(40))],
                [sg.Input("Filtrar por afiliação (vazio para não filtrar)",key='-AFIL-',font=font,s=(40))],
                [sg.Input("Filtrar por palavra-chave (vazio para não filtrar)",key='-KEYWORDS-',font=font,s=(40))],
                [sg.Input("Filtrar por data de publicação (vazio para não filtrar)",key='-PDATE-',font=font,s=(40))],
                [sg.Button('Filtrar',k='-FILT-', font=font,s= (10))],
                [sg.Text(version+trademark, text_color= '#7C615C'),sg.Push(),sg.Button('Back',k='-BACK-', font=font,s= (10))]
            ]

            m4 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMenu4,finalize=True,element_justification='c',size = (575,250))

            while True:
                eventMenu4, valuesMenu4 = m4.read()

                if eventMenu4 == sg.WINDOW_CLOSED:
                    break

                match eventMenu4:
                    case '-FILT-':
                        filtrado = publicacoes.values()
                        
                        if valuesMenu4['-TITLE-'] != '':
                            filtrado = [publicacao for publicacao in filtrado if valuesMenu4['-TITLE-'] in publicacao.get('title', '').lower()]
                        if valuesMenu4['-AUTOR-'] != '':
                            filtrado = [publicacao for publicacao in filtrado for autor in publicacao.get('authors', []) if valuesMenu4['-AUTOR-'] in autor.get('name', '').lower()]
                        if valuesMenu4['-AFIL-'] != '':
                            filtrado = [publicacao for publicacao in filtrado for autor in publicacao.get('authors', []) if valuesMenu4['-AFIL-'] in autor.get('affiliation', '').lower()]
                        if valuesMenu4['-KEYWORDS-'] != '':
                            keyword = valuesMenu4['-KEYWORDS-'].lower()
                            filtrado = [publicacao for publicacao in filtrado if any(keyword in kw.strip().lower() for kw in publicacao.get('keywords', '').split(','))] 
                        if valuesMenu4['-PDATE-'] != '':
                            filtrado = [publicacao for publicacao in filtrado if valuesMenu4['-PDATE-'] in publicacao.get('publish_date', '').lower()]

                        if filtrado :
                            filtrado = list(filtrado)
                            tamanho_pagina = 10

                            total_paginas = (len(filtrado) + tamanho_pagina - 1) // 10
                            pagina_atual = 0
                            inicio = pagina_atual * tamanho_pagina
                            fim = inicio + tamanho_pagina
                            pub_column = []
                            publicacoes_pagina = filtrado[inicio:fim]
                            for publicacao in publicacoes_pagina:
                                title = publicacao.get('title', 'Sem título')
                                pub_text = [sg.Button(f'{title}',key=f'{title}')]
                                
                                pub_column.append(pub_text)
                            layoutMiniMenuFiltrado = [
                                [sg.Text('Publicações Filtradas', font=font)],
                                [sg.Button('Previous',k='-PREV-', font=font),sg.Column(pub_column,key = '-COL-', size=(300, 300)),sg.Button('Next',k='-NEXT-', font=font)],
                                [sg.Text(f"Página {pagina_atual + 1} de {total_paginas}",key = '-PAG-' ,font=font)],
                                [sg.Input("Path",key='-PATH-',font=font,s=(20)),sg.Button('Exportar',k='-EXPORT-', font=font)],
                                [sg.Button('Back',k='-BACK-', font=font)],
                                [sg.Text(version+trademark, text_color= '#7C615C')]
                            ]
                            
                
                            mini4 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMiniMenuFiltrado,finalize=True,element_justification='c')
                                
                            while True:
                                m4.hide()
                                mini4.bind('<Escape>','-BACK-')

                                eventMini4, valuesMini4 = mini4.read()

                                if eventMini4 == sg.WINDOW_CLOSED:
                                    break

                                match eventMini4:

                                    case '-PREV-':
                                        if pagina_atual > 0 - 1:
                                            pagina_atual -= 1
                                            inicio = pagina_atual * tamanho_pagina
                                            fim = inicio + tamanho_pagina
                                            pub_column = []
                                            publicacoes_pagina = filtrado[inicio:fim]
                                            for publicacao in publicacoes_pagina:
                                                title = publicacao.get('title', 'Sem título')
                                                pub_text = [sg.Button(f'{title}',key=f'{title}')]
                                                
                                                pub_column.append(pub_text)
                                            layoutMiniMenuFiltrado = [
                                                [sg.Text('Publicações Filtradas', font=font)],
                                                [sg.Button('Previous',k='-PREV-', font=font),sg.Column(pub_column,key = '-COL-', size=(300, 300)),sg.Button('Next',k='-NEXT-', font=font)],
                                                [sg.Text(f"Página {pagina_atual + 1} de {total_paginas}",key = '-PAG-' ,font=font)],
                                                [sg.Input("Path",key='-PATH-',font=font,s=(20)),sg.Button('Exportar',k='-EXPORT-', font=font)],
                                                [sg.Button('Back',k='-BACK-', font=font)],
                                                [sg.Text(version+trademark, text_color= '#7C615C')]
                                            ]
                                            mini4.close()
                                            mini4 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMiniMenuFiltrado,finalize=True,element_justification='c')
                                    case '-NEXT-':
                                        if pagina_atual < total_paginas - 1:
                                            pagina_atual += 1
                                            inicio = pagina_atual * tamanho_pagina
                                            fim = inicio + tamanho_pagina
                                            pub_column = []
                                            publicacoes_pagina = filtrado[inicio:fim]
                                            for publicacao in publicacoes_pagina:
                                                title = publicacao.get('title', 'Sem título')
                                                pub_text = [sg.Button(f'{title}',key=f'{title}')]
                                                
                                                pub_column.append(pub_text)
                                            layoutMiniMenuFiltrado = [
                                                [sg.Text('Publicações Filtradas', font=font)],
                                                [sg.Button('Previous',k='-PREV-', font=font),sg.Column(pub_column,key = '-COL-', size=(300, 300)),sg.Button('Next',k='-NEXT-', font=font)],
                                                [sg.Text(f"Página {pagina_atual + 1} de {total_paginas}",key = '-PAG-' ,font=font)],
                                                [sg.Input("Path",key='-PATH-',font=font,s=(20)),sg.Button('Exportar',k='-EXPORT-', font=font)],
                                                [sg.Button('Back',k='-BACK-', font=font)],
                                                [sg.Text(version+trademark, text_color= '#7C615C')]
                                            ]
                                            mini4.close()
                                            mini4 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMiniMenuFiltrado,finalize=True,element_justification='c')
                                    case '-EXPORT-':
                                        path = valuesMini4['-PATH-']
                                        try:
                                            exportar_json(path, filtrado)
                                            sg.popup("Publicações exportadas com sucesso")
                                        except:
                                            sg.popup("Erro a exportar publicações")
                                    case '-BACK-':
                                        break
                                    case _:
                                        mini4.hide()
                                        for publicacao in publicacoes_pagina:
                                            if eventMini4 == publicacao.get('title', 'Sem título'):
                                                mostrar_publicacao(publicacao)
                                                break
                                        mini4.un_hide()
                            mini4.close()
                            m4.un_hide()
                    case '-BACK-':
                        break
            m4.close()
            window.un_hide()

        case '-ES-': # Delete Publication
            window.hide()

            layoutMenu5 = [
                [sg.Text('Eliminar Publicação', font=font)],
                [sg.Input("ID",key='-ID-',font=font,s=(20)),sg.Button('ID',k='-IDB-', font=font)],
                [sg.Button('Back',k='-BACK-', font=font)],
                [sg.Text(version+trademark, text_color= '#7C615C')]
            ]

            m5 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMenu5,finalize=True,element_justification='c')

            m5.bind('<Escape>','-BACK-')

            while True:
                eventMenu5, valuesMenu5 = m5.read()

                if eventMenu5 == sg.WINDOW_CLOSED:
                    break

                match eventMenu5:
                    case '-IDB-':
                        try:
                            publicacao = publicacoes[valuesMenu5['-ID-']]
                            id_publicacao = extrair_id_publicacao(publicacao.get('url', ''))
                            eliminar_publicacao_grafica(id_publicacao,fcc_data)
                            sg.popup("Publicação eliminada com sucesso")
                        except:
                            sg.popup("Erro a eliminar publicação")
                    case '-BACK-':
                        break
            m5.close()
            window.un_hide()
        case '-EST-': # Statistics
            window.hide()
            layoutMenu6 = [
                [sg.Text('Estatísticas', font=font)],
                [sg.Button('Distribuição de publicações por ano',k='-DPA-', font=font),sg.Button('Distribuição de publicações por mês de um determinado ano',k='-DPMA-', font=font)],
                [sg.Button('Número de publicações por autor (top 20 autores)',k='-NPA20-', font=font),sg.Button('Distribuição de publicações de um autor por anos',k='-DPAA-', font=font)],
                [sg.Input("Número de palavras chave a representar",k='-INDPCFA-'),sg.Button('Distribuição de palavras-chave mais frequente por ano',k='-DPCFA-', font=font)],
                [sg.Button('Distribuição de palavras-chave pela sua frequência (top 20 palavras-chave)',k='-DPC20-', font=font)],
                [sg.Button('Back',k='-BACK-', font=font)],
                [sg.Text(version+trademark, text_color= '#7C615C')]
            ]

            m6 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMenu6,finalize=True,element_justification='c')

            m6.bind('<Escape>','-BACK-')

            while True:
                eventMenu6, valuesMenu6 = m6.read()

                if eventMenu6 == sg.WINDOW_CLOSED:
                    break

                match eventMenu6:
                    case '-DPA-':
                        # Done
                        anos, counts = zip(*sorted(estatisticas['publicacoes_por_ano'].items(), key=lambda x: x[1], reverse=True))
                        plt.figure(figsize=(10, 5))
                        plt.bar(anos, counts)
                        plt.title('Distribuição de publicações por ano')
                        plt.xlabel('Ano')
                        plt.ylabel('Número de publicações')
                        plt.show()
                        
                    case '-DPMA-':
                        ano_mais_recente = max(estatisticas['publicacoes_por_ano'], key=estatisticas['publicacoes_por_ano'].get)
                        publicacoes_por_mes = sorted(estatisticas['publicacoes_por_mes'][ano_mais_recente].items(), key=lambda x: x[1], reverse=True)
                        meses, counts = zip(*publicacoes_por_mes)
                        plt.figure(figsize=(10, 5))
                        plt.bar(meses, counts)
                        plt.title(f'Distribuição de publicações por mês em {ano_mais_recente}')
                        plt.xlabel('Mês')
                        plt.ylabel('Número de publicações')
                        plt.show()
                    case '-NPA20-':
                        top_autores = sorted(estatisticas['publicacoes_por_autor'].items(), key=lambda x: x[1], reverse=True)[:20]
                        autores, counts = zip(*top_autores)
                        plt.figure(figsize=(10, 5))
                        plt.barh(autores, counts)
                        plt.title('Número de publicações por autor (top 20 autores)')
                        plt.xlabel('Número de publicações')
                        plt.ylabel('Autor')
                        plt.gca().invert_yaxis()
                        plt.show()
                    case '-DPAA-': 
                        autor_mais_publicacoes = max(estatisticas['publicacoes_por_autor'], key=estatisticas['publicacoes_por_autor'].get)
                        publicacoes_por_ano = sorted(estatisticas['publicacoes_por_autor_por_ano'][autor_mais_publicacoes].items(), key=lambda x: x[1], reverse=True)
                        anos, counts = zip(*publicacoes_por_ano)
                        plt.figure(figsize=(10, 5))
                        plt.bar(anos, counts)
                        plt.title(f'Distribuição de publicações por ano para {autor_mais_publicacoes}')
                        plt.xlabel('Ano')
                        plt.ylabel('Número de publicações')
                        plt.show()
                    case '-DPC20-':
                        top_palavras_chave = sorted(estatisticas['palavras_chave_frequencia'].items(), key=lambda x: x[1], reverse=True)[:20]
                        palavras, counts = zip(*top_palavras_chave)
                        plt.figure(figsize=(10, 5))
                        plt.barh(palavras, counts)
                        plt.title('Distribuição de palavras-chave pela sua frequência (top 20 palavras-chave)')
                        plt.xlabel('Frequência')
                        plt.ylabel('Palavra-chave')
                        plt.gca().invert_yaxis()
                        plt.show()
                    case '-DPCFA-':
                        max_palavras = valuesMenu6['-INDPCFA-']
                        if max_palavras == '':
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
                    case '-BACK-':
                        break
            m6.close()
            window.un_hide()

        case '-LA-': # List Authors
            window.hide()

            if not autores_ordenados :
                autores_ordenados = sorted(publicacoes_autor, key=lambda x: len(x[1]), reverse=True)
            
            tamanho_pagina = 10

            total_paginas = (len(autores_ordenados) + tamanho_pagina - 1) // 10
            pagina_atual = 0
            inicio = pagina_atual * tamanho_pagina
            fim = inicio + tamanho_pagina
            author_column = []
            autores_pagina = autores_ordenados[inicio:fim]
            for autor, n_p in autores_pagina:
                author_text = [sg.Button(f'Autor: {autor}',key=f'{autor}')]
                
                author_column.append(author_text)
            
            layoutMenu7 = [
                [sg.Text('Listar Autores', font=font)],
                [sg.Button('Previous',k='-PREV-', font=font),sg.Column(author_column,key = '-COL-', size=(150, 300)),sg.Button('Next',k='-NEXT-', font=font)],
                [sg.Text(f"Página {pagina_atual + 1} de {total_paginas}",key = '-PAG-' ,font=font)],
                [sg.Button('Back',k='-BACK-', font=font)],
                [sg.Text(version+trademark, text_color= '#7C615C')]
            ]

            m7 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMenu7,finalize=True,element_justification='c')

            m7.bind('<Escape>','-BACK-')

            while True:
                eventMenu7, valuesMenu7 = m7.read()

                if eventMenu7 == sg.WINDOW_CLOSED:
                    break

                match eventMenu7:
                    case '-PREV-':
                            if pagina_atual > 0:
                                pagina_atual -= 1
                                inicio = pagina_atual * tamanho_pagina
                                fim = inicio + tamanho_pagina
                                author_column = []
                                autores_pagina = autores_ordenados[inicio:fim]
                                for autor, n_p in autores_pagina:
                                    author_text = [sg.Button(f'Autor: {autor}',key=f'{autor}')]
                                    author_column.append(author_text)
                                layoutMenu7 = [
                                    [sg.Text('Listar Autores', font=font)],
                                    [sg.Button('Previous',k='-PREV-', font=font),sg.Column(author_column,key = '-COL-', size=(150, 300)),sg.Button('Next',k='-NEXT-', font=font)],
                                    [sg.Text(f"Página {pagina_atual + 1} de {total_paginas}",key = '-PAG-' ,font=font)],
                                    [sg.Button('Back',k='-BACK-', font=font)],
                                    [sg.Text(version+trademark, text_color= '#7C615C')]
                                ]
                                m7.close()
                                m7 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMenu7,finalize=True,element_justification='c')
                    case '-NEXT-':
                        if pagina_atual < total_paginas - 1:
                            pagina_atual += 1
                            inicio = pagina_atual * tamanho_pagina
                            fim = inicio + tamanho_pagina
                            author_column = []
                            autores_pagina = autores_ordenados[inicio:fim]
                            for autor, n_p in autores_pagina:
                                author_text = [sg.Button(f'Autor: {autor}',key=f'{autor}')]
                                author_column.append(author_text)
                            layoutMenu7 = [
                                [sg.Text('Listar Autores', font=font)],
                                [sg.Button('Previous',k='-PREV-', font=font),sg.Column(author_column,key = '-COL-', size=(150, 300)),sg.Button('Next',k='-NEXT-', font=font)],
                                [sg.Text(f"Página {pagina_atual + 1} de {total_paginas}",key = '-PAG-' ,font=font)],
                                [sg.Button('Back',k='-BACK-', font=font)],
                                [sg.Text(version+trademark, text_color= '#7C615C')]
                            ]
                            m7.close()
                            m7 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMenu7,finalize=True,element_justification='c')
                    case '-BACK-':
                        break
                    case _ :
                        autor = m7[eventMenu7].get_text().split(': ')[1]
                        publicacoes_total = []
                        for autor2, n_p in autores_pagina:
                            if autor == autor2:
                                for publication in n_p:
                                    title = publicacoes[publication].get('title', 'Sem título')
                                    publicacoes_total.append([sg.Text(f'  - {title}')])
                                break

                        layoutMiniMenuAutorPublicações = [
                            [sg.Text(f'Publicações de {autor}', font=font)],
                            [sg.Column(publicacoes_total, size=(500, 250),scrollable=True)],
                            [sg.Button('Back',k='-BACK-', font=font)],
                            [sg.Text(version+trademark, text_color= '#7C615C'),sg.Push()]
                            ]
                        while True:
                            m7.hide()
                            mini7 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMiniMenuAutorPublicações,finalize=True,element_justification='c')
                            mini7.bind('<Escape>','-BACK-')

                            eventMini7, valuesMini7 = mini7.read()

                            if eventMini7 == sg.WINDOW_CLOSED:
                                break

                            match eventMini7:
                                case '-BACK-':
                                    break
                        m7.un_hide()
                        mini7.close()

            m7.close()
            window.un_hide()
        case '-IP-': # Import Publications
            window.hide()

            layoutMenu8 = [
                [sg.Text('Importar Publicações', font=font)],
                [sg.Input("Path",key='-PATH-',font=font,s=(20)),sg.Button('Importar',k='-IPB-', font=font)],
                [sg.Button('Back',k='-BACK-', font=font)],
                [sg.Text(version+trademark, text_color= '#7C615C')]
            ]

            m8 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMenu8,finalize=True,element_justification='c')

            m8.bind('<Escape>','-BACK-')

            while True:
                eventMenu8, valuesMenu8 = m8.read()

                if eventMenu8 == sg.WINDOW_CLOSED:
                    break

                match eventMenu8:
                    case '-IPB-':
                        try :
                            carregar_json(valuesMenu8['-PATH-'])
                            sg.popup("Publicações importadas com sucesso")
                        except:
                            sg.popup("Erro ao importar publicações")
                    case '-BACK-':
                        break
            m8.close()
            window.un_hide()
        
        case '-EP-': # Export Publications
            window.hide()

            layoutMenu9 = [
                [sg.Text('Exportar Publicações', font=font)],
                [sg.Input("Path",key='-PATH-',font=font,s=(20)),sg.Button('Exportar',k='-IPB-', font=font)],
                [sg.Button('Back',k='-BACK-', font=font)],
                [sg.Text(version+trademark, text_color= '#7C615C')]
            ]

            m9 = sg.Window("Sistema de Consulta e Análise de Publicações Científicas", layout=layoutMenu9,finalize=True,element_justification='c')

            m9.bind('<Escape>','-BACK-')

            while True:
                eventMenu9, valuesMenu9 = m9.read()

                if eventMenu9 == sg.WINDOW_CLOSED:
                    break

                match eventMenu9:
                    case '-IPB-':
                        try:
                            exportar_json(valuesMenu9['-PATH-'],fcc_data)
                            sg.popup("Publicações exportadas com sucesso")
                        except:
                            sg.popup("Erro ao exportar publicações")
                        
                    case '-BACK-':
                        break
            m9.close()
            window.un_hide()
        case '-CLOSE-':
                break


window.close()



