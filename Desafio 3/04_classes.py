import math
import sqlite3
from datetime import date
from pathlib import Path


def texto_obrigatorio(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f'Preencha o campo {campo}.')
    return valor.strip()


class Tecnico:
    def __init__(self, nome, matricula, setor, id_tecnico=None):
        self.id_tecnico = id_tecnico
        self.nome = nome
        self.matricula = matricula
        self.setor = setor
        self.validar()

    def validar(self):
        self.nome = texto_obrigatorio(self.nome, 'nome')
        self.matricula = texto_obrigatorio(self.matricula, 'matrícula')
        self.setor = texto_obrigatorio(self.setor, 'setor')


class Equipamento:
    def __init__(self, codigo, descricao, fabricante=None, id_equipamento=None):
        self.id_equipamento = id_equipamento
        self.codigo = codigo
        self.descricao = descricao
        self.fabricante = fabricante
        self.validar()

    def validar(self):
        self.codigo = texto_obrigatorio(self.codigo, 'código')
        self.descricao = texto_obrigatorio(self.descricao, 'descrição')


class Medicao:
    def __init__(self, id_tecnico, id_equipamento, referencia_calibracao,
                 data_calibracao, solicitante, parametro, unidade,
                 valor_nominal, tolerancia_mais, tolerancia_menos,
                 medida_1, medida_2, id_medicao=None):
        self.id_medicao = id_medicao
        self.id_tecnico = id_tecnico
        self.id_equipamento = id_equipamento
        self.referencia_calibracao = referencia_calibracao
        self.data_calibracao = data_calibracao
        self.solicitante = solicitante
        self.parametro = parametro
        self.unidade = unidade
        self.valor_nominal = valor_nominal
        self.tolerancia_mais = tolerancia_mais
        self.tolerancia_menos = tolerancia_menos
        self.medida_1 = medida_1
        self.medida_2 = medida_2
        self.validar()

    def validar(self):
        self.referencia_calibracao = texto_obrigatorio(self.referencia_calibracao, 'referência')
        self.data_calibracao = date.fromisoformat(self.data_calibracao).isoformat()
        self.solicitante = texto_obrigatorio(self.solicitante, 'solicitante')
        self.parametro = texto_obrigatorio(self.parametro, 'parâmetro')
        self.unidade = texto_obrigatorio(self.unidade, 'unidade')
        try:
            self.valor_nominal = float(self.valor_nominal)
            self.tolerancia_mais = float(self.tolerancia_mais)
            self.tolerancia_menos = float(self.tolerancia_menos)
            self.medida_1 = float(self.medida_1)
            self.medida_2 = float(self.medida_2)
        except (TypeError, ValueError) as erro:
            raise ValueError('Informe números para as medidas e tolerâncias.') from erro
        valores = [self.valor_nominal, self.tolerancia_mais, self.tolerancia_menos,
                   self.medida_1, self.medida_2]
        if not all(math.isfinite(valor) for valor in valores):
            raise ValueError('As medidas e tolerâncias precisam ser números finitos.')
        if self.tolerancia_mais < 0 or self.tolerancia_menos > 0:
            raise ValueError('A tolerância superior deve ser positiva ou zero, e a inferior negativa ou zero.')

    @property
    def valor_obtido(self):
        return self.medida_1 / 2 + self.medida_2 / 2

    def avaliar_status(self):
        self.validar()
        minimo = self.valor_nominal - abs(self.tolerancia_menos)
        maximo = self.valor_nominal + self.tolerancia_mais
        # Margem usada na Aula 02 para pequenas diferenças de ponto flutuante.
        if minimo - 0.0000001 <= self.valor_obtido <= maximo + 0.0000001:
            return 'APROVADO'
        return 'REPROVADO'

    def dados_para_salvar(self):
        return (self.id_tecnico, self.id_equipamento, self.referencia_calibracao,
                self.data_calibracao, self.solicitante, self.parametro, self.unidade,
                self.valor_nominal, self.tolerancia_mais, self.tolerancia_menos,
                self.medida_1, self.medida_2, self.valor_obtido, self.avaliar_status())


