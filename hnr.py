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

# Función para calcular el Ratio de Respuesta
def calcular_ratio(tiempo_actual, proceso):
    tiempo_espera = tiempo_actual - proceso.tiempo_llegada
    ratio = (tiempo_espera + proceso.duracion) / proceso.duracion
    return ratio

# Función para simular HRN
def hrn_simulacion(procesos):
    tiempo_actual = 0
    linea_tiempo = []
    tabla_resultados = []  # Para almacenar el estado de cada proceso en cada ciclo
    ciclo = 0

    # Registrar encabezados de la tabla
    encabezados = ["Ciclo"] + [f"Proceso {p.id}" for p in procesos] + ["Proceso Seleccionado", "Response Ratio"]
    tabla_resultados.append(encabezados)

    while any(p.tiempo_restante > 0 for p in procesos):
        ciclo += 1
        # Seleccionar procesos disponibles
        procesos_disponibles = [p for p in procesos if p.tiempo_llegada <= tiempo_actual and not p.finalizado]
        
        selected_proceso = None
        response_ratio = None
        
        if procesos_disponibles:
            # Calcular el ratio de respuesta para cada proceso disponible
            procesos_con_ratio = [(p, calcular_ratio(tiempo_actual, p)) for p in procesos_disponibles]
            # Seleccionar el proceso con el mayor ratio de respuesta
            proceso_elegido, response_ratio = max(procesos_con_ratio, key=lambda x: x[1])
            
            selected_proceso = proceso_elegido.id
            
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
            selected_proceso = "Idle"
            response_ratio = None
            tiempo_actual += 1

        # Registrar el estado actual de los procesos en este ciclo
        estado_procesos = [(p.id, p.tiempo_restante) for p in procesos]
        fila = [ciclo] + [f"{pid}:{rest}" for pid, rest in estado_procesos] + [selected_proceso, response_ratio]
        tabla_resultados.append(fila)

    # Crear DataFrame
    columnas = encabezados
    df = pd.DataFrame(tabla_resultados[1:], columns=columnas)  # Excluir encabezados duplicados
    return linea_tiempo, df

# Simulación
procesos = [
    Proceso("P1", 0, 4),
    Proceso("P2", 1, 3),
    Proceso("P3", 2, 2),
    Proceso("P4", 3, 2),
]

# Ejecutar la simulación
linea_tiempo, tabla_resultados = hrn_simulacion(procesos)

# Mostrar la tabla de resultados
print("Tabla de Resultados:")
print(tabla_resultados)

# Graficar la línea de tiempo
plt.figure(figsize=(12, 6))

x = list(range(len(linea_tiempo)))
y = linea_tiempo

# Asignar colores únicos a cada proceso
procesos_ids = list(set(y))
procesos_ids = [p for p in procesos_ids if p != "Idle"]  # Excluir "Idle" de la lista de procesos
colores = plt.cm.get_cmap('tab20', len(procesos_ids))

color_dict = {pid: colores(i) for i, pid in enumerate(procesos_ids)}
color_dict["Idle"] = 'grey'

# Asignar colores a cada punto
colors = [color_dict[pid] for pid in y]

plt.scatter(x, y, c=colors, s=100, zorder=5)

# Dibujar líneas de seguimiento
for i in range(1, len(x)):
    plt.plot([x[i-1], x[i]], [y[i-1], y[i]], color='gray', linestyle='--', linewidth=1)

# Configuración del gráfico
plt.title("Simulación del algoritmo HRN (Highest Response Ratio Next)")
plt.xlabel("Tiempo")
plt.ylabel("Proceso en ejecución")
plt.yticks(procesos_ids + ["Idle"])
plt.grid(True)

# Crear una leyenda personalizada
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=color_dict[pid], label=pid) for pid in color_dict]
plt.legend(handles=legend_elements, title="Procesos", bbox_to_anchor=(1.05, 1), loc='upper left')

# Ajustar el layout para que la leyenda no se superponga
plt.tight_layout()

# Mostrar la gráfica
plt.show()
