# Neighborhood Action Dashboard

Global Solution FIAP 2026.2 – CitizenTech

**Equipe:** 

Eduardo Henrique Campos da Silva - [PREENCHER RM]
Julia de Oliveira Silva - [PREENCHER RM]
Pedro Henrique Monteiro Scabio - [PREENCHER RM]
Maria Eduarda Fernandes Guimaraes - [PREENCHER RM]
Maria Fernanda Barbosa Firmo - [PREENCHER RM]

## 1. Bairro simulado, problema e público

Os dados são **fictícios**, sem nenhuma informação pessoal. Foram criados quatro bairros imaginários (Jardim Aurora, Vila Esperança, Parque Verde e Centro Novo) com 12 ocorrências de iluminação, acessibilidade, limpeza e conservação de espaços coletivos.

Problema: os relatos de melhoria do bairro ficam dispersos, as prioridades não ficam claras e os moradores não conseguem acompanhar a situação das solicitações. O protótipo organiza esses relatos em um painel de terminal.

Público beneficiado: moradores que registram e acompanham demandas, e quem organiza a comunidade e precisa saber o que está pendente.

## 2. Como executar

Requisito: Python 3 (somente biblioteca padrão, sem instalar nada).

```
python src/sistema.py      # abre o menu interativo
python src/dados.py        # carrega os dados e mostra o teste do registro inválido
python src/indicadores.py  # mostra só o painel de indicadores
python testes.py           # executa os testes de validação
```

## 3. Formato dos dados

Os registros são inicializados no código Python (`src/dados.py`). Cada ocorrência é um dicionário:

| Campo | Obrigatório | Regra |
|---|---|---|
| `codigo` | sim | `OC` + 3 dígitos (ex.: `OC001`), único |
| `categoria` | sim | Iluminação, Acessibilidade, Limpeza ou Conservação de Espaços Coletivos |
| `local_referencia` | sim | local genérico com pelo menos 4 caracteres |
| `bairro` | sim | texto não vazio |
| `dia_abertura` | sim | dia simulado, inteiro positivo |
| `status` | sim | Aberta, Em Análise ou Concluída |
| `descricao` | não | descrição breve |
| `rota` | não | rota escolar ou de transporte simulada |
| `tipo_lampada` | não | LED, Vapor de Sódio ou Vapor Metálico (só para Iluminação) |

**Significado dos status**

- **Aberta:** registrada e ainda não examinada (aguarda na fila de triagem).
- **Em Análise:** já examinada e em avaliação.
- **Concluída:** problema tratado e encerrado (simulado).

## 4. Estruturas de dados e justificativa

| Estrutura | Onde | Por que |
|---|---|---|
| Lista (`lista_ocorrencias`) | `sistema.py` | guarda todas as ocorrências e permite percorrê-las em listagens e indicadores |
| Fila (`fila_triagem`) | `sistema.py` | demandas ainda não examinadas, atendidas pela ordem de registro (primeiro a entrar, primeiro a sair) |
| Pilha (`pilha_historico`) | `sistema.py` | cada mudança de status é empilhada; o evento mais recente é o primeiro a ser consultado |
| Dicionário (`dict_ocorrencias`) | `sistema.py` | acesso direto a uma ocorrência pelo código, sem percorrer a lista |
| Hierarquia (`hierarquia_bairro`) | `sistema.py` | bairro → categoria → códigos; mostra rapidamente que tipos de problema cada bairro tem |
| Matrizes (lista de listas) | `sistema.py`, `indicadores.py` | resumem quantidades: categoria × status (4×3) e tipo de lâmpada × status (3×3) |

## 5. Regras lógicas principais

- **Cadastro:** `inserir_na_estrutura` só aceita o registro se `validar_ocorrencia` retornar verdadeiro e o código ainda não existir. Registros inválidos recebem a mensagem "Registro inválido ou incompleto".
- **Validação (expressão booleana):**
  ```python
  return (codigo_valido and categoria_valida and status_valido
          and local_valido and bairro_valido and data_valida)
  ```
  Todas as condições precisam ser verdadeiras (AND). Se uma falhar, o registro é rejeitado. O registro `OC013`, com categoria vazia, é rejeitado por isso.
- **Dia válido (AND e NOT):**
  ```python
  return isinstance(valor, int) and not isinstance(valor, bool) and valor > 0
  ```
  O `not` impede que `True` seja aceito como dia (em Python, `True` é um inteiro).