class BancoDados:
    def __init__(self, caminho):
        self._conexao = sqlite3.connect(caminho)
        self._conexao.row_factory = sqlite3.Row
        self._conexao.execute('PRAGMA foreign_keys = ON')
        try:
            sql = Path(__file__).with_name('03_banco.sql').read_text(encoding='utf-8')
            self._conexao.executescript(sql)
        except (sqlite3.Error, OSError):
            self._conexao.close()
            raise

    def _executar(self, sql, dados):
        try:
            with self._conexao:
                return self._conexao.execute(sql, dados)
        except sqlite3.IntegrityError as erro:
            raise ValueError('Operação recusada: verifique dados obrigatórios, cadastro duplicado ou vínculo entre registros.') from erro

    def inserir_tecnico(self, tecnico):
        tecnico.validar()
        cursor = self._executar('INSERT INTO tecnico (nome, matricula, setor) VALUES (?, ?, ?)',
                               (tecnico.nome, tecnico.matricula, tecnico.setor))
        tecnico.id_tecnico = cursor.lastrowid
        return tecnico.id_tecnico

    def listar_tecnicos(self):
        return self._conexao.execute('SELECT * FROM tecnico ORDER BY id_tecnico').fetchall()

    def atualizar_tecnico(self, tecnico):
        tecnico.validar()
        cursor = self._executar('UPDATE tecnico SET nome=?, matricula=?, setor=? WHERE id_tecnico=?',
                               (tecnico.nome, tecnico.matricula, tecnico.setor, tecnico.id_tecnico))
        if cursor.rowcount == 0:
            raise ValueError('Técnico não encontrado.')

    def excluir_tecnico(self, id_tecnico):
        cursor = self._executar('DELETE FROM tecnico WHERE id_tecnico=?', (id_tecnico,))
        if cursor.rowcount == 0:
            raise ValueError('Técnico não encontrado.')

    def inserir_equipamento(self, equipamento):
        equipamento.validar()
        cursor = self._executar('INSERT INTO equipamento (codigo, descricao, fabricante) VALUES (?, ?, ?)',
                               (equipamento.codigo, equipamento.descricao, equipamento.fabricante))
        equipamento.id_equipamento = cursor.lastrowid
        return equipamento.id_equipamento

    def listar_equipamentos(self):
        return self._conexao.execute('SELECT * FROM equipamento ORDER BY id_equipamento').fetchall()

    def atualizar_equipamento(self, equipamento):
        equipamento.validar()
        cursor = self._executar('UPDATE equipamento SET codigo=?, descricao=?, fabricante=? WHERE id_equipamento=?',
                               (equipamento.codigo, equipamento.descricao, equipamento.fabricante, equipamento.id_equipamento))
        if cursor.rowcount == 0:
            raise ValueError('Equipamento não encontrado.')

    def excluir_equipamento(self, id_equipamento):
        cursor = self._executar('DELETE FROM equipamento WHERE id_equipamento=?', (id_equipamento,))
        if cursor.rowcount == 0:
            raise ValueError('Equipamento não encontrado.')

    def inserir_medicao(self, medicao):
        cursor = self._executar('''INSERT INTO medicao
            (id_tecnico, id_equipamento, referencia_calibracao, data_calibracao,
             solicitante, parametro, unidade, valor_nominal, tolerancia_mais,
             tolerancia_menos, medida_1, medida_2, valor_obtido, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', medicao.dados_para_salvar())
        medicao.id_medicao = cursor.lastrowid
        return medicao.id_medicao

    def listar_medicoes(self):
        return self._conexao.execute('SELECT * FROM medicao ORDER BY id_medicao').fetchall()

    def atualizar_medicao(self, medicao):
        cursor = self._executar('''UPDATE medicao SET
            id_tecnico=?, id_equipamento=?, referencia_calibracao=?, data_calibracao=?,
            solicitante=?, parametro=?, unidade=?, valor_nominal=?, tolerancia_mais=?,
            tolerancia_menos=?, medida_1=?, medida_2=?, valor_obtido=?, status=?
            WHERE id_medicao=?''', medicao.dados_para_salvar() + (medicao.id_medicao,))
        if cursor.rowcount == 0:
            raise ValueError('Medição não encontrada.')

    def excluir_medicao(self, id_medicao):
        cursor = self._executar('DELETE FROM medicao WHERE id_medicao=?', (id_medicao,))
        if cursor.rowcount == 0:
            raise ValueError('Medição não encontrada.')

    def consultar_relatorio(self):
        return self._conexao.execute('''SELECT m.*, t.nome AS tecnico,
            t.matricula, t.setor, e.codigo, e.descricao, e.fabricante
            FROM medicao AS m
            JOIN tecnico AS t ON t.id_tecnico = m.id_tecnico
            JOIN equipamento AS e ON e.id_equipamento = m.id_equipamento
            ORDER BY m.referencia_calibracao, m.id_medicao''').fetchall()

    def fechar(self):
        self._conexao.close()
