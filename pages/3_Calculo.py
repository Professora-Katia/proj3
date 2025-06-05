
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Cálculo - Interseção com Newton-Raphson", layout="wide")
st.title("🧮 Análise de Interseção entre Aeronaves com Newton-Raphson")

# Verifica se dados da simulação estão disponíveis
if "trajetorias" not in st.session_state:
    st.warning("⚠️ Execute o simulador com ao menos duas aeronaves para gerar dados.")
    st.stop()

rA = np.array(st.session_state["trajetorias"]["rA"])
rB = np.array(st.session_state["trajetorias"]["rB"])

if len(rA) < 3 or len(rB) < 3:
    st.warning("⚠️ Trajetórias insuficientes. Avance mais a simulação.")
    st.stop()

# Ignora o primeiro ponto (posição inicial coincidente)
rA0 = rA[1]
vA = rA[2] - rA[1]
rB0 = rB[1]
vB = rB[2] - rB[1]

def posicao(r0, v, t):
    return r0 + v * t

def distancia2(t):
    rA = posicao(rA0, vA, t)
    rB = posicao(rB0, vB, t)
    return np.sum((rA - rB) ** 2)

def derivada(f, t, h=1e-5):
    return (f(t + h) - f(t - h)) / (2 * h)

def segunda_derivada(f, t, h=1e-5):
    return (f(t + h) - 2 * f(t) + f(t - h)) / (h ** 2)

# Newton-Raphson para encontrar t mínimo (com t >= 0)
t = 0.0
for _ in range(20):
    f1 = derivada(distancia2, t)
    f2 = segunda_derivada(distancia2, t)
    if abs(f2) < 1e-10:
        break
    t = t - f1 / f2
    if t < 0:
        t = 0.0
        break

# Resultados
rA_final = posicao(rA0, vA, t)
rB_final = posicao(rB0, vB, t)
d_min = np.linalg.norm(rA_final - rB_final)

st.subheader("📊 Resultados da Interseção")
st.write(f"**Instante de menor distância:** {t:.2f} s")
st.write(f"**Distância mínima:** {d_min:.2f} unidades")
st.write(f"**Posição da Aeronave A:** {rA_final}")
st.write(f"**Posição da Aeronave B:** {rB_final}")
if d_min < 5:
    st.warning("⚠️ Risco de colisão detectado!")

# Gráfico
ts = np.linspace(0, 10, 200)
ds = [np.sqrt(distancia2(ti)) for ti in ts]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(ts, ds, label="Distância entre A e B")
ax.axvline(t, color='red', linestyle='--', label="t mínimo")
ax.set_title("Distância entre Aeronaves ao Longo do Tempo")
ax.set_xlabel("Tempo (s)")
ax.set_ylabel("Distância")
ax.legend()
ax.grid(True)
st.pyplot(fig)

if st.button("🔙 Voltar ao Início"):
    st.switch_page("streamlit app")
