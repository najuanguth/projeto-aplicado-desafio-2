# Dicionário de dados

TEXT representa texto, INTEGER representa número inteiro e REAL representa número com casas decimais.

## tecnico

| Campo | Tipo | Descrição |
|---|---|---|
| id_tecnico | INTEGER | Chave primária do técnico. |
| nome | TEXT | Nome do técnico executante. |

## equipamento

| Campo | Tipo | Descrição |
|---|---|---|
| id_equipamento | INTEGER | Chave primária do equipamento. |
| codigo | TEXT | Código de identificação do instrumento. |
| descricao | TEXT | Descrição ou denominação do instrumento. |
| fabricante | TEXT | Fabricante do instrumento, quando informado. |

## medicao

| Campo | Tipo | Descrição |
|---|---|---|
| id_medicao | INTEGER | Chave primária da medição. |
| id_tecnico | INTEGER | Chave estrangeira que indica o técnico. |
| id_equipamento | INTEGER | Chave estrangeira que indica o equipamento. |
| referencia_calibracao | TEXT | Identificação usada para agrupar os resultados de uma calibração. |
| data_calibracao | TEXT | Data no formato AAAA-MM-DD. |
| solicitante | TEXT | Setor que solicitou a calibração. |
| parametro | TEXT | Característica avaliada, como diâmetro ou planicidade. |
| unidade | TEXT | Unidade usada nos resultados, como mm. |
| valor_nominal | REAL | Valor de referência do parâmetro. |
| tolerancia_mais | REAL | Tolerância superior, positiva ou zero. |
| tolerancia_menos | REAL | Tolerância inferior, negativa ou zero. |
| medida_1 | REAL | Primeira leitura realizada. |
| medida_2 | REAL | Segunda leitura realizada. |
| valor_obtido | REAL | Média das duas leituras. |
| status | TEXT | Resultado do parâmetro: APROVADO ou REPROVADO. |

## Preenchimento

Os dados de técnico, equipamento e medição foram identificados na aba Registro da planilha de calibração.
Os identificadores e a referência da calibração foram acrescentados para organizar o banco.
O status segue a regra de tolerâncias apresentada na Aula 02.
O programa deverá calcular a média e avaliar o status antes de gravar os resultados.
A avaliação com incerteza da planilha da empresa não está incluída nesta etapa.
Campos obrigatórios usam NOT NULL no SQL. O fabricante pode ficar sem informação, como NULL.
A data, os valores e o texto do status deverão ser conferidos pelo programa antes do cadastro.
