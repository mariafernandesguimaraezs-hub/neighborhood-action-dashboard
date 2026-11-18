"""Dados ficticios do Tema A - Global Solution FIAP 2026.2.
Importa e usa as estruturas ja implementadas em sistema.py.
"""
from sistema import inserir_na_estrutura, atualizar_situacao

# Cada rota e ficticia; o campo 'rota' permite calcular o indicador especifico.
# Todos os registros comecam como 'Aberta' para gerar historico real de eventos.
DADOS_INICIAIS = [
    ('OC001','Iluminação','Poste 01, Rua das Flores','Jardim Aurora',1,'Rota Escolar Norte','LED','Luminaria apagada proxima a escola'),
    ('OC002','Acessibilidade','Calçada 01, Rua das Flores','Jardim Aurora',2,'Rota Escolar Norte',None,'Calcada sem rampa de acesso proxima a escola'),
    ('OC003','Limpeza','Praça 01, Av. do Colegio','Jardim Aurora',3,'Rota Escolar Norte',None,'Lixo acumulado na praca em frente ao colegio'),
    ('OC004','Acessibilidade','Parada 01, Av. Central','Vila Esperança',1,'Rota Transporte Central',None,'Ponto de onibus sem rampa e sem piso tatil'),
    ('OC005','Iluminação','Poste 04, Av. Central','Vila Esperança',2,'Rota Transporte Central','Vapor de Sódio','Lampada queimada no corredor'),
    ('OC006','Conservação de Espaços Coletivos','Praça 02, Av. Central','Vila Esperança',3,'Rota Transporte Central',None,'Brinquedo da praca quebrado'),
    ('OC007','Limpeza','Calçada 02, Rua do Mercado','Parque Verde',2,'Rota Escolar Sul',None,'Entulho acumulado na calcada'),
    ('OC008','Iluminação','Parada 02, Rua do Mercado','Parque Verde',4,'Rota Escolar Sul','Vapor Metálico','Parada escura no trajeto escolar'),
    ('OC009','Conservação de Espaços Coletivos','Quadra 01, Rua do Mercado','Parque Verde',3,'Rota Escolar Sul',None,'Alambrado da quadra danificado'),
    ('OC010','Limpeza','Praça 03, Av. das Palmeiras','Centro Novo',1,'Rota Transporte Leste',None,'Lixeiras cheias e sem coleta na praca'),
    ('OC011','Conservação de Espaços Coletivos','Banco 01, Av. das Palmeiras','Centro Novo',2,'Rota Transporte Leste',None,'Banco da praca com assento quebrado'),
    ('OC012','Acessibilidade','Abrigo 01, Av. das Palmeiras','Centro Novo',3,'Rota Transporte Leste',None,'Abrigo de passageiros sem espaco para cadeira de rodas'),
]

# (codigo, novo_status, dia simulado)
EVENTOS_INICIAIS = [
    ('OC001','Em Análise',4), ('OC001','Concluída',6),
    ('OC002','Em Análise',5), ('OC002','Concluída',7),
    ('OC003','Em Análise',6), ('OC003','Concluída',9),
    ('OC004','Em Análise',4), ('OC004','Concluída',8),
    ('OC005','Em Análise',5),
    ('OC007','Em Análise',6), ('OC007','Concluída',10),
    ('OC008','Em Análise',7),
    ('OC010','Em Análise',3), ('OC010','Concluída',5),
    ('OC011','Em Análise',5), ('OC011','Concluída',8),
    ('OC012','Em Análise',6), ('OC012','Concluída',9),
]

# Um registro intencionalmente inconsistente para demonstrar validacao.
REGISTRO_INVALIDO = {
    'codigo':'OC013', 'categoria':'', 'descricao':'Lampada apagada',
    'local_referencia':'Rua sem nome', 'bairro':'Jardim Aurora',
    'dia_abertura':5, 'status':'Aberta', 'rota':'Rota Escolar Norte',
    'tipo_lampada':'LED'
}


def carregar_dados():
    """Insere 12 registros e aplica eventos; evita duplicacao se executada novamente."""
    from sistema import dict_ocorrencias
    inseridos = 0
    for codigo, categoria, local, bairro, dia, rota, tipo, descricao in DADOS_INICIAIS:
        if codigo in dict_ocorrencias:
            continue
        registro = {
            'codigo':codigo, 'categoria':categoria, 'descricao':descricao,
            'local_referencia':local, 'bairro':bairro, 'dia_abertura':dia,
            'status':'Aberta', 'rota':rota, 'tipo_lampada':tipo
        }
        ok, mensagem = inserir_na_estrutura(registro)
        if not ok:
            raise ValueError(mensagem)
        inseridos += 1
    # Eventos apenas para os registros recem-inseridos; nao sobrescreve alteracoes do usuario.
    if inseridos:
        for codigo, status, dia in EVENTOS_INICIAIS:
            ok, mensagem = atualizar_situacao(codigo, status, dia)
            if not ok:
                raise ValueError(mensagem)
    return inseridos


def testar_registro_invalido():
    """Deve retornar (False, mensagem), sem inserir OC013."""
    return inserir_na_estrutura(REGISTRO_INVALIDO.copy())


if __name__ == '__main__':
    from sistema import lista_ocorrencias, pilha_historico
    print('Registros adicionados:', carregar_dados())
    print('Total de ocorrencias:', len(lista_ocorrencias))
    print('Eventos no historico:', len(pilha_historico))
    print('Teste de validacao:', testar_registro_invalido())
