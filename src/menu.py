"""Interface textual do Neighborhood Action Dashboard (Tema A).

Consultas, filtros, cadastro, atualização de status e painel de indicadores,
construídos sobre as estruturas de sistema.py.
Execução: python src/sistema.py
"""
import sistema
from dados import carregar_dados
from indicadores import mostrar_painel, TIPOS_LAMPADA

SIGNIFICADO_STATUS = {
    "Aberta": "registrada e ainda não examinada (aguarda na fila de triagem)",
    "Em Análise": "já examinada e em avaliação pela equipe responsável",
    "Concluída": "problema tratado e encerrado (simulado)",
}

MENU = """
=== NEIGHBORHOOD ACTION DASHBOARD ===
 1) Listar ocorrências
 2) Buscar por código
 3) Filtrar por categoria / status
 4) Cadastrar nova ocorrência
 5) Atualizar status
 6) Eventos recentes (pilha de histórico)
 7) Fila de triagem (ordem de registro)
 8) Painel de indicadores
 9) Hierarquia bairro -> categoria -> ocorrências
10) Significado dos status
 0) Sair"""


def ler(mensagem):
    return input(mensagem).strip()


def ler_dia(mensagem):
    """Converte para int quando possível; o resto vai para a validação."""
    texto = ler(mensagem)
    return int(texto) if texto.isdigit() else texto


def formatar_linha(o):
    return (f"{o['codigo']} | {o['categoria']} | "
            f"{o['local_referencia']} | {o['status']}")


def listar_ocorrencias():
    return [formatar_linha(o) for o in sistema.lista_ocorrencias]


def buscar_por_codigo(codigo):
    """Acesso direto pelo dicionário; devolve None se não existir."""
    return sistema.dict_ocorrencias.get(str(codigo).strip().upper())


def filtrar_ocorrencias(categoria=None, status=None, modo="E"):
    """Filtra por categoria e/ou status.

    modo 'E'  : precisa bater em todos os filtros informados (AND).
    modo 'OU' : basta bater em um dos filtros informados (OR).
    """
    resultado = []
    for o in sistema.lista_ocorrencias:
        bate_cat = categoria is not None and o["categoria"] == categoria
        bate_st = status is not None and o["status"] == status
        if modo == "OU":
            incluir = bate_cat or bate_st
        else:
            incluir = ((categoria is None or bate_cat)
                       and (status is None or bate_st))
        if incluir:
            resultado.append(o)
    return resultado


def eventos_recentes(n=5):
    """Topo da pilha primeiro (último evento a entrar é o primeiro a sair)."""
    return list(reversed(sistema.pilha_historico[-n:]))


def escolher(titulo, opcoes, opcional=False):
    print(titulo)
    for i, opcao in enumerate(opcoes, 1):
        print(f"  {i}) {opcao}")
    sufixo = " (Enter = qualquer): " if opcional else ": "
    texto = ler("Escolha o número" + sufixo)
    if texto == "" and opcional:
        return None
    if texto.isdigit() and 1 <= int(texto) <= len(opcoes):
        return opcoes[int(texto) - 1]
    raise ValueError("opção inválida")


def mostrar_lista():
    linhas = listar_ocorrencias()
    print("\n--- OCORRÊNCIAS (código | categoria | local | status) ---")
    for linha in linhas:
        print(linha)
    print(f"Total: {len(linhas)}")


def buscar_interativo():
    codigo = ler("Código da ocorrência: ")
    o = buscar_por_codigo(codigo)
    if o is None:
        print(f"Ocorrência não encontrada ({codigo or 'código vazio'}).")
        return
    print("\n--- DETALHES ---")
    print(f"Código: {o['codigo']}")
    print(f"Categoria: {o['categoria']}")
    print(f"Descrição: {o.get('descricao', '-')}")
    print(f"Local: {o['local_referencia']} (bairro {o['bairro']})")
    print(f"Aberta no dia: {o['dia_abertura']}")
    print(f"Status: {o['status']}")
    if o["status"] == "Aberta":
        print("Situação: aguardando exame na fila de triagem.")
    elif o["status"] == "Em Análise":
        print("Situação: já examinada, em avaliação.")
    else:
        print("Situação: concluída.")
    if "dias_resolucao" in o:
        print(f"Dias até a conclusão: {o['dias_resolucao']}")


