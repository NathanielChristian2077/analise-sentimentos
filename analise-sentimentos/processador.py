import re

class ProcessadorTexto:

    def __init__(self):
        # palavras que serão ignoradas
        self.stopwords = set([
            "o", "a", "os", "as", "de", "da", "do", "e", "é", "em",
            "um", "uma", "para", "pra", "com", "não", "na", "no"
        ])

    def limpar_texto(self, texto):
        texto = texto.lower()
        texto = re.sub(r'[^\w\sÀ-ÿ]', ' ', texto)  # remove pontuação, mas mantem acentos
        texto = re.sub(r'\s+', ' ', texto) # remove espaços duplicados
        return texto

    def tokenizar(self, texto):
        return texto.split()

    def remover_stopwords(self, tokens):
        return [t for t in tokens if t not in self.stopwords]

    def processar(self, texto):
        texto = self.limpar_texto(texto)
        tokens = self.tokenizar(texto)
        tokens = self.remover_stopwords(tokens)
        return tokens

    def separar_comentarios(self, texto):
        comentarios = texto.split('\n\n')  # separa os comments por linha em branco
        comentarios = [c.strip() for c in comentarios if c.strip()]
        return comentarios

    def processar_arquivo(self, caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            texto = f.read()

        comentarios = self.separar_comentarios(texto)

        resultado = []
        for comentario in comentarios:
            tokens = self.processar(comentario)
            resultado.append(tokens)

        return resultado
    