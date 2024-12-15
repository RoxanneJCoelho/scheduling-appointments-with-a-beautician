# MARCAÇÃO DE ESTÉTICA
# NOME: Roxanne Coelho

import sqlite3 
from datetime import datetime
import LOG

# Primeiro, cria-se a base de dados da estética
# Função para conectar á base de dados
def criar_conexao():
    return sqlite3.connect('estetica.db')

# Função para criar as tabelas
def criar_tabelas():
    with criar_conexao() as conexao:
        execucao = conexao.cursor()

        # Cria a tabela Cliente
        execucao.execute(''' 
            CREATE TABLE IF NOT EXISTS Cliente (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                sobrenome TEXT NOT NULL,
                email TEXT NOT NULL,
                telemovel TEXT,
                localidade TEXT,
                estado TEXT CHECK(estado IN ('ativo', 'inativo')) DEFAULT 'ativo'
            )
        ''')

        # Cria a tabela Servicos
        execucao.execute('''
            CREATE TABLE IF NOT EXISTS Servicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL
            )
        ''')

        # Cria a tabela Marcacoes
        execucao.execute('''
            CREATE TABLE IF NOT EXISTS Marcacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_servico INTEGER NOT NULL,
                id_cliente INTEGER NOT NULL,
                data TEXT NOT NULL,
                hora TEXT NOT NULL,
                estado TEXT CHECK(estado IN ('agendado', 'cancelado')) DEFAULT 'agendado',
                FOREIGN KEY (id_servico) REFERENCES Servicos(id),
                FOREIGN KEY (id_cliente) REFERENCES Cliente(id)          
            )
        ''')
        conexao.commit()  # Salva as alterações feitas
criar_tabelas()

# Segundo, cria-se as funções necessárias para o menu de registro e o menu para aceder ao espaço cliente

# Função para validar o primeiro e último nome e a localidade (garantir que este campo apenas contém letras)
def validar_texto(texto):
        return texto.isalpha()

# Função para validar o email (garantir que tenha estrutura de email)
def validar_email(email):
    if '@' and '.' in email:
        return True
    return False

# Função para verificar se o email já ta na base de dados
def email_existe(email):
    con=criar_conexao()
    cur=con.cursor().execute(f'SELECT * FROM Cliente WHERE email=\'{email}\' ;').fetchall()    
    con.close()
    if len(cur)>0:
        return True
    else:
        return False

# Função para validar o número de telemóvel (garantir que este campo apenas contém números e tenha um comprimento maior que 9 digitos)
def validar_telemovel(telemovel):
     return telemovel.isdigit() and len(telemovel)>=9

# Função para coletar os dados do cliente e criar a estrutura do menu registro
def coletar_dados():
    while True:
        print('Bem-vindo ao Menu de Registro')
        nome = input('Primeiro Nome: ').strip()
        if not validar_texto(nome): 
            print('Por favor, insira um nome válido.')
            continue
        sobrenome = input('Último Nome: ').strip()
        if not validar_texto(sobrenome):
            print('Por favor, insira um nome válido.')
            continue
        email = input('Email: ').strip()
        if not validar_email(email):
            print('Por favor, insira um email válido.')
            continue
        if email_existe(email)==True:
           print('Este email já está registrado. Tente outro email.')        
           continue
        telemovel = input('Telemóvel: ').strip()
        if not validar_telemovel(telemovel):
            print('Por favor, insira um número de telemóvel válido.')
            continue        
        localidade = input('Localidade: ').strip()
        if not validar_texto(localidade):
            print('Por favor, insira um nome de localidade válido.')
            continue

        # Verifica se todos os campos foram preenchidos
        if not nome or not sobrenome or not email or not telemovel or not localidade:
            print('Por favor, preencha todos os campos obrigatórios.')
            continue
        
        return nome, sobrenome, email, telemovel, localidade


# Função para registrar o novo cliente na base de dados
def registrar_cliente(nome, sobrenome, email, telemovel, localidade):
    with criar_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Cliente (nome, sobrenome, email, telemovel, localidade) VALUES (?, ?, ?, ?, ? )', (nome, sobrenome, email, telemovel, localidade))
        conn.commit()
        print(f'\nParabéns pelo seu registo, {nome}! Recebeu 10% de promoção na sua primeira marcação enviada para o seu email.')
        return nome

# Função para aceder ao espaço cliente através do email
def acessar_espaco_cliente():  
    while True:
        email = input('Digite o seu email para acessar ao seu espaço cliente: ').strip()
        
        # Valida o formato do email
        if not validar_email(email):
            print('Erro: Formato de email inválido. Tente novamente.')
            continue

        try:
            with criar_conexao() as conn:
                cursor1 = conn.cursor()
                cursor1.execute('SELECT id, nome FROM cliente WHERE email = ?', (email,))
                cliente = cursor1.fetchone()
                            
                if cliente:
                 print(f'\nBem-vindo/a, {cliente[1]}!')
                 espaco_cliente(cliente[0]) 
                 break
                else:
                 print('Este email não está registado.')
                 continue
        except Exception as e:
            print(f'Ocorreu um erro ao acessar a base de dados: {e}')
            LOG.registar_erro(e)
            break

