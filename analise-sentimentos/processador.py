import re
import unicodedata


class ProcessadorTexto:

    def remover_acentos(self, texto):
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )

    def reduzir_repeticoes(self, texto):
        # reduz repetições exageradas de letras:
        # "seeeennnnsacionalllllllllll" -> "sensacional"
        # "ameiiii" -> "amei"
        return re.sub(r'([a-zA-Z])\1{2,}', r'\1', texto)

    def limpar_texto(self, texto):
        texto = texto.lower()
        texto = self.remover_acentos(texto)
        texto = self.reduzir_repeticoes(texto)
        texto = re.sub(r'[^\w\s/]', ' ', texto)  # mantém letras, números, espaços e '/'
        texto = re.sub(r'\s+', ' ', texto).strip()
        return texto

    def processar_comentario(self, comentario):
        return {
            'original': comentario,
            'processado': self.limpar_texto(comentario)
        }

    def processar_comentarios(self, comentarios):
        return [self.processar_comentario(comentario) for comentario in comentarios]

    def separar_comentarios(self, texto):
        comentarios = texto.split('\n\n')
        return [c.strip() for c in comentarios if c.strip()]

    def ler_comentarios_arquivo(self, caminho):
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            texto = arquivo.read()
        return self.separar_comentarios(texto)

    def processar_arquivo(self, caminho):
        comentarios = self.ler_comentarios_arquivo(caminho)
        return self.processar_comentarios(comentarios)

    def salvar_comentarios_processados(self, comentarios_processados, caminho_saida):
        with open(caminho_saida, 'w', encoding='utf-8') as arquivo:
            for comentario in comentarios_processados:
                arquivo.write('Original: ' + comentario['original'] + '\n')
                arquivo.write('Processado: ' + comentario['processado'] + '\n\n')
