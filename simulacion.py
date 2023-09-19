#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 11:27:31 2023

@author: Juan Jose Vidal Justamante
"""

"""
El codigo genera una animacion sencilla de la pupila a partir de los datos 
ya extraidos en la carpeta /exports.
Dentro de las funciones hay explicaciones de que es cada uno de los datos.
Para mas informacion consultar fichero pupil_gaze_positions.txt incluido
al exportar los datos
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
from functools import partial
import csv

np.random.seed(19680801)

class cositas():
    def reader(path):
        '''
        
        Parameters
        ----------
        path : camino a la carpeta exports/XXX. (normalmente 000,001,...)

        Returns
        -------
        data : matriz que contiene los datos en columnas, la primera es el tipo.

        '''
        data = [[]]
        
        if not os.path.isdir(path):
            print('Error: la carpeta no se ha encontrado.')
        
        with open(os.path.join(path,'pupil_positions.csv'),'r') as file:
            
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
            file.close()
        del data[0] # quito el primer elemento, sale vacio
        return data
    
    def organizer(data):
        
        '''

        Parameters
        ----------
        data : Resultado de reader(path). Datos de pupil_positions.csv organizados

        Returns
        -------
        eye0_2d : datos de ojo0 en 2d
        eye1_2d : datos de ojo1 en 2d
        eye0_3d : datos de ojo0 en 3d
        eye1_3d : datos de ojo1 en 3d

        '''
        
        '''
        INFORMACION ACERCA DE data
        eye0_2d son matrices de listas. Cada lista contiene todos los datos que la 
        aplicacion toma en cada frame. Las que son en 2d tienen la mitad de datos.
        Aqui pongo unos cuantos datos y su indice (python) correspondiente

        OJO:
        posicion x,y = 4,5
        diametro = 6
        PUPILA:
        centro elipse x, y = 8,9
        ejes elipse a, b = 10,11
        angulo elipse = 12
        '''
        eye0_2d = []
        eye1_2d = []
        eye0_3d = []
        eye1_3d = []
        
        # esta parte hay que optimizarla
        
        for i in range(len(data)): #recorro todas las filas y organizo los datos
            
            if data[i][2] == '0':
                if data[i][7] == '2d c++':
                    eye0_2d.append(data[i])
                elif data[i][7] == 'pye3d 0.3.0 post-hoc':
                    eye0_3d.append(data[i])
            elif data[i][2] == '1':
                if data[i][7] == '2d c++':
                    eye1_2d.append(data[i])
                elif data[i][7] == 'pye3d 0.3.0 post-hoc':
                    eye1_3d.append(data[i])
            eye0_3d.append(data[i])
            
        return eye0_2d, eye1_2d, eye0_3d, eye1_3d
    

    def animate_2d(frame,ps):
        
        theta = np.linspace(0,2*np.pi,100)
        x0 = float(eye1_2d[frame][8]) #centro x
        y0 = float(eye1_2d[frame][9]) #centro y
        a = float(eye1_2d[frame][10]) #parametro a
        b = float(eye1_2d[frame][11]) #parametro b
        
        x = x0+a*np.cos(theta)
        y = y0+b*np.sin(theta)
        
        line1.set_data(x, y)
        return line1, 
    
    

# defino el camino a la carpeta 000,001,002... dentro de exports
path = '/path-to' 
#leo los datos del .csv
data = cositas.reader(path)
#guardo la primera fila porque contiene los titulos
data_type = data[0] 
#organizo los datos en 2d
eye0_2d, eye1_2d, eye0_3d, eye1_3d = cositas.organizer(data) 


# =============================================================================
# ANIMACION 2D
# =============================================================================

fig = plt.figure()

# exijo que el centro de la animacion este en 
# la media de las posiciones de la pupila
x_clist = [float(row[8]) for row in eye1_2d]
y_clist = [float(row[9]) for row in eye1_2d]
x_center = sum(x_clist)/len(x_clist)
y_center = sum(y_clist)/len(y_clist)

axis = plt.axes(xlim = (x_center-200,x_center+200),ylim=(y_center-200,y_center+200))

line1, = axis.plot([], [], lw = 2)
anim = FuncAnimation(fig, partial(cositas.animate_2d,ps=0),
					frames = len(data),
					interval = 10,
					blit = True)

plt.show()


