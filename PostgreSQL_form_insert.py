#
#
####################    Change log  #################################
#           Update 0.0.3
#           
#           Adicionamos o botão de busca que pega os valores das caixas
#           e verificas os checkbox para montar a Query           
#
#           Adicionamos checkbox na aba de busca
#           A checkbox define quais colunas o select irá buscar
#         
#           Aprimorado a função de busca, agora as colunas cabeçalhos
#           são criadas de acordo com as checkboxes selecionadas
#
#####################################################################
#       Proximas update : 
#       Nas caixas de busca de plataforma, iremos adicionar uma caixa
#       no formato lista que terá os resultados das plataformas pelo
#       nome e não pelo ID
#
#       Adicionar outra aba para se conectar ao banco de dados          
#       de acordo com os dados que foram inseridos
#   
#       Adicionar Aba para deletar um valor da tabela do banco de dados
#
#
#
#       Estilizar alguns widgets 
#       
#      
#     
#
#
#
#
#####################################################################
########### Importando as libs necessárias
import tkinter as tk
from tkinter import *
from tkinter import ttk
import psycopg2 
import random
import pdb

#############################################
############ Se conectando ao postgresql
try:
    con = psycopg2.connect(
            database="Senhas",
            user="hexdien",
            password="zxcjkl",
            host="192.168.0.12",
            port=5433
            )
    pgcursor = con.cursor()
    print("Banco de dados conectado!")
except (Exception, psycopg2.Error) as error:
    print("Falha ao se conectar no banco de dados: "+error)
#############################################


#############################################
win = Tk()
win.title("Login Form")
win.geometry("405x350")
tabcon = ttk.Notebook(win)

#############################################
#   Estilizando
#############################################
style = ttk.Style(win)
style.theme_use("classic")

#############################################
#       Frames
#############################################

frm1 = ttk.Frame(tabcon)            #### Aba Adicionar Login
frm1.pack(expand=True,fill="both")


frm2 = ttk.Frame(tabcon)            #### Aba Buscar Loging
frm2.pack()

#############################################
# Tabs
#############################################
tabcon.add(frm1, text='Adicionar Login')
tabcon.add(frm2, text='Buscar Login')
tabcon.pack(expand=1, fill="both")





#############################################
#   Funções
#############################################

logins = {}

colunas = []

colempt = ['0','0','0','0']
def mostrarsenha():
    global ent2, checkb
    if checkb.var.get():
        field2['entry_senha']['show'] = ""
        #ent2['show'] = ""
    else:
        field2['entry_senha']['show'] = "*"
        #ent2['show'] = "*"

def usuario():
    sname = field3['search_usuario'].get()
    logins['usuario'] = sname
    global item2
    if checkuser.var.get():
        colunas.insert(0,"usuario,")
        colempt[0] = "1"
    else:
        colunas.remove("usuario,")
        colempt[0] = "0"
        print("Usuario removido")


def psenha():
    ssenha = field3['search_senha'].get()
    logins['senha'] = ssenha
    global item2
    if checksenha.var.get():
        colunas.insert(1,"senha,")
        colempt[1] = "1"
        
    else:
        colunas.remove("senha,")
        colempt[1] = "0"
        print("Senha removido")

def pemail():
    semail = field3['search_email'].get()
    logins['email'] = semail
    global item2
    if checkemail.var.get():
        colunas.insert(2,"email,")
        colempt[2] = "1"
    else:
        colunas.remove("email,")
        colempt[2] = "0"
        print("Email removido")

def pplat():
    splataforma = field3['search_plataforma'].get()
    logins['id_plataforma'] = splataforma
 
    if checkplat.var.get():
        colunas.insert(3,"id_plataforma,")
        colempt[3] = "1"
    else:
        #for row in tv.get_children():
        colunas.remove("id_plataforma,")
        colempt[3] = "0"
        print("Plataforma removido")



# Desconectar do banco de dados
def logoff():
    if con:
        print("Conexão com o Postgresql Encerrada!")
        pgcursor.close()
        con.close()
        win.destroy()

