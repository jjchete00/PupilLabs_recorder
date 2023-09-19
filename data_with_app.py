#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 09:12:45 2023

@author: Juan Jose Vidal Justamante
"""

'''
Accede a la API de la aplicación de Pupil Labs en Mac. OJO! Tiene que 
estar abierta para que funcione
Ademas, saca todos los datos del algoritmo de deteccion por la terminal
a tiempo real.
Asegurate de que dentro de la aplicacion, el algoritmo esta activado.
'''

import zmq
import msgpack
import time

if __name__ == '__main__':
    
    ctx = zmq.Context()
    pupil_remote = zmq.Socket(ctx,zmq.REQ)
    
    ip = 'localhost'  # Por si acaso utilizas la IP de otra maquina 
    port = 50020  # El puerto por defecto es 50020

    pupil_remote.connect(f'tcp://{ip}:{port}')

    # Le pide a SUB_PORT leer los datos
    pupil_remote.send_string('SUB_PORT')
    sub_port = pupil_remote.recv_string()
    
    # nos suscribimos al socket
    subscriber = ctx.socket(zmq.SUB)
    
    try:
        
        # Me conecto a la direccion donde estan los datos de las gafas
        subscriber.connect(f'tcp://{ip}:{sub_port}') 
        # Me suscribo a la informacion que necesito, en este caso 3d        
        subscriber.subscribe(b'pupil.0.3d')
        # Envio un mensaje si todo va bien
        print("Conectado con el servidor.")
        
    except zmq.error.ZMQError as e:
        print("Conexion fallida. Error: " + str(e)) # Aviso si no se conecta
        
    # Organizo la informacion en listas 
    
    norm_pos = []
    diameter = []
    confidence = []
    timestamp = []
    ellipse = []
    sphere = []
    projected_sphere = []
    circle_3d = []
    location = []
    model_confidence = []
    theta = []
    phi = []
    tiempo_real = []
    diferencia = []
    
    # Establezco la duracion de la recogida de datos 
    start_time = time.time()
    tiempo = int(input('Introduce la duracion de la grabacion (t > 3s): '))
    
    # La siguiente linea hace una diferencia entre el momento en el que se
    # empieza a grabar y el actual. Esta diferencia debe ser menor que el 
    # tiempo total de grabacion
    
    while time.time() - start_time < tiempo:
        
        
        topic, payload = subscriber.recv_multipart()
        data = msgpack.loads(payload) #(payload, encoding='utf-8')
        
        # de una forma un poco cuestionable organizo la informacion en listas
        
        norm_pos.append(data['norm_pos'])
        diameter.append(data['diameter'])
        confidence.append(data['confidence'])
        timestamp.append(data['timestamp'])
        ellipse.append(data['ellipse']) 
        projected_sphere.append(data['projected_sphere'])
        circle_3d.append(data['circle_3d'])
        location.append(data['location'])
        model_confidence.append(data['model_confidence'])
        theta.append(data['theta'])
        phi.append(data['phi'])
        tiempo_real.append(time.time())
        diferencia.append(data['timestamp']-time.time())
        # aqui vemos la diferencia entre el tiempo unix y el pupil
        
        print('-------------------------------------------------')
        print(f"{topic}: {data}") 
        # saca por la terminal todos los datos a tiempo real

    
    