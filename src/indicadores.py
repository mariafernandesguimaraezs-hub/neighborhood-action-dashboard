"""Indicadores e matrizes 2D do Tema A - compativel com sistema.py."""
from sistema import (lista_ocorrencias, CATEGORIAS_VALIDAS, STATUS_VALIDOS,
                     construir_matriz_resumo)

TIPOS_LAMPADA = ['LED', 'Vapor de Sódio', 'Vapor Metálico']


def matriz_tipo_status():
    """Linhas: tipos de lampada; colunas: status. Lista de listas (matriz 3x3)."""
    matriz = [[0 for _ in STATUS_VALIDOS] for _ in TIPOS_LAMPADA]
    for ocorrencia in lista_ocorrencias:
        tipo = ocorrencia.get('tipo_lampada')
        status = ocorrencia['status']
        if tipo in TIPOS_LAMPADA and status in STATUS_VALIDOS:
            matriz[TIPOS_LAMPADA.index(tipo)][STATUS_VALIDOS.index(status)] += 1
    return matriz


def calcular_indicadores():
    total = len(lista_ocorrencias)
    por_categoria = {categoria: 0 for categoria in CATEGORIAS_VALIDAS}
    por_status = {status: 0 for status in STATUS_VALIDOS}
    resolucoes = []
    rotas = {}
    for ocorrencia in lista_ocorrencias:
        por_categoria[ocorrencia['categoria']] += 1
        por_status[ocorrencia['status']] += 1
        if ocorrencia['status'] == 'Concluída' and 'dias_resolucao' in ocorrencia:
            resolucoes.append(ocorrencia['dias_resolucao'])
        rota = ocorrencia.get('rota')
        if rota:
            if rota not in rotas:
                rotas[rota] = []
            rotas[rota].append(ocorrencia)

    rotas_operacionais = sum(
        1 for registros in rotas.values()
        if registros and all(item['status'] == 'Concluída' for item in registros)
    )
    qtd_rotas = len(rotas)
    return {
        'total': total,
        'por_categoria': por_categoria,
        'por_status': por_status,
        'proporcao_categoria': {k: (100*v/total if total else 0) for k,v in por_categoria.items()},
        'proporcao_status': {k: (100*v/total if total else 0) for k,v in por_status.items()},
        'pendentes': total - por_status['Concluída'],
        'tempo_medio_resolucao': (sum(resolucoes)/len(resolucoes) if resolucoes else None),
        'rotas_total': qtd_rotas,
        'rotas_operacionais': rotas_operacionais,
        'percentual_rotas_operacionais': (100*rotas_operacionais/qtd_rotas if qtd_rotas else 0),
    }


def mostrar_painel():
    info = calcular_indicadores()
    print('\n=== PAINEL COMUNITARIO - NEIGHBORHOOD ACTION DASHBOARD ===')
    print('Total de ocorrencias:', info['total'])
    print('\nPOR CATEGORIA (quantidade e porcentagem)')
    for nome, qtd in info['por_categoria'].items():
        print(f'  {nome}: {qtd} ({info["proporcao_categoria"][nome]:.1f}%)')
    print('\nPOR STATUS (quantidade e porcentagem)')
    for nome, qtd in info['por_status'].items():
        print(f'  {nome}: {qtd} ({info["proporcao_status"][nome]:.1f}%)')
    print('Pendentes (Aberta + Em Análise):', info['pendentes'])
    media = info['tempo_medio_resolucao']
    print('Tempo medio de resolucao:', f'{media:.2f} dias simulados' if media is not None else 'Sem conclusoes com prazo')
    print('\nMATRIZ 2D - CATEGORIA x STATUS')
    print('Ordem das colunas:', ', '.join(STATUS_VALIDOS))
    for nome, linha in zip(CATEGORIAS_VALIDAS, construir_matriz_resumo()):
        print(f'  {nome}: {linha}')
    print('\nMATRIZ 2D - TIPO DE LAMPADA x STATUS (somente ocorrencias de Iluminacao)')
    print('Ordem das colunas:', ', '.join(STATUS_VALIDOS))
    for nome, linha in zip(TIPOS_LAMPADA, matriz_tipo_status()):
        print(f'  {nome}: {linha}')
    print('\nROTAS ESCOLARES / TRANSPORTE')
    print(f'  Rotas 100% operacionais: {info["rotas_operacionais"]}/{info["rotas_total"]} ({info["percentual_rotas_operacionais"]:.1f}%)')
    print('  Regra simulada: rota operacional = todas as ocorrencias da rota concluidas.')
    print('\nFORMULAS: percentual = quantidade / total * 100;')
    print('  tempo medio = soma(dias_resolucao) / numero de conclusoes com prazo;')
    print('  percentual de rotas = rotas operacionais / rotas cadastradas * 100.')
    # Conclusao calculada: categoria com mais pendencias (Aberta + Em Analise)
    pendentes_cat = {nome: linha[0] + linha[1]
                     for nome, linha in zip(CATEGORIAS_VALIDAS, construir_matriz_resumo())}
    maximo = max(pendentes_cat.values())
    lideres = [nome for nome, qtd in pendentes_cat.items() if qtd == maximo]
    if info['pendentes'] == 0:
        print('\nCONCLUSAO: neste conjunto simulado, nao ha demandas pendentes.')
    else:
        rotulo = 'a categoria com mais pendencias e' if len(lideres) == 1 else 'as categorias empatadas com mais pendencias sao'
        print(f'\nCONCLUSAO: neste conjunto simulado, {rotulo}')
        print(f'  {", ".join(lideres)} ({maximo} pendente(s) cada, de {info["pendentes"]} no total),')
        print('  o que sugere prioridade de atencao da comunidade para esse tipo de demanda.')
    print('\nINTERPRETACAO: indicadores mostram demandas ficticias e nao comprovam')
    print('  o funcionamento real da iluminacao ou a seguranca das rotas.')


if __name__ == '__main__':
    from dados import carregar_dados
    carregar_dados()
    mostrar_painel()
