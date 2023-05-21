import tkinter as tk					
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import time

def set_pid():
    return

def set_IP():
    return

#Función para realizar adquisición de datos
def log():
    cont=0
    lvalues=[]
    lcont=[]
    while cont<=10:
        data=time.ctime()
        lvalues.append(data)
        lcont.append(cont)
        print(data)
        print(cont)
        time.sleep(1)
        cont=cont+1
    return(lvalues)
        
        
def plot():

	# the figure that will contain the plot
	fig = Figure(figsize = (5, 5),
				dpi = 100)
    
	# list of squares
	y = log()
	# adding the subplot
	plot1 = fig.add_subplot(111)

	# plotting the graph
	plot1.plot(y)

	# creating the Tkinter canvas
	# containing the Matplotlib figure
	canvas = FigureCanvasTkAgg(fig,
							master = tab3)
	canvas.draw()

	# placing the canvas on the Tkinter window
	canvas.get_tk_widget().pack()

	# creating the Matplotlib toolbar
	toolbar = NavigationToolbar2Tk(canvas,
								tab3)
	toolbar.update()

	# placing the toolbar on the Tkinter window
	canvas.get_tk_widget().pack()


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

IP=ttk.Entry(tab0).grid(column = 1,
row = 0,
padx = 30,
pady = 30)

ttk.Button(tab0,text='Establecer conexión', command=set_IP).grid(column = 0,
row = 3,
padx = 30,
pady = 30)

#Elementos de la pestaña 1
ttk.Label(tab1,text="Nivel Tanque 1: ").grid(column = 0,
row = 0,
padx = 30,
pady = 30)

ttk.Label(tab1,text="Nivel Tanque 2: ").grid(column = 0,
row = 1,
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
