# MVP de calibração

Alunos: Élcio Hemckmeier e Najuan Loss Guth
Florianópolis, 26 de outubro de 2026

## Classes

A classe Tecnico guarda nome, matrícula e setor do metrologista.
A classe Equipamento guarda código, descrição e fabricante do instrumento.
A classe Medicao guarda os valores de um parâmetro e calcula o resultado.
A classe BancoDados faz a conexão com SQLite e executa os comandos SQL.

```text
Tecnico
  id_tecnico, nome, matricula, setor
  validar(): confere os campos obrigatórios

Equipamento
  id_equipamento, codigo, descricao, fabricante
  validar(): confere os campos obrigatórios

Medicao
  id_medicao, id_tecnico, id_equipamento
  referencia_calibracao, data_calibracao, solicitante
  parametro, unidade, valor_nominal
  tolerancia_mais, tolerancia_menos, medida_1, medida_2
  validar(): confere os dados da medição
  valor_obtido: média das medidas
  avaliar_status(): compara a média com os limites
  dados_para_salvar(): reúne os dados para o banco

BancoDados
  _conexao
  inserir, listar, atualizar e excluir para cada entidade
  consultar_relatorio(): consulta com JOIN
  fechar(): encerra a conexão

Tecnico (1) ----- (N) Medicao
Equipamento (1) - (N) Medicao
BancoDados salva e consulta os dados dessas classes.
```

## Orientação a objetos

Criamos os objetos a partir das classes para reunir os dados de cada cadastro.
A validação da medição fica na classe Medicao, enquanto o SQL fica em BancoDados.
Assim, o cálculo e o acesso ao banco têm responsabilidades separadas.
A conexão usa o atributo _conexao, indicando que seu uso é interno à classe.
O valor_obtido usa uma propriedade sem método de escrita: a média é obtida das duas leituras.
Não usamos herança, pois as classes representam informações diferentes e não precisam compartilhar uma classe-base.

## Avaliação da medição

O valor obtido é a média das duas medidas.
O limite inferior é o nominal menos o módulo da tolerância negativa.
O limite superior é o nominal mais a tolerância positiva.
Se a média estiver entre os limites, inclusive nas extremidades, o parâmetro fica APROVADO.
Caso contrário, fica REPROVADO.
Usamos a margem numérica de 0,0000001 apresentada na Aula 02.
A comparação não inclui o cálculo de incerteza da planilha da empresa.
Todas as medidas e tolerâncias de um parâmetro devem estar na mesma unidade.

## Banco de dados

Mantivemos as tabelas tecnico, equipamento e medicao do banco anterior.
Acrescentamos matrícula e setor ao cadastro de técnico; a matrícula é única.
O atributo codigo representa o código/tag do equipamento.
A referência da calibração agrupa os parâmetros de uma execução.
O script 03_banco.sql cria a estrutura atual em um banco novo.
Não fizemos conversão automática de bancos antigos: a demonstração usa um banco separado.

Os métodos de BancoDados permitem cadastrar, consultar, alterar e excluir os registros.
O relatório usa JOIN para reunir o nome do técnico, os dados do equipamento e a medição.
As chaves estrangeiras impedem vínculos inexistentes e exclusão de cadastros que tenham medições.
O programa calcula novamente a média e o status ao inserir ou atualizar uma medição.

## Tratamento de erros

O método validar() confere campos vazios, data inválida, números não finitos e sinais das tolerâncias.
Ele é chamado ao criar o objeto e antes de salvar os dados, inclusive nas atualizações.
As consultas usam parâmetros com ?, separando os valores dos comandos SQL.
Se houver erro de integridade, como matrícula ou código repetido, o banco desfaz a operação e o programa apresenta uma mensagem.
Uma alteração ou exclusão de identificador inexistente também gera mensagem de erro.
Outros erros do SQLite são tratados na execução principal.
A conexão é fechada no bloco finally, inclusive quando a demonstração falha.

## Execução e verificação

No terminal, dentro desta pasta, execute:

```sh
python 05_main.py
```

Usamos apenas bibliotecas que já vêm com Python 3.
O arquivo 05_main.py carrega 04_classes.py com runpy, pois o nome solicitado começa com número e não pode ser usado em um import comum.

A demonstração cadastra um técnico, um equipamento e duas medições fictícias.
Depois altera os cadastros e o solicitante das medições, e remove um técnico temporário.
A consulta com JOIN mostra no terminal um parâmetro aprovado, com média 10,030, e outro reprovado, com média 20,220.
Ao tentar repetir o código do equipamento, o programa exibe uma mensagem e mantém os registros anteriores.

Cada execução salva um arquivo diferente na pasta dados, com data e hora no nome.
O caminho aparece ao final, permitindo abrir o banco no SQLite e consultar as tabelas.
O programa demonstra cadastro, cálculo e consulta pelo terminal. Não realiza importação de Excel nem emissão do certificado em PDF.
