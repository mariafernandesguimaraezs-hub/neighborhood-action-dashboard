"""Teste do Neighborhood Action Dashboard.
Cada linha mostra [OK] ou [FALHOU]. A ultima linha mostra o resumo.
"""

import os
import sys
 
# Faz o Python enxergar a pasta src (onde estao os arquivos do sistema)
pasta = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(pasta, "src"))
sys.path.insert(0, pasta)
 
import sistema
import menu
from dados import carregar_dados, testar_registro_invalido
from indicadores import calcular_indicadores
 
resultados = []
 
 
def verificar(descricao, condicao):
    """Mostra [OK] se a condicao for verdadeira, senao [FALHOU]."""
    resultados.append(condicao)
    if condicao:
        print("[OK]", descricao)
    else:
        print("[FALHOU]", descricao)
 
 
def novo_registro(codigo="OC900", **mudancas):
    """Cria um registro valido; os campos podem ser trocados para testar erros."""
    registro = {
        "codigo": codigo,
        "categoria": "Iluminação",
        "descricao": "Teste",
        "local_referencia": "Poste 99, Rua Teste",
        "bairro": "Bairro Teste",
        "dia_abertura": 1,
        "status": "Aberta",
    }
    registro.update(mudancas)
    return registro
 
 
# ---------------------------------------------------------------
print("\n--- 1. Dados iniciais ---")
carregar_dados()
verificar("Tem 12 ocorrencias", len(sistema.lista_ocorrencias) == 12)
verificar("Tem 18 eventos no historico (minimo 8)", len(sistema.pilha_historico) == 18)
verificar("Usa as 4 categorias",
          {o["categoria"] for o in sistema.lista_ocorrencias} == set(sistema.CATEGORIAS_VALIDAS))
verificar("Usa os 3 status",
          {o["status"] for o in sistema.lista_ocorrencias} == set(sistema.STATUS_VALIDOS))
 
# ---------------------------------------------------------------
print("\n--- 2. Validacao (registros invalidos devem ser recusados) ---")
ok, mensagem = testar_registro_invalido()
verificar("Registro OC013 (sem categoria) e recusado", ok is False)
verificar("OC013 nao foi guardado", "OC013" not in sistema.dict_ocorrencias)
 
ok, _ = sistema.inserir_na_estrutura(novo_registro("XX900"))
verificar("Codigo sem 'OC' e recusado", ok is False)
 
ok, _ = sistema.inserir_na_estrutura(novo_registro(categoria="Outra"))
verificar("Categoria inexistente e recusada", ok is False)
 
ok, _ = sistema.inserir_na_estrutura(novo_registro(status="Fechada"))
verificar("Status inexistente e recusado", ok is False)
 
ok, _ = sistema.inserir_na_estrutura(novo_registro(local_referencia="Rua"))
verificar("Local com menos de 4 letras e recusado", ok is False)
 
ok, _ = sistema.inserir_na_estrutura(novo_registro(bairro=""))
verificar("Bairro vazio e recusado", ok is False)
 
ok, _ = sistema.inserir_na_estrutura(novo_registro(dia_abertura=0))
verificar("Dia zero e recusado", ok is False)
 
ok, _ = sistema.inserir_na_estrutura(novo_registro("OC001"))
verificar("Codigo repetido (OC001) e recusado", ok is False)
 
verificar("Nenhum registro invalido entrou (continua 12)", len(sistema.lista_ocorrencias) == 12)
 
# ---------------------------------------------------------------
print("\n--- 3. Cadastro e atualizacao de status ---")
ok, _ = sistema.inserir_na_estrutura(novo_registro())
verificar("Registro valido OC900 e aceito", ok is True)
verificar("OC900 (Aberta) entrou na fila", "OC900" in sistema.fila_triagem)
 
ok, _ = sistema.atualizar_situacao("OC999", "Concluída", 5)
verificar("Codigo que nao existe e recusado", ok is False)
 
ok, _ = sistema.atualizar_situacao("OC900", "Fechada", 5)
verificar("Status invalido e recusado", ok is False)
 
ok, _ = sistema.atualizar_situacao("OC900", "Em Análise", 3)
verificar("Atualizar OC900 para Em Analise funciona", ok is True)
verificar("OC900 saiu da fila", "OC900" not in sistema.fila_triagem)
verificar("A mudanca foi para o topo da pilha de historico",
          sistema.pilha_historico[-1]["codigo"] == "OC900")
 
ok, _ = sistema.atualizar_situacao("OC900", "Concluída", 8)
verificar("Tempo de resolucao = 8 - 1 = 7 dias",
          sistema.dict_ocorrencias["OC900"]["dias_resolucao"] == 7)
 
# ---------------------------------------------------------------
print("\n--- 4. Busca e filtros ---")
verificar("Busca por codigo encontra OC001", menu.buscar_por_codigo("OC001") is not None)
verificar("Busca por codigo inexistente devolve None", menu.buscar_por_codigo("OC999") is None)
 
concluidas = menu.filtrar_ocorrencias(status="Concluída")
verificar("Filtro por status Concluida: 9 ocorrencias (8 dos dados + OC900)", len(concluidas) == 9)
 
acessibilidade = menu.filtrar_ocorrencias(categoria="Acessibilidade")
verificar("Filtro por categoria Acessibilidade: 3 ocorrencias", len(acessibilidade) == 3)
 
ambos = menu.filtrar_ocorrencias("Limpeza", "Concluída")
verificar("Filtro Limpeza E Concluida: 3 ocorrencias", len(ambos) == 3)
 
um_ou_outro = menu.filtrar_ocorrencias("Limpeza", "Aberta", modo="OU")
verificar("Filtro Limpeza OU Aberta: 5 ocorrencias", len(um_ou_outro) == 5)
 
# ---------------------------------------------------------------
print("\n--- 5. Indicadores ---")
info = calcular_indicadores()
verificar("Total do painel = total da lista", info["total"] == len(sistema.lista_ocorrencias))
verificar("Soma dos status = total", sum(info["por_status"].values()) == info["total"])
verificar("Pendentes = total - concluidas",
          info["pendentes"] == info["total"] - info["por_status"]["Concluída"])
 
matriz = sistema.construir_matriz_resumo()
verificar("Matriz tem 4 linhas e 3 colunas", len(matriz) == 4 and len(matriz[0]) == 3)
verificar("Soma da matriz = total", sum(sum(linha) for linha in matriz) == info["total"])
 
# ---------------------------------------------------------------
print("\n--- RESUMO ---")
passou = sum(resultados)
print(passou, "de", len(resultados), "testes passaram")
if passou != len(resultados):
    raise SystemExit(1)