import re


class ClassificadorSentimento:

    def __init__(self):
        self.padroes_positivos_leves = [
            r'\bgostei\b',
            r'\bbom\b',
            r'\bboa\b',
            r'\bbonito\b',
            r'\bbonita\b',
            r'\blindo\b',
            r'\blinda\b',
            r'\brecomendo\b',
            r'\blegal\b',
            r'\bvale a pena\b',
            r'\bcurti\b'
        ]

        self.padroes_positivos_medios = [
            r'\badorei\b',
            r'\bamei\b',
            r'\botimo\b',
            r'\bexcelente\b',
            r'\bincrivel\b',
            r'\bespetacular\b',
            r'\bmaravilhoso\b',
            r'\bmaravilhosa\b',
            r'\bfantastico\b',
            r'\bfantastica\b',
            r'\bsensacional\b',
            r'\bemocionante\b',
            r'\bgenial\b',
            r'\bcativante\b',
            r'\bempolgante\b',
            r'\bgrandioso\b',
            r'\bmemoravel\b',
            r'\bmarcante\b',
            r'\bbelissimo\b',
            r'\bbelissima\b',
            r'\bindescritivel\b',
            r'\bmuito bom\b',
            r'\bmuito boa\b',
            r'\bum show\b',
            r'\bo melhor\b'
        ]

        self.padroes_positivos_fortes = [
            r'\bperfeito\b',
            r'\bperfeita\b',
            r'\bobra prima\b',
            r'\bobra-prima\b',
            r'\bclassico\b',
            r'\bepico\b',
            r'\bfenomenal\b',
            r'\bimpecavel\b',
            r'\bmagnifico\b',
            r'\bextraordinario\b',
            r'\bextraordinaria\b',
            r'\bmelhor filme\b',
            r'\bmelhor da trilogia\b',
            r'\bmelhor da saga\b',
            r'\bfinal perfeito\b',
            r'\bfechou com chave de ouro\b',
            r'\bsem duvida\b',
            r'\badoro esse filme\b',
            r'\bum dos melhores filmes\b',
            r'\bo melhor da saga inteira\b',
            r'\bo melhor da saga\b',
            r'\bo melhor da trilogia\b'
        ]

        self.padroes_negativos_leves = [
            r'\blento\b',
            r'\blenta\b',
            r'\bfraco\b',
            r'\bfraca\b',
            r'\bchato\b',
            r'\bchata\b',
            r'\bcansativo\b',
            r'\bcansativa\b',
            r'\bsem graca\b',
            r'\bsem sal\b',
            r'\bmediano\b',
            r'\bmediana\b',
            r'\bmais ou menos\b'
        ]

        self.padroes_negativos_medios = [
            r'\bruim\b',
            r'\bdecepcionante\b',
            r'\bfrustrante\b',
            r'\bpior\b',
            r'\bnao gostei\b',
            r'\bnao recomendo\b',
            r'\bnao curti\b',
            r'\bmuito ruim\b',
            r'\bentediante\b',
            r'\bmassante\b',
            r'\bmal feito\b',
            r'\bfraco demais\b'
        ]

        self.padroes_negativos_fortes = [
            r'\bodiei\b',
            r'\bpessimo\b',
            r'\bhorrivel\b',
            r'\bterrivel\b',
            r'\blixo\b',
            r'\bmedonho\b',
            r'\bpior filme\b',
            r'\bdesastre\b',
            r'\buma porcaria\b',
            r'\bnao presta\b'
        ]

        self.padroes_negacao_positiva = [
            r'\bnao gostei\b',
            r'\bnao recomendo\b',
            r'\bnao curti\b',
            r'\bnao e bom\b',
            r'\bnao e boa\b',
            r'\bnao foi bom\b',
            r'\bnao foi boa\b',
            r'\bnunca gostei\b',
            r'\bnao achei bom\b',
            r'\bnao achei boa\b'
        ]

        self.padroes_negacao_negativa = [
            r'\bnao e ruim\b',
            r'\bnao foi ruim\b',
            r'\bnao achei ruim\b',
            r'\bnao e pessimo\b',
            r'\bnao foi pessimo\b',
            r'\bnao e horrivel\b'
        ]

    def contar_ocorrencias(self, texto, padroes):
        total = 0
        for padrao in padroes:
            total += len(re.findall(padrao, texto))
        return total

    def extrair_nota(self, texto):
        padroes_nota = [
            r'\b([0-9]|10)/10\b',
            r'\bnota\s+([0-9]|10)\b',
            r'\bdou\s+([0-9]|10)\b',
            r'\bmerece\s+([0-9]|10)\b'
        ]

        for padrao in padroes_nota:
            match = re.search(padrao, texto)
            if match:
                return int(match.group(1))

        return None

    def calcular_score_comentario(self, comentario_processado):
        score = 0

        positivos_leves = self.contar_ocorrencias(comentario_processado, self.padroes_positivos_leves)
        positivos_medios = self.contar_ocorrencias(comentario_processado, self.padroes_positivos_medios)
        positivos_fortes = self.contar_ocorrencias(comentario_processado, self.padroes_positivos_fortes)

        negativos_leves = self.contar_ocorrencias(comentario_processado, self.padroes_negativos_leves)
        negativos_medios = self.contar_ocorrencias(comentario_processado, self.padroes_negativos_medios)
        negativos_fortes = self.contar_ocorrencias(comentario_processado, self.padroes_negativos_fortes)

        neg_positiva = self.contar_ocorrencias(comentario_processado, self.padroes_negacao_positiva)
        neg_negativa = self.contar_ocorrencias(comentario_processado, self.padroes_negacao_negativa)

        score += positivos_leves * 1
        score += positivos_medios * 2
        score += positivos_fortes * 3

        score -= negativos_leves * 1
        score -= negativos_medios * 2
        score -= negativos_fortes * 3

        score -= neg_positiva * 2
        score += neg_negativa * 2

        nota = self.extrair_nota(comentario_processado)
        if nota is not None:
            if nota >= 9:
                score += 3
            elif nota >= 7:
                score += 2
            elif nota == 6:
                score += 1
            elif nota <= 2:
                score -= 3
            elif nota <= 4:
                score -= 2
            elif nota == 5:
                score -= 1

        return score

    def classificar_comentario(self, comentario_processado):
        score = self.calcular_score_comentario(comentario_processado)

        if score > 0:
            return 'positivo'
        elif score < 0:
            return 'negativo'
        else:
            return 'neutro'

    def classificar_comentarios(self, comentarios_processados):
        resultados = []

        for comentario in comentarios_processados:
            categoria = self.classificar_comentario(comentario['processado'])

            resultados.append({
                'original': comentario['original'],
                'processado': comentario['processado'],
                'categoria': categoria
            })

        return resultados

    def calcular_resumo(self, comentarios_classificados):
        total = len(comentarios_classificados)

        positivos = sum(1 for c in comentarios_classificados if c['categoria'] == 'positivo')
        negativos = sum(1 for c in comentarios_classificados if c['categoria'] == 'negativo')
        neutros = sum(1 for c in comentarios_classificados if c['categoria'] == 'neutro')

        if total == 0:
            return {
                'total': 0,
                'positivos_qtd': 0,
                'negativos_qtd': 0,
                'neutros_qtd': 0,
                'positivos_pct': 0.0,
                'negativos_pct': 0.0,
                'neutros_pct': 0.0
            }

        return {
            'total': total,
            'positivos_qtd': positivos,
            'negativos_qtd': negativos,
            'neutros_qtd': neutros,
            'positivos_pct': (positivos / total) * 100,
            'negativos_pct': (negativos / total) * 100,
            'neutros_pct': (neutros / total) * 100
        }

    def classificar_filme(self, percentual_positivo):
        if percentual_positivo <= 10:
            return 'extremamente negativas'
        elif percentual_positivo <= 20:
            return 'muito negativas'
        elif percentual_positivo <= 30:
            return 'negativas'
        elif percentual_positivo <= 40:
            return 'ligeiramente negativas'
        elif percentual_positivo <= 60:
            return 'neutras'
        elif percentual_positivo <= 70:
            return 'ligeiramente positivas'
        elif percentual_positivo <= 80:
            return 'positivas'
        elif percentual_positivo <= 90:
            return 'muito positivas'
        else:
            return 'extremamente positivas'

    def analisar_filme(self, comentarios_processados):
        comentarios_classificados = self.classificar_comentarios(comentarios_processados)
        resumo = self.calcular_resumo(comentarios_classificados)
        categoria_final = self.classificar_filme(resumo['positivos_pct'])

        return {
            'comentarios_classificados': comentarios_classificados,
            'resumo': resumo,
            'categoria_final': categoria_final
        }
