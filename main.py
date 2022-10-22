from sqlite3 import Cursor
from PyQt5 import uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

new_codigo_id = 0
#conecta o banco de dados
banco = mysql.connector.connect(
    host= "localhost",
    user= "root",
    passwd='',
    database ="cadastro_produtos"
);

def get_codigo():
    select_codigo.show()
    select_codigo.lineEdit.setText("")

def editar():
    global new_codigo_id
    #armazena o codigo do produto
    codigo_id = select_codigo.lineEdit.text()
    try:
        #realiza as alterações no banco de dados
        cursor = banco.cursor() 
        cursor.execute("SELECT * FROM produtos WHERE codigo="+ str(codigo_id))
        #retorna uma lista com tuplas 
        produto = cursor.fetchall()
        edit.lineEdit_2.setText(str(produto[0][0]))
        edit.lineEdit_3.setText(str(produto[0][1]))
        edit.lineEdit_4.setText(str(produto[0][2]))
        edit.lineEdit_5.setText(str(produto[0][3]))
        edit.lineEdit_6.setText(str(produto[0][4]))
        edit.show()
        new_codigo_id = codigo_id
        select_codigo.close()
    except:
        error_dialog.showMessage('Verique se você selecionou um código valido, lembre-se que os códigos dos produtos devem ser diferentes')
    
   

def function_main():
    linha1 = form.lineEdit.text()
    linha2 = form.lineEdit_4.text()
    linha3 = form.lineEdit_5.text()
    linha4 = form.lineEdit_6.text()
    

    categoria = ""
    if form.radioButton_4.isChecked():
        print("Categoria alimentos foi selecionada")
        categoria = "alimentos"
    elif form.radioButton_5.isChecked():
        print("Categoria informatica foi selecionada")
        categoria ="informatica"
    else:
        print("Categoria medicamentos foi selecionada")
        categoria = "medicamentos"

    if ',' in linha3:
        linha3 = linha3.replace(',','.')
    #verifica se os campos foram preenchidos com corretamente
    if not linha2.isnumeric() or not linha4.isnumeric():
        error_dialog.showMessage('Oh não alguma coisa está errada! verifique se todos os campos estão corretos ')  
    else:
        try:
            cursor = banco.cursor()
            comand_sql = "INSERT INTO produtos(codigo,descricao,preco,categoria,quantidade) VALUES(%s,%s,%s,%s,%s)"
            dados = (str(linha2),str(linha1),str(linha3),str(categoria),str(linha4))
            cursor.execute(comand_sql,dados)
            banco.commit()
            form.lineEdit.setText("")
            form.lineEdit_4.setText("")
            form.lineEdit_5.setText("")
            form.lineEdit_6.setText("")
        except:
            error_dialog.showMessage('verique se os campos estão digitados corretamente, lembre-se que cada produto precisa de um codigo único')

def chama2pagina():
    listar_dados.show()

    cursor = banco.cursor()
    comando_sql = "SELECT * FROM produtos"
    cursor.execute(comando_sql)
    dados_lidos = cursor.fetchall()

    listar_dados.tableWidget.setRowCount(len(dados_lidos))
    listar_dados.tableWidget.setColumnCount(5)

    #percore toda a matriz
    for i in range(0,len(dados_lidos)):
        for j in range(0,5):
            listar_dados.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
    
def voltar():
    listar_dados.close()
    form.show()
  
def gerar_pdf():
    #salva os dados do banco
    cursor = banco.cursor()
    comando_sql = "SELECT * FROM produtos"
    cursor.execute(comando_sql)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold",25)
    pdf.drawString(200,800,"Produtos cadastrados")
    pdf.setFont("Times-Bold",18)


    pdf.drawString(10,750,"Codigo")
    pdf.drawString(110,750,"Produto")
    pdf.drawString(210,750,"Preço")
    pdf.drawString(310,750,"Categoria")
    pdf.drawString(410,750,"Quantidade")


    for i in range(0,len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 -y ,str(dados_lidos[i][0]))
        pdf.drawString(110,750 -y ,str(dados_lidos[i][1]))
        pdf.drawString(210,750 -y ,str(dados_lidos[i][2]))
        pdf.drawString(310,750 -y ,str(dados_lidos[i][3]))
        pdf.drawString(410,750 -y ,str(dados_lidos[i][4]))
     
        
    pdf.save()
    error_dialog.showMessage('Pdf gerado com sucesso.')


def salvar_dados():
    
    print(new_codigo_id)
    #armazena os dados da pagina de editar
    codigo = edit.lineEdit_2.text()
    descricao = edit.lineEdit_3.text()   
    preco = edit.lineEdit_4.text()
    categoria = edit.lineEdit_5.text()
    quantidade = edit.lineEdit_6.text()
    
    if ',' in preco:
        preco = preco.replace(',','.')

    if not descricao or not categoria:
        error_dialog.showMessage('Verique se todos os campos estão preenchidos corretaente')    

        #atualizar os dados do banco de dados
    else:
        try:
            cursor = banco.cursor()
            cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}',categoria = '{}', quantidade = '{}' WHERE codigo = {}".format(codigo,descricao,preco,categoria,quantidade,new_codigo_id))
            banco.commit()
            edit.close()
            listar_dados.close()
            #chama a função para recarregar a tela dos dados listados
            chama2pagina()
        except:
            error_dialog.showMessage('Verifique se todos os campos estão preenchidos corretamente, o id do produto não pode ser alterado. e o codigo do produto deve ser somente números')


def excluir():
    codigo_id = select_codigo.lineEdit.text()
    select_codigo.close()
    try:
        #deleta as informações no banco de dados 
        cursor = banco.cursor()      
        cursor.execute(f"DELETE FROM produtos WHERE codigo ={codigo_id}" )
        banco.commit()
        listar_dados.close()
        chama2pagina()
    except:
        error_dialog.showMessage('Verique se o código está correto')

app = QtWidgets.QApplication([])
form = uic.loadUi("formulario.ui")
listar_dados = uic.loadUi("listar_dados2.ui")
edit = uic.loadUi("edit2.ui")
select_codigo = uic.loadUi("select.ui")
form.pushButton.clicked.connect(function_main)
form.pushButton_2.clicked.connect(chama2pagina)
listar_dados.pushButton_3.clicked.connect(voltar)
listar_dados.pushButton_4.clicked.connect(gerar_pdf)
listar_dados.pushButton_5.clicked.connect(get_codigo)
listar_dados.pushButton_6.clicked.connect(get_codigo)
select_codigo.pushButton.clicked.connect(editar)   
select_codigo.pushButton_2.clicked.connect(excluir)            
edit.pushButton.clicked.connect(salvar_dados)
error_dialog = QtWidgets.QErrorMessage()

form.show()
app.exec()



