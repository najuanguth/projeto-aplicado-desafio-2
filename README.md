# Projeto Aplicado I - Entrega 02

Élcio Hemckmeier e Najuan Loss Guth

Banco de dados para organizar informações de calibração da Schulz.

## Arquivos

- 01_estrutura.md: explicação das tabelas e dos relacionamentos.
- 02_dicionario.md: descrição dos 21 campos do banco.
- 03_banco.sql: comandos de criação das três tabelas.
- 04_relatorio.pdf: apresentação do trabalho.

## Execução

Abra um banco SQLite novo e execute os comandos do arquivo 03_banco.sql.
As tabelas serão criadas sem dados.
Em cada nova conexão, execute PRAGMA foreign_keys = ON para ativar as chaves estrangeiras.
O programa que usar o banco deverá calcular o valor obtido e o status antes de salvar a medição.