- **Filtro (AND e OR):** em `menu.py`, o modo `E` exige que a ocorrência bata em todos os filtros informados; o modo `OU` exige que bata em pelo menos um (`bate_cat or bate_st`).
- **Atualização de status (IF, ELIF, ELSE):** `atualizar_situacao` rejeita código inexistente, status desconhecido, dia inválido, dia anterior à abertura e status repetido. Se o novo status for Aberta, a ocorrência volta ao fim da fila (`if`); se deixar de estar Aberta, sai da fila (`elif`); nas demais trocas a fila não muda (`else`). Cada mudança válida vira um evento na pilha.
- **Busca:** por código (dicionário) e filtro por categoria e/ou status, informando claramente quando nada é encontrado.

## 6. Indicadores

| Indicador | Fórmula |
|---|---|
| Percentual por categoria e por status | quantidade ÷ total × 100 |
| Pendentes | total − concluídas (Aberta + Em Análise) |
| Tempo médio de resolução | soma(`dias_resolucao`) ÷ número de conclusões; `dias_resolucao` = dia da conclusão − dia de abertura |
| Rotas operacionais | rota operacional = todas as ocorrências da rota concluídas; percentual = rotas operacionais ÷ rotas cadastradas × 100 |

Resultado com os dados iniciais: 12 ocorrências, 3 em cada categoria (25% cada); 2 abertas, 2 em análise e 8 concluídas; 4 pendentes; tempo médio de 5,88 dias simulados (47 ÷ 8); 2 de 4 rotas totalmente operacionais (50%).

**Interpretação:** a maior parte das demandas simuladas foi concluída (66,7%). As pendências ficam em Iluminação (2, ambas em análise) e Conservação de Espaços Coletivos (2, ambas ainda abertas), então essas categorias merecem atenção. Os números vêm de dados fictícios e não provam a situação real de nenhum bairro.

## 7. Exemplo de uso

Cadastro (opção 4):
```
Código (ex.: OC014): OC014
Categoria: 1 Iluminação ...  -> 1
Local de referência: Poste 10, Rua Nova
Bairro: Centro Novo
Dia de abertura: 5
Ocorrência OC014 registrada com sucesso.
```

Consulta (opção 2):
```
Código da ocorrência: OC005
Código: OC005
Categoria: Iluminação
Local: Poste 04, Av. Central (bairro Vila Esperança)
Status: Em Análise
Situação: já examinada, em avaliação.
```

Alteração de status (opção 5) e histórico (opção 6):
```
Status de OC014 atualizado: Aberta -> Em Análise.
Dia 6: OC014 Aberta -> Em Análise
```

Saída (opção 0): `Saindo do sistema.`

Registro inválido (carga em `dados.py`): `Registro inválido ou incompleto (OC013).`

## 8. Acessibilidade, inclusão e privacidade

- **Privacidade:** os dados são fictícios; os locais são genéricos (poste, praça, parada) e o sistema não pede nome, endereço de morador, telefone ou qualquer dado pessoal. O cadastro lembra o usuário disso.
- **Acessibilidade:** a interface é só texto, compatível com leitores de tela, sem depender de cores nem de mouse. As mensagens de erro dizem o que corrigir.
- **Inclusão:** a categoria Acessibilidade registra barreiras como falta de rampa, piso tátil e espaço para cadeira de rodas, tratando-as como demandas do bairro. As mensagens usam linguagem simples.

## 9. Conclusões, limitações e aprendizados

- O protótipo cadastra, valida, consulta, filtra, atualiza status com histórico e calcula indicadores usando apenas Python básico.
- Limitações: os dados são simulados e ficam só na memória (somem ao fechar o programa); não há integração com a prefeitura nem promessa de atendimento; o tempo de resolução usa dias simulados; a entrada de dados no terminal é simples.
- Aprendizados: escolher a estrutura certa para cada finalidade (fila para ordem de chegada, pilha para histórico, dicionário para busca por código) deixa o código mais claro, e testar casos de erro evitou registros inconsistentes.

## 10. Estrutura do repositório

```
README.md
entrega.txt
testes.py
src/
  sistema.py      estruturas, validação, atualização e ponto de entrada
  menu.py         interface de terminal, buscas e filtros
  dados.py        dados fictícios e registro inválido
  indicadores.py  indicadores e matrizes
docs/
  uso_ia.md       registro do uso de IA
```

Uso de IA documentado em `docs/uso_ia.md`.
