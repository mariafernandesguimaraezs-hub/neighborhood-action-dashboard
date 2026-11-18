# Uso de Inteligência Artificial

Este arquivo registra como a IA apoiou o projeto e como os resultados foram verificados.

## Ferramenta utilizada

Claude (Anthropic), usado pelo Integrante 5 (validação, testes e envio).

## Como a IA apoiou

| Etapa | Apoio da IA | Quem usou |
|---|---|---|
| Testes | Gerou o `testes.py` com cenários de erro (código inválido, categoria ausente, dia inválido, duplicidade, status inválido) e verificações de fila, pilha, matrizes e indicadores | Integrante 5 |
| Comparação com o enunciado | Comparou o código do grupo com os requisitos da atividade e apontou o que faltava (menu, busca, filtros, categorias, `or`/`elif`/`else`, conclusão dos indicadores) | Integrante 5 |
| Código | Criou o `menu.py` (interface de terminal, busca por código, filtros por categoria e status, cadastro e atualização interativos), ajustou as categorias e os dados, e incluiu `elif/else` e a conclusão no painel | Integrante 5 |
| Documentação | Gerou um rascunho do `README.md` e deste arquivo | Integrante 5 |

[COMPLETAR: se outros integrantes usaram IA (ideias, dados fictícios, revisão de texto), registrar aqui quem usou e para quê.]

## Como os resultados foram verificados

- O código gerado foi lido pela equipe e executado com `python src/sistema.py`.
- O `testes.py` executa os testes automáticos e deve terminar com "todos os testes passaram"; ele também executa o programa real e confere a saída.
- Os números do README (percentuais, 5,88 dias de tempo médio, 2 de 4 rotas operacionais) foram conferidos contra a saída do painel e recalculados à mão (47 dias ÷ 8 conclusões).
- Os dados são fictícios, e foi conferido que não há dados pessoais.
- A equipe deve ser capaz de explicar cada estrutura e cada regra de validação no vídeo.

## Responsabilidade

A IA foi apoio. A equipe revisou, testou e responde pelo código, pela análise e pelos textos entregues.
