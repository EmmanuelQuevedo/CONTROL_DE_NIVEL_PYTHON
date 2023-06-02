from tkinter import ttk
import serial
from tkinter import Tk, Frame, Button, Label, ttk
from tkinter import *
import time
import pygame, sys
from pygame.locals import*
from tkinter import messagebox as MessageBox


pygame.init() #Iniciamos modulo de pygame

pygame.mixer.music.load("alerta.mp3") #Cargamos el sonido en mp3
 
try:
    serialArduino = serial.Serial('COM3', 9600)
    time.sleep(1)
except:
    print('CANNOT CONNECT TO THE PORT')
    MessageBox.showerror("Error", "No fue posible conectarse al puerto, por favor verifique la conexión")

Alto='#008080'
Bajo='#f12'

class Tank(Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_rectangle(50, 50, 150, 250)
        self.fill = self.create_rectangle(50, 50, 150, 250, fill="blue")
        self.text = self.create_text(100, 150, text="0 %", font=("Roboto", 20, "bold"))
        self.full_distance = 2  # Distancia para considerar el tanque lleno
        self.empty_distance = 14  # Distancia para considerar el tanque vacío
        self.tank_full = False  # Estado del tanque
        self.tank_filled = False  # Estado de la alarma

    def set_fill(self, dist):
        dist = int(dist)
        if dist == self.empty_distance:
            dist = 0  # Establecer el tanque como vacío
            self.tank_filled= False
            self.tank_full = False  # El tanque no está lleno
        elif dist == self.full_distance:
            dist = 14  # Establecer el tanque como lleno
            self.tank_full = True  # El tanque está lleno
        else:
            dist = self.empty_distance - dist  # Calcular la cantidad de llenado inversamente
            self.tank_full = False  # El tanque no está lleno
            self.tank_filled= False


        fill_height = 250 - (dist / self.empty_distance) * 200  # Calcular la altura del llenado
        self.coords(self.fill, 50, fill_height, 150, 250)
        self.itemconfigure(self.text, text=f"{int(dist / self.empty_distance * 100)} %")


def fill_tank():
    distancia_str = serialArduino.readline().decode().strip()  # Lee la distancia desde el puerto serie
    dist = float(distancia_str)  # Convierte en número decimal
    tank.set_fill(dist)
    tank.update()

    if tank.tank_full and not tank.tank_filled:
        tank.tank_filled = True
        MessageBox.showinfo("Tanque Lleno", "El tanque ha sido llenado exitosamente")

    tank.after(50, fill_tank)

def alarma():
    llenado = int(tank.itemcget(tank.text, "text").split()[0])
    if llenado <= 40:
        titulo6.config(bg=Bajo)  
    else:
        titulo6.config(bg=Alto)  
    
    root.after(100, alarma)
 

root = Tk()
root.title("Control del nivel del agua")
root.iconbitmap("tanque.ico")
root.grid()

tank = Tank(root)
tank.grid(row=2, column=0, columnspan=2)

frame = Frame(root, bg="#d0d0d0")
frame.grid()
titulo = Label(root, text="Control del nivel del agua", font=("Roboto", 24))
titulo.grid(row=0, column=0)

titulo2 = Label(root, text="NIVEL DEL AGUA", font=("Roboto", 12))
titulo2.grid(row=3, column=0)

titulo3 = Label(root, width=15, text="")
titulo3.grid(row=4, column=0)

titulo4 = Label(root, text="BAJO NIVEL", font=("Roboto", 12), width=18, height=2, bg="#f12", fg="#fff")
titulo4.grid(row=3, column=2)

titulo5 = Label(root, text="ALTO NIVEL", font=("Roboto", 12), width=18, height=2, bg="#008080", fg="#fff")
titulo5.grid(row=3, column=1)

titulo6 = Label(root, text="ALARMA", font=("Roboto", 12), width=18, height=2, bg="#fff", fg="#fff")
titulo6.grid(row=2, column=1, columnspan=2)

tank.after(1000, fill_tank)

alarma()

root.mainloop()
