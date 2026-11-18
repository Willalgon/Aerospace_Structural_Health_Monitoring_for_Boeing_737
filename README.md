# ✈️ Predictive Maintenance System for 3D-Printed Boeing 737-800 Wing Assembly

An end-to-end Structural Health Monitoring (SHM) and Predictive Maintenance system utilizing vibration analysis on a 3D-printed Boeing 737-800 wing section. The system captures triaxial acceleration data via an ADXL345 accelerometer, transmits it through an Elegoo Uno R3 microcontroller, and processes it with Python for Machine Learning and Deep Learning classification models.

---

## 📌 1. Project Overview

Predictive maintenance in aerospace applications reduces downtime and prevents catastrophic structural failures. This project simulates real-world aero-structural degradation by subjecting a custom 3D-printed Boeing 737-800 wing assembly to mechanical vibration tests under various structural states:

1. **Nominal State (`normal`)**: Fully secured wing assembly in optimal condition.
2. **Structural Degradation (`tornillo_suelto`)**: Loose attachment bolts or structural joint play.
3. **Dynamic Imbalance (`desbalance_masa`)**: Unbalanced mass distribution (simulating ice accumulation or structural damage).

By extracting time-domain and frequency-domain features (FFT) from triaxial accelerometer data, Machine Learning models (e.g., Random Forest, SVM) and Deep Learning models (1D-CNN / LSTM) classify the structural health of the wing section in real time.

---

## 🛠️ 2. Hardware Architecture & Hardware Setup

### Component List
* **Structure**: 3D-printed Boeing 737-800 wing section with winglet (Designed via **OpenSCAD**).
* **Microcontroller**: Elegoo Uno R3 (Arduino Uno compatible).
* **Sensor**: ADXL345 Triaxial Digital Accelerometer.
* **Prototyping**: Breadboard, jumper wires, USB-A to USB-B cable.

### Circuit Wiring Diagram & Bus Configuration
The ADXL345 communicates via the **$I^2C$ protocol**. To operate in $I^2C$ mode, the `CS` (Chip Select) pin must be pulled high to $3.3\text{V}$.

| ADXL345 Pin | Elegoo Uno R3 / Connection | Function |
| :--- | :--- | :--- |
| **VCC** | Breadboard $3.3\text{V}$ Rail | Power Input ($3.3\text{V}$) |
| **CS** | Breadboard $3.3\text{V}$ Rail | Sets $I^2C$ protocol mode (Active High) |
| **GND** | Elegoo Uno R3 `GND` | Ground |
| **SDA** | Elegoo Uno R3 Pin `A4` | $I^2C$ Data Line |
| **SCL** | Elegoo Uno R3 Pin `A5` | $I^2C$ Clock Line |

---

## 📐 3. CAD & 3D Printing (OpenSCAD)

The physical structure is an aero-structural testbed modeled in **OpenSCAD**. 

* **Geometry**: Based on Boeing 737-800 wing profiles with specialized internal ribs and mounting points for sensor integration.
* **Sensor Housing**: Embedded mounting bracket designed directly on the winglet/rib assembly for rigid mechanical coupling with the ADXL345 sensor to minimize structural resonance attenuation.
* **Vibration Testing**: Mounted on a custom shake table / excitation rig to simulate aerodynamic turbulence and structural flutter.

---

## 💻 4. Software Stack & Environment

### Conda Environment (`final_project_plane`)
* **Python Version**: 3.10
* **Core Libraries**:
  * `pyserial`: Hardware serial communication with Elegoo Uno R3.
  * `pandas`, `numpy`: Data manipulation and dataset aggregation.
  * `scipy`: Digital Signal Processing (DSP) & Fast Fourier Transform (FFT).
  * `scikit-learn`: Feature extraction, training ML classifiers, evaluation metrics.
  * `torch` (PyTorch): Deep Learning models (1D Convolutional Neural Networks & LSTMs).
  * `matplotlib`, `seaborn`: Time-series and spectral analysis plotting.

---

## ⚙️ 5. Data Flow & Firmware Configuration

```
[ ADXL345 Sensor ] ──(I2C)──> [ Elegoo Uno R3 ] ──(USB 115200 baud)──> [ Python / PyCharm Pipeline ]
```

### Firmware Highlights (Arduino C++)
* **I2C Address**: `0x53`
* **Sampling Rate**: $\approx 100\text{ Hz}$ ($\Delta t = 10\text{ ms}$)
* **Output Format**: CSV stream over Serial (`Time_ms, AccX, AccY, AccZ`)
* **Sensitivity**: $\pm 2\text{g}$ range ($3.9\text{ mg/LSB}$ scale factor)

---

## 📊 6. Machine Learning & Signal Processing Pipeline

### 6.1 Feature Engineering
Raw vibration data is chunked into sliding time windows (e.g., 2-second windows with 50% overlap). For each window, two feature sets are extracted:

