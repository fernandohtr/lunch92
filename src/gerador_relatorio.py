import csv
import re

from typing import List
from unicodedata import normalize

VALORES_MARMITA = {
    'p': '9',
    'g': '12'
}


def gera_relatorio(mes: int, ano: int, caminho_arquivo: str) -> None:
    arquivo = abre_arquivo_txt(caminho_arquivo)
    pedidos_mes = obtem_pedidos_mes(arquivo, mes, ano)
    dados_sanitizados = sanitiza_dados(pedidos_mes)
    imprime_relatorio(dados_sanitizados)
    grava_dados_em_csv(mes, ano, dados_sanitizados)


def abre_arquivo_txt(caminho_arquivo: str) -> str:
    with open(caminho_arquivo) as f:
        return f.read()


def obtem_pedidos_mes(arquivo: str, mes: int, ano: int) -> List[tuple]:
    regex_data = _ajusta_formatacao_data(arquivo[:50], mes, ano)

    regex = (
        rf'^{regex_data}'  # data
        r',? \d+:\d+.+?: *'
        r'\*(.+?)\*.*?'  # nome
        r'\((.+?)\).*?'  # tamanho
        r'\((\d+?)\)'  # quantidade
    )
    return re.findall(
        regex,
        arquivo,
        re.M
    )


def _ajusta_formatacao_data(texto: str, mes: int, ano: int) -> str:
    """Ao gerar o relatório de conversas do whatsapp, a data pode vir com a formatação:
       - longa: DD/MM/YYYY; ou
       - curta: MM/DD/YY
    """
    data_formatacao_longa = re.search(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}', texto, re.M)
    if data_formatacao_longa:
        return rf'(\d{{2}}/{mes:02d}/20{ano})'
    return  rf'({mes}/\d{{1,2}}/{ano})'


def sanitiza_dados(pedidos_mes: List[tuple]) -> List[tuple]:
    dados_sanitizados = []

    for pedido in pedidos_mes:
        dados_pedidos = (
            pedido[0],
            _sanitiza_nome(pedido[1]),
            _converte_valor(pedido[2]),
            pedido[3],
        )

        dados_sanitizados.append(dados_pedidos)
    return dados_sanitizados


def _sanitiza_nome(nome: str) -> str:
    nome = nome.strip().capitalize()
    nome = re.sub(r'(?:\.|:|,)', '', nome)
    
    def _remove_acentos(texto: str) -> str:
        return normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

    return _remove_acentos(nome)


def _converte_valor(tamanho: str) -> str:
    return VALORES_MARMITA.get(tamanho.strip()[0].lower())


def imprime_relatorio(dados_sanitizados: List[tuple]) -> None:
    for pedido in dados_sanitizados:
        print(pedido)
    print('-' * 30)
    print(f'TOTAL DE PEDIDOS: {len(dados_sanitizados)}')



def grava_dados_em_csv(mes: int, ano: int, dados_sanitizados: List[dict]) -> None:
    with open(f'relatorio_almoco_{ano}_{mes}.csv', 'w') as arquivo_csv:
        colunas = ['Data', 'Nome', 'Valor', 'Quantidade']

        saida_csv = csv.writer(arquivo_csv, delimiter=',', lineterminator='\n')
        saida_csv.writerow(colunas)
        for linha in dados_sanitizados:
            saida_csv.writerow(linha)
