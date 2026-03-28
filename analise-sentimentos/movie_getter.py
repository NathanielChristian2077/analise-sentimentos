import re
import time
import requests
from bs4 import BeautifulSoup


class MovieGetter:
    BASE_URL = 'https://www.adorocinema.com/filmes-todos/'

    def __init__(self, delay=0.0):
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0'
        }

    def extrair_codigos_pagina(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', class_='meta-title-link')

        codigos = []
        for link in links:
            href = link.get('href', '')
            match = re.search(r'/filmes/filme-(\d+)/', href)
            if match:
                codigos.append(match.group(1))

        return codigos

    def obter_codigo_unico(self, codigo):
        return [str(codigo).strip()]

    def obter_varios_codigos(self, quantidade):
        codigos = []
        pagina = 1

        while len(codigos) < quantidade:
            url = self.BASE_URL if pagina == 1 else f'{self.BASE_URL}?page={pagina}'

            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            codigos_pagina = self.extrair_codigos_pagina(response.text)

            if not codigos_pagina:
                break

            for codigo in codigos_pagina:
                if codigo not in codigos:
                    codigos.append(codigo)

                if len(codigos) >= quantidade:
                    break

            pagina += 1

            if self.delay > 0:
                time.sleep(self.delay)

        return codigos

    def salvar_codigos(self, codigos, caminho='movie_codes.txt'):
        with open(caminho, 'w', encoding='utf-8') as f:
            for codigo in codigos:
                f.write(codigo + '\n')