#############################################
# Inserir no banco de dados
def addlogin():
    cname = field2['entry_usuario'].get()
    senha = field2['entry_senha'].get()
    email = field2['entry_email'].get()
    plataforma = field2['entry_plataforma'].get()
    try:
        pgsql_insert = """ INSERT INTO login(usuario,senha,email,id_plataforma)
                        values (%s,%s,%s,%s)"""
        inserir = (cname,senha,email,plataforma)
        pgcursor.execute(pgsql_insert,inserir)
        con.commit()
        print(pgcursor.rowcount,"Dado(s) inserido(s) com sucesso na tabela login")
        return True
    except (Exception, psycopg2.Error) as error:
        print("Falha ao inserir dado(s) na tabela", error)

#############################################
#############################################
#   Query Select
#############################################
def buscarloginADV():
    global item2, rowcount, columns
    sname = field3['search_usuario'].get()
    ssenha = field3['search_senha'].get()
    semail = field3['search_email'].get()
    splataforma = field3['search_plataforma'].get()
    
    logins = {}
    logins['usuario'] = sname
    logins['senha'] = ssenha
    logins['email'] = semail
    logins['id_plataforma'] = splataforma
   
    ###################################################################


    ###################################################################
        
    ############### Criando a query SELECT ###############
    cstring = ""
    cntr=0
    clnsu=len(colunas) 

    
    colunastrip=' '.join(colunas).strip(',')
    slct = "SELECT " + colunastrip + " FROM login WHERE "
    qop = " = %s "
    qand = "and "
    queryselect=""
    arg=0
    querydados = ()
    qdlist = list(querydados)
    qcol2=""
    for i in logins:
        if logins[i] != "":
            qdlist.append(logins.get(i))
            cnns=colunas.index(i+",")
            qcol = colunas[cnns].strip(',')         ## Variavel com colunas removendo a virgula do final
            arg+=1
            if arg == 1:
                queryselect+= qcol + qop
            elif arg > 1 and arg != clnsu:
                queryselect+= qand + qcol + qop + qand
            elif arg == clnsu:
                queryselect+=qand + qcol + qop
               

    querydados = tuple(qdlist)
    querysant=queryselect.replace('and and', 'and')
    pgquery2=slct+querysant
    pgquery1=pgquery2.strip()
    if lastword(pgquery1) == "and":
        pgquery=pgquery1.rsplit(' ',1)[0]
    else:
        pgquery=pgquery1
    #                       Fim do bloco que cria a QUERY
    ###################################################################


    #                       Inicio do bloco que Executa a query
    ###################################################################
    pgcursor.execute(pgquery,(querydados))
    rows = pgcursor.fetchall()
    
    cntrows= 0              ## Contar quantas linhas o select retornou
    tvsize = 0              ## Contar tamanho da treeview
    cntitem = 0             ## conta quantas colunas foram selecionadas

    for i in tv.get_children():     ## apaga todas as rows antes de 
        tv.delete(i)                ## inserir novas

    tv.insert('',index=0,iid="teste",value="TESTE") ## item para crar 
    avbl=0                                          ## Header


    for item in colempt:
        if item == "1":
            tv.set("teste",column=avbl,value=columns[cntitem])
            avbl+=1
        cntitem+=1

    for i in rows:
        tv.insert('','end',value=i)     ## insere as linhas resultante
                                        ## do SELECT

###################################################################



def lastword(string):
    lis = list(string.split(" "))
    length = len(lis)
    return lis[length-1]

 
    if pgquery1.rsplit(' ',1)[0] == 'and':
        pgquery=pgquery1.rsplit(' ',1)[0]
    else:
        pgquery=pgquery1
###################################################################

#############################################
#   Aba Buscar Login
#############################################

####################
#Listas/tuples/dicts
####################
columns = ("usuario", "senha", "email", "plataforma")
rowcount =  { col:0 for col in columns }


####################
#   Caixa Treeview
####################

tv = ttk.Treeview(frm2, columns=columns,show="",height="6")
tv.grid(row=5,column=0,columnspan=3)
for col in columns:
    tv.heading(col, text=col)
    tv.column(col, anchor="c", width=100)



####################
#   Variaveis
####################



var1s = StringVar()
sname = StringVar()
var2s = StringVar()
ssenha = StringVar()
var3s = StringVar()
semail = StringVar()
var4s = StringVar()
splataforma = StringVar()

####################

#   Caixas
ff3 = frm2
field3 = {}

