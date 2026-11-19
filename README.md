# Neighborhood Action Dashboard

Global Solution 2 — Graduação ON em Ciência da Computação — FIAP 2026.2

## Equipe

**Integrantes e RMs:**

- Eduardo Henrique Campos da Silva - RM576932
- Julia de Oliveira Silva - RM576345
- Pedro Henrique Monteiro Scabio - RM576607
- Maria Eduarda Fernandes Guimaraes - RM576947
- Maria Fernanda Barbosa Firmo - RM575160

## Sobre o projeto

O Neighborhood Action Dashboard é um programa de terminal que simula um painel comunitário de ocorrências. Ele permite cadastrar pedidos de melhoria em bairros, consultar o andamento, mudar o status e ver indicadores simples.

O desafio da Global Solution é aplicar o que foi estudado nas fases 1, 2 e 3: lógica de programação, estruturas de dados e algoritmos, sem banco de dados, APIs ou serviços externos.

## Objetivo

Organizar as demandas de um bairro de forma clara, garantindo:

- Cadastro de ocorrências com verificação dos campos obrigatórios;
- Consulta por código e filtro por categoria e status;
- Atualização de status com histórico das mudanças;
- Indicadores simples e fáceis de entender;
- Cuidado com acessibilidade, inclusão e privacidade.

## Tecnologias utilizadas

- Python 3, usando só a biblioteca padrão (nada para instalar);
- Interface de texto no terminal;
- Dados inicializados no próprio código, sem banco de dados.

## Estrutura do projeto

```
📁 GLOBAL-SOLUTION-2
│
├── 📁 src
│   ├── sistema.py       funções principais e início do programa
│   ├── menu.py          menu, busca e filtros
│   ├── dados.py         dados fictícios
│   └── indicadores.py   indicadores e matrizes
│
├── 📁 docs
│   └── uso_ia.md        registro do uso de IA
│
├── testes.py            testes automáticos
└── README.md
```

## Como executar

Com o Python 3 instalado, abra o terminal dentro da pasta do projeto (a que tem o `README.md` e a pasta `src`) e execute:

```
python src/sistema.py
```

O menu aparece no terminal e as opções são escolhidas digitando o número. Para rodar os testes:

```
python testes.py
```

## Bairro simulado, problema e público

Os dados são inventados e não têm informação pessoal. Criamos quatro bairros imaginários (Jardim Aurora, Vila Esperança, Parque Verde e Centro Novo) com 12 ocorrências de iluminação, acessibilidade, limpeza e conservação de espaços coletivos.

O problema é que os pedidos de melhoria do bairro ficam espalhados, ninguém sabe o que é mais urgente e os moradores não conseguem acompanhar o andamento. O programa organiza esses pedidos em um painel no terminal. Ele ajuda os moradores que registram e acompanham os pedidos e quem organiza a comunidade.

Cada ocorrência tem código, categoria, local, bairro, dia de abertura e status. Todos esses campos são obrigatórios. Os dados iniciais estão no próprio código em Python.

Os status significam:

- **Aberta:** o pedido foi registrado e ainda não foi examinado;
- **Em Análise:** o pedido já foi visto e está sendo avaliado;
- **Concluída:** o problema foi resolvido (de forma simulada).

## Estruturas de dados utilizadas

- **Lista:** guarda todas as ocorrências e permite percorrer elas.
- **Fila:** guarda os pedidos que ainda não foram examinados, porque eles devem ser atendidos na ordem em que chegaram.
- **Pilha:** guarda o histórico de mudanças de status, porque a mudança mais recente é a que mais interessa consultar.
- **Dicionário:** acha uma ocorrência rápido pelo código, sem precisar percorrer a lista.
- **Hierarquia (bairro, categoria e códigos):** mostra que tipos de problema cada bairro tem.
- **Matriz (lista de listas):** conta quantas ocorrências existem em cada categoria e em cada status.

## Regras lógicas principais