1. **Time-Domain Features**:
   * Root Mean Square ($\text{RMS} = \sqrt{\frac{1}{N} \sum x_i^2}$)
   * Peak-to-Peak Amplitude
   * Variance, Standard Deviation
   * Kurtosis and Skewness (indicative of impulse shocks from loose structural joints)

2. **Frequency-Domain Features (FFT via `scipy.fft`)**:
   * Dominant peak frequencies
   * Spectral energy distribution across frequency bands
   * Spectral Centroid

### 6.2 Model Architecture
* **Baseline ML**: Random Forest Classifier & Support Vector Machines (SVM).
* **Deep Learning (PyTorch)**: 
  * 1D-CNN taking raw 3-channel acceleration series (`AccX`, `AccY`, `AccZ`) directly to learn spatial-temporal feature maps.
  * Multi-class output: `[normal, tornillo_suelto, desbalance_masa]`.

---

## 📂 7. Project Folder Structure

```text
final_project_plane/
├── data/
│   ├── raw/                  # CSV raw recordings from serial acquisition
│   └── processed/            # Processed windowed features ready for training
├── models/                   # Saved model weights (.pkl, .pt)
├── src/
│   ├── 01_data_acquisition.py # Serial reader & automatic CSV logger
│   ├── 02_feature_engineering.py # FFT & statistical feature extraction
│   └── 03_train_model.py     # PyTorch / Scikit-Learn training script
├── docs/                     # Schematics, OpenSCAD files, reports
├── main.py                   # Real-time inference entry point
└── README.md                 # Project documentation
```

---

## 🚀 8. Quick Start Guide

1. **Upload Firmware**: Load the C++ sketch onto the Elegoo Uno R3 using Arduino IDE.
2. **Activate Environment**:
   ```bash
   conda activate final_project_plane
   ```
3. **Run Data Acquisition Script**:
   ```bash
   python src/01_data_acquisition.py
   ```
4. **Train Classification Model**:
   ```bash
   python src/03_train_model.py
   ```
   






------
MI STUFF

Lo primero que voy a obtener son los resultados del sensor si no hay vibracion (sin haber conectado aun la shake table). Esto lo almacenaremos como una clase que cumple dos funciones criticas:
1. Deteccion de fallo de instrumentacion (Sensor Failure)
2. Linea de base y calibracion (Baseline and Noise Floor): ruido de fondo inherente del ADXL345 (su desviacion estandar en reposo) y registrar el vector de gravedad constante (1.0g en el eje vertical Z debido a la gravedad terrestre).

Primero de todo hay que entender como funciona este sistema. Basicamente comprende tres niveles:
el sensor -> la placa Egoo (microcontrolador) -> ordenador.
1. Primero de todo ejecutamos en arduino el codigo C++. Este codigo se traduce a lenguaje maquina (ceros y unos en formato .hex). Este codigo ahora vive dentro de la placa.
En este instante la placa Elegoo esta ejecutando en bucle infinito a la velocidad que le hemos marcado (delay(10), unos 100 ciclos por segundo)
2. El baud rate es la velocidad de comunicacion en bits por segundo a traves del cable serie. Para mantenimiento necesitamos capturar vibraciones de alta frecuencia. 
3. Al ejecutar el programa de python, los resultados los almacenaremos en el ordenador en local. Por eso debemos de cerrar la pestana del 'Monitor Serie' porque un puerto COM solo puede ser abierto y leido por un programa a la vez.

### no_vibration.py:
llamamos a serial.Serial('COM3', 115200). En este instante nos conectamos al puerto serie del cual obtendremos los datos.
A continuacion procesamos los datos y los almacenamos en 4 columnas. Estas cuatro columnas las definimos asi ya que es como hemos definido el codigo C++ en arduino.
Obtenemos datos para 15 segundos del sensor.
Los almacenamos en data/raw.

Las caracteristicas del dataset serian:
#### Time_ms: para clasificar cada medicion en el tiempo en milisegundos
#### Acc_X: aceleracion a lo largo del eje longitudinal o tranversal del sensor en unidades de fuerza de gravedad (g)
#### Acc_Y: aceleración a lo largo del otro eje plano del sensor
#### Acc_Z: aceleracion vertical. Como podemos ver no tenemos un valor de 1, esto se debe a que el acelerometro no lo tenemos apollado con una pequena inclinacion fisica sobre el ala del avion.
IMPORTANTE:
Una buena comprobacion para ver si nuestros datos estan bien:
raiz de (Acc_X)^2 + (Acc_Y)^2 + (Acc_X)^2 = 1 (aproximadamente)

La variacion que podemos encontrar entre las diversas muestras se debe a ruido termico y electrico natural (noise floor) del acelerometro.

### no_vibration_quality.py:
Con este archivo ensenamos metricas como la desviacion estandar (Ruido) la media y el RMS. 
Tambien imprimimos un grafico (pegar).
