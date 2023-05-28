import matplotlib.pyplot as plt
import tkinter as tk					
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import time
import pandas as pd
from tkinter import filedialog
import plcComm as pc
import threading


plc=pc.plcComm() #communications with plc instance

        
def set_pid():
    return

def set_IP(): #Funci�n para establecer conexi�n con el PLC
    
    connection=plc.connection(ip_direction=str(IP.get()))
    Estado=ttk.Label(tab0,text="Conectado a: "+str(IP.get()))
    Estado.grid(column = 1,
    row = 1,
    padx = 30,
    pady = 30)
    if ("b' TCP : Invalid address'" in str(connection)):
        Estado=ttk.Label(tab0,text="Direcci�n inv�lida")
        Estado.grid(column = 1,
        row = 1,
        padx = 30,
        pady = 30)
            
    return

def updateLevel():
    if tabControl.index('current')==1:
        try:
            list_variables=["nivel1high","nivel1low","nivel2"] #list to store name of vars to read on db1 on plc
            ldatos={i:False for i in list_variables} #dict to store data of readings
            # db = plc.db_read(5, 0, 4) #(DB,Inicio (byte),Tama�o)
            # data = snap7.util.get_real(db, 0)
            for i in list_variables:
                data=plc.read_from_db(i) #Lectura de datos del PLC
                #data=cont
                ldatos[i]=data #Datos adquiridos
                print(ldatos)
            time.sleep(0.3) #Tiemo de espera en segundos
            if ldatos["nivel1high"]==True and ldatos["nivel1low"]==True:
                Tank1['value']=100
            elif ldatos["nivel1high"]==False and ldatos["nivel1low"]==True:
                Tank1['value']=50
            else:
                Tank1['value']=0
            Tank2['value']=ldatos['nivel2']*10
            root.update_idletasks()
            root.after(2000, updateLevel())
        except:
            return

        
# 192.168.0.2

#Funci�n para realizar adquisici�n de datos
def plot():
    list_variables=["nivel2"] #list to store name of vars to read on db1 on plc
    ltiempos=[] #dict to store times of readings
    ldatos={i:[] for i in list_variables} #dict to store data of readings
    cont=0 #counter for while cycle
    while cont<=10:
        
        # db = plc.db_read(5, 0, 4) #(DB,Inicio (byte),Tama�o)
        # data = snap7.util.get_real(db, 0)
        for i in list_variables:
            data=plc.read_from_db(i)   #Lectura de datos del PLC
            #data=cont
            ldatos[i].append(data) #Datos adquiridos
            print(data)
        tiempo=time.ctime() #Tiempo en que se toma la medici�n
        ltiempos.append(tiempo)
        print(tiempo)
        time.sleep(1) #Tiemo de espera en segundos
        cont=cont+1

	#Figura que contiene la gr�fica
    fig,ax1=plt.subplots(1,1)
    ax1.plot(ltiempos,ldatos["nivel2"]) #plot with respect to time, each variable

    #fig = Figure(figsize = (5, 5),
				#dpi = 100)
    
    
    #plot1 = fig.add_subplot(111)

	# plotting the graph
    #plot1.plot(ltiempos,ldatos)

	#Canvas que contiene la figura
    canvas = FigureCanvasTkAgg(fig,
							master = tab3)
    canvas.draw()

	#Ubicaci�n de la figura en el canvas
    canvas.get_tk_widget().pack()

	#Barra de herramientas del gr�fico
    toolbar = NavigationToolbar2Tk(canvas,
								tab3)
    toolbar.update()

	#Ubicaci�n de la barra de herramientas
    canvas.get_tk_widget().pack()

     
    #Diccionario de listas
    dict1 = {'Tiempo': ltiempos}
    for i in list_variables:
        dict1[i]=ldatos[i]
    df = pd.DataFrame(dict1)
    
    #Guardado del archivo de datos 
    df.to_csv(f'Datos_PLC_nivel.csv')
    
    root.filename =  filedialog.asksaveasfilename(initialdir = "/",title = 'Seleccione la ubicaci�n de destino',filetypes = (("CSV","csv"),("excel","xlsx"),("all files","*.*")))
    df.to_csv(root.filename+'.csv',index=False) #prompt wimdow to store file
    root.update_idletasks()
    


