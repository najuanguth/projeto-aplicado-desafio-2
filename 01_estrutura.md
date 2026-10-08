# Organização dos dados

O banco foi dividido em três tabelas: tecnico, equipamento e medicao.
Essa organização separa os cadastros dos resultados das calibrações.

## Técnico e solicitante
A tabela tecnico guarda o identificador e o nome do técnico.
O técnico é o metrologista que realiza a calibração.
Um técnico pode realizar várias medições.
O solicitante é o setor que pede a calibração.
O nome desse setor fica na tabela medicao, pois está ligado à calibração realizada.

## Equipamento
A tabela equipamento guarda o instrumento que será calibrado.
Ela contém identificador, código, descrição e fabricante.
O código é salvo como texto, pois identifica o instrumento.
Cada equipamento é cadastrado uma única vez.
O mesmo equipamento pode passar por várias calibrações.

## Medição
A tabela medicao guarda os resultados de cada parâmetro avaliado.
Ela registra a data, o solicitante, o nominal, as tolerâncias e as duas medidas.
Também guarda o valor obtido e o status do resultado.
O valor obtido corresponde à média das duas medidas.
O status indica se o parâmetro foi aprovado ou reprovado.
Esses valores serão preenchidos pelo programa que utilizar o banco.
A data é guardada como texto em ano-mês-dia, por exemplo, 2026-10-07.
Esse formato facilita colocar as datas em ordem; no certificado ela pode aparecer como 07/10/2026.
A referência da calibração permite agrupar os parâmetros de uma mesma execução.

## Relacionamentos
Cada técnico e equipamento possui um identificador, chamado chave primária.
A medição guarda esses identificadores como chaves estrangeiras.
Assim, cada medição fica ligada ao técnico responsável e ao equipamento calibrado.
Um técnico pode ter várias medições, e um equipamento também.
Separar essas informações evita repetir o nome do técnico e os dados do equipamento em cada resultado.
Isso reduz a duplicação de cadastros e facilita a atualização das informações.
A data e o solicitante se repetem nas linhas de uma mesma calibração, pois usamos somente três tabelas.
