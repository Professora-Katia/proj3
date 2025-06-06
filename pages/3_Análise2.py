
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Cálculo - Interseção", layout="wide")
st.title(" Análise de Interseção entre Aeronaves")

if "trajetorias" not in st.session_state:
    st.warning("⚠️ Execute o simulador com ao menos duas aeronaves para gerar dados.")
    st.stop()

rA = np.array(st.session_state["trajetorias"]["rA"])
rB = np.array(st.session_state["trajetorias"]["rB"])

if len(rA) < 3 or len(rB) < 3:
    st.warning(" Trajetórias insuficientes. Avance mais a simulação.")
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

rA_final = posicao(rA0, vA, t)
rB_final = posicao(rB0, vB, t)
d_min = np.linalg.norm(rA_final - rB_final)

st.subheader("📊 Resultados da Interseção")
st.write(f"**Instante de menor distância:** {t:.2f} s")
st.write(f"**Distância mínima:** {d_min:.2f} unidades")
st.write(f"**Posição da Aeronave A:** {rA_final}")
st.write(f"**Posição da Aeronave B:** {rB_final}")
if d_min < 5:
    st.warning(" Risco de colisão detectado!")

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

st.title("✈️ Simulação Numérica de Trajetórias")

# Função para simular trajetória usando Método de Euler
def simular_trajetoria(pos_inicial, vel, dt, passos):
    trajetoria = [np.array(pos_inicial)]
    for _ in range(passos):
        nova_pos = trajetoria[-1] + dt * np.array(vel)
        trajetoria.append(nova_pos)
    return np.array(trajetoria)

dt = 1.0
passos = 20

cenarios = {
    "Cenário 1 - Rotas Cruzadas": {
        "A_inicial": [0, 0, 0],
        "A_vel": [1, 1, 0],
        "B_inicial": [10, 0, 0],
        "B_vel": [-1, 1, 0]
    },
    "Cenário 2 - Rotas Paralelas": {
        "A_inicial": [0, 0, 0],
        "A_vel": [1, 0, 0],
        "B_inicial": [0, 5, 0],
        "B_vel": [1, 0, 0]
    }
}

cenario = st.selectbox("Escolha o cenário de simulação:", list(cenarios.keys()))
dados = cenarios[cenario]

rA = simular_trajetoria(dados["A_inicial"], dados["A_vel"], dt, passos)
rB = simular_trajetoria(dados["B_inicial"], dados["B_vel"], dt, passos)


distancias = np.linalg.norm(rA - rB, axis=1)
min_idx = np.argmin(distancias)
min_dist = distancias[min_idx]
tempo_critico = min_idx * dt

st.subheader(" Resultados da Simulação")
st.write(f"**Menor distância:** {min_dist:.2f} unidades no tempo t = {tempo_critico:.1f} s")
st.write(f"**Posição da Aeronave A:** {rA[min_idx]}")
st.write(f"**Posição da Aeronave B:** {rB[min_idx]}")

# Gráfico das trajetórias
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(121, projection='3d')
ax.plot(rA[:, 0], rA[:, 1], rA[:, 2], label="Aeronave A", color='blue')
ax.plot(rB[:, 0], rB[:, 1], rB[:, 2], label="Aeronave B", color='green')
ax.scatter(*rA[min_idx], color='red', label="Ponto Crítico A")
ax.scatter(*rB[min_idx], color='orange', label="Ponto Crítico B")
ax.set_title("Trajetórias 3D")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.legend()


ax2 = fig.add_subplot(122)
tempos = np.arange(passos + 1) * dt
ax2.plot(tempos, distancias, label="Distância", color='purple')
ax2.axvline(tempo_critico, color='red', linestyle='--', label="Ponto Crítico")
ax2.scatter(tempo_critico, min_dist, color='red')
ax2.set_title("Distância entre Aeronaves")
ax2.set_xlabel("Tempo (s)")
ax2.set_ylabel("Distância")
ax2.legend()

st.pyplot(fig)


if st.button("🔙 Voltar ao Início"):
    st.switch_page("streamlit app")