No **cadastro**, o programa só aceita a ocorrência se todos os campos estiverem corretos e se o código ainda não existir. Se algo estiver errado, mostra a mensagem "Registro inválido ou incompleto".

Na **atualização**, o programa recusa código que não existe (mensagem "Ocorrência não encontrada"), status desconhecido (mensagem "Status informado é inválido") e dia inválido (zero, negativo ou anterior ao dia de abertura, com mensagem explicando o motivo). Cada mudança aceita vai para o histórico.

Na **consulta**, dá para buscar pelo código e filtrar por categoria e/ou status. Se o código não existir, aparece "Ocorrência não encontrada". Se o filtro não achar nada, aparece "Nenhuma ocorrência encontrada com esses filtros".

Expressão booleana usada na validação do cadastro:

`codigo_valido and categoria_valida and status_valido and local_valido and bairro_valido and data_valida`

O `and` exige que todas as condições sejam verdadeiras. Se uma falhar, o cadastro é recusado e aparece a mensagem de registro inválido. Foi isso que aconteceu com o registro OC013, que não tem categoria.

O programa também usa `not` (o dia não pode ser verdadeiro ou falso) e `or` (no filtro por categoria ou status, basta combinar com um dos dois).

## Indicadores, fórmulas e interpretação

- **Porcentagem por categoria e por status:** quantidade dividida pelo total, vezes 100.
- **Pendentes:** total menos as concluídas.
- **Tempo médio de resolução:** soma dos dias até a conclusão dividida pelo número de ocorrências concluídas.
- **Porcentagem de rotas resolvidas:** número de rotas com todas as ocorrências concluídas dividido pelo total de rotas, vezes 100.

Resultado com os dados iniciais: 12 ocorrências, 3 em cada categoria (25% cada); 2 abertas, 2 em análise e 8 concluídas (66,7%); 4 pendentes; tempo médio de 5,88 dias simulados (47 dividido por 8); 2 de 4 rotas resolvidas (50%).

**Interpretação:** a maior parte dos pedidos simulados foi resolvida. As pendências estão em Iluminação (2, em análise) e em Conservação de Espaços Coletivos (2, ainda abertas), então essas categorias precisam de mais atenção. Como os dados são inventados, os números não mostram a situação real de nenhum bairro.

## Exemplo de uso

**Cadastro (opção 4 do menu):**

- Código: OC014
- Categoria: 1 (Iluminação)
- Local de referência: Poste 10, Rua Nova
- Bairro: Centro Novo
- Dia de abertura: 5
- Resultado: Ocorrência OC014 registrada com sucesso.

**Consulta (opção 2):**

- Código da ocorrência: OC005
- Categoria: Iluminação
- Local: Poste 04, Av. Central (bairro Vila Esperança)
- Status: Em Análise

**Alteração de status (opção 5) e histórico (opção 6):**

- Status de OC014 atualizado: Aberta -> Em Análise.
- Dia 6: OC014 Aberta -> Em Análise

**Saída (opção 0):**

- Saindo do sistema.

## Acessibilidade, inclusão e privacidade

- Os dados são inventados e os locais são genéricos (poste, praça, parada). O programa não pede nome, telefone nem endereço de morador.
- A interface usa só texto, sem depender de cores ou de mouse, o que ajuda no uso com leitores de tela. As mensagens de erro explicam o que precisa ser corrigido.
- A categoria Acessibilidade registra problemas como falta de rampa, piso tátil e espaço para cadeira de rodas. A linguagem do programa é simples.

## Conclusões, limitações e aprendizados

O programa cadastra, valida, consulta, filtra, muda o status com histórico e calcula indicadores, usando só Python básico.

Como limitações, os dados são inventados e somem quando o programa fecha, não existe ligação com a prefeitura, os dias são simulados e a entrada é só por digitação no terminal.

Aprendemos que cada estrutura de dados serve para um fim (fila para ordem de chegada, pilha para histórico, dicionário para busca por código) e que testar os casos de erro evitou registros errados.

## Uso de IA

O uso de IA está registrado em [docs/uso_ia.md](docs/uso_ia.md).
