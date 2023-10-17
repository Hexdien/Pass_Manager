#
# 0.0.1
#####################################################################
#       Proxima update : 
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
con = psycopg2.connect(
        database="Senhas",
        user="hexdien",
        password="zxcjkl",
        host="192.168.0.12",
        port=5433
        )
pgcursor = con.cursor()
print("Banco de dados conectado!")

#############################################
#############################################
#   Funções
#############################################

def mostrarsenha():
    global ent2, checkb
    if checkb.var.get():
        field2['entry_senha']['show'] = ""
        #ent2['show'] = ""
    else:
        field2['entry_senha']['show'] = "*"
        #ent2['show'] = "*"

# Desconectar do banco de dados
def logoff():
    if con:
        pgcursor.close()
        con.close()
        print("Conexão com o Postgresql Encerrada!")
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
def buscarlogin():
    sqlselect = "SELECT usuario,senha,email,id_plataforma FROM login"
    pgcursor.execute(sqlselect)
    rows = pgcursor.fetchall()
    for row in tv.get_children():
        tv.delete(row)
    for i in rows:
        tv.insert('','end',values=i)

#############################################
win = Tk()
win.title("Login Form")
win.geometry("400x300")
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
frm2.pack(padx=20)

#############################################
# Tabs
#############################################
tabcon.add(frm1, text='Adicionar Login')
tabcon.add(frm2, text='Buscar Login')
tabcon.pack(expand=1, fill="both")


#############################################
#   Aba Buscar Login
#############################################
frm2.grid_rowconfigure(5, weight=1)
#frm2.rowconfigure(1, 1)

tv = ttk.Treeview(frm2, columns=(1,2,3,4),show="headings",height="5")
tv.grid(row=10,column=0,columnspan=3)
tv.column(1,width=100)
tv.column(2,width=100)
tv.column(3,width=100)
tv.column(4,width=100)


tv.heading(1, text="Login")
tv.heading(2, text="Senha")
tv.heading(3, text="Email")
tv.heading(4, text="Plataforma")
#########
btn3 = Button(frm2, text="Buscar", command=buscarlogin,bg="Green")
btn3.grid(row=4,column=1,padx=20,pady=20)



var1s = StringVar()
sname = StringVar()
var2s = StringVar()
ssenha = StringVar()
var3s = StringVar()
semail = StringVar()
var4s = StringVar()
splataforma = IntVar()

#
field3 = {}

field3['search_usuario'] = ttk.Entry(frm2, textvariable=sname)
field3['search_senha'] = ttk.Entry(frm2, textvariable=ssenha)
field3['search_email'] = ttk.Entry(frm2, textvariable=semail)
field3['search_plataforma'] = ttk.Entry(frm2, textvariable=splataforma)


rs = 0
for fields3 in field3.values():
    fields3.grid(row=rs, column=1,pady=5,sticky=tk.EW)
    rs += 1

#
field4 = {}

field4['search_usuario'] = ttk.Label(frm2, text="Usuario")
field4['search_senha'] = ttk.Label(frm2, text="Senha")
field4['search_email'] = ttk.Label(frm2, text="Email")
field4['search_plataforma'] = ttk.Label(frm2, text="Plataforma")


rs2 = 0
for fields4 in field4.values():
    fields4.grid(row=rs2, column=0,pady=5,sticky=tk.E)
    rs2 += 1

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

