import sqlite3
import time
from datetime import datetime, timedelta


def adicionar_cliente(nome):
    conn = sqlite3.connect('barbearia.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clientes (nome) VALUES (?)', (nome,))
    conn.commit()
    conn.close()


def adicionar_barbeiro(nome):
    conn = sqlite3.connect('barbearia.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO barbeiros (nome) VALUES (?)', (nome,))
    conn.commit()
    conn.close()


def listar_agendamentos():
    conn = sqlite3.connect('barbearia.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT a.id, c.nome, b.nome, a.data, a.horario, a.servico
    FROM agendamentos a
    JOIN clientes c ON a.cliente_id = c.id
    JOIN barbeiros b ON a.barbeiro_id = b.id
    ''')
    agendamentos = cursor.fetchall()
    conn.close()
    return agendamentos


def listar_agendamentos_atuais():
    conn = sqlite3.connect('barbearia.db')
    cursor = conn.cursor()
    agora = datetime.now()
    cursor.execute('''
    SELECT a.id, c.nome, b.nome, a.data, a.horario, a.servico
    FROM agendamentos a
    JOIN clientes c ON a.cliente_id = c.id
    JOIN barbeiros b ON a.barbeiro_id = b.id
    ''')
    agendamentos = cursor.fetchall()
    agendamentos_atuais = []

    for agendamento in agendamentos:
        try:
            data_horario = datetime.strptime(f"{agendamento[3]} {agendamento[4]}", '%Y-%m-%d %H:%M')
            if data_horario + timedelta(hours=2) >= agora:
                agendamentos_atuais.append(agendamento)
        except ValueError as e:
            print(f"Erro ao converter data e hora: {e}")
            continue

    conn.close()
    return agendamentos_atuais


def listar_clientes():
    conn = sqlite3.connect('barbearia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    return clientes


def buscar_cliente_por_nome(nome):
    conn = sqlite3.connect('barbearia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome FROM clientes WHERE nome LIKE ?', ('%' + nome + '%',))
    clientes = cursor.fetchall()
    conn.close()
    return clientes


def verificar_disponibilidade(barbeiro_id, data, horario, duracao):
    conn = sqlite3.connect('barbearia.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT horario, servico FROM agendamentos
    WHERE barbeiro_id = ? AND data = ?
    ''', (barbeiro_id, data))

    agendamentos = cursor.fetchall()
    conn.close()

    horario_novo = datetime.strptime(horario, '%H:%M')
    for agendamento in agendamentos:
        horario_existente = datetime.strptime(agendamento[0], '%H:%M')
        duracao_existente = timedelta(minutes=30) if agendamento[1] in ['cabelo', 'barba'] else timedelta(hours=1)

        if horario_existente <= horario_novo < horario_existente + duracao_existente or \
           horario_novo <= horario_existente < horario_novo + duracao:
            return False
    return True


def marcar_agendamento(cliente_id, barbeiro_id, data, horario, servico, valor):
    try:
        data_formatada = datetime.strptime(data, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        raise ValueError("Formato de data inválido. Use DD/MM/AAAA.")

    duracao = timedelta(minutes=30) if servico in ['cabelo', 'barba'] else timedelta(hours=1)

    tentativa = 0
    sucesso = False
    while tentativa < 5 and not sucesso:
        try:
            if verificar_disponibilidade(barbeiro_id, data_formatada, horario, duracao):
                conn = sqlite3.connect('barbearia.db')
                cursor = conn.cursor()
                cursor.execute('''
                INSERT INTO agendamentos (cliente_id, barbeiro_id, data, horario, servico, valor) 
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (cliente_id, barbeiro_id, data_formatada, horario, servico, valor))
                conn.commit()
                conn.close()
                sucesso = True
            else:
                raise Exception("Horário não disponível. Escolha outro horário.")
        except sqlite3.OperationalError as e:
            tentativa += 1
            time.sleep(0.1)
        finally:
            if 'conn' in locals():
                conn.close()

    if not sucesso:
        raise Exception("Não foi possível realizar o agendamento após várias tentativas.")


def calcular_lucro_mensal(mes, ano):
    conn = sqlite3.connect('barbearia.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT b.nome, SUM(a.valor) as total_faturado
    FROM agendamentos a
    JOIN barbeiros b ON a.barbeiro_id = b.id
    WHERE strftime('%m', a.data) = ? AND strftime('%Y', a.data) = ?
    GROUP BY b.nome
    ORDER BY total_faturado DESC
    ''', (f"{mes:02}", str(ano)))
    lucros = cursor.fetchall()
    conn.close()
    return lucros


def remover_agendamentos_antigos():
    conn = sqlite3.connect('barbearia.db')
    cursor = conn.cursor()
    agora = datetime.now()
    cursor.execute('SELECT id, data, horario FROM agendamentos')
    agendamentos = cursor.fetchall()

    for agendamento in agendamentos:
        try:
            data_horario = datetime.strptime(f"{agendamento[1]} {agendamento[2]}", '%Y-%m-%d %H:%M')
            if data_horario + timedelta(hours=2) < agora:
                cursor.execute('DELETE FROM agendamentos WHERE id = ?', (agendamento[0],))
        except ValueError as e:
            print(f"Erro ao converter data e hora: {e}")
            continue

    conn.commit()
    conn.close()
