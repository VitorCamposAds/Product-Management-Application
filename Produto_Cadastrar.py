#Importa o Módulo para a conexão com o BD
import pyodbc

#Importa o módulo para interface gráfica
from tkinter import *

#Importa classes ttk do módulo tkinter
from tkinter import ttk

#Função que verifica se login e senha estão corretos
def verifica_credenciais():
    # Drive - drive
    # Server - servidor
    # Database - nome do banco de dados
    conexao = pyodbc.connect("Driver={SQLite3 ODBC Driver};Server=localhost;Database=Projeto_Compras.db")

    # Responsável por executar os códigos SQL
    cursor = conexao.cursor()

    # Query para selecionar usuários que possuem o nome de usuários e senhas inseridos pelo mesmo
    cursor.execute("SELECT * FROM Usuários WHERE Nome = ? AND Senha = ?", (nome_usuario_entry.get(), senha_usuario_entry.get()))

    usuario = cursor.fetchone()

    if usuario:
        # Fechar janela de login caso o usuário exista no BD (senha e usuário corretos)
        janela_principal.destroy()

        # Conexão com o banco de dados
        dadosConexao = ("Driver={SQLite3 ODBC Driver};Server=localhost;Database=Projeto_Compras.db")

        conexao = pyodbc.connect(dadosConexao)

        # Cria objeto cursor para executar comandos SQL no banco de dados
        cursor = conexao.cursor()

        # Seleciona a tabela de Produtos
        conexao.execute("SELECT * FROM Produtos")

        print("Conectado com sucesso!")

        def listar_dados():
            # Limpa os valores da treeview
            for i in treeview.get_children():
                treeview.delete(i)

            # Seleciona a tabela de Produtos
            cursor.execute("SELECT * FROM Produtos")

            # Armazena os valores retornados pelo comando SQL em uma variável
            valores = cursor.fetchall()

            # Adiciona os valores na treeview
            for valor in valores:
                # Popula linha por linha
                treeview.insert("", "end", values=(valor[0], valor[1], valor[2], valor[3]))


        # Cria uma janela tkinter para cadastro de produtos
        janela = Tk()
        janela.title("Cadastro de Produtos")
        janela.configure(bg="#D3D3D3")
        janela.attributes("-fullscreen", True)

        Label(janela, text="Nome do Produto: ", font=("Arial", 12, "bold"), bg="#F5F5F5").grid(row=0, column=2, padx=10, pady=10)
        nome_produto = Entry(janela, font="Arial 14")
        nome_produto.grid(row=0, column=3, padx=10, pady=10)

        Label(janela, text="Descrição do Produto: ", font=("Arial", 12, "bold"), bg="#F5F5F5").grid(row=0, column=5, padx=10, pady=10)
        descricao_produto = Entry(janela, font="Arial 14")
        descricao_produto.grid(row=0, column=6, padx=10, pady=10)

        Label(janela, text="Produtos", font="Arial 12", fg="blue", bg="#F5F5F5").grid(row=2, column=0, columnspan=10, padx=10, pady=10)

        # Função de cadastro do produto
        def cadastrar():

            def salvar_dados():
                # Obtém os valores inseridos nos campos de entrada
                novo_produto_cadastrar = (nome_produto_cadastrar.get(), descricao_produto_cadastrar.get(), preco_produto_cadastrar.get())

                # Executa um comando SQL para inserir os valores na tabela Produtos
                cursor.execute("INSERT INTO Produtos (NomeProduto, Descricao, Preco) VALUES (?, ?, ?)", novo_produto_cadastrar)

                # Realiza o commit da transação para salvar as alterações no banco de dados
                conexao.commit()
                print("Dados Cadastrados com sucesso!")

                # Fecha a janela de cadastro
                janela_cadastrar.destroy()

                #Chama a função para listar o BD
                listar_dados()


            # Cria uma nova janela para o cadastro de produtos
            janela_cadastrar = Toplevel(janela)
            janela_cadastrar.title("Cadastrar Produto")
            janela_cadastrar.configure(bg="#FFFFFF")

            # Define as dimensões e posição da janela de cadastro
            largura_janela = 400
            altura_janela = 225
            largura_tela = janela_cadastrar.winfo_screenwidth()
            altura_tela = janela_cadastrar.winfo_screenheight()  # Corrigido para obter a altura correta da tela
            pos_x = (largura_tela // 2) - (largura_janela // 2)
            pos_y = (altura_tela // 2) - (altura_janela // 2)  # Corrigido para calcular a posição y correta
            janela_cadastrar.geometry('{}x{}+{}+{}'.format(largura_janela, altura_janela, pos_x, pos_y))

            for i in range(5):
                janela_cadastrar.grid_rowconfigure(i, weight=1)

            #Aqui se faz o mesmo que o comentário acima, porém para as colunas.
            for i in range(5):
                janela_cadastrar.grid_columnconfigure(i, weight=1)

            estilo_borda = {"borderwidth": 2, "relief": "groove"}

            # Criação dos rótulos e campos de entrada na janela de cadastro
            Label(janela_cadastrar, text="Nome do Produto:", font=("Arial", 12), bg="#FFFFFF").grid(row=0, column=0, padx=10, pady=10, sticky="W")
            nome_produto_cadastrar = Entry(janela_cadastrar, font=("Arial", 12), **estilo_borda)
            nome_produto_cadastrar.grid(row=0, column=1, padx=10, pady=10)

            Label(janela_cadastrar, text="Descrição do Produto:", font=("Arial", 12), bg="#FFFFFF").grid(row=1, column=0, padx=10, pady=10, sticky="W")
            descricao_produto_cadastrar = Entry(janela_cadastrar, font=("Arial", 12), **estilo_borda)
            descricao_produto_cadastrar.grid(row=1, column=1, padx=10, pady=10)

            Label(janela_cadastrar, text="Preço do Produto:", font=("Arial", 12), bg="#FFFFFF").grid(row=2, column=0, padx=10, pady=10, sticky="W")
            preco_produto_cadastrar = Entry(janela_cadastrar, font=("Arial", 12), **estilo_borda)
            preco_produto_cadastrar.grid(row=2, column=1, padx=10, pady=10)

            botao_salvar_dados = Button(janela_cadastrar, text="Salvar", font=("Arial", 12), command=salvar_dados)
            botao_salvar_dados.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="NSEW")

            botao_cancelar = Button(janela_cadastrar, text="Cancelar", font=("Arial", 12), command=janela_cadastrar.destroy)
            botao_cancelar.grid(row=4, column=0, columnspan=2, padx=10, pady=10, stick="NSEW")

        #Cria Botão para gravar os dados na tabela Produtos do BD
        botao_gravar = Button(janela, text="Novo", command=cadastrar, font="Arial 12")
        botao_gravar.grid(row=4, column=0, columnspan=4, stick="NSEW", padx=80, pady=1)



        #Define o estilo da treeview
        style = ttk.Style(janela)


        # Cria a treeview
        treeview = ttk.Treeview(janela, style="mystyle.Treeview")

        style.theme_use("default")

        style.configure("mystyle.Treeview", font=("Arial", 12))

        treeview = ttk.Treeview(janela, style="mystyle.Treeview", columns=("ID", "NomeProduto", "Descricao", "Preco"), show="headings", height=20)

        treeview.heading("ID", text="ID")
        treeview.heading("NomeProduto", text="Nome do Produto")
        treeview.heading("Descricao", text="Descrição do Produto")
        treeview.heading("Preco", text="Preço do Produto")

        #A primeira coluna identificada como "#0"
        #A opção "strech=NO" indica que a coluna não deve esticar para preencher o espaço.
        treeview.column("#0", width=0, stretch=NO) #coluna invisível
        treeview.column("ID", width=100)
        treeview.column("NomeProduto", width=300)
        treeview.column("Descricao", width=400)
        treeview.column("Preco", width=180)

        treeview.grid(row=3, column=0, columnspan=10, stick="NSEW")

        #Chama a função para listar o BD
        listar_dados()

        def editar_dados(event):

            #Obtém o item selecionado na treeview
            item_selecionado = treeview.selection()[0]

            valores_selecionados = treeview.item(item_selecionado)['values']

             # Cria uma nova janela para o cadastro de produtos
            janela_edicao = Toplevel(janela)
            janela_edicao.title("Editar Produto")
            janela_edicao.configure(bg="#FFFFFF")

            # Define as dimensões e posição da janela de cadastro
            largura_janela = 500
            altura_janela = 200
            largura_tela = janela_edicao.winfo_screenwidth()
            altura_tela = janela_edicao.winfo_screenheight()  # Corrigido para obter a altura correta da tela
            pos_x = (largura_tela // 2) - (largura_janela // 2)
            pos_y = (altura_tela // 2) - (altura_janela // 2)  # Corrigido para calcular a posição y correta
            janela_edicao.geometry('{}x{}+{}+{}'.format(largura_janela, altura_janela, pos_x, pos_y))

            for i in range(5):
                janela_edicao.grid_rowconfigure(i, weight=1)

            #Aqui se faz o mesmo que o comentário acima, porém para as colunas.
            for i in range(2):
                janela_edicao.grid_columnconfigure(i, weight=1)

            estilo_borda = {"borderwidth": 2, "relief": "groove"}

            # Criação dos rótulos e campos de entrada na janela de cadastro
            Label(janela_edicao, text="Nome do Produto:", font=("Arial", 12), bg="#FFFFFF").grid(row=0, column=0, padx=10, pady=10, sticky="W")
            nome_produto_edicao = Entry(janela_edicao, font=("Arial", 12), **estilo_borda, bg="#FFFFFF", textvariable=StringVar(value=valores_selecionados[1]))
            nome_produto_edicao.grid(row=0, column=1, padx=10, pady=10)

            Label(janela_edicao, text="Descrição do Produto:", font=("Arial", 12), bg="#FFFFFF").grid(row=1, column=0, padx=10, pady=10, sticky="W")
            descricao_produto_edicao = Entry(janela_edicao, font=("Arial", 12), **estilo_borda, bg="#FFFFFF", textvariable=StringVar(value=valores_selecionados[2]))
            descricao_produto_edicao.grid(row=1, column=1, padx=10, pady=10)

            Label(janela_edicao, text="Preço do Produto:", font=("Arial", 12), bg="#FFFFFF").grid(row=2, column=0, padx=10, pady=10, sticky="W")
            preco_produto_edicao = Entry(janela_edicao, font=("Arial", 12), **estilo_borda, bg="#FFFFFF", textvariable=StringVar(value=valores_selecionados[3]))
            preco_produto_edicao.grid(row=2, column=1, padx=10, pady=10)


            def salvar_edicao():

                # Obtém os novos valores do item selecionado na treeview
                novo_produto = nome_produto_edicao.get()
                nova_descricao = descricao_produto_edicao.get()
                novo_preco = preco_produto_edicao.get()

                # Atualiza os valores do item selecionado
                valores_selecionados[1] = novo_produto
                valores_selecionados[2] = nova_descricao
                valores_selecionados[3] = novo_preco
                treeview.item(item_selecionado, values=valores_selecionados)

                # Executa um comando SQL para atualizar os valores na tabela Produtos
                cursor.execute("UPDATE Produtos SET NomeProduto = ?, Descricao = ?, Preco = ? WHERE ID = ?", (novo_produto, nova_descricao, novo_preco, valores_selecionados[0]))

                # Realiza o commit da transação para salvar as alterações no banco de dados
                conexao.commit()
                print("Dados alterados com sucesso!")

                # Fecha a janela de cadastro
                janela_edicao.destroy()

                # Chama a função para listar o BD
                listar_dados()

            def deletar_registro():

                #Recupera o id do registro selecionado na treeview
                selected_item = treeview.selection()[0]
                id = treeview.item(selected_item)['values'][0]

                #Deleta o registro do BD
                cursor.execute("DELETE FROM PRODUTOS WHERE id = ?", (id,))

                conexao.commit()

                #Fecha a janela de edição
                janela_edicao.destroy()

                #Recarregar os dados sem o novo registro
                listar_dados()




            botao_salvar_edicao = Button(janela_edicao, text="Alterar", font=("Arial", 12), bg="#008000", fg="#FFFFFF", command=salvar_edicao)
            botao_salvar_edicao.grid(row=4, column=0, padx=20, pady=20)

            botao_deletar_edicao = Button(janela_edicao, text="Deletar", font=("Arial", 12), bg="#FF0000", fg="#FFFFFF", command=deletar_registro)
            botao_deletar_edicao.grid(row=4, column=1, padx=20, pady=20)


        #Chama a função editar dados ao dar duplo clique na treeview
        treeview.bind("<Double-1>", editar_dados)


        menu_barra = Menu(janela)
        janela.configure(menu=menu_barra)

        menu_arquivo = Menu(menu_barra, tearoff=0)
        menu_barra.add_cascade(label="Arquivo", menu=menu_arquivo)

        menu_arquivo.add_command(label="Cadastrar", command=cadastrar)
        menu_arquivo.add_command(label="Sair", command=janela.destroy)



        ''' Concatena a string 'sql' com a cláusula SQL "WHERE NomeProduto LIKE ?". Essa cláusula é usada para filtrar
        resultados de uma consulta de BD com base em um padrão de correspondência de texto, representado pelo carctere
        coringa "?" na cláusula "LIKE". Em resumo, esta linha está adicionando uma condição de filtro à consulta SQL
        para buscar registros que tenham o campo 'nome_produto' correspondente ao padrão especificado.'''


        def limparDados():

            #Limpando os valores(dados) da treeview
            for linha in treeview.get_children():

                #Deleta linha por linha da treeview
                treeview.delete(linha)

        def filtrar_dados(nome_produto, descricao_produto):

            #Verifica se os campos estão vazios
            if not nome_produto.get() and not descricao_produto.get():

                listar_dados()

                #Se os campos estiverem vazios, não faz nada
                return

            sql = "SELECT * FROM Produtos"

            params = []

            '''Associa um evento que libera a tecla "KeyRelease", ao widget de entrada de texto
        chamado nome_produto. Quando o evento de liberação de tecla ocorrer, a função lambda
        definida será executada. Essa função lambda recebe um objeto de evento (geralmente abreviado com 'e')
        como seu argumento e chama uma outra função chamada "filtrar_dados". A função "filtrar_dados" é passada
        como argumento aos widgets "nome_produto" e "descricao_produto". O objetivo dessa linha de código é permitir ao
        usuário que filtre os dados mostrados no programa com base no que foi digitadono campo "nome_produto". Quando
        o usuário digita algo no campo "nome_produo" e solta a tecla, a função "filtrar_dados" é chamada para atualizar
        a exibição dos dados de acordo com o que foi digitado.'''

            if nome_produto.get():

                '''Adiciona um parâmetro à lista params. Esse parâmetro é uma string composta por 3 partes concatenadas:
                1 - O caractere coringa '%' no início da string, que representa qualquer número de (ou nenhum) antes do padrão
                de correspondência de texto.
                2-O valor do campo 'nome_produto' (obtido com o método 'get()' do widget de entrada de texto correspondente).
                3-Outro caractere coringa "%" no final da string, que representa qualquer número de caracteres (ou nenhum)
                depois do padrão de correspondência de texto. Essa string será usada como o valor do parâmetro da clausula 'LIKE'
                da consulta SQL, permitindo que a consulta retorne registros que tenham o campo 'NomeProduto' correspondente
                ao padrão especificado pelo usuário na interface do programa. Em resumo essa linha de código está criando um
                parâmetro de consulta dinamicamente com base no texto digitado pelo usuário e adicionando-o à lista de
                parâmetros que serão usados na consulta SQL.
                '''
                sql += " WHERE NomeProduto LIKE ?"
                params.append('%' + nome_produto.get() + '%')

            '''Verifica se o campo de entrada de texto 'descricao_produto' tem alguma valor preenchido. Caso tenha,
            ele adiciona uma cláusula SQL adicional à consulta em andamento para filtrar os resultados com base
            em um padrão de correspondência de texto na coluna 'Descricao'. Se o campo 'nome_produto' também tiver
            um valor preenchido, é adicionada uma cláusula 'AND' para juntar as duas condições de filtro. Caso contrário,
            é adicionada a cláusula 'WHERE' para começar a filtrar diretamente pela coluna 'Descricao'. A linha params.append,
            cria um parâmetro de consulta dinamicamente com base no texto digitado pelo usuário no campo 'descricao_produto'
            permitindo que o usuário filtre os resultados com base em dois campos diferentes ('NomeProduto' e 'Descricao') ao
            mesmo tempo, caso estejam preenchidos'''


            if descricao_produto.get():

                if nome_produto.get():
                    sql += " AND"
                else:
                    sql += " WHERE"

                sql += " Descricao LIKE ?"
                params.append('%' + descricao_produto.get() + '%')

            cursor.execute(sql, tuple(params))
            produtos = cursor.fetchall()

            #Lipa os dados da treeview
            limparDados()

            #Preenche treeview com os dados filtrados
            for dado in produtos:

                treeview.insert('', 'end', values=(dado[0], dado[1], dado[2], dado[3]))

        nome_produto.bind("<KeyRelease>", lambda e: filtrar_dados(nome_produto, descricao_produto))
        descricao_produto.bind("<KeyRelease>", lambda e: filtrar_dados(nome_produto, descricao_produto))

        #Deleta o registro
        def deletar():

            #Recupera o id do registro selecionado na treeview
            selected_item = treeview.selection()[0]
            id = treeview.item(selected_item)['values'][0]

            #Deleta o registro do BD
            cursor.execute("DELETE FROM PRODUTOS WHERE id = ?", (id,))

            conexao.commit()

            #Recarregar os dados sem o novo registro
            listar_dados()

        #Cria Botão para gravar os dados na tabela Produtos do BD
        botao_deletar = Button(janela, text="Deletar", command=deletar, font="Arial 12")
        botao_deletar.grid(row=4, column=4, columnspan=4, stick="NSEW", padx=80, pady=1)


        janela.mainloop()

        # Fecha o cursor e a conexão com o banco de dados
        cursor.close()
        conexao.close()
        
    else:
        mensagem_lbl = Label(janela_principal, text="Nome de usuário ou senha incorretos", fg="red")
        mensagem_lbl.grid(row=3, column=0, columnspan=2)        
    
#Criando a tela principal para a tela de login
janela_principal = Tk()
janela_principal.title("Tela de Login")


#bg = background plano de fundo
janela_principal.configure(bg="#F5F5F5")

#Define altura e largura da janela(ficam fixas)
largura_janela = 450
altura_janela = 300

#Obtém a largura e altura da tela do computador
largura_tela = janela_principal.winfo_screenwidth()
altura_tela = janela_principal.winfo_screenwidth()


''' Essas linhas calculam a posição em que a janela deve ser exibida
centralizada na tela do computador. A posição x é definida pela
diferença entre a largura da tela e a largura da janela, dividida por 2
Já a posição y é definida pela diferença entre a altura da tela e a altura da janela,
também dividia por 2 '''

#Calcula a posição da janela para centralizá-la na tela
pos_x = (largura_tela // 2) - (largura_janela // 2)
pos_y = (largura_tela // 2) - (largura_janela // 2)

'''define a geometria da janela principal, especificando a largura e a altura da janela,
bem como a posição onde a janela será exibida na tela, usando as variáveis previamente definidas
para a posição x e y da janela. O formato utilizado é uma string que contém os valores da largura,
altura, posição x e posição y da janela separados por "x" e "+" e passados como argumentospara o
método geometry() da janela principal.

O formato  {}x{}+{}+{}' é uma string de formatação que espera quatro valores, que correspondem
à largura da janela, altura da janela, posição x da janela e posição y da janela, respectivamente.

Esses valores são passados na ordem especificada para a string de formatação e, em seguida,
são utilizados para definir a geometria da janela através do método geometry() do objeto
janela_principal'''

#Define a posição da janela
janela_principal.geometry('{}x{}+{}+{}'.format(largura_janela, altura_janela, pos_x, pos_y))

#Configurações de cor da letra (fg - foreground), fonte e texto
titulo_lbl = Label(janela_principal, text="Tela de Login", font="Arial 20", fg="blue", bg="#F5F5F5")
#Método que divide como se fosse uma tabela em partes
#row(linhas) - column(coluna), columnspan (quantas colunas vai ocupar no grid), pady (espaço quevai ocupar)
titulo_lbl.grid(row=0, column=0, columnspan=2, pady=20)


#Campo Label
nome_usuario_lbl = Label(janela_principal, text="Senha", font="Arial 14 bold", bg="#F5F5F5")
nome_usuario_lbl.grid(row=2, column=0, stick="e")#NSEW

#Campo Label
senha_usuario_lbl = Label(janela_principal, text="Nome de Usuário", font="Arial 14 bold", bg="#F5F5F5")
senha_usuario_lbl.grid(row=1, column=0, stick="e")#NSEW


#Criando um entry para o campo usuário
nome_usuario_entry = Entry(janela_principal, font="Arial 14")
nome_usuario_entry.grid(row=1, column=1, pady=10)


#Criando um entry para o campo usuário
senha_usuario_entry = Entry(janela_principal, show="*", font="Arial 14")
senha_usuario_entry.grid(row=2, column=1, pady=10)

#Stick preenche as laterais -NSEW (North, South, East, West)
entrar_btn = Button(janela_principal, text="Entrar", font="Arial 14", command=verifica_credenciais)
entrar_btn.grid(row=4, column=0, columnspan=2, padx=20, pady=10, stick="NSEW")

#Stick preenche as laterais -NSEW (North, South, East, West)
sair_btn = Button(janela_principal, text="Sair", font="Arial 14", command=janela_principal.destroy)
sair_btn.grid(row=5, column=0, columnspan=2, padx=20, pady=10, stick="NSEW")

''' Laço for que executa 5 vezes e serve para configurar o comportamento de uma grade (ou grid)
no tkinter. A função grid_rowconfigure() permite definir a configuração de uma determinada linha na
grade, com dois parâmetros: o índice da linha e um peso (weight) que determina como essa linha
deve se comportar em relação às outras linhas da grade. No código em questão, o laço for está
configurando as 5 linhas da grade da janela_principal com um peso igual a 1. Isso significa que
todas as linhas terão a mesma altura e que a altura da janela será dividida igualmente entre elas.
'''
for i in range(5):
    janela_principal.grid_rowconfigure(i, weight=1)
       
#Aqui se faz o mesmo que o comentário acima, porém para as colunas.
for i in range(5):
    janela_principal.grid_columnconfigure(i, weight=1)
    
#inicia a janela do tkinter
janela_principal.mainloop()
