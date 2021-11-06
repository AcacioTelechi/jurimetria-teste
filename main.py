from selenium import webdriver

class tjpr_scraper():

    def __init__(self, hide=True):
        self.driver = self._inicializar_drivier(hide)
    
    def _inicializar_drivier(self, hide):
        options = webdriver.ChromeOptions()
        if hide:
            options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        return driver

    def _get_itens_tabela_resultado(self, url):
        self.driver.get(url)
        tab = scraper.driver.find_elements_by_class_name("resultTable")[1]
        itens = tab.find_elements_by_tag_name("tr")[1:]
        return itens, tab

    def _get_dados_item(self, item):
        dados_item = item.find_element_by_class_name("juris-tabela-dados")
        link = dados_item.find_element_by_tag_name("a").get_attribute("href")
        return dados_item.text, link

    def _get_ementa_itam(self, item):
        ementa_item = item.find_element_by_class_name("juris-tabela-ementa")
        try:
            ementa_item.find_element_by_tag_name("a").click()
            ementa_item = ementa_item.text
        except:
            ementa_item = ementa_item.text
        return ementa_item
    
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


if __name__ == "__main__":
    url = 'https://portal.tjpr.jus.br/jurisprudencia/publico/pesquisa.do?actionType=pesquisar'
    scraper = tjpr_scraper()
    url_list = scraper.get_url_list(url)
    print(url_list)
    lista_final = []
    for url in url_list:
        dados = scraper.get_data_from_processo(url)
        lista_final.append(dados)
    print(lista_final)
