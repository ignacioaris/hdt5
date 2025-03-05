import simpy
import random
import matplotlib.pyplot as plt
import numpy as np

RANDOM_SEED = 42
MEMORIA_TOTAL = 100
INSTRUCCIONES_POR_UNIDAD_TIEMPO = 3
INTERVALO_LLEGADA_PROCESOS = 1
random.seed(RANDOM_SEED)

def proceso(env, nombre, ram, cpu, tiempos):
    memoria_requerida = random.randint(1, 10)
    yield ram.get(memoria_requerida)
    tiempo_inicio = env.now
    print(f'[{env.now:.2f}] {nombre} obtuvo {memoria_requerida} unidades de RAM.')

    instrucciones = random.randint(1, 10)
    while instrucciones > 0:
        with cpu.request() as req:
            yield req
            yield env.timeout(1)
            ejecutadas = min(INSTRUCCIONES_POR_UNIDAD_TIEMPO, instrucciones)
            instrucciones -= ejecutadas
            print(f'[{env.now:.2f}] {nombre} ejecutó {ejecutadas} instrucciones, {instrucciones} restantes.')

        if instrucciones > 0:
            evento = random.randint(1, 21)
            if evento == 1:
                yield env.timeout(2)
                print(f'[{env.now:.2f}] {nombre} completó I/O.')

    yield ram.put(memoria_requerida)
    tiempo_final = env.now
    tiempos.append(tiempo_final - tiempo_inicio)
    print(f'[{env.now:.2f}] {nombre} liberó {memoria_requerida} unidades de RAM y terminó.')
