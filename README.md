
# 🛫 Simulador de Tráfego Aéreo com Análise

Este projeto simula o controle de tráfego aéreo com visualização 3D e análises físicas e matemáticas aplicadas. Desenvolvido com **Streamlit** e **Python**, permite a simulação de decolagens, priorização de aeronaves, detecção de possíveis colisões e análise de trajetórias com ferramentas de Física e Cálculo.

---

## 🔧 Tecnologias Utilizadas

- [Python 3.9+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Matplotlib](https://matplotlib.org/)
- [NumPy](https://numpy.org/)

---

## 📁 Estrutura do Projeto

- `streamlit_app.py` → Página principal com o menu
- `1_Simulador.py` → Simulador de decolagens, movimentação e controle de tráfego aéreo
- `2_Analise1.py` → Análise Física: vetores, radar e efeito Doppler
- `3_Análise2.py` → Análise Matemática: interseção de trajetórias com Newton-Raphson e simulações com Método de Euler

---

## 🚀 Como Executar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/simulador-trafego-aereo.git
cd simulador-trafego-aereo
```

### 2. Instale as dependências

Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # no Windows use: venv\Scripts\activate
```

Instale os pacotes necessários:

```bash
pip install -r requirements.txt
```

> Se o arquivo `requirements.txt` não estiver disponível, use:

```bash
pip install streamlit matplotlib numpy
```

### 3. Execute a aplicação

```bash
streamlit run streamlit_app.py
```

---

## 📌 Funcionalidades

### 🛫 Simulador Principal

- Cadastro de aeronaves com vetores de velocidade e prioridade
- Simulação de decolagem com pistas limitadas
- Prioridade: normal, baixo combustível ou emergência
- Detecção automática de risco de colisão
- Visualização 3D das trajetórias no radar
- Registro e exibição do histórico de eventos

### 📡 Análise Física

- Visualização das trajetórias em 3D
- Cálculo da distância entre aeronaves ao longo do tempo
- Identificação de **alertas de colisão**
- Determinação do ponto de **menor distância**

### 📐 Análise Matemática

- Cálculo do ponto de interseção com o método de Newton-Raphson
- Simulações numéricas com o **Método de Euler**
- Dois cenários: rotas cruzadas e rotas paralelas
- Gráficos 3D e análise da distância ao longo do tempo

---

## 🧑‍🏫 Aplicações Educacionais

Este projeto pode ser utilizado como:

- Ferramenta de ensino interdisciplinar entre Programação, Física e Cálculo
- Simulação didática para tópicos como vetores, MRU, colisões, métodos numéricos
- Base para desenvolvimento de projetos práticos e interativos

---

## 🙋‍♂️ Contribuição

Sinta-se à vontade para abrir _issues_, sugerir melhorias ou enviar _pull requests_!

