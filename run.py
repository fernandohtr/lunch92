import argparse
import csv
import re

from datetime import date, timedelta
from typing import List
from unicodedata import normalize

VALORES_MARMITA = {
    'p': '8',
    'g': '10'
}


def gera_relatorio() -> None:
    arquivo = abre_arquivo_txt()
    pedidos_mes = obtem_pedidos_mes(arquivo, args.mes, args.ano)
    dados_organizados = obtem_dados_organizados(pedidos_mes)
    imprime_relatorio(dados_organizados)
    grava_dados_em_csv(dados_organizados)


def abre_arquivo_txt() -> str:
    with open(args.caminho_arquivo) as f:
        return f.read()


def obtem_pedidos_mes(arquivo: str, mes: int, ano: int) -> List[tuple]:
    regex = (
        rf'^({mes}/\d{{1,2}}/{ano})'  # data
        r', \d+:\d+.+?: *'
        r'\*(.+?)\*.*?'  # nome
        r'\((.+?)\).*?'  # tamanho
        r'\((\d+?)\)'  # quantidade
    )
    return re.findall(
        regex,
        arquivo,
        re.M
    )


def obtem_dados_organizados(pedidos_mes: List[tuple]) -> List[dict]:
    dados_organizados = []

    for pedido in pedidos_mes:
        dados_pedidos = {
            'Data': pedido[0],
            'Nome': _obtem_nome(pedido[1]),
            'Valor': _obtem_valor(pedido[2]),
            'Quantidade': pedido[3]
        }

        dados_organizados.append(tuple(dados_pedidos.values()))
    return dados_organizados


def _obtem_nome(nome):
    nome = nome.strip().capitalize()
    
    def _remove_acentos(texto):
        return normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

    return _remove_acentos(nome)


def _obtem_valor(tamanho: str) -> str:
    return VALORES_MARMITA.get(tamanho.strip()[0].lower())


def imprime_relatorio(dados_organizados: List[tuple]) -> None:
    for pedido in dados_organizados:
        print(pedido)
    print('-' * 30)
    print(f'TOTAL DE PEDIDOS: {len(dados_organizados)}')



def grava_dados_em_csv(dados_organizados: List[dict]) -> None:
    with open(f'relatorio_almoco_{args.ano}_{args.mes}.csv', 'w') as arquivo_csv:
        colunas = ['Data', 'Nome', 'Valor', 'Quantidade']

        saida_csv = csv.writer(arquivo_csv, delimiter=',', lineterminator='\n')
        saida_csv.writerow(colunas)
        for linha in dados_organizados:
            saida_csv.writerow(linha)


def _obtem_mes_passado() -> int:
    hoje = date.today()
    primeiro_dia_mes = hoje.replace(day=1)
    mes_passado = primeiro_dia_mes - timedelta(days=1)
    return int(mes_passado.strftime('%-m'))


def _obtem_ano_mes_passado() -> int:
    hoje = date.today()
    primeiro_dia_mes = hoje.replace(day=1)
    mes_passado = primeiro_dia_mes - timedelta(days=1)
    return int(mes_passado.strftime('%y'))


def _verifica_parametro_ano(entrada: str) -> int:
    if len(entrada) != 2:
        raise argparse.ArgumentError('O ano deve conter 2 dígitos. ex.: "21"')
    return int(entrada)


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
                        type=int,
                        help='Mês a ser gerado o relatório (padrão: mês passado, ex. formato: "7")')

    parser.add_argument('-a',
                        '--ano',
                        action='store',
                        default=_obtem_ano_mes_passado(),
                        type=_verifica_parametro_ano,
                        help='Ano a ser gerado o relatório (padrão: ano relativo ao mês passado, ex. formato: "20")')

    args = parser.parse_args()
    gera_relatorio()
