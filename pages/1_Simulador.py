from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
from abc import ABC, abstractmethod
from enum import Enum
import pandas as pd
import random

class PistaOcupadaException(Exception):
    pass

class Prioritizavel(ABC):
    @property
    @abstractmethod
    def prioridade(self): pass

class AeronaveBase(ABC):
    @abstractmethod
    def solicitar_decolagem(self): pass
    @abstractmethod
    def atualizar_status(self): pass
    @abstractmethod
    def obter_posicao(self): pass

class StatusAeronave(Enum):
    EM_ESPERA = "🕓 Em espera"
    AUTORIZADA = "🛫 Autorizada"
    EM_VOO = "✈️ Em voo"
    FINALIZADA = "✅ Finalizada"

class Pista:
    def __init__(self, id):
        self.id = id
        self.ocupada = False

    def ocupar(self):
        if self.ocupada:
            raise PistaOcupadaException(f"Pista {self.id} está ocupada.")
        self.ocupada = True

    def liberar(self):
        self.ocupada = False

class Aeronave(AeronaveBase, Prioritizavel):
    def __init__(self, nome, r0, v, prioridade):
        self.nome = nome
        self.r0 = np.array(r0)
        self.v = np.array(v)
        self._prioridade = prioridade
        self.status = StatusAeronave.EM_ESPERA
        self.t = 0
        self.pista = None
        self.eventos = []
        self.cor = (random.random(), random.random(), random.random())

    @property
    def prioridade(self):
        ordem = {"emergencia": 1, "baixo_combustivel": 2, "normal": 3}
        return ordem.get(self._prioridade, 3)

    def solicitar_decolagem(self):
        if self.status == StatusAeronave.EM_ESPERA:
            self.status = StatusAeronave.AUTORIZADA
            self.eventos.append("Autorizada para decolagem")

    def associar_pista(self, pista):
        self.pista = pista

    def atualizar_status(self):
        if self.status == StatusAeronave.AUTORIZADA:
            self.pista.ocupar()
            self.status = StatusAeronave.EM_VOO
            self.eventos.append("Decolou pela pista " + str(self.pista.id))
        elif self.status == StatusAeronave.EM_VOO:
            self.t += 1
            
        if self.t >= 2:
            if self.t == 2:
                self.pista.liberar()
                self.eventos.append("Pista liberada")
            if self.t >= 6:
                self.status = StatusAeronave.FINALIZADA
                self.eventos.append("Saiu do espaço aéreo")

                self.status = StatusAeronave.FINALIZADA
                self.pista.liberar()
                self.eventos.append("Finalizou o voo")

    def obter_posicao(self):
        return self.r0 + self.v * self.t

class TorreControle:
    def __init__(self):
        self.pistas = [Pista(1), Pista(2)]
        self.aeronaves = []
        self.log = []

    def cadastrar_aeronave(self, nome, r0, v, prioridade):
        a = Aeronave(nome, r0, v, prioridade)
        self.aeronaves.append(a)
        self.log.append(f"Aeronave {nome} cadastrada.")

    def atualizar(self):
        fila = sorted([a for a in self.aeronaves if a.status == StatusAeronave.EM_ESPERA], key=lambda x: x.prioridade)
        for aeronave in fila:
            pista_livre = next((p for p in self.pistas if not p.ocupada), None)
            if pista_livre:
                aeronave.associar_pista(pista_livre)
                aeronave.solicitar_decolagem()
        for a in self.aeronaves:
            try:
                a.atualizar_status()
            except PistaOcupadaException as e:
                self.log.append(f"{a.nome}: {str(e)}")
        self.detectar_colisoes()

    def detectar_colisoes(self):
        voando = [a for a in self.aeronaves if a.status == StatusAeronave.EM_VOO]
        for i in range(len(voando)):
            for j in range(i + 1, len(voando)):
                pos1 = voando[i].obter_posicao()
                pos2 = voando[j].obter_posicao()
                if np.linalg.norm(pos1 - pos2) < 5:
                    msg = f"⚠️ Risco de colisão entre {voando[i].nome} e {voando[j].nome}!"
                    if msg not in self.log:
                        self.log.append(msg)

    def aeronaves_ativas(self):
        return [a for a in self.aeronaves if a.status != StatusAeronave.FINALIZADA]

    def obter_log(self):
        return self.log[-10:]

    def fila_espera(self):
        return sorted(
            [a for a in self.aeronaves if a.status == StatusAeronave.EM_ESPERA],
            key=lambda x: x.prioridade
        )

st.set_page_config("Simulador Torre ", layout="wide")
st.title("🛫 Simulador com Trajetos ")

if "torre" not in st.session_state:
    st.session_state.torre = TorreControle()

torre = st.session_state.torre

with st.sidebar:
    st.subheader("✈️ Cadastro de Aeronave")
    nome = st.text_input("Nome da Aeronave")
    st.markdown("📍 Posição inicial fixa: `[0.0, 0.0, 0.0]`")
    vetor_v = st.text_input("Velocidade (ex: 1,2,0.5)", "1,2,0.5")
    prioridade = st.selectbox("Prioridade", ["normal", "baixo_combustivel", "emergencia"])
    if st.button("Cadastrar Aeronave"):
        r0 = [0.0, 0.0, 0.0]
        try:
            v = [float(x) for x in vetor_v.split(",")]
            if len(v) != 3:
                raise ValueError
            torre.cadastrar_aeronave(nome, r0, v, prioridade)
            st.success("Aeronave cadastrada!")
        except:
            st.error("Erro no vetor de velocidade. Use 3 números separados por vírgula.")

    st.subheader("🔁 Simulação")
    if st.button("Avançar Simulação"):
        torre.atualizar()

    # Registrar trajetórias para a aba Física/Cálculo
    aeronaves_ativas = torre.aeronaves_ativas()
    if len(aeronaves_ativas) >= 2:
        a1 = aeronaves_ativas[0]
        a2 = aeronaves_ativas[1]

        def calcular_trajetoria(a):
            return [a.r0 + a.v * t for t in range(a.t + 1)]

        st.session_state["trajetorias"] = {
            "rA": calcular_trajetoria(a1),
            "vA": a1.v.tolist(),
            "rB": calcular_trajetoria(a2),
            "vB": a2.v.tolist()
        }


    if st.button("🔄 Resetar"):
        st.session_state.clear()

st.subheader("📡 Radar")

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')



for aeronave in torre.aeronaves:
    pos = aeronave.obter_posicao()
    traj = [aeronave.r0 + aeronave.v * t for t in range(aeronave.t + 1)]
    traj = np.array(traj)
    ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], linestyle="--", color=aeronave.cor)
    ax.text(pos[0], pos[1], pos[2], '✈️', fontsize=12, ha="center", va="center", color="black")

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
st.pyplot(fig)

st.subheader("📋 Status das Aeronaves")
tabela = []
for a in torre.aeronaves:
    tabela.append({
        "Nome": a.nome,
        "Status": a.status.value,
        "Tempo de Voo": a.t if a.status in [StatusAeronave.EM_VOO, StatusAeronave.FINALIZADA] else 0,
        "Prioridade": a._prioridade,
        "Pista": a.pista.id if a.pista else "-"
    })
st.dataframe(pd.DataFrame(tabela))

st.subheader("📝 Log de Eventos")
for linha in torre.obter_log():
    st.text(linha)


# Botão de navegação

import streamlit as st
if st.button("🔙 Voltar ao Início"):
    st.switch_page("streamlit_app.py")
