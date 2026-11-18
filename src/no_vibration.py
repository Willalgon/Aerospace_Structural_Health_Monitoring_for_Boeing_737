import serial # Nos permite comunicarnos por puerto serie con hardware (Arduino)
import pandas as pd
import time # Para medir tiempos

PUERTO = 'COM3' # Puerto al que tenemos conectado el Elegoo
BAUD_RATE = 115200 # velocidad de transmision en Baudios (bits por segundo). Debe coincidir con el microcontrolador
DURATION_SECONDS = 15 # Tiempo capturando datos del sensor

ser = serial.Serial(PUERTO, BAUD_RATE) # Abrimos la conexion en el puerto que hemos especificado a la velocidad configurada
time.sleep(2) # Esperamos 2 segundo tras abrir el puerto serie. Al abrirlo muchso microcontroladores se reinician

print(f"Capturing baseline (0% vibration)")
datos = [] # para almacenar las lecturas numericas
inicio = time.time() # Guardamos el timestamp como punto de inicio

# Mientras la diferencia entre el tiempo de actual y el tiempo de inicio sea menor a 15 segundos seguimos recopilando datos.
while (time.time() - inicio) < DURATION_SECONDS:
    # lee una linea de texto del puerto serie hasta encontrar un salto de linea
    linea = ser.readline().decode('utf-8', errors='ignore').strip()
    if linea:
        partes = linea.split(',')
        if len(partes) == 4:
            try:
                datos.append([float(p) for p in partes])
            except ValueError:
                pass

ser.close()

# Crear DataFrame y asignar etiqueta
df = pd.DataFrame(datos, columns=['Time_ms', 'Acc_X', 'Acc_Y', 'Acc_Z'])
df['Label'] = 'sin_vibracion'

df.to_csv('../data/raw/raw_no_vibration.csv', index=False)
print(f"Captura finalizada: {len(df)} muestras guardadas en '{'../data/raw/raw_no_vibration.csv'}'")