def filtrar_interativo():
    try:
        categoria = escolher("Categoria:", sistema.CATEGORIAS_VALIDAS, True)
        status = escolher("Status:", sistema.STATUS_VALIDOS, True)
    except ValueError:
        print("Opção inválida.")
        return
    modo = "E"
    if categoria and status:
        m = ler("Combinar com E (ambos) ou OU (qualquer um)? [E/OU]: ").upper()
        modo = "OU" if m == "OU" else "E"
    itens = filtrar_ocorrencias(categoria, status, modo)
    if not itens:
        print("Nenhuma ocorrência encontrada com esses filtros.")
        return
    for o in itens:
        print(formatar_linha(o))
    print(f"Encontradas: {len(itens)}")


def cadastrar_interativo():
    print("\n--- CADASTRAR OCORRÊNCIA ---")
    print("Use apenas dados fictícios ou consentidos; não informe dados pessoais.")
    codigo = ler("Código (ex.: OC014): ").upper()
    try:
        categoria = escolher("Categoria:", sistema.CATEGORIAS_VALIDAS)
    except ValueError:
        categoria = ""
    local = ler("Local de referência (genérico, ex.: Poste 10, Rua X): ")
    bairro = ler("Bairro: ")
    dia = ler_dia("Dia de abertura (inteiro positivo): ")
    rota = ler("Rota escolar/transporte (opcional): ")
    try:
        tipo = escolher("Tipo de lâmpada (opcional, só para Iluminação):",
                        TIPOS_LAMPADA, True)
    except ValueError:
        tipo = None
    descricao = ler("Descrição breve: ")
    registro = {
        "codigo": codigo,
        "categoria": categoria,
        "descricao": descricao,
        "local_referencia": local,
        "bairro": bairro,
        "dia_abertura": dia,
        "status": "Aberta",
        "rota": rota,
        "tipo_lampada": tipo,
    }
    ok, mensagem = sistema.inserir_na_estrutura(registro)
    print(mensagem)
    if not ok:
        print("Confira: código OC + 3 dígitos único, categoria da lista, "
              "local com 4+ caracteres, bairro preenchido e dia positivo.")


def atualizar_interativo():
    codigo = ler("Código da ocorrência: ")
    o = buscar_por_codigo(codigo)
    if o is None:
        print(f"Ocorrência não encontrada ({codigo or 'código vazio'}).")
        return
    print(f"Status atual de {o['codigo']}: {o['status']}")
    try:
        novo = escolher("Novo status:", sistema.STATUS_VALIDOS)
    except ValueError:
        print("Status informado é inválido.")
        return
    dia = ler_dia("Dia da atualização (inteiro positivo): ")
    ok, mensagem = sistema.atualizar_situacao(o["codigo"], novo, dia)
    print(mensagem)


def mostrar_eventos():
    eventos = eventos_recentes(5)
    print("\n--- EVENTOS RECENTES (mais novo primeiro) ---")
    if not eventos:
        print("Nenhum evento registrado.")
    for e in eventos:
        print(f"Dia {e['dia']}: {e['codigo']} {e['de']} -> {e['para']}")


def mostrar_fila():
    print("\n--- FILA DE TRIAGEM (ordem de registro) ---")
    if not sistema.fila_triagem:
        print("Nenhuma ocorrência aguardando triagem.")
    for posicao, codigo in enumerate(sistema.fila_triagem, 1):
        print(f"{posicao}º: {formatar_linha(sistema.dict_ocorrencias[codigo])}")


def mostrar_hierarquia():
    print("\n--- HIERARQUIA: BAIRRO -> CATEGORIA -> OCORRÊNCIAS ---")
    for bairro, categorias in sistema.hierarquia_bairro.items():
        print(bairro)
        for categoria, codigos in categorias.items():
            if codigos:
                print(f"  {categoria}: {', '.join(codigos)}")


def mostrar_significados():
    print("\n--- SIGNIFICADO DOS STATUS ---")
    for status, texto in SIGNIFICADO_STATUS.items():
        print(f"{status}: {texto}")


ACOES = {
    "1": mostrar_lista,
    "2": buscar_interativo,
    "3": filtrar_interativo,
    "4": cadastrar_interativo,
    "5": atualizar_interativo,
    "6": mostrar_eventos,
    "7": mostrar_fila,
    "8": mostrar_painel,
    "9": mostrar_hierarquia,
    "10": mostrar_significados,
}


def executar():
    qtd = carregar_dados()
    print(f"Dados fictícios carregados: {qtd} ocorrências novas.")
    while True:
        print(MENU)
        try:
            opcao = ler("Opção: ")
            if opcao == "0":
                print("Saindo do sistema.")
                break
            acao = ACOES.get(opcao)
            if acao is None:
                print("Opção inválida. Escolha um número do menu.")
            else:
                acao()
        except EOFError:
            print("\nEntrada encerrada. Saindo do sistema.")
            break
