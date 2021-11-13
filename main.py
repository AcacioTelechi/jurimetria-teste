from selenium import webdriver
import re
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

    def _get_dict_item(self, item):
        tab_dados = item.find_element_by_class_name("juris-tabela-dados")
        link = tab_dados.find_element_by_tag_name("a").get_attribute("href")
        dados = self._get_dados_item(tab_dados.text)
        ementa = self._get_ementa_item(item)
        return {
            "link": link,
            "processo": dados['processo'],
            "tipo": dados['tipo'],
            "relator": dados['relator'],
            "cargo": dados['cargo'],
            "orgao": dados['orgao'],
            "data": dados['data'],
            "ementa": ementa
        }

    def _get_ementa_item(self, item):
        ementa_item = item.find_element_by_class_name("juris-tabela-ementa")
        try:
            ementa_item.find_element_by_tag_name("a").click()
            # colocar para esperar um pouco pq tá pegando o "carregando"
            ementa_item = ementa_item.text
        except:
            ementa_item = ementa_item.text
        return ementa_item
    
    def _get_dados_item(self, dados_item):
        processo = self._tratar_processo(dados_item)
        tipo = self._tratar_tipo(dados_item)
        relator = self._tratar_relator(dados_item)
        cargo = self._tratar_cargo(dados_item)
        orgao = self._tratar_orgao(dados_item)
        data = self._tratar_data(dados_item)
        return {
            "processo": processo,
            "tipo": tipo,
            "relator": relator,
            "cargo": cargo,
            "orgao": orgao,
            "data": data
        }
    
    def _tratar_tipo(self, texto):
        pattern=r'\(.*\)'
        match = re.search(pattern, texto)
        if match:
            return match[0].replace('(','').replace(')','')
        else:
            return ''
    
    def _tratar_processo(self, texto):
        pattern=r'\bProcesso:.*\b'
        match = re.search(pattern, texto)
        if match:
            return match[0].replace('Processo:', '').strip()
        else:
            return ''

    def _tratar_relator(self, texto):
        pattern=r'\bRelator:.*\b'
        match = re.search(pattern, texto)
        if match:
            return match[0].replace('Relator:', '').strip()
        else:
            return ''

    def _tratar_cargo(self, texto):
        pattern=r'\bRelator:.*\n.*\b'
        match = re.search(pattern, texto)
        if match:
            return match[0].split('\n')[-1]
        else:
            return ''

    def _tratar_orgao(self, texto):
        pattern=r'\bÓrgão Julgador: .*\b'
        match = re.search(pattern, texto)
        if match:
            return match[0].replace('Órgão Julgador:', '').strip()
        else:
            return ''

    def _tratar_data(self, texto):
        pattern=r'\d{2}/\d{2}/\d{4}'
        match = re.search(pattern, texto)
        if match:
            return match[0]
        else:
            return ''

    def get_dados(self, max_paginas = 10):
        total_processos = self.get_total_processos()
        lista_ok = []
        lista_pendentes = []
        for i in range(max_paginas):
            itens = self._get_itens_tabela_resultado()
            for item in itens:
                dados_item = self._get_dict_item(item)
                if dados_item['ementa'] == 'Conteúdo pendente de análise e liberação para consulta pública.':
                    lista_pendentes.append(dados_item)
                else:
                    lista_ok.append(dados_item)
            self.driver.find_element_by_class_name("arrowNextOn").click()
        self.driver.quit()
        print(f"Total de processos baixados: {len(lista_ok)} ok e {len(lista_pendentes)} sem ementa. \nTotal de procesos: {total_processos}")
        return lista_ok, lista_pendentes
    
    def get_total_processos(self):
        return int(self.driver.find_element_by_class_name("navLeft").text.split(' ')[0])

if __name__ == "__main__":
    url = 'https://portal.tjpr.jus.br/jurisprudencia/publico/pesquisa.do?actionType=pesquisar'
    scraper = tjpr_scraper(hide=False)
    scraper.driver.get(url)
    lista_ok, lista_pendentes = scraper.get_dados(max_paginas=5)
    with open(r'./output/teste_ok.json', 'w', encoding='utf8') as f:
        json.dump(lista_ok, f, ensure_ascii=False)
    with open(r'./output/teste_pendentes.json', 'w', encoding='utf8') as f:
        json.dump(lista_pendentes, f, ensure_ascii=False)   