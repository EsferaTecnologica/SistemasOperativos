# import matplotlib.pyplot as plt

# # Clase que define un proceso
# class Proceso:
#     def __init__(self, id, tiempo_llegada, duracion):
#         self.id = id
#         self.tiempo_llegada = tiempo_llegada
#         self.duracion = duracion
#         self.tiempo_restante = duracion
#         self.tiempo_finalizacion = 0
#         self.tiempo_inicio = -1
#         self.finalizado = False

# # Función para simular STR
# def str_simulacion(procesos):
#     tiempo_actual = 0
#     linea_tiempo = []
#     while any(p.tiempo_restante > 0 for p in procesos):
#         # Seleccionar el proceso con el menor tiempo restante que haya llegado
#         procesos_disponibles = [p for p in procesos if p.tiempo_llegada <= tiempo_actual and not p.finalizado]
#         if procesos_disponibles:
#             proceso_elegido = min(procesos_disponibles, key=lambda p: p.tiempo_restante)
#             if proceso_elegido.tiempo_inicio == -1:
#                 proceso_elegido.tiempo_inicio = tiempo_actual
#             proceso_elegido.tiempo_restante -= 1
#             linea_tiempo.append(proceso_elegido.id)
#             tiempo_actual += 1
#             if proceso_elegido.tiempo_restante == 0:
#                 proceso_elegido.tiempo_finalizacion = tiempo_actual
#                 proceso_elegido.finalizado = True
#         else:
#             # No hay procesos disponibles, avanzar el tiempo
#             linea_tiempo.append("Idle")
#             tiempo_actual += 1

#     return linea_tiempo

# # Simulación
# procesos = [
#     Proceso("P1", 0, 7),
#     Proceso("P2", 2, 4),
#     Proceso("P3", 4, 1),
#     Proceso("P4", 5, 4),
# ]

# linea_tiempo = str_simulacion(procesos)

# # Graficar la línea de tiempo
# plt.figure(figsize=(10, 6))
# plt.plot(linea_tiempo, drawstyle="steps", marker="o")
# plt.title("Simulación del algoritmo STR")
# plt.xlabel("Tiempo")
# plt.ylabel("Proceso en ejecución")
# plt.grid(True)
# plt.show()


import matplotlib.pyplot as plt
import pandas as pd

# Clase que define un proceso
class Proceso:
    def __init__(self, id, tiempo_llegada, duracion, critico=False):
        self.id = id
        self.tiempo_llegada = tiempo_llegada
        self.duracion = duracion
        self.tiempo_restante = duracion
        self.critico = critico  # Identificar si el proceso es crítico o no
        self.finalizado = False
        self.tiempo_inicio = -1
        self.tiempo_finalizacion = 0

# Función para simular planificación con procesos críticos y no críticos
def planificacion_tiempo_real(procesos):
    tiempo_actual = 0
    linea_tiempo = []
    tabla_resultados = []  # Para almacenar el estado de cada proceso en cada ciclo
    ciclo = 0

    # Registrar estado inicial
    tabla_resultados.append([ciclo] + [(p.id, p.tiempo_restante, 'Crítico' if p.critico else 'No Crítico') for p in procesos])

    while any(p.tiempo_restante > 0 for p in procesos):
        ciclo += 1
        # Seleccionar el proceso crítico disponible primero, si no hay críticos, usar STR
        procesos_criticos = [p for p in procesos if p.tiempo_llegada <= tiempo_actual and not p.finalizado and p.critico]
        procesos_no_criticos = [p for p in procesos if p.tiempo_llegada <= tiempo_actual and not p.finalizado and not p.critico]

        if procesos_criticos:
            proceso_elegido = procesos_criticos[0]  # Ejecutar el primer proceso crítico
        elif procesos_no_criticos:
            proceso_elegido = min(procesos_no_criticos, key=lambda p: p.tiempo_restante)  # STR para no críticos
        else:
            # Si no hay procesos disponibles, el sistema está en Idle
            linea_tiempo.append(("Idle", False))
            tiempo_actual += 1
            continue

        if proceso_elegido.tiempo_inicio == -1:
            proceso_elegido.tiempo_inicio = tiempo_actual

        proceso_elegido.tiempo_restante -= 1
        linea_tiempo.append((proceso_elegido.id, proceso_elegido.critico))
        tiempo_actual += 1

        if proceso_elegido.tiempo_restante == 0:
            proceso_elegido.tiempo_finalizacion = tiempo_actual
            proceso_elegido.finalizado = True

        # Registrar el estado actual de los procesos en este ciclo
        tabla_resultados.append([ciclo] + [(p.id, p.tiempo_restante, 'Crítico' if p.critico else 'No Crítico') for p in procesos])

    return linea_tiempo, pd.DataFrame(tabla_resultados, columns=["Ciclo"] + [f"Proceso {p.id}" for p in procesos])

# Simulación
procesos = [
    Proceso("P1", 0, 5, critico=False),   # Crítico
    Proceso("P2", 1, 3, critico=False),  # No crítico
    Proceso("P3", 2, 2, critico=True),   # Crítico
    Proceso("P4", 3, 4, critico=False),  # No crítico
]

# Ejecutar la simulación
linea_tiempo, tabla_resultados = planificacion_tiempo_real(procesos)

# Mostrar la tabla de resultados
print(tabla_resultados)

# Graficar la línea de tiempo con colores y líneas de seguimiento para procesos críticos
plt.figure(figsize=(10, 6))

# Inicializar listas para las líneas y colores
x = []
y = []
colors = []

# Construir los datos para el gráfico
for i, (proceso, critico) in enumerate(linea_tiempo):
    x.append(i)
    y.append(proceso)
    color = 'red' if critico else 'blue'
    colors.append(color)

# Dibujar líneas de seguimiento y los puntos
plt.step(x, y, where='mid', color='gray', linestyle='--', label='')
plt.scatter(x, y, c=colors, s=100, zorder=5)  # Puntos coloreados según criticidad

# Configuración del gráfico
plt.title("Simulación de Planificación Tiempo Real (Críticos en Rojo, No Críticos en Azul)")
plt.xlabel("Tiempo")
plt.ylabel("Proceso en ejecución")
plt.grid(True)
plt.legend()

# Mostrar la gráfica
plt.show()

