import matplotlib.pyplot as plt
import pandas as pd

# Clase que define un proceso
class Proceso:
    def __init__(self, id, tiempo_llegada, duracion):
        self.id = id
        self.tiempo_llegada = tiempo_llegada
        self.duracion = duracion
        self.tiempo_restante = duracion
        self.tiempo_inicio = -1
        self.tiempo_finalizacion = 0
        self.finalizado = False

# Función para simular FIFO
def fifo_simulacion(procesos):
    tiempo_actual = 0
    linea_tiempo = []
    tabla_resultados = []  # Para almacenar el estado de cada proceso en cada ciclo
    ciclo = 0

    # Registrar estado inicial
    tabla_resultados.append([ciclo] + [(p.id, p.tiempo_restante) for p in procesos])

    while any(p.tiempo_restante > 0 for p in procesos):
        ciclo += 1
        # Seleccionar el primer proceso que llegó y que no ha finalizado
        procesos_disponibles = [p for p in procesos if p.tiempo_llegada <= tiempo_actual and not p.finalizado]
        if procesos_disponibles:
            proceso_elegido = procesos_disponibles[0]  # FIFO selecciona el primer proceso que llegó
            if proceso_elegido.tiempo_inicio == -1:
                proceso_elegido.tiempo_inicio = tiempo_actual
            proceso_elegido.tiempo_restante -= 1
            linea_tiempo.append(proceso_elegido.id)
            tiempo_actual += 1
            if proceso_elegido.tiempo_restante == 0:
                proceso_elegido.tiempo_finalizacion = tiempo_actual
                proceso_elegido.finalizado = True
        else:
            # No hay procesos disponibles, avanzar el tiempo
            linea_tiempo.append("Idle")
            tiempo_actual += 1

        # Registrar el estado actual de los procesos en este ciclo
        tabla_resultados.append([ciclo] + [(p.id, p.tiempo_restante) for p in procesos])

    return linea_tiempo, pd.DataFrame(tabla_resultados, columns=["Ciclo"] + [f"Proceso {p.id}" for p in procesos])

# Simulación
procesos = [
    Proceso("P1", 0, 5),
    Proceso("P2", 2, 3),
    Proceso("P3", 4, 2),
    Proceso("P4", 6, 4),
]

# Ejecutar la simulación
linea_tiempo, tabla_resultados = fifo_simulacion(procesos)

# Mostrar la tabla de resultados
print(tabla_resultados)

# Graficar la línea de tiempo
plt.figure(figsize=(10, 6))

x = list(range(len(linea_tiempo)))
y = linea_tiempo

# Dibujar líneas de seguimiento y los puntos
plt.step(x, y, where='mid', color='gray', linestyle='--', label='')
plt.scatter(x, y, c='blue', s=100, zorder=5, label='')  # Puntos de los procesos

# Configuración del gráfico
plt.title("Simulación del algoritmo FIFO")
plt.xlabel("Tiempo")
plt.ylabel("Proceso en ejecución")
plt.grid(True)
plt.legend()

# Mostrar la gráfica
plt.show()
