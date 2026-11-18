import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 1. Cargar el CSV subiendo un nivel desde src
df = pd.read_csv('../data/raw/raw_no_vibration.csv')

print("\n--- ESTADÍSTICAS DEL SENSOR EN REPOSO ---")
for col in ['Acc_X', 'Acc_Y', 'Acc_Z']:
    media = df[col].mean()
    std = df[col].std()
    rms = np.sqrt(np.mean(df[col]**2))
    print(f"{col} -> Media: {media:.4f} g | Desv. Estándar (Ruido): {std:.4f} g | RMS: {rms:.4f} g")

# 2. Generar la gráfica
plt.figure(figsize=(12, 5))
tiempo_sec = (df['Time_ms'] - df['Time_ms'].iloc[0]) / 1000.0

plt.plot(tiempo_sec, df['Acc_X'], label='Acc X')
plt.plot(tiempo_sec, df['Acc_Y'], label='Acc Y')
plt.plot(tiempo_sec, df['Acc_Z'], label='Acc Z (Gravedad ~1g)')

plt.title('Señal del Acelerómetro ADXL345 en Reposo (0% Vibración)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Aceleración (g)')
plt.legend()
plt.grid(True)
plt.tight_layout()

# 3. Guardar la imagen subiendo un nivel desde src
plt.savefig('../images/no_vibration_signal.png', dpi=300)
print("\nGráfica guardada en '../images/no_vibration_signal.png'")

plt.show()