# Terceiro, cria-se o espaço cliente: neste campo é possível fazer, cancelar, reagendar e ver as marcações do cliente

# Função para validar se a data e hora estão disponíveis
def horario_disponivel(data, hora):
    with criar_conexao() as conn:
        cursor2 = conn.cursor()
        cursor2.execute('SELECT * FROM marcacoes WHERE data = ? AND hora = ?', (data, hora))
        return cursor2.fetchone() is None
        
# Função para exibir o menu com os serviços e retornar o serviço escolhido
def selecionar_servico():
    servicos = {
        '1': ('Limpeza de pele', 30),
        '2': ('Manicure', 30),
        '3': ('Pedicure', 30),
        '4': ('Massagem', 60),
        '5': ('Pressoterapia', 40),
        '6': ('Campanha de Natal (leve 3 e pague 2)', 90)
    }
    print('\nEscolha um serviço:')
    for codigo, (descricao, preco) in servicos.items():
        print(f'[{codigo}] {descricao} - {preco} euros')
 
    while True:
        opcao = input('Escolha uma opção: ')
        if opcao in servicos:
            return servicos[opcao]
        else:
            print('Opção inválida. Tente novamente.')
 
# Usando as duas funções acima, esta função serve para fazer uma marcação
def fazer_marcacao(id_cliente):
    id_servico, preco = selecionar_servico()

    while True:
        data = input('Digite a data (DD/MM/AAAA): ').strip() # Validação da data
        try:
            data_formatada = datetime.strptime(data, '%d/%m/%Y').strftime('%d/%m/%Y')
        except ValueError as v:
            print('Formato de data inválido. Tente novamente.')
            LOG.registar_erro(v)
            continue

        hora = input('Digite a hora (HH:MM): ').strip() # Validação da hora
        try:
            hora_formatada = datetime.strptime(hora, '%H:%M').strftime('%H:%M')
        except ValueError as v:
            print('Formato de hora inválido. Tente novamente.')
            LOG.registar_erro(v)
            continue
        
        if not horario_disponivel(data_formatada, hora_formatada): # Validação do horário
            print('Esse horário já está preenchido, tente outro.')
            continue

        # Valida a marcação com o número de telefone
        try:
            with criar_conexao() as conn:
                cursor3 = conn.cursor()
                cursor3.execute('SELECT telemovel FROM cliente WHERE id = ?', (id_cliente,))
                telefone_cliente = cursor3.fetchone()

                if not telefone_cliente:
                    print('Cliente não encontrado na base de dados.')
                    return  # Sai da função se o cliente não existir

                telefone_cliente = telefone_cliente[0]  # Extrai o número do telemóvel do cliente

        except Exception as e:
            print(f'Ocorreu um erro ao acessar a base de dados: {e}')
            LOG.registar_erro(e)
            return  # Sai da função se houver erro no base de dados

        # Solicita o telemóvel do cliente e valida
        while True:
            telefone = input('Para validar a sua marcação, por favor, insira o seu número de telemóvel: ').strip()

            if telefone == telefone_cliente:
                # Insere a marcação na base de dados
                try:
                    with criar_conexao() as conn:
                        cursor4 = conn.cursor()
                        cursor4.execute('INSERT INTO marcacoes (id_cliente, id_servico, data, hora, estado) VALUES (?, ?, ?, ?, ?)', (id_cliente, id_servico, data_formatada, hora_formatada, "agendado"))
                        conn.commit()
                        print('Marcação realizada com sucesso!')

                        # Busca os dados da marcação feita para exibir
                        cursor4.execute('SELECT id FROM marcacoes WHERE data = ? AND hora = ? AND id_cliente = ?', (data_formatada, hora_formatada, id_cliente))
                        id_marcacao = cursor4.fetchone()[0]

                        print(f'''\nMarcação feita com sucesso!
                        Dados da marcação:
                        ID Marcação: {id_marcacao}
                        Data: {data_formatada}
                        Hora: {hora_formatada}
                        Serviço: {id_servico}
                        Preço: {preco} euros''')
                        return  # Sai completamente da função após a marcação

                except Exception as e:
                    print(f'Ocorreu um erro ao inserir a marcação na base de dados: {e}')
                    LOG.registar_erro(e)
                    return
            else:
                print('Número de telemóvel inválido. Tente novamente.')

# Função para visualizar as marcações do cliente
def ver_marcacoes(id_cliente):
    with criar_conexao() as conn:
                cursor5 = conn.cursor()
    cursor5.execute("SELECT * FROM marcacoes WHERE id_cliente = ? AND estado ='agendado'", (id_cliente,))
    marcacoes = cursor5.fetchall()
      
    if marcacoes:
        print('\nAs suas Marcações:')
        for marcacao in marcacoes:
            print(f'ID Marcação: {marcacao[0]}, Serviço: {marcacao[2]}, Data: {marcacao[3]}, Hora: {marcacao[4]}')
    else:
        print('Não foi encontrada nenhuma marcação.')
    return marcacoes
        
