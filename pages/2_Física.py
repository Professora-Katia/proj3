
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Física - Radar", layout="wide")
st.title("📡 Simulação de Radar com Vetores e Efeito Doppler")

# Obter dados do simulador
if "trajetorias" not in st.session_state:
    st.warning("⚠️ Os dados do simulador não foram encontrados. Exibindo exemplo.")

    rA_traj = np.array([[t, 0.5*t, 0.1*t] for t in range(20)])
    rB_traj = np.array([[t, t, 0] for t in range(20)])
    vA = np.array([1.0, 0.5, 0.1])
    vB = np.array([1.0, 1.0, 0])
else:
    rA_traj = np.array(st.session_state["trajetorias"]["rA"])
    rB_traj = np.array(st.session_state["trajetorias"]["rB"])
    vA = np.array(st.session_state["trajetorias"]["vA"])
    vB = np.array(st.session_state["trajetorias"]["vB"])

def velocidade_radial(r, v):
    return np.dot(r, v) / np.linalg.norm(r)

def distancia(r1, r2):
    return np.linalg.norm(r1 - r2)

def emitir_alerta(r1, v1, r2, v2, limite=5.0):
    d = distancia(r1, r2)
    vr = velocidade_radial(r2 - r1, v2 - v1)
    if d < limite and vr < 0:
        return True, d, vr
    return False, d, vr

n = min(len(rA_traj), len(rB_traj))
tempos = range(n)
distancias, alertas = [], []

for i in tempos:
    alerta, d, vr = emitir_alerta(rA_traj[i], vA, rB_traj[i], vB)
    alertas.append(alerta)
    distancias.append(d)

fig = plt.figure(figsize=(10, 5))
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot(rA_traj[:,0], rA_traj[:,1], rA_traj[:,2], label="Aeronave A")
ax1.plot(rB_traj[:,0], rB_traj[:,1], rB_traj[:,2], label="Aeronave B")
ax1.set_title("Trajetórias 3D das Aeronaves")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_zlabel("Z")
ax1.legend()

ax2 = fig.add_subplot(122)
ax2.plot(tempos, distancias, label="Distância")
for i, alerta in enumerate(alertas):
    if alerta:
        ax2.axvline(tempos[i], color='red', linestyle='--')
ax2.set_title("Distância entre Aeronaves (tempo)")
ax2.set_xlabel("Tempo (s)")
ax2.set_ylabel("Distância")
ax2.legend()

st.pyplot(fig)

if st.button("🔙 Voltar ao Início"):
    st.switch_page("Simulador")
