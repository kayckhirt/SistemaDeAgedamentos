import tkinter as tk
from tkinter import messagebox, ttk
from db.database import criar_banco
from db.crud import (
    adicionar_cliente,
    adicionar_barbeiro,
    listar_agendamentos_atuais,
    listar_clientes,
    buscar_cliente_por_nome,
    marcar_agendamento,
    calcular_lucro_mensal,
    remover_agendamentos_antigos,
)

# Funções auxiliares


def exibir_mensagem(titulo, mensagem):
    messagebox.showinfo(titulo, mensagem)


def adicionar_cliente_interface(nome_entry):
    nome = nome_entry.get()
    adicionar_cliente(nome)
    exibir_mensagem("Sucesso", f"Cliente '{nome}' adicionado com sucesso!")


def adicionar_barbeiro_interface(nome_entry):
    nome = nome_entry.get()
    adicionar_barbeiro(nome)
    exibir_mensagem("Sucesso", f"Barbeiro '{nome}' adicionado com sucesso!")


def listar_agendamentos_interface(tree):
    remover_agendamentos_antigos()
    for row in tree.get_children():
        tree.delete(row)
    agendamentos = listar_agendamentos_atuais()
    for agendamento in agendamentos:
        tree.insert('', 'end', values=agendamento)


def listar_clientes_interface(tree):
    for row in tree.get_children():
        tree.delete(row)
    clientes = listar_clientes()
    for cliente in clientes:
        tree.insert('', 'end', values=cliente)


def buscar_cliente_interface(nome_entry, tree):
    nome = nome_entry.get()
    for row in tree.get_children():
        tree.delete(row)
    clientes = buscar_cliente_por_nome(nome)
    for cliente in clientes:
        tree.insert('', 'end', values=cliente)


def marcar_agendamento_interface(cliente_id_entry, barbeiro_id_entry, data_entry, horario_entry, servico_entry, valor_entry):
    cliente_id = int(cliente_id_entry.get())
    barbeiro_id = int(barbeiro_id_entry.get())
    data = data_entry.get()
    horario = horario_entry.get()
    servico = servico_entry.get()
    valor = float(valor_entry.get())
    try:
        marcar_agendamento(cliente_id, barbeiro_id, data, horario, servico, valor)
        exibir_mensagem("Sucesso", f"Agendamento realizado para {data} às {horario}, Serviço: {servico}, Valor: R${valor:.2f}")
    except Exception as e:
        exibir_mensagem("Erro", str(e))


# Inicializar o banco de dados
criar_banco()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Gestor de Barbearia")

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Aba de adicionar cliente
frame_cliente = ttk.Frame(notebook, width=400, height=280)
frame_cliente.pack(fill='both', expand=True)
notebook.add(frame_cliente, text='Adicionar Cliente')

tk.Label(frame_cliente, text="Nome do Cliente").pack(pady=10)
nome_cliente_entry = tk.Entry(frame_cliente, width=30)
nome_cliente_entry.pack(pady=5)
tk.Button(frame_cliente, text="Adicionar Cliente", command=lambda: adicionar_cliente_interface(nome_cliente_entry)).pack(pady=10)

# Aba de adicionar barbeiro
frame_barbeiro = ttk.Frame(notebook, width=400, height=280)
frame_barbeiro.pack(fill='both', expand=True)
notebook.add(frame_barbeiro, text='Adicionar Barbeiro')

tk.Label(frame_barbeiro, text="Nome do Barbeiro").pack(pady=10)
nome_barbeiro_entry = tk.Entry(frame_barbeiro, width=30)
nome_barbeiro_entry.pack(pady=5)
tk.Button(frame_barbeiro, text="Adicionar Barbeiro", command=lambda: adicionar_barbeiro_interface(nome_barbeiro_entry)).pack(pady=10)

# Aba de listar clientes
frame_listar_clientes = ttk.Frame(notebook, width=400, height=280)
frame_listar_clientes.pack(fill='both', expand=True)
notebook.add(frame_listar_clientes, text='Listar Clientes')

tree_clientes = ttk.Treeview(frame_listar_clientes, columns=('ID', 'Nome'), show='headings')
tree_clientes.heading('ID', text='ID')
tree_clientes.heading('Nome', text='Nome')
tree_clientes.pack(pady=20)

tk.Button(frame_listar_clientes, text="Listar Clientes", command=lambda: listar_clientes_interface(tree_clientes)).pack(pady=10)

# Aba de buscar cliente por nome
frame_buscar_cliente = ttk.Frame(notebook, width=400, height=280)
frame_buscar_cliente.pack(fill='both', expand=True)
notebook.add(frame_buscar_cliente, text='Buscar Cliente')

