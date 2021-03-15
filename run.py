import argparse
import csv
import re

from datetime import date, timedelta
from unicodedata import normalize


def gera_relatorio(args):
    arquivo = _abre_arquivo_txt()
    pedidos_mes = _obtem_pedidos_mes(arquivo)
    dados_organizados = _obtem_dados_organizados(pedidos_mes)
    grava_dados_em_csv(dados_organizados)


def _abre_arquivo_txt():
    with open(args.caminho_arquivo) as f:
        return f.read()


def _obtem_pedidos_mes(arquivo):
    return re.findall(
        rf'^{args.mes}/\d{{1,2}}/{args.ano}, \d+:\d+ - '
        r'[\w +-]+:[* ]+[A-ü]+[*: ]+[\w)( ]+[):;].+',
        arquivo,
        re.M
    )


def _obtem_dados_organizados(pedidos_mes):
    dados_organizados = []

    for pedido in pedidos_mes:
        regex = (
            r'^(?P<data>\d{1,2}/\d{1,2}/\d{2})'
            r', \d+:\d+ - [A-ü0-9+ ]+:[* ]+'
            r'(?P<nome>[A-ü]+)'
            r'[*: ]+(?: *\(?'
            r'(?P<valor>[PpGg][A-z]+)'
            r'\)?| *\('
            r'(?P<quantidade>\d)'
            r'\))+'
        )
        
        dados_pedido = re.search(regex, pedido)
        if dados_pedido is None:
            raise PedidoDespadronizado(f'Remova a conversa ou conserte o pedido: {pedido}')

        dados_pedidos = {
            'Data': dados_pedido.group('data'),
            'Nome': _obtem_nome(dados_pedido),
            'Valor': _obtem_valor(dados_pedido),
            'Quantidade': dados_pedido.group('quantidade')
        }

        print(dados_pedidos)
        dados_organizados.append(tuple(dados_pedidos.values()))
    print('-' * 30)
    print(f'TOTAL DE PEDIDOS: {len(pedidos_mes)}')
    return dados_organizados


def _obtem_nome(dados):
    nome = dados.group('nome').strip().capitalize()
    
    def _remove_acentos(texto):
        return normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

    return _remove_acentos(nome)


def _obtem_valor(dados):
    VALORES = {
        'p': '8',
        'g': '10'
    }
    tamanho = dados.group('valor')
    return VALORES.get(tamanho[0].lower())


def grava_dados_em_csv(dados_organizados):
    with open(f'relatorio_almoco_{args.ano}_{args.mes}.csv', 'w') as arquivo_csv:
        colunas = ['Data', 'Nome', 'Valor', 'Quantidade']

        saida_csv = csv.writer(arquivo_csv, delimiter=',', lineterminator='\n')
        saida_csv.writerow(colunas)
        for linha in dados_organizados:
            saida_csv.writerow(linha)


def _obtem_mes_passado():
    hoje = date.today()
    primeiro_dia_mes = hoje.replace(day=1)
    mes_passado = primeiro_dia_mes - timedelta(days=1)
    return mes_passado.strftime('%-m')


def _obtem_ano_mes_passado():
    hoje = date.today()
    primeiro_dia_mes = hoje.replace(day=1)
    mes_passado = primeiro_dia_mes - timedelta(days=1)
    return mes_passado.strftime('%y')


def _verifica_parametro_ano(string):
    if len(string) != 2:
        raise argparse.ArgumentError('O ano deve conter 2 dígitos. ex.: "21"')
    return string


class PedidoDespadronizado(Exception):
    """Pedido ou mensagem não desejada que esteja fora do padrão requisitado.
    """
    ...


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gera relatório de almoço do Cairo 92')
    parser.add_argument('caminho_arquivo',
                        action='store',
                        type=str,
                        help='Caminho do .txt com a conversa do whatsapp para gerar o relatório.')

    parser.add_argument('-m',
                        '--mes',
                        action='store',
                        default=_obtem_mes_passado(),
                        help='Mês a ser gerado o relatório (padrão: mês passado, ex. formato: "7")')

    parser.add_argument('-a',
                        '--ano',
                        action='store',
                        default=_obtem_ano_mes_passado(),
                        type=_verifica_parametro_ano,
                        help='Ano a ser gerado o relatório (padrão: ano relativo ao mês passado, ex. formato: "20")')

    args = parser.parse_args()

    gera_relatorio(args)
