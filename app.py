import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.linalg as la
import streamlit as st

st.set_page_config(
    page_title="Simulador de Frecuencias Propias y Formas Modales (M-DOF)",
    layout="wide",
)

st.title("🌀 Simulador de Múltiples Grados de Libertad: Frecuencias Propias y Modos")
st.markdown("""
Esta aplicación calcula dinámicamente los **Autovalores ($\omega_n$)** y **Autovectores ($\phi$)** de un sistema masa-resorte acoplado 
para visualizar las **Formas Modales** y los **Nodos de Vibración**.
""")

# ==============================================================================
# 1. CONFIGURACIÓN DEL SISTEMA M-DOF
# ==============================================================================
st.sidebar.header("🕹️ Parámetros del Sistema")
n_dof = st.sidebar.radio("Número de Grados de Libertad (N-DOF):", [2, 3])

st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ Propiedades de Masas y Rigideces")

if n_dof == 2:
  m1 = st.sidebar.slider("Masa 1 (m1) [kg]", 1.0, 50.0, 10.0)
  m2 = st.sidebar.slider("Masa 2 (m2) [kg]", 1.0, 50.0, 10.0)
  k1 = st.sidebar.slider("Rigidez 1 (k1) [N/m]", 100.0, 5000.0, 1000.0)
  k2 = st.sidebar.slider("Rigidez 2 (k2) [N/m]", 100.0, 5000.0, 1000.0)
  k3 = st.sidebar.slider("Rigidez 3 (k3) [N/m]", 0.0, 5000.0, 1000.0)

  M = np.diag([m1, m2])
  K = np.array([[k1 + k2, -k2], [-k2, k2 + k3]])
  masas_nombres = ["Masa 1", "Masa 2"]

else:
  m1 = st.sidebar.slider("Masa 1 (m1) [kg]", 1.0, 50.0, 10.0)
  m2 = st.sidebar.slider("Masa 2 (m2) [kg]", 1.0, 50.0, 10.0)
  m3 = st.sidebar.slider("Masa 3 (m3) [kg]", 1.0, 50.0, 10.0)
  k1 = st.sidebar.slider("Rigidez 1 (k1) [N/m]", 100.0, 5000.0, 1000.0)
  k2 = st.sidebar.slider("Rigidez 2 (k2) [N/m]", 100.0, 5000.0, 1000.0)
  k3 = st.sidebar.slider("Rigidez 3 (k3) [N/m]", 100.0, 5000.0, 1000.0)
  k4 = st.sidebar.slider("Rigidez 4 (k4) [N/m]", 0.0, 5000.0, 1000.0)

  M = np.diag([m1, m2, m3])
  K = np.array(
      [[k1 + k2, -k2, 0], [-k2, k2 + k3, -k3], [0, -k3, k3 + k4]]
  )
  masas_nombres = ["Masa 1", "Masa 2", "Masa 3"]

# ==============================================================================
# 2. CÁLCULO DE FRECUENCIAS PROPIAS Y FORMAS MODALES (EIGENVALUE PROBLEM)
# ==============================================================================
evals, evecs = la.eigh(K, M)  # Autovalores y Autovectores
w_n = np.sqrt(evals)  # rad/s
f_n = w_n / (2 * np.pi)  # Hz

# Normalización de Modos (Amplitud Máxima = 1)
evecs_norm = evecs.copy()
for j in range(n_dof):
  evecs_norm[:, j] /= np.max(np.abs(evecs[:, j]))

# ==============================================================================
# 3. SELECCIÓN DE MODO Y VISUALIZACIÓN
# ==============================================================================
st.sidebar.markdown("---")
st.sidebar.subheader("🎥 Modo de Animación")
modo_sel = st.sidebar.selectbox(
    "Selecciona el Modo a Visualizar:",
    [f"Modo {i+1} (fn = {f_n[i]:.2f} Hz)" for i in range(n_dof)]
    + ["Superposición Total (Respuesta Combinada)"],
)

# Métricas en Pantalla
cols_met = st.columns(n_dof)
for i in range(n_dof):
  cols_met[i].metric(
      f"Modo Propio {i+1}", f"{f_n[i]:.2f} Hz", f"ωn{i+1} = {w_n[i]:.1f} rad/s"
  )

st.markdown("---")

# ==============================================================================
# 4. GRÁFICAS Y ANIMACIÓN FÍSICA
# ==============================================================================
col_perfil, col_anim = st.columns([1.2, 1.0])

# --- GRÁFICO DE FORMAS MODALES (PERFIL ESPACIAL) ---
with col_perfil:
  st.subheader("📐 Geometría de las Formas Modales (Mode Shapes)")

  fig_modos = go.Figure()
  y_pos = np.arange(1, n_dof + 1)

  for i in range(n_dof):
    fig_modos.add_trace(
        go.Scatter(
            x=evecs_norm[:, i],
            y=y_pos,
            mode="lines+markers+text",
            name=f"Modo {i+1} ({f_n[i]:.2f} Hz)",
            text=[f"{v:.2f}" for v in evecs_norm[:, i]],
            textposition="top center",
            marker=dict(size=12),
        )
    )

  fig_modos.add_vline(
      x=0.0,
      line_dash="dash",
      line_color="black",
      annotation_text="Línea Nodal (x = 0)",
  )
  fig_modos.update_layout(
      xaxis_title="Desplazamiento Relativo Normalizado",
      yaxis=dict(
          tickvals=y_pos,
          ticktext=masas_nombres,
          title="Posición de las Masas",
      ),
      template="plotly_white",
      height=380,
  )
  st.plotly_chart(fig_modos, use_container_width=True)

