from PyQt5 import uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas
#fazendo conexão entre o código e o banco de dados
banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_covid"
)
numero_id = 0  

#função que recebe os inputs e envia ao banco de dados
def funcao_principal():
    nome = formulario.lineEdit.text()
    endereco = formulario.lineEdit_2.text()
    email = formulario.lineEdit_3.text()
    telefone = formulario.lineEdit_4.text()
    cpf = formulario.lineEdit_5.text()
    categoria = ""
    
    #validando  os campos do formulário
    if formulario.checkBox_2.isChecked():
        print('Não pode cadastrar')
        categoria = "Outra cidade"
    elif formulario.checkBox_3.isChecked() and formulario.checkBox.isChecked():
        print("Pode se cadastar")
        categoria = "Alto Risco"
    elif formulario.checkBox.isChecked() and formulario.checkBox_4.isChecked() and formulario.checkBox_5.isChecked():
        print('Não pode se cadastrar')
        categoria = "Baixo Risco"
    elif formulario.checkBox_6.isChecked():
        print("Pode se cadastrar")
        categoria =  "Alto Risco"

    print('Nome:', nome)
    print('Endereço:', endereco)
    print('E-mail:', email)
    print('Telefone:', telefone)
    print('CPF:', cpf)
    print(categoria)

    #ENVIANDO AO BANCO DE DADOS
    cursor =banco.cursor()
    comando_SQL = "INSERT INTO formulario (nome,endereco,email,telefone,cpf,categoria) VALUES (%s,%s,%s,%s,%s,%s)"
    dados = (str(nome), str(endereco), str(email), str(telefone), str(cpf) ,categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit() 

    #VALIDANDO SE PODE SE CADASTRAR OU NÃO
    if categoria == "Baixo Risco":
        segunda_tela.show()
        segunda_tela.pushButton.clicked.connect(segunda_tela.close)
    elif categoria == "Alto Risco":
        aviso_tela.show()
        aviso_tela.pushButton.clicked.connect(aviso_tela.close)
   
    #limpando o formulário
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")
    formulario.lineEdit_4.setText("")
    formulario.lineEdit_5.setText("")




def salvar_dados():
    global numero_id

    # pegado os valores digitados
    nome = editar_tela.lineEdit_2.text()
    endereco = editar_tela.lineEdit_3.text()
    email= editar_tela.lineEdit_4.text()
    cpf = editar_tela.lineEdit_5.text()
    telefone = editar_tela.lineEdit_6.text()
    categoria = editar_tela.lineEdit_7.text()

    #atualizando os valores no banco de dados
    cursor = banco.cursor()
    cursor.execute("UPDATE formulario SET nome = '{}', endereco = '{}', email = '{}', cpf = '{}', telefone = '{}', categoria = '{}' WHERE id = {}".format(nome,endereco,email,cpf,telefone,categoria,numero_id))
    #atualizando os dados na janela
    editar_tela.close()
    lista_tela.close()
    funcao_lista()


#exclui os dados da lista e do banco de dados
def excluir_dados():
    id_linha = lista_tela.tableWidget.currentRow()
    lista_tela.tableWidget.removeRow(id_linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM formulario")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[id_linha][0]
    cursor.execute("DELETE FROM formulario WHERE id="+ str(valor_id))

#edita os dados da lista e do banco de dados
def editar_dados():
    global numero_id
    id_linha = lista_tela.tableWidget.currentRow()  

    #seleciona os itens do banco de dados e recebe pela matriz e edita
    cursor= banco.cursor()
    cursor.execute("SELECT id FROM formulario")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[id_linha][0]
    cursor.execute("SELECT * FROM formulario WHERE id="+ str(valor_id))
    editar = cursor.fetchall()
    editar_tela.show()
    numero_id = valor_id

    editar_tela.lineEdit.setText(str(editar[0][0]))
    editar_tela.lineEdit_2.setText(str(editar[0][1]))
    editar_tela.lineEdit_3.setText(str(editar[0][2]))
    editar_tela.lineEdit_4.setText(str(editar[0][3]))
    editar_tela.lineEdit_5.setText(str(editar[0][4]))
    editar_tela.lineEdit_6.setText(str(editar[0][5]))
    editar_tela.lineEdit_7.setText(str(editar[0][6]))
   




#função pra  gerar um pdf da tabela
def gerar_pdf():

    cursor =banco.cursor()
    comando_SQL = "SELECT * FROM formulario"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y=0
    pdf = canvas.Canvas("Cadastro_covid.pdf")
    pdf.setFont("Times-Bold",15)
    pdf.drawString(200, 800, "Pessoas Cadastradas:")
    pdf.setFont("Times-Italic",10)
    
    #posição dos itens da tabela
    pdf.drawString(10,  750, "ID")
    pdf.drawString(50, 750, "NOME")
    pdf.drawString(150, 750, "ENDEREÇO")
    pdf.drawString(250, 750, "EMAIL")
    pdf.drawString(350, 750, "CPF")
    pdf.drawString(440, 750, "TELEFONE:")
    pdf.drawString(520, 750, "CATEGORIA")

    for linha in range(0, len(dados_lidos)):
        y += 20
        pdf.drawString(10,  750 - y, str(dados_lidos[linha][0]))
        pdf.drawString(50,  750 - y, str(dados_lidos[linha][1]))
        pdf.drawString(150, 750 - y, str(dados_lidos[linha][2]))
        pdf.drawString(250, 750 - y, str(dados_lidos[linha][3]))
        pdf.drawString(350, 750 - y, str(dados_lidos[linha][4]))
        pdf.drawString(440, 750 - y, str(dados_lidos[linha][5]))
        pdf.drawString(520, 750 - y, str(dados_lidos[linha][6]))
    
    pdf.save()
    print("PDF FOI GERADO COM SUCESSO")


#função pra mostrar a tela de login
def funcao_login():
    login_tela.show()
   
       





#função pra mostrar os dados da tabela
def funcao_lista():
    lista_tela.show()

    cursor =banco.cursor()
    comando_SQL = "SELECT * FROM formulario"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()


    lista_tela.tableWidget.setRowCount(len(dados_lidos))
    lista_tela.tableWidget.setColumnCount(7)

    #porcorrendo por toda tabela
    for linha in range(0, len(dados_lidos)):
        for coluna in range(0, 7):
            lista_tela.tableWidget.setItem(linha,coluna,QtWidgets.QTableWidgetItem(str(dados_lidos[linha][coluna])))



# criando variaveis com os aquivos do PYQT5
app=QtWidgets.QApplication([])
formulario=uic.loadUi("formulario.ui")
segunda_tela=uic.loadUi("segunda.ui")
aviso_tela=uic.loadUi("aviso.ui")
login_tela=uic.loadUi("login.ui")
lista_tela=uic.loadUi("lista.ui")
editar_tela=uic.loadUi("editar.ui")
#ENVIANDO AS AÇÕES DOS BOTÕES PARA AS FUNÇÕES
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(funcao_login)
login_tela.pushButton.clicked.connect(funcao_lista)
lista_tela.pushButton.clicked.connect(gerar_pdf)
lista_tela.pushButton_2.clicked.connect(excluir_dados)
lista_tela.pushButton_3.clicked.connect(editar_dados)
editar_tela.pushButton.clicked.connect(salvar_dados)
formulario.show()
app.exec()


#@JONATHAN REIS !

"""  #criando a tabela

create table formulario (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100),
    endereco VARCHAR(100),
    email VARCHAR(100),
    telefone INT NOT NULL,
    cpf INT NOT NULL,
    categoria VARCHAR(30),
    PRIMARY KEY (id)

);

# Inserindo registros na tabela
INSERT INTO formulario (nome,endereco,email,telefone,cpf,categoria) VALUES ("Jonathan","rua 13","jonathan@123", 55555-5555, 4201-6585-5522,"Baixo Risco");  """