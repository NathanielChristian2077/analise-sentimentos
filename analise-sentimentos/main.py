import argparse

from movie_getter import MovieGetter
from filmes import AdoroCinemaFilmes
from processador import ProcessadorTexto
from classificador import ClassificadorSentimento


OUTPUT_PATH = './crawler_output/'


def salvar_resultado_final(dados_filme, analise_filme):
    codigo = dados_filme['codigo']
    titulo = dados_filme['titulo']
    sinopse = dados_filme['sinopse']
    comentarios_classificados = analise_filme['comentarios_classificados']
    resumo = analise_filme['resumo']
    categoria_final = analise_filme['categoria_final']

    caminho_saida = f'{OUTPUT_PATH}{titulo}_{codigo}_resultado.txt'

    with open(caminho_saida, 'w', encoding='utf-8') as arquivo:
        arquivo.write(f'Código do filme: {codigo}\n')

        if titulo:
            arquivo.write(f'Título: {titulo}\n')

        arquivo.write('\nSinopse:\n')
        arquivo.write(sinopse if sinopse else 'Sinopse não encontrada.')
        arquivo.write('\n\n')

        arquivo.write('Comentários classificados:\n\n')
        for item in comentarios_classificados:
            arquivo.write(f'Comentário: {item["original"]}\n')
            arquivo.write(f'Categoria: {item["categoria"]}\n\n')

        arquivo.write('Resumo da análise:\n')
        arquivo.write(f'Quantidade de comentários lidos: {resumo["total"]}\n')
        arquivo.write(f'Comentários positivos: {resumo["positivos_qtd"]} ({resumo["positivos_pct"]:.2f}%)\n')
        arquivo.write(f'Comentários negativos: {resumo["negativos_qtd"]} ({resumo["negativos_pct"]:.2f}%)\n')
        arquivo.write(f'Comentários neutros: {resumo["neutros_qtd"]} ({resumo["neutros_pct"]:.2f}%)\n')
        arquivo.write(f'Categoria final do filme: {categoria_final}\n')
        arquivo.close()


def exibir_resumo_console(dados_filme, analise_filme):
    codigo = dados_filme['codigo']
    titulo = dados_filme['titulo']
    resumo = analise_filme['resumo']
    categoria_final = analise_filme['categoria_final']

    print('-' * 60)
    print(f'Filme: {codigo}' + (f' - {titulo}' if titulo else ''))
    print(f'Quantidade de comentários lidos: {resumo["total"]}')
    print(f'Comentários positivos: {resumo["positivos_qtd"]} ({resumo["positivos_pct"]:.2f}%)')
    print(f'Comentários negativos: {resumo["negativos_qtd"]} ({resumo["negativos_pct"]:.2f}%)')
    print(f'Comentários neutros: {resumo["neutros_qtd"]} ({resumo["neutros_pct"]:.2f}%)')
    print(f'Categoria final do filme: {categoria_final}')


def obter_codigos(args):
    getter = MovieGetter(delay=args.delay)

    if args.filme:
        return getter.obter_codigo_unico(args.filme)

    codigos = getter.obter_varios_codigos(args.quantidade)

    if args.salvar_codigos:
        getter.salvar_codigos(codigos)

    return codigos


def main():
    parser = argparse.ArgumentParser(description='Pipeline de coleta e classificação de comentários de filmes.')

    parser.add_argument(
        '-f', '--filme',
        type=str,
        help='Código de um filme específico.'
    )

    parser.add_argument(
        '-q', '--quantidade',
        type=int,
        default=1,
        help='Quantidade de filmes a obter quando não for informado um código específico.'
    )

    parser.add_argument(
        '-p', '--paginas',
        type=int,
        default=1,
        help='Número de páginas de comentários a coletar por filme.'
    )

    parser.add_argument(
        '-d', '--delay',
        type=float,
        default=0.0,
        help='Delay entre requisições do movie_getter.'
    )

    parser.add_argument(
        '--salvar-codigos',
        action='store_true',
        help='Salva os códigos obtidos em movie_codes.txt.'
    )

    args = parser.parse_args()

    codigos = obter_codigos(args)

    crawler = AdoroCinemaFilmes()
    processador = ProcessadorTexto()
    classificador = ClassificadorSentimento()

    for codigo in codigos:
        try:
            print(f'Processando filme {codigo}...')

            dados_filme = crawler.extrair_dados_filme(codigo, paginas_comentarios=args.paginas)

            comentarios_processados = processador.processar_comentarios(dados_filme['comentarios'])

            analise_filme = classificador.analisar_filme(comentarios_processados)

            salvar_resultado_final(dados_filme, analise_filme)
            exibir_resumo_console(dados_filme, analise_filme)

        except Exception as e:
            print(f'Erro ao processar filme {codigo}: {e}')

    print('-' * 60)
    print('Processo concluído.')


if __name__ == '__main__':
    main()