tk.Label(frame_buscar_cliente, text="Nome do Cliente").pack(pady=10)
nome_busca_entry = tk.Entry(frame_buscar_cliente, width=30)
nome_busca_entry.pack(pady=5)
tk.Button(frame_buscar_cliente, text="Buscar Cliente", command=lambda: buscar_cliente_interface(nome_busca_entry, tree_clientes)).pack(pady=10)

# Aba de visualização de lucros
frame_lucros = ttk.Frame(notebook, width=400, height=280)
frame_lucros.pack(fill='both', expand=True)
notebook.add(frame_lucros, text='Lucros do Mês')

tk.Label(frame_lucros, text="Mês (MM)").pack(pady=5)
mes_lucro_entry = tk.Entry(frame_lucros, width=30)
mes_lucro_entry.pack(pady=5)

tk.Label(frame_lucros, text="Ano (AAAA)").pack(pady=5)
ano_lucro_entry = tk.Entry(frame_lucros, width=30)
ano_lucro_entry.pack(pady=5)

tree_lucros = ttk.Treeview(frame_lucros, columns=('Barbeiro', 'Lucro'), show='headings')
tree_lucros.heading('Barbeiro', text='Barbeiro')
tree_lucros.heading('Lucro', text='Lucro')
tree_lucros.pack(pady=20)

tk.Button(frame_lucros, text="Ver Lucros", command=lambda: ver_lucros_interface(mes_lucro_entry, ano_lucro_entry, tree_lucros)).pack(pady=10)


def ver_lucros_interface(mes_entry, ano_entry, tree):
    mes = int(mes_entry.get())
    ano = int(ano_entry.get())
    lucros = calcular_lucro_mensal(mes, ano)

    for row in tree.get_children():
        tree.delete(row)

    for lucro in lucros:
        tree.insert('', 'end', values=lucro)


# Aba de listar agendamentos
frame_listar_agendamentos = ttk.Frame(notebook, width=400, height=280)
frame_listar_agendamentos.pack(fill='both', expand=True)
notebook.add(frame_listar_agendamentos, text='Listar Agendamentos')

tree_agendamentos = ttk.Treeview(frame_listar_agendamentos, columns=('ID', 'Cliente', 'Barbeiro', 'Data', 'Horário', 'Serviço'), show='headings')
tree_agendamentos.heading('ID', text='ID')
tree_agendamentos.heading('Cliente', text='Cliente')
tree_agendamentos.heading('Barbeiro', text='Barbeiro')
tree_agendamentos.heading('Data', text='Data')
tree_agendamentos.heading('Horário', text='Horário')
tree_agendamentos.heading('Serviço', text='Serviço')
tree_agendamentos.pack(pady=20)

tk.Button(frame_listar_agendamentos, text="Listar Agendamentos", command=lambda: listar_agendamentos_interface(tree_agendamentos)).pack(pady=10)

# Aba de marcar agendamento
frame_agendamento = ttk.Frame(notebook, width=400, height=280)
frame_agendamento.pack(fill='both', expand=True)
notebook.add(frame_agendamento, text='Marcar Agendamento')

tk.Label(frame_agendamento, text="ID do Cliente").pack(pady=5)
cliente_id_entry = tk.Entry(frame_agendamento, width=30)
cliente_id_entry.pack(pady=5)

tk.Label(frame_agendamento, text="ID do Barbeiro").pack(pady=5)
barbeiro_id_entry = tk.Entry(frame_agendamento, width=30)
barbeiro_id_entry.pack(pady=5)

tk.Label(frame_agendamento, text="Data (DD/MM/AAAA)").pack(pady=5)
data_entry = tk.Entry(frame_agendamento, width=30)
data_entry.pack(pady=5)

tk.Label(frame_agendamento, text="Horário (HH:MM)").pack(pady=5)
horario_entry = tk.Entry(frame_agendamento, width=30)
horario_entry.pack(pady=5)

tk.Label(frame_agendamento, text="Serviço (cabelo, barba, cabelo e barba)").pack(pady=5)
servico_entry = tk.Entry(frame_agendamento, width=30)
servico_entry.pack(pady=5)

tk.Label(frame_agendamento, text="Valor do Serviço (R$)").pack(pady=5)
valor_entry = tk.Entry(frame_agendamento, width=30)
valor_entry.pack(pady=5)

tk.Button(frame_agendamento, text="Marcar Agendamento", command=lambda: marcar_agendamento_interface(cliente_id_entry, barbeiro_id_entry, data_entry, horario_entry, servico_entry, valor_entry)).pack(pady=10)


root.mainloop()