field3['search_usuario'] = ttk.Entry(ff3, textvariable=sname)
field3['search_senha'] = ttk.Entry(ff3, textvariable=ssenha)
field3['search_email'] = ttk.Entry(ff3, textvariable=semail)
field3['search_plataforma'] = ttk.Entry(ff3, textvariable=splataforma)


rs = 0
for fields3 in field3.values():
    fields3.grid(row=rs, column=1,pady=5,sticky=tk.W)
    rs += 1

#   Labels
field4 = {}

field4['search_usuario'] = ttk.Label(ff3, text="Usuario")
field4['search_senha'] = ttk.Label(ff3, text="Senha")
field4['search_email'] = ttk.Label(ff3, text="Email")
field4['search_plataforma'] = ttk.Label(ff3, text="Plataforma")


rs2 = 0
for fields4 in field4.values():
    fields4.grid(row=rs2, column=0,pady=5,sticky=tk.E)
    rs2 += 1


# Botões

btn3 = Button(frm2, text="Buscar", command=buscarloginADV,bg="Green")
btn3.grid(row=4,column=1)

#################################################################### Fim da aba buscar
###########################
#   Variaveis de inserção
###########################


var1 = StringVar()
cname = StringVar()
var2 = StringVar()
senha = StringVar()
var3 = StringVar()
email = StringVar()
var4 = StringVar()
plataforma = IntVar()

###########################

field = {}

field['usuario'] = ttk.Label(frm1, textvariable=var1)
var1.set("Usuario")

field['senha'] = ttk.Label(frm1, textvariable=var2)
var2.set("Senha")

field['email'] = ttk.Label(frm1, textvariable=var3)
var3.set("Email")

field['plataforma'] = ttk.Label(frm1, textvariable=var4)
var4.set("Plataforma")

field2 = {}

field2['entry_usuario'] = ttk.Entry(frm1, textvariable=cname)
field2['entry_senha'] = ttk.Entry(frm1, textvariable=senha)
field2['entry_email'] = ttk.Entry(frm1, textvariable=email)
field2['entry_plataforma'] = ttk.Entry(frm1, textvariable=plataforma)


r=0    
      
for fields in field.values():
    fields.grid(row=r, column=1,pady=5)
    r += 1

r2=0
for fields2 in field2.values():
    fields2.grid(row=r2, column=2,pady=5)
    r2 += 1


########################

# checkbox Procurar usuario

checkuser = ttk.Checkbutton(ff3, text='Procurar Usuario',onvalue=True,offvalue=False,command=usuario)
checkuser.grid(row=0,column=2,sticky=tk.W)
checkuser.var = tk.BooleanVar(value=False)
checkuser['variable'] = checkuser.var
#########################

# Checkbox Procurar senha

checksenha = ttk.Checkbutton(ff3, text='Procurar Senha',onvalue=True,offvalue=False,command=psenha)
checksenha.grid(row=1,column=2,sticky=tk.W)
checksenha.var = tk.BooleanVar(value=False)
checksenha['variable'] = checksenha.var

# Checkbox Procurar Email

checkemail= ttk.Checkbutton(ff3, text='Procurar Email',onvalue=True,offvalue=False,command=pemail)
checkemail.grid(row=2,column=2,sticky=tk.W)
checkemail.var = tk.BooleanVar(value=False)
checkemail['variable'] = checkemail.var


# Checkbox Procurar Plataforma

checkplat= ttk.Checkbutton(ff3, text='Procurar Plataforma',onvalue=True,offvalue=False,command=pplat)
checkplat.grid(row=3,column=2,sticky=tk.W)
checkplat.var = tk.BooleanVar(value=False)
checkplat['variable'] = checkplat.var





###########################
#       Widgets
###########################
checkb = ttk.Checkbutton(frm1, text='Mostrar senha',onvalue=True,offvalue=False,command=mostrarsenha)
checkb.grid(row=1,column=3)
checkb.var = tk.BooleanVar(value=False)
checkb['variable'] = checkb.var

btn = Button(frm1, text="Adicionar Login", command=addlogin,fg="green")
btn.grid(row=4, column=2)

btn2 = Button(frm1, text="Sair", command=logoff,bg="red")
btn2.grid(row=5, column=2)

##################
#       Geometria
##################

#win.geometry("300x350")
#win.resizable(False,False)
win.mainloop()

