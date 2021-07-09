import argparse
import os

from datetime import date, timedelta

from src.gerador_relatorio import gera_relatorio


def _diretorio_arquivo(caminho: str) -> str:
    caminho_diretorio = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(caminho_diretorio, caminho)


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
                        type=_diretorio_arquivo,
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
    gera_relatorio(args.mes, args.ano, args.caminho_arquivo)