# Função para cancelar ou reagendar marcações
def cancelar_ou_reagendar_marcacao(id_cliente):
    sinalizador=False
    try:
        # Obtem as marcações do cliente
        marcacoes = ver_marcacoes(id_cliente)
        if not marcacoes:
            return marcacoes

        # Solicita o ID da marcação
        while True:
         if sinalizador==True:
          break
         try:
            id_marcacao = int(input('Digite o ID da marcação que deseja cancelar ou reagendar: '))

            # Encontra a marcação pelo ID
            marcacao = next((m for m in marcacoes if m[0] == id_marcacao), None)

            if marcacao:
                print(f'Selecionou a marcação: ID {marcacao[0]}, Data: {marcacao[3]}, Hora: {marcacao[4]}, Serviço: {marcacao[2]}')

                # Solicita a ação de cancelar ou reagendar
                opcao_cancelar_reagendar = input('Deseja cancelar ou reagendar? (C/R): ').strip().upper()

                with criar_conexao() as conn:
                    cursor6 = conn.cursor()

                    if opcao_cancelar_reagendar == 'C':
                        # Atualiza o estado da marcação para 'cancelado'
                        cursor6.execute("UPDATE marcacoes SET estado = 'cancelado' WHERE id = ?", (id_marcacao,))
                        conn.commit()
                        print('A sua marcação foi cancelada com sucesso.')
                        sinalizador=True

                    elif opcao_cancelar_reagendar == 'R':
                        # Solicita uma nova data e hora
                        while True:
                            nova_data = input('Digite a nova data (DD/MM/AAAA): ').strip()
                            nova_hora = input('Digite a nova hora (HH:MM): ').strip()
                            try:
                                # Valida o formato da data e hora
                                datetime.strptime(nova_data, '%d/%m/%Y')
                                datetime.strptime(nova_hora, '%H:%M')

                                # Atualiza a base de dados
                                cursor6.execute("UPDATE marcacoes SET data = ?, hora = ?, estado = 'agendado' WHERE id = ?", (nova_data, nova_hora, id_marcacao))
                                conn.commit()
                                print('A sua marcação foi reagendada com sucesso.')
                                sinalizador=True
                                break  # Sai do loop após reagendar com sucesso
                            except ValueError as v:
                                print('Data ou hora inválida. Tente novamente.')                                
                                LOG.registar_erro(v)
                    else:
                        print('Opção inválida.')                        
            else:
                print('Marcação não encontrada.') 
                               
         except ValueError as v:
            print('ID inválido. Certifique-se de inserir um número.')            
            LOG.registar_erro(v)            
    except Exception as e:
        print(f'Ocorreu um erro ao acessar a base de dados: {e}')
        LOG.registar_erro(e)
    
# Função para a estrutura do menu do espaço cliente
def espaco_cliente(id_cliente):
    
    while True:
        print('''\nEspaço Cliente
        Que operação deseja efetuar?
        [1] Fazer marcação
        [2] Cancelar/reagendar marcação
        [3] Ver as minhas marcações
        [4] Sair do espaço cliente''')

        opcao1 = input('>>>: ')

        if opcao1 == '1':
            fazer_marcacao(id_cliente)  
        elif opcao1 == '2':
            cancelar_ou_reagendar_marcacao(id_cliente)  
        elif opcao1 == '3':
            ver_marcacoes(id_cliente)  
        elif opcao1 == '4':
            print('Agradecemos a sua visita, volte sempre!')
            break
        else:
            print('Opção inválida. Tente novamente.')

# Função da página inicial da estética e criação da estrutura do programa
def main_menu():
    print('''\nBem-vindo/a à estética! Venha conhecer os nossos serviços e promoções!
          - Limpeza de pele (30 euros)
          - Manicure (30 euros)
          - Pedicure (30 euros)
          - Massagem (60 euros)
          - Pressoterapia (40 euros)
          - Campanha de Natal (leve 3 e pague 2)
          
          Quer registar-se? Introduza o número correspondente:
          [1] Sim
          [2] Não
          [3] Já tenho registro
    ''')
    
    while True:
        opcao2 = input('>>>: ')
        if opcao2 == '1':        
            nome, sobrenome, email, telefone, localidade = coletar_dados()
            registrar_cliente(nome, sobrenome, email, telefone, localidade)
            acessar_espaco_cliente()  
            break

        elif opcao2 == '2':
            # Confirmação para não se registrar
            print('Tem a certeza? Se não se registar, não poderá aceder aos nossos benefícios no espaço cliente.\n [1] Quero registar\n [2] Não quero registrar')
            opcao3 = input('>>>: ')
            
            if opcao3 == '1':
                print('Redirecionando para o menu de registro...')
                nome, sobrenome, email, telefone, localidade = coletar_dados()
                registrar_cliente(nome, sobrenome, email, telefone, localidade)
                acessar_espaco_cliente()
                break
            elif opcao3 == '2':
                print('Agradecemos a sua visita, volte sempre!')
                break
            else:
                print('Opção inválida. Por favor, escolha uma opção válida.')

        elif opcao2 == '3':
            acessar_espaco_cliente()  
            break

        else:
            print('Opção inválida. Por favor, escolha uma opção válida.')

main_menu()


            



   
