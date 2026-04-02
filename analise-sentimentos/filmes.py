import requests
from bs4 import BeautifulSoup


class AdoroCinemaFilmes:
    BASE_URL = 'https://www.adorocinema.com/filmes/filme-'
    CRAWLER_OUTPUT_PATH = './crawler_output/'

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0'
        }

    def _fazer_request(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.text

    def extrair_titulo_e_sinopse(self, filme):
        url = f'{self.BASE_URL}{filme}/'
        html = self._fazer_request(url)
        soup = BeautifulSoup(html, 'html.parser')

        titulo = ''
        sinopse = ''

        titulo_tag = soup.find('h1')
        if titulo_tag:
            titulo = titulo_tag.get_text(strip=True)

        sinopse_tag = soup.find('div', class_='content-txt')
        if sinopse_tag:
            sinopse = sinopse_tag.get_text(strip=True)

        return titulo, sinopse

    def extrair_comentarios_filme(self, filme, paginas_comentarios):
        comentarios = []
        comentarios_vistos = set()

        for pagina in range(1, paginas_comentarios + 1):
            url = f'{self.BASE_URL}{filme}/criticas/espectadores/?page={pagina}'
            html = self._fazer_request(url)
            soup = BeautifulSoup(html, 'html.parser')

            comentarios_tags = soup.find_all('div', class_='content-txt review-card-content')

            if not comentarios_tags:
                print(f'Página {pagina}: nenhum comentário encontrado. Encerrando coleta.')
                break

            novos_na_pagina = 0

            for comentario_tag in comentarios_tags:
                comentario = comentario_tag.get_text().strip()

                if comentario and comentario not in comentarios_vistos:
                    comentarios.append(comentario)
                    comentarios_vistos.add(comentario)
                    novos_na_pagina += 1

            print(f'Página {pagina}: {novos_na_pagina} comentários novos.')

            if novos_na_pagina == 0:
                print(f'Página {pagina}: nenhum comentário novo. Encerrando coleta.')
                break

        return comentarios

    def extrair_dados_filme(self, filme, paginas_comentarios=1):
        titulo, sinopse = self.extrair_titulo_e_sinopse(filme)
        comentarios = self.extrair_comentarios_filme(filme, paginas_comentarios)

        return {
            'codigo': str(filme),
            'titulo': titulo,
            'sinopse': sinopse,
            'comentarios': comentarios
        }

    def salvar_sinopse_filme(self, filme, sinopse):
        caminho = f'{self.CRAWLER_OUTPUT_PATH}{filme}_sinopse.txt'
        with open(caminho, 'w', encoding='utf-8') as arquivo:
            arquivo.write(sinopse)

    def salvar_comentarios_filme(self, filme, comentarios):
        caminho = f'{self.CRAWLER_OUTPUT_PATH}{filme}_comentarios.txt'
        with open(caminho, 'w', encoding='utf-8') as arquivo:
            for comentario in comentarios:
                arquivo.write(comentario + '\n\n')

    def salvar_dados_filme(self, dados_filme):
        codigo = dados_filme['codigo']
        self.salvar_sinopse_filme(codigo, dados_filme['sinopse'])
        self.salvar_comentarios_filme(codigo, dados_filme['comentarios'])
