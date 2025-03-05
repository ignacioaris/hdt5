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

def setup(env, num_procesos, ram_capacidad, cpu_capacidad, intervalo, tiempos):
    ram = simpy.Container(env, init=ram_capacidad, capacity=ram_capacidad)
    cpu = simpy.Resource(env, capacity=cpu_capacidad)
    for i in range(num_procesos):
        env.process(proceso(env, f'Proceso-{i}', ram, cpu, tiempos))

def simulacion(num_procesos, intervalo):
    env = simpy.Environment()
    tiempos = []
    setup(env, num_procesos, MEMORIA_TOTAL, 2, intervalo, tiempos)
    env.run()  # Ejecutar hasta que todos los procesos terminen
    return np.mean(tiempos), np.std(tiempos)

# Recoger datos de simulación para diferentes cargas
cantidades_procesos = [25, 50, 100, 150, 200]
promedios = []
desviaciones = []

for cantidad in cantidades_procesos:
    promedio, desviacion = simulacion(cantidad, INTERVALO_LLEGADA_PROCESOS)
    promedios.append(promedio)
    desviaciones.append(desviacion)

# Generar gráficas de los resultados
plt.figure(figsize=(10, 5))
plt.errorbar(cantidades_procesos, promedios, yerr=desviaciones, fmt='-o', color='b', ecolor='r', capsize=5)
plt.title('Tiempo promedio de procesamiento vs. Número de procesos')
plt.xlabel('Número de Procesos')
plt.ylabel('Tiempo Promedio de Procesamiento (unidades de tiempo)')
plt.grid(True)
plt.show()
