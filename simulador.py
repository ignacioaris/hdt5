import simpy
import random
import matplotlib.pyplot as plt
import numpy as np

RANDOM_SEED = 42
MEMORIA_TOTAL = 100
INSTRUCCIONES_POR_UNIDAD_TIEMPO = 3
INTERVALO_LLEGADA_PROCESOS = 1
random.seed(RANDOM_SEED)
