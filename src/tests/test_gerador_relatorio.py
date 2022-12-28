import unittest

from src import gerador_relatorio


def obtem_fixture(nome_arquivo):
    with open(f'src/tests/fixture/{nome_arquivo}') as f:
        return f.read()


class Lauch92TestCase(unittest.TestCase):
    def test_obtem_pedidos_mes_nome_correto(self):
        conversa_whatsapp = obtem_fixture('conversa_whatsapp_test.txt')
        pedidos_mes = gerador_relatorio.obtem_pedidos_mes(conversa_whatsapp, 6, 21)
        self.assertIn('Pidgey', pedidos_mes[-1])
        self.assertIn('6/30/21', pedidos_mes[-1])
        self.assertEqual(122, len(pedidos_mes))

    def test_sanitiza_nome(self):
        nome = 'PIKACHu. '
        self.assertEqual('Pikachu', gerador_relatorio._sanitiza_nome(nome))

    def test_converte_valor(self):
        self.assertEqual('12', gerador_relatorio._converte_valor('Grande'))
        self.assertEqual('9', gerador_relatorio._converte_valor('Pequeno'))

    def test_sanitiza_dados_com_erro_de_padrão(self):
        pedidos_mes = [('6/30/21', 'Ca.terpie:', 'Grande', '2')]
        dados_sanitizados = gerador_relatorio.sanitiza_dados(pedidos_mes)
        valor_marmita = '12'

        self.assertIn('Caterpie', dados_sanitizados[0])
        self.assertIn(valor_marmita, dados_sanitizados[0])

    def test_ajusta_formatacao_data(self):
        conversa_data_curta = obtem_fixture('conversa_whatsapp_test.txt')
        conversa_data_longa = obtem_fixture('formato_data_longa.txt')

        self.assertEqual(
            '(6/\\d{1,2}/21)',
            gerador_relatorio._ajusta_formatacao_data(conversa_data_curta, 6, 21)
        )
        self.assertEqual(
            '(\\d{2}/06/2021)',
            gerador_relatorio._ajusta_formatacao_data(conversa_data_longa, 6, 21)
        )
