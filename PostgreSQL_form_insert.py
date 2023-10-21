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
#           Caixas de buscas funcionando (*precisa de testes*)
#
#
#####################################################################
#       Proxima update : 
#       Estilizar alguns widgets 
#       
#       Iremos adicionar a função ao botão buscar para que 
#       ele busque os dados que forem inseridos nos Entrys do frame2
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
#   Funções
#############################################

logins = {}

colunas = []
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
 
    if checkuser.var.get():
        #print(logins['usuario'])
        colunas.insert(0,"usuario,")
        print("colunas LIST = "+ str(colunas))
    else:
        colunas.remove("usuario,")
        print("Usuario removido")

def psenha():
    ssenha = field3['search_senha'].get()
    logins['senha'] = ssenha
 
    if checksenha.var.get():
        colunas.insert(1,"senha,")
        print("colunas LIST = "+ str(colunas))
    else:
        colunas.remove("senha,")
        print("Senha removido")

def pemail():
    semail = field3['search_email'].get()
    logins['email'] = semail
 
    if checkemail.var.get():
        colunas.insert(2,"email,")
        print("colunas LIST = "+ str(colunas))
    else:
        colunas.remove("email,")
        print("Email removido")

def pplat():
    splataforma = field3['search_plataforma'].get()
    logins['id_plataforma'] = splataforma
 
    if checkplat.var.get():
        colunas.insert(3,"id_plataforma,")
        print("colunas LIST = "+ str(colunas))
    else:
        colunas.remove("id_plataforma,")
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

    ######################  Este bloco irá adicionar para dentro da
    ######################  variavel colunastrip, apenas as colunas
    ######################  que tiverem dados preenchidos          

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
            qcol = colunas[cnns].strip(',')
            print("qcol VAR = "+qcol)
            arg+=1
            if arg == 1:
                queryselect+= qcol + qop
            elif arg > 1 and arg != clnsu:
                queryselect+= qand + qcol + qop + qand
            elif arg == clnsu:
                queryselect+=qand + qcol + qop

    querydados = tuple(qdlist)
    print("querydados VAR = "+str(querydados))
    querysant=queryselect.replace('and and', 'and')
    pgquery2=slct+querysant
    pgquery1=pgquery2.strip()
    if lastword(pgquery1) == "and":
        pgquery=pgquery1.rsplit(' ',1)[0]
    else:
        pgquery=pgquery1
    pgcursor.execute(pgquery,(querydados))
    print("pgquery VAR = "+pgquery)
    print("querydados VAR = "+str(querydados))
    print(pgcursor.fetchall())

def lastword(string):
    lis = list(string.split(" "))
    length = len(lis)
    return lis[length-1]

 
 #'''   if pgquery1.rsplit(' ',1)[0] == 'and':
  #      print("caiu no IF")
   #     pgquery=pgquery1.rsplit(' ',1)[0]
   # else:
   #     print("caiu no ELSE")
   #     pgquery=pgquery1'''
    ###################################################################


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
#   Aba Buscar Login
#############################################
#frm2.grid_rowconfigure(5, weight=1)
#frm2.rowconfigure(1, 1)

tv = ttk.Treeview(frm2, columns=(1,2,3,4),show="headings",height="6")
tv.grid(row=5,column=0,columnspan=3)
tv.column(1,width=100)
tv.column(2,width=100)
tv.column(3,width=100)
tv.column(4,width=100)


tv.heading(1, text="Login")
tv.heading(2, text="Senha")
tv.heading(3, text="Email")
tv.heading(4, text="Plataforma")
#########
btn3 = Button(frm2, text="Buscar", command=buscarloginADV,bg="Green")
btn3.grid(row=4,column=1)



var1s = StringVar()
sname = StringVar()
var2s = StringVar()
ssenha = StringVar()
var3s = StringVar()
semail = StringVar()
var4s = StringVar()
splataforma = StringVar()


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

#
field4 = {}

field4['search_usuario'] = ttk.Label(ff3, text="Usuario")
field4['search_senha'] = ttk.Label(ff3, text="Senha")
field4['search_email'] = ttk.Label(ff3, text="Email")
field4['search_plataforma'] = ttk.Label(ff3, text="Plataforma")


rs2 = 0
for fields4 in field4.values():
    fields4.grid(row=rs2, column=0,pady=5,sticky=tk.E)
    rs2 += 1


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


r=0             ### variavel para incrementar linhas
                ### loop para organizar o grid
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
# label1 = Label(frm1, textvariable=var1)
# var1.set("Login")
# label1.grid(row=0,column=1)
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

