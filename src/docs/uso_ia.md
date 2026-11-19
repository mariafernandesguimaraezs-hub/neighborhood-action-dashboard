# RELATÓRIO DE USO DE INTELIGÊNCIA ARTIFICIAL

**Global Solution FIAP**

**PROJETO:** Iluminação Pública e Segurança em Rotas Noturnas

Este relatório registra com transparência o papel das ferramentas de Inteligência Artificial Generativa durante o ciclo de desenvolvimento da aplicação, demonstrando a autonomia analítica da equipe, a autoria intelectual do código em Python e os testes rigorosos de validação manual realizados conforme as diretrizes acadêmicas da FIAP.

## 1. Como a Inteligência Artificial Apoiou o Desenvolvimento

A IA foi utilizada estritamente como suporte técnico-pedagógico para esclarecimento de sintaxe, apoio na concepção das matrizes 2D, formulação da massa de dados simulada e revisão textual da documentação técnica:

- **Modelagem Lógica das Matrizes 2D:** Suporte na estruturação de matrizes bidimensionais em Python puro (listas de listas) sem uso de bibliotecas externas (como NumPy ou Pandas). Isso resultou na implementação das funções `construir_matriz_resumo()` (dimensão 4×3, cruzando categorias e situações em `src/sistema.py`) e `matriz_tipo_status()` (dimensão 3×3, correlacionando tecnologias de lâmpadas com o status da manutenção em `src/indicadores.py`).
- **Tratamento de Tipos e Condicionais Booleanas:** Discussão sobre casos de borda na tipagem do Python, especificamente na função `dia_valido(valor)`. A ferramenta auxiliou na formulação da regra lógica booleana `isinstance(valor, int) and not isinstance(valor, bool) and valor > 0`, impedindo que valores booleanos (`True`/`False`) fossem interpretados erroneamente como inteiros (1/0) pelo interpretador.
- **Geração de Dados Simulados e Anonimizados:** Auxílio na formulação do conjunto fictício de 12 ocorrências (`DADOS_INICIAIS`) e 18 eventos de transição de status (`EVENTOS_INICIAIS`) em `src/dados.py`, distribuídos em quatro bairros (Jardim Aurora, Vila Esperança, Parque Verde e Centro Novo) e quatro eixos noturnos (Rota Escolar Norte, Rota Escolar Sul, Rota Transporte Central e Rota Transporte Leste), além do registro com campo ausente (OC013, sem categoria) para teste de validação, assegurando total conformidade com a LGPD e privacidade por padrão.
- **Padronização Estrutural da Documentação:** Apoio na organização dos relatórios técnicos (`README.md` e documentação oficial), estruturando seções, tabelas analíticas e fórmulas matemáticas em conformidade com o edital.

## 2. Como os Resultados Foram Verificados e Validados pela Equipe

Nenhum bloco de código ou cálculo gerado por IA foi incorporado sem auditoria manual, testes empíricos no interpretador e verificação matemática independente realizada pelos integrantes da equipe:

- **Execução Integral no Terminal (Python 3):** Todos os módulos (`src/sistema.py`, `src/dados.py` e `src/indicadores.py`) foram executados e depurados localmente no terminal sem qualquer erro de execução, comprovando a operação exclusiva com estruturas nativas da linguagem.
- **Auditoria de Estruturas de Dados (FIFO, LIFO, Dicionário e Hierarquia):** A equipe verificou manualmente o ciclo de vida dos dados: entrada na `fila_triagem` (FIFO) apenas quando o status é "Aberta", desenfileiramento imediato ao mudar para "Em Análise" ou "Concluída", empilhamento cronológico na `pilha_historico` (LIFO) a cada atualização, acesso direto via `dict_ocorrencias` em tempo O(1) e correta indexação territorial no dicionário aninhado `hierarquia_bairro`.
- **Validação do Tratamento de Inconsistências (Tolerância a Falhas):** Testou-se a função `testar_registro_invalido()` com o registro OC013 (categoria vazia `""`). A equipe confirmou que a validação lógica rejeita o registro retornando `(False, "Registro inválido ou incompleto (OC013).")`, impedindo que inconsistências contaminem a lista principal ou as matrizes.
- **Recálculo Matemático Manual dos Indicadores Comunitários:** Todos os cálculos estatísticos exibidos no painel textual foram conferidos manualmente pela equipe:
  - **Distribuição por Status:** 8 Concluídas (66,7%), 2 Em Análise (16,7%) e 2 Abertas (16,7%).
  - **Volume de Pendências:** 12 − 8 = 4 chamados ativos (33,3%).
  - **Tempo Médio de Resolução:** Soma dos prazos das ocorrências concluídas (5 + 5 + 6 + 7 + 8 + 4 + 6 + 6 = 47 dias) dividida por 8 = **5,88 dias simulados** (5,875 arredondado).
  - **Rotas 100% Operacionais:** Auditoria individual das 4 rotas, confirmando que apenas a Rota Escolar Norte (3/3) e a Rota Transporte Leste (3/3) atingiram 100% de conclusão, validando a taxa de **50,0%** (2 de 4 rotas).

## DECLARAÇÃO DE AUTORIA E RESPONSABILIDADE ÉTICA

Os integrantes da equipe declaram que compreendem integralmente o funcionamento lógico de todos os algoritmos, estruturas de dados e regras de negócio implementadas. A utilização da Inteligência Artificial ocorreu estritamente como instrumento de produtividade e apoio educacional, assumindo os estudantes a total autoria e responsabilidade pelo código e pelas conclusões técnicas apresentadas.