root = tk.Tk()
root.title("SCADA Banco de instrumentaci�n")
tabControl = ttk.Notebook(root)
tabControl.config(width=400, height=300)

s = ttk.Style()
s.theme_use('default')
s.configure('TNotebook.Tab', background="light blue") #Color de las pesta�as
s.configure('TNotebook', background="dark grey") #Color del fondo de las pesta�as
s.configure('TFrame', background="light grey")   #Color de fondo del cuadro


tab0 = ttk.Frame(tabControl)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab0, text ='Conexi�n')
tabControl.add(tab1, text ='Visualizaci�n')
tabControl.add(tab2, text ='Control PID')
tabControl.add(tab3, text ='Adquisici�n')
tabControl.pack(expand = 1, fill ="both")

#Elementos de la pesta�a 0
ttk.Label(tab0,text="Direcci�n IP: ").grid(column = 0,
row = 0,
padx = 30,
pady = 30)

IP=ttk.Entry(tab0)
IP.grid(column = 1,
row = 0,
padx = 30,
pady = 30)

Estado=ttk.Label(tab0,text="Desconectado")
Estado.grid(column = 1,
row = 1,
padx = 30,
pady = 30)

ttk.Button(tab0,text='Establecer conexi�n', command=set_IP).grid(column = 0,
row = 3,
padx = 30,
pady = 30)

#Elementos de la pesta�a 1
ttk.Label(tab1,text="Nivel Tanque 1: ").grid(column = 0,
row = 1,
padx = 30,
pady = 30)

ttk.Label(tab1,text="Nivel Tanque 2: ").grid(column = 0,
row = 0,
padx = 30,
pady = 30)

Tank2 = ttk.Progressbar(tab1,orient=tk.VERTICAL, length=100,mode="determinate")
Tank2.grid(column = 1,
row = 0,
padx = 30,
pady = 30)

global Tank1
Tank1 = ttk.Progressbar(tab1,orient=tk.VERTICAL, length=100,mode="determinate")
Tank1.grid(column = 1,
row = 1,
padx = 30,
pady = 30)



def upBar(level1=0,level2=0):
    Tank1['value']=level1
    Tank2['value']=level2

def dBar():
    Tank1['value']=10
    Tank2['value']=10

ttk.Button(tab1,text='Subir', command=updateLevel).grid(column = 2,
row = 0,
padx = 30,
pady = 30)

ttk.Button(tab1,text='Bajar', command=dBar).grid(column = 3,
row = 0,
padx = 30,
pady = 30)

#Elementos de la pesta�a 2
ttk.Label(tab2,text="kp: ").grid(column = 0,
row = 0,
padx = 30,
pady = 30)

k_p=ttk.Entry(tab2).grid(column = 1,
row = 0,
padx = 30,
pady = 30)

ttk.Label(tab2,text="ki: ").grid(column = 0,
row = 1,
padx = 30,
pady = 30)

k_i=ttk.Entry(tab2).grid(column = 1,
row = 1,
padx = 30,
pady = 30)

ttk.Label(tab2,text="kd: ").grid(column = 0,
row = 2,
padx = 30,
pady = 30)

k_d=ttk.Entry(tab2).grid(column = 1,
row = 2,
padx = 30,
pady = 30)

ttk.Button(tab2,text='Enviar', command=set_pid).grid(column = 0,
row = 3,
padx = 30,
pady = 30)

#Elementos de la pesta�a 3
ttk.Button(tab3,text='Iniciar adquisici�n', command=plot).pack()

root.mainloop()