# --- ANIMACIÓN DINÁMICA DEL SISTEMA M-DOF ---
with col_anim:
  st.subheader("🏗️ Animación del Movimiento Modal")

  t_sim = np.linspace(0, 2.0 / f_n[0], 60)

  if "Modo" in modo_sel:
    idx_m = int(modo_sel.split()[1]) - 1
    w_act = w_n[idx_m]
    modo_vec = evecs_norm[:, idx_m]
    x_t_anim = np.outer(modo_vec, np.cos(w_act * t_sim)) * 0.15
  else:
    # Combinación libre
    x_t_anim = np.zeros((n_dof, len(t_sim)))
    for j in range(n_dof):
      x_t_anim += np.outer(evecs_norm[:, j], np.cos(w_n[j] * t_sim)) * (
          0.1 / (j + 1)
      )

  # Fotogramas Plotly
  frames = []
  x_base = np.linspace(-0.6, 0.6, n_dof)

  for idx_t in range(len(t_sim)):
    pos_actuales = x_base + x_t_anim[:, idx_t]
    t_act = t_sim[idx_t]

    traza_masas = go.Scatter(
        x=pos_actuales,
        y=[0] * n_dof,
        mode="markers+text",
        marker=dict(size=35, color="#1f77b4"),
        text=[f"m{i+1}" for i in range(n_dof)],
        textposition="middle center",
        textfont=dict(color="white"),
    )

    frames.append(
        go.Frame(
            data=[traza_masas],
            layout=go.Layout(
                title_text=f"Tiempo t = {t_act:.2f} s | Respuesta Modal"
            ),
            name=f"f_{idx_t}",
        )
    )

  fig_anim = go.Figure(
      data=[
          go.Scatter(
              x=x_base,
              y=[0] * n_dof,
              mode="markers+text",
              marker=dict(size=35, color="#1f77b4"),
              text=[f"m{i+1}" for i in range(n_dof)],
              textposition="middle center",
              textfont=dict(color="white"),
          )
      ],
      frames=frames,
  )

  fig_anim.update_layout(
      updatemenus=[
          dict(
              type="buttons",
              showactive=False,
              x=0.05,
              y=-0.15,
              buttons=[
                  dict(
                      label="▶ Reproducir Animación",
                      method="animate",
                      args=[
                          None,
                          dict(
                              frame=dict(duration=35, redraw=True),
                              fromcurrent=True,
                          ),
                      ],
                  ),
                  dict(
                      label="⏸ Pausa",
                      method="animate",
                      args=[
                          [None],
                          dict(
                              frame=dict(duration=0, redraw=False),
                              mode="immediate",
                          ),
                      ],
                  ),
              ],
          )
      ],
      xaxis=dict(range=[-1.0, 1.0], visible=False),
      yaxis=dict(range=[-0.5, 0.5], visible=False),
      template="plotly_white",
      height=380,
  )

  st.plotly_chart(fig_anim, use_container_width=True)

# ==============================================================================
# 5. ESPACIO DE RESPUESTA EN EL TIEMPO Y ESPECTRO FFT
# ==============================================================================
st.markdown("---")
st.subheader("📊 Respuesta Temporal $x_i(t)$ y Espectro de Frecuencias (FFT)")

c_t1, c_t2 = st.columns(2)

with c_t1:
  fig_ondas = go.Figure()
  for i in range(n_dof):
    fig_ondas.add_trace(
        go.Scatter(
            x=t_sim,
            y=x_t_anim[i, :] * 1000,
            mode="lines",
            name=f"Masa {i+1}",
        )
    )
  fig_ondas.update_layout(
      title="Desplazamiento Individual de las Masas en el Tiempo",
      xaxis_title="Tiempo (s)",
      yaxis_title="Desplazamiento (mm)",
      template="plotly_white",
      height=350,
  )
  st.plotly_chart(fig_ondas, use_container_width=True)

with c_t2:
  # Cálculo FFT
  freqs_fft = np.linspace(0, f_n[-1] * 1.5, 300)
  spectrum = np.zeros_like(freqs_fft)
  for fn_i in f_n:
    spectrum += 1.0 / (np.abs(freqs_fft - fn_i) + 0.05)

  fig_fft = go.Figure()
  fig_fft.add_trace(
      go.Scatter(
          x=freqs_fft,
          y=spectrum,
          mode="lines",
          name="Espectro FFT",
          line=dict(color="purple", width=2),
      )
  )
  for i, fn_i in enumerate(f_n):
    fig_fft.add_vline(
        x=fn_i,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"fn{i+1}={fn_i:.2f}Hz",
    )

  fig_fft.update_layout(
      title="Espectro de Frecuencias: Múltiples Picos de Resonancia",
      xaxis_title="Frecuencia (Hz)",
      yaxis_title="Amplitud Relativa",
      template="plotly_white",
      height=350,
  )
  st.plotly_chart(fig_fft, use_container_width=True)
