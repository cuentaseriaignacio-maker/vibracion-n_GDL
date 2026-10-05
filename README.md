# vibracion-n_GDL

# 🌀 Simulador de Frecuencias Propias y Formas Modales (M-DOF)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-red.svg)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-brightgreen.svg)
![SciPy](https://img.shields.io/badge/SciPy-Linalg-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Simulador interactivo en **Python**, **Streamlit**, **SciPy** y **Plotly** diseñado para la enseñanza universitaria y técnica de sistemas mecánicos de **Múltiples Grados de Libertad (2-DOF y 3-DOF)**.

Permite calcular en tiempo real las **Frecuencias Propias (\\(\omega_n\\))**, las **Formas Modales (Autovectores)**, los **Nodos de Vibración** y observar la respuesta espectral (FFT) con múltiples picos de resonancia.

---

## 🚀 Acceso a la Aplicación Web

Puedes utilizar el simulador directamente desde tu navegador sin instalar nada:
👉 **[Abrir Simulador M-DOF en Streamlit Cloud](https://tu-usuario.streamlit.app)** *(reemplaza con la URL de tu app)*

---

## 🕹 Funcionalidades Principales

1. **Configuración de Grados de Libertad (2-DOF y 3-DOF):**
   - Selección interactiva entre 2 o 3 masas acopladas.
   - Modificación en tiempo real de masas (\\(m_1, m_2, m_3\\)) y rigideces de resorte (\\(k_1, k_2, k_3, k_4\\)).

2. **Cálculo Matricial de Autovalores y Autovectores:**
   - Resolución automática del problema de autovalores \\(\det([K] - \omega^2 [M]) = 0\\).
   - Normalización de formas modales (deformadas geométricas de las masas).

3. **Animación Modal Interactiva (Play / Pausa):**
   - Visualización de cada **Modo Puro** de oscilación o de la **Superposición Total**.
   - Identificación visual del **primer modo** (en fase), **segundo modo** (oposición de fase y nodo intermedio) y **tercer modo**.

4. **Análisis de Respuesta Temporal y Espectro FFT:**
   - Gráfica de desplazamiento \\(x_i(t)\\) para cada masa.
   - Espectro de frecuencias con marcado automático de los múltiples picos de resonancia.

---

## 📐 Fundamentos Físicos y Ecuaciones

Para un sistema libre de \\(N\\) grados de libertad, la ecuación matricial de movimiento es:

\\[[M]\{\ddot{x}(t)\} + [K]\{x(t)\} = \{0\}\\]

Al asumir una solución armónica \\(\{x(t)\} = \{\phi\} \cos(\omega t)\\), se obtiene el **Problema de Autovalores**:

\\[([K] - \omega^2 [M])\{\phi\} = \{0\}\\]

### Conceptos Clave

* **Frecuencias Naturales (\\(\omega_{n1} < \omega_{n2} < \dots < \omega_{nN}\\)):**
  \\[\omega_{ni} \quad [\text{rad/s}], \qquad f_{ni} = \frac{\omega_{ni}}{2\pi} \quad [\text{Hz}]\\]

* **Formas Modales (\\(\{\phi\}_i\\)):**
  Describen la relación de amplitudes y la dirección relativa de movimiento entre las masas para el modo \\(i\\).
  - **Modo 1 (Modo Fundamental):** Las masas se mueven en la misma dirección (en fase).
  - **Modos Superiores:** Aparecen puntos de amplitud nula (**Nodos de Vibración**).

---

## 🛠️ Ejecución Local en PC

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/simulador-vibraciones-mdof.git
cd simulador-vibraciones-mdof

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Lanzar la app
streamlit run app.py
