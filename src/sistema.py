# Constantes padronizadas do Tema A
CATEGORIAS_VALIDAS = [
    "Iluminação",
    "Acessibilidade",
    "Limpeza",
    "Conservação de Espaços Coletivos",
]

STATUS_VALIDOS = ["Aberta", "Em Análise", "Concluída"]

# Estruturas de dados
lista_ocorrencias = []
dict_ocorrencias = {}
fila_triagem = []
pilha_historico = []

# Hierarquia: Bairro -> Categoria -> Lista de códigos
hierarquia_bairro = {}


def dia_valido(valor):
    #Aceita apenas números inteiros positivos, sem aceitar bool.
    return isinstance(valor, int) and not isinstance(valor, bool) and valor > 0


def validar_ocorrencia(registro):
    #Verifica os campos obrigatórios e seus formatos.
    if not isinstance(registro, dict):
        return False

    codigo = str(registro.get("codigo", "")).strip()
    categoria = registro.get("categoria", "")
    status = registro.get("status", "")
    local = str(registro.get("local_referencia", "")).strip()
    bairro = str(registro.get("bairro", "")).strip()
    dia_abertura = registro.get("dia_abertura")

    codigo_valido = (
        len(codigo) == 5
        and codigo.startswith("OC")
        and codigo[2:].isdigit()
    )
    categoria_valida = categoria in CATEGORIAS_VALIDAS
    status_valido = status in STATUS_VALIDOS
    local_valido = len(local) >= 4
    bairro_valido = bool(bairro)
    data_valida = dia_valido(dia_abertura)

    return (
        codigo_valido
        and categoria_valida
        and status_valido
        and local_valido
        and bairro_valido
        and data_valida
    )


def inserir_na_estrutura(registro):
 #Valida e distribui a ocorrência nas estruturas de dados.
    if not validar_ocorrencia(registro):
        codigo = registro.get("codigo", "SEM_CODIGO") if isinstance(registro, dict) else "SEM_CODIGO"
        return False, f"Registro inválido ou incompleto ({codigo})."

    # Normaliza os campos de texto usados como identificadores
    registro["codigo"] = str(registro["codigo"]).strip()
    registro["bairro"] = str(registro["bairro"]).strip()
    registro["local_referencia"] = str(registro["local_referencia"]).strip()

    codigo = registro["codigo"]

    if codigo in dict_ocorrencias:
        return False, f"Código {codigo} já existe no sistema."

    lista_ocorrencias.append(registro)
    dict_ocorrencias[codigo] = registro

    if registro["status"] == "Aberta":
        fila_triagem.append(codigo)

    bairro = registro["bairro"]
    categoria = registro["categoria"]

    if bairro not in hierarquia_bairro:
        hierarquia_bairro[bairro] = {
            cat: [] for cat in CATEGORIAS_VALIDAS
        }

    hierarquia_bairro[bairro][categoria].append(codigo)

    return True, f"Ocorrência {codigo} registrada com sucesso."


def atualizar_situacao(codigo, novo_status, dia_atual):
    #Atualiza status, fila de triagem e histórico.
    codigo = str(codigo).strip()

    if codigo not in dict_ocorrencias:
        return False, "Ocorrência não encontrada."

    if novo_status not in STATUS_VALIDOS:
        return False, "Status informado é inválido."

    if not dia_valido(dia_atual):
        return False, "O dia atual deve ser um número inteiro positivo."

    ocorrencia = dict_ocorrencias[codigo]
    dia_abertura = ocorrencia["dia_abertura"]

    if dia_atual < dia_abertura:
        return False, "O dia da atualização não pode ser anterior à abertura."

    status_anterior = ocorrencia["status"]

    if status_anterior == novo_status:
        return False, f"A ocorrência já está com o status '{novo_status}'."

    ocorrencia["status"] = novo_status

    if novo_status == "Concluída":
        ocorrencia["dias_resolucao"] = dia_atual - dia_abertura

    # Se voltar para Aberta, entra no fim da fila;
    # caso contrário, sai da fila ao deixar de estar Aberta.
    if novo_status == "Aberta":
        if codigo not in fila_triagem:
            fila_triagem.append(codigo)
    elif status_anterior == "Aberta" and codigo in fila_triagem:
        fila_triagem.remove(codigo)
    else:
        pass  # Em Análise <-> Concluída: a fila não é afetada

    evento = {
        "codigo": codigo,
        "de": status_anterior,
        "para": novo_status,
        "dia": dia_atual,
    }
    pilha_historico.append(evento)

    return (
        True,
        f"Status de {codigo} atualizado: {status_anterior} -> {novo_status}.",
    )


def construir_matriz_resumo():
    #Monta a matriz 4x3: categorias por status.
    matriz = [
        [0 for _ in STATUS_VALIDOS]
        for _ in CATEGORIAS_VALIDAS
    ]

    for ocorrencia in lista_ocorrencias:
        linha = CATEGORIAS_VALIDAS.index(ocorrencia["categoria"])
        coluna = STATUS_VALIDOS.index(ocorrencia["status"])
        matriz[linha][coluna] += 1

    return matriz


if __name__ == "__main__":
    # Ponto de entrada oficial: python src/sistema.py
    # O menu importa este módulo pelo nome "sistema", assim todas as
    # estruturas de dados ficam em um único lugar.
    import menu

    menu.executar()