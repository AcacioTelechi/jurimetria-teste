   # url = 'https://portal.tjpr.jus.br/jurisprudencia/publico/pesquisa.do?actionType=pesquisar'
    # scraper = tjpr_scraper()
    # url_list = scraper.get_url_list(url)
    # print(url_list)
    # lista_final = []
    # for url in url_list:
    #     dados = scraper.get_data_from_processo(url)
    #     lista_final.append(dados)
    # print(lista_final)

def get_url_list(self, url):
    self.driver.get(url)
    dados = self.driver.find_elements_by_class_name("juris-tabela-propriedades")
    return [dado.find_element_by_tag_name("a").get_attribute("href") for dado in dados]

def get_data_from_processo(self, url):
    self.driver.get(url)
    dados = self.driver.find_element_by_class_name('juris-dados-completos')
    dados_list = dados.text.split('\n')
    ementa = dados_list[-1]
    for i, dado in enumerate(dados_list):
        if "Processo" in dado:
            split = dado.split(' ')
            processo = split[1].strip()
            tipo = split[2].replace('(', '').replace(')', '').strip()
        if "Segredo" in dado:
            segredo = dado.split(':')[1].strip()
        if "Relator" in dado:
            relator = dado.split(':')[1].strip()
            relator_cargo = dados_list[i+1].strip()
        if "Órgão Julgador" in dado:
            orgao_julgador = dado.split(':')[1].strip()
        if "Comarca" in dado:
            comarca = dado.split(':')[1].strip()
        if "Data do Julgamento" in dado:
            data_julgamento = dado.split(': ')[1].strip()
        if "Data da Publicação" in dado:
            data_publicacao = dado.split(': ')[1].strip()
    return {
        'processo': processo,
        'tipo': tipo,
        'segredo': segredo,
        'relator': relator,
        'relator_cargo': relator_cargo,
        'orgao_julgador': orgao_julgador,
        'comarca': comarca,
        'data_julgamento': data_julgamento,
        'data_publicacao': data_publicacao,
        'ementa': ementa
    }

