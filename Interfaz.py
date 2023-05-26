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
    

plc=pc.plcComm() #communications with plc instance

        
def set_pid():
    return

def set_IP(): #Función para establecer conexión con el PLC
    
    try: 
        plc.connection(ip_direction=str(IP.get()))
        Estado=ttk.Label(tab0,text="Conectado a: "+str(IP.get()))
        Estado.grid(column = 1,
        row = 1,
        padx = 30,
        pady = 30)
    except Exception as err:
        Estado=ttk.Label(tab0,text=str(err))
        Estado.grid(column = 1,
        row = 1,
        padx = 30,
        pady = 30)
    return


#Función para realizar adquisición de datos
def plot():
    cont=0
    ltiempos=[]
    ldatos=[]

    while cont<=10:
        
        # db = plc.db_read(5, 0, 4) #(DB,Inicio (byte),Tamaño)
        # data = snap7.util.get_real(db, 0)
        data=plc.read_from_db()   #Lectura de datos del PLC
        #data=cont
        tiempo=time.ctime() #Tiempo en que se toma la medición
        ldatos.append(data) #Datos adquiridos
        ltiempos.append(tiempo)
        print(data)
        print(tiempo)
        time.sleep(1) #Tiemo de espera en segundos
        cont=cont+1

	#Figura que contiene la gráfica
    fig = Figure(figsize = (5, 5),
				dpi = 100)
    
    
    plot1 = fig.add_subplot(111)

	# plotting the graph
    plot1.plot(ltiempos,ldatos)

	#Canvas que contiene la figura
    canvas = FigureCanvasTkAgg(fig,
							master = tab3)
    canvas.draw()

	#Ubicación de la figura en el canvas
    canvas.get_tk_widget().pack()

	#Barra de herramientas del gráfico
    toolbar = NavigationToolbar2Tk(canvas,
								tab3)
    toolbar.update()

	#Ubicación de la barra de herramientas
    canvas.get_tk_widget().pack()

     
    #Diccionario de listas
    dict1 = {'Datos': ldatos, 'Tiempo': ltiempos}  
       
    df = pd.DataFrame(dict1) 
    
    #Guardado del archivo de datos 
    df.to_csv('Datos_PLC.csv')
    
    root.filename =  filedialog.asksaveasfilename(initialdir = "/",title = 'Seleccione la ubicación de destino',filetypes = (("CSV","csv"),("excel","xlsx"),("all files","*.*")))
    df.to_csv(root.filename+'.csv',index=False)
    


root = tk.Tk()
root.title("SCADA Banco de instrumentación")
tabControl = ttk.Notebook(root)
tabControl.config(width=400, height=300)

s = ttk.Style()
s.theme_use('default')
s.configure('TNotebook.Tab', background="light blue") #Color de las pestañas
s.configure('TNotebook', background="dark grey") #Color del fondo de las pestañas
s.configure('TFrame', background="light grey")   #Color de fondo del cuadro


tab0 = ttk.Frame(tabControl)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab0, text ='Conexión')
tabControl.add(tab1, text ='Visualización')
tabControl.add(tab2, text ='Control PID')
tabControl.add(tab3, text ='Adquisición')
tabControl.pack(expand = 1, fill ="both")

#Elementos de la pestaña 0
ttk.Label(tab0,text="Dirección IP: ").grid(column = 0,
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

ttk.Button(tab0,text='Establecer conexión', command=set_IP).grid(column = 0,
row = 3,
padx = 30,
pady = 30)

#Elementos de la pestaña 1
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

Tank1 = ttk.Progressbar(tab1,orient=tk.VERTICAL, length=100,mode="determinate")
Tank1.grid(column = 1,
row = 1,
padx = 30,
pady = 30)

def upBar():
    Tank1['value']+=10
    Tank2['value']+=10

def dBar():
    Tank1['value']-=10
    Tank2['value']-=10

ttk.Button(tab1,text='Subir', command=upBar).grid(column = 2,
row = 0,
padx = 30,
pady = 30)

ttk.Button(tab1,text='Bajar', command=dBar).grid(column = 3,
row = 0,
padx = 30,
pady = 30)

#Elementos de la pestaña 2
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

#Elementos de la pestaña 3
ttk.Button(tab3,text='Iniciar adquisición', command=plot).pack()

root.mainloop()