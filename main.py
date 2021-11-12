from selenium import webdriver
import json

class tjpr_scraper():

    def __init__(self, hide=True):
        self.driver = self._inicializar_drivier(hide)
        self.base = None
    
    def _inicializar_drivier(self, hide):
        options = webdriver.ChromeOptions()
        if hide:
            options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        return driver

    def _get_itens_tabela_resultado(self):
        tab = self.driver.find_elements_by_class_name("resultTable")[1]
        itens = tab.find_elements_by_tag_name("tr")[1:]
        return itens

    def get_dados_item(self, item):
        tab_dados = item.find_element_by_class_name("juris-tabela-dados")
        link = tab_dados.find_element_by_tag_name("a").get_attribute("href")
        dados = self._get_dados_item(tab_dados)
        ementa = self._get_ementa_item(item)
        return {
            "link": link,
            "dados": dados,
            "ementa": ementa
        }

    def _get_ementa_item(self, item):
        ementa_item = item.find_element_by_class_name("juris-tabela-ementa")
        try:
            ementa_item.find_element_by_tag_name("a").click()
            ementa_item = ementa_item.text
        except:
            ementa_item = ementa_item.text
        return ementa_item
    
    def _get_dados_item(self, dados_item):
        dados_split = dados_item.text.split("\n")
        processo, tipo = self._tratar_tipo(dados_split[0])
        relator = self._tratar_relator(dados_split[2])
        cargo = dados_split[3]
        orgao = self._tratar_orgao(dados_split[6])
        data = self._tratar_data(dados_split[7])
        return {
            "processo": processo,
            "tipo": tipo,
            "relator": relator,
            "cargo": cargo,
            "orgao": orgao,
            "data": data
        }
    
    def _tratar_tipo(self, processo):
        split = processo.split(' ')
        numero = split[1]
        tipo = split[3].replace('(', '') + ' ' + split[4].replace(')', '')
        return numero, tipo
    
    def _tratar_relator(self, relator):
        split = relator.split(' ')
        r = split[2:]
        r = ' '.join(r)
        return r

    def _tratar_orgao(self, orgao):
        split = orgao.split(' ')
        o = split[2:]
        o = ' '.join(o)
        return o

    def _tratar_data(self, data):
        return data.split(' ')[2]

    def get_dados(self):
        itens = scraper._get_itens_tabela_resultado()
        lista_ok = []
        lista_pendentes = []
        for item in itens:
            dados_item = scraper.get_dados_item(item)
            if dados_item['ementa'] == 'Conteúdo pendente de análise e liberação para consulta pública.':
                lista_pendentes.append(dados_item)
            else:
                lista_ok.append(dados_item)
        return lista_ok, lista_pendentes

if __name__ == "__main__":
    url = 'https://portal.tjpr.jus.br/jurisprudencia/publico/pesquisa.do?actionType=pesquisar'
    scraper = tjpr_scraper()
    scraper.driver.get(url)
    lista_ok, lista_pendentes = scraper.get_dados()
    with open('teste3.json', 'w', encoding='utf8') as f:
        json.dump(lista_ok, f, ensure_ascii=False)