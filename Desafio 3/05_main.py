from datetime import datetime
from pathlib import Path
import runpy
import sqlite3

# O nome solicitado começa com número, por isso carregamos o arquivo com runpy.
classes = runpy.run_path(str(Path(__file__).with_name('04_classes.py')))
Tecnico = classes['Tecnico']
Equipamento = classes['Equipamento']
Medicao = classes['Medicao']
BancoDados = classes['BancoDados']


def main():
    pasta = Path(__file__).parent / 'dados'
    pasta.mkdir(exist_ok=True)
    caminho = pasta / f'demonstracao_{datetime.now():%Y%m%d_%H%M%S_%f}.db'
    banco = None
    try:
        banco = BancoDados(caminho)
        tecnico = Tecnico('Elcio teste', 'TESTE-01', 'Metrologia')
        equipamento = Equipamento('TESTE-001', 'Dispositivo de controle', 'Fabricante de teste')
        banco.inserir_tecnico(tecnico)
        banco.inserir_equipamento(equipamento)

        aprovada = Medicao(tecnico.id_tecnico, equipamento.id_equipamento,
                           'CAL-TESTE-01', '2026-10-26', 'Usinagem', 'Diâmetro',
                           'mm', 10.0, 0.1, -0.1, 10.02, 10.04)
        reprovada = Medicao(tecnico.id_tecnico, equipamento.id_equipamento,
                            'CAL-TESTE-01', '2026-10-26', 'Usinagem', 'Comprimento',
                            'mm', 20.0, 0.1, -0.1, 20.20, 20.24)
        banco.inserir_medicao(aprovada)
        banco.inserir_medicao(reprovada)

        equipamento.descricao = 'Dispositivo de controle dimensional'
        banco.atualizar_equipamento(equipamento)
        tecnico.setor = 'Laboratório de metrologia'
        banco.atualizar_tecnico(tecnico)
        aprovada.solicitante = 'Usinagem I'
        reprovada.solicitante = 'Usinagem I'
        banco.atualizar_medicao(aprovada)
        banco.atualizar_medicao(reprovada)

        temporario = Tecnico('Cadastro temporário', 'TEMP-01', 'Teste')
        banco.inserir_tecnico(temporario)
        banco.excluir_tecnico(temporario.id_tecnico)

        print('DEMONSTRAÇÃO COM DADOS FICTÍCIOS')
        print(f'Técnicos cadastrados: {len(banco.listar_tecnicos())}')
        print(f'Equipamentos cadastrados: {len(banco.listar_equipamentos())}')
        print(f'Medições cadastradas: {len(banco.listar_medicoes())}')
        print('\nRELATÓRIO DE CALIBRAÇÃO')
        for linha in banco.consultar_relatorio():
            print(f"\nReferência: {linha['referencia_calibracao']} | Data: {linha['data_calibracao']}")
            print(f"Técnico: {linha['tecnico']} | Matrícula: {linha['matricula']}")
            print(f"Equipamento: {linha['codigo']} - {linha['descricao']}")
            print(f"Solicitante: {linha['solicitante']}")
            print(f"Parâmetro: {linha['parametro']} | Unidade: {linha['unidade']}")
            print(f"Nominal: {linha['valor_nominal']:.3f} | Tolerâncias: {linha['tolerancia_menos']:+.3f} / {linha['tolerancia_mais']:+.3f}")
            print(f"Medidas: {linha['medida_1']:.3f} e {linha['medida_2']:.3f}")
            print(f"Valor obtido: {linha['valor_obtido']:.3f} | Status: {linha['status']}")

        print('\nTESTE DE CADASTRO DUPLICADO')
        try:
            banco.inserir_equipamento(equipamento)
        except ValueError as erro:
            print(erro)
        print(f'\nBanco salvo em: {caminho}')
    except (ValueError, sqlite3.Error, OSError) as erro:
        print(f'Não foi possível concluir: {erro}')
        raise SystemExit(1)
    finally:
        if banco is not None:
            banco.fechar()


if __name__ == '__main__':
    main()
