import streamlit as st
import random
import numpy as np

# --------------------------
# Palavras por fase
# --------------------------
fases = [
    ["PLATAO", "ETICA", "SOCRATES", "VIRTUDE", "RAZAO"],
    ["NIETZSCHE", "VALORES", "ETERNORETORNO", "MORAL", "SUPERHOMEM"],
    ["BEAUVOIR", "EXISTENCIA", "LIBERDADE", "OPRESSAO", "FEMINISMO"],
    ["KANT", "CATEGORIA", "IMPERATIVO", "AUTONOMIA", "DEVER"],
    ["HEGEL", "DIALETICA", "TESE", "ANTITESE", "SINTESE"],
]

# --------------------------
# Função para gerar grade
# --------------------------

def gerar_grade(palavras, tamanho=14):
    grade = np.full((tamanho, tamanho), ' ')
    direcoes = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    
    for palavra in palavras:
        colocada = False
        tentativas = 0
        while not colocada and tentativas < 100:
            direcao = random.choice(direcoes)
            linha = random.randint(0, tamanho - 1)
            coluna = random.randint(0, tamanho - 1)
            fim_linha = linha + direcao[0] * len(palavra)
            fim_coluna = coluna + direcao[1] * len(palavra)
            
            if 0 <= fim_linha < tamanho and 0 <= fim_coluna < tamanho:
                posicoes = []
                for i in range(len(palavra)):
                    l = linha + direcao[0] * i
                    c = coluna + direcao[1] * i
                    if grade[l][c] != ' ' and grade[l][c] != palavra[i]:
                        break
                    posicoes.append((l, c))
                else:
                    for i, (l, c) in enumerate(posicoes):
                        grade[l][c] = palavra[i]
                    colocada = True
            tentativas += 1

    # Preenche espaços restantes com letras aleatórias
    for i in range(tamanho):
        for j in range(tamanho):
            if grade[i][j] == ' ':
                grade[i][j] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    return grade

# --------------------------
# App Streamlit
# --------------------------

st.set_page_config(page_title="Caça-palavras Filosófico", layout="centered")
st.title("🧠 Caça-palavras Filosófico")
st.markdown("Encontre os filósofos e conceitos escondidos na grade!")

# Estado da sessão
if "fase_atual" not in st.session_state:
    st.session_state.fase_atual = 0
    st.session_state.encontradas = set()

fase_palavras = fases[st.session_state.fase_atual]
grade = gerar_grade(fase_palavras)

# Exibe Fase
st.subheader(f"Fase {st.session_state.fase_atual + 1}")

# Exibe grade de letras
st.markdown("### 🔡 Grade de Letras")
grade_str = ""
for linha in grade:
    grade_str += " ".join(linha) + "\n"
st.text(grade_str)

# Exibe lista de palavras
st.markdown("### 📚 Palavras para encontrar:")
for palavra in fase_palavras:
    if palavra in st.session_state.encontradas:
        st.markdown(f"- ~~{palavra}~~ ✅")
    else:
        st.markdown(f"- **{palavra}**")

# Entrada do jogador
palpite = st.text_input("Digite uma palavra que você encontrou").upper().strip()

if palpite:
    if palpite in fase_palavras:
        if palpite not in st.session_state.encontradas:
            st.session_state.encontradas.add(palpite)
            st.success(f"Você encontrou: {palpite}!")
        else:
            st.info("Você já marcou essa palavra.")
    else:
        st.error("Essa palavra não está na lista.")

# Verifica se completou a fase
if set(fase_palavras) == st.session_state.encontradas:
    st.success("🎉 Fase completa!")
    if st.button("➡️ Próxima fase"):
        st.session_state.fase_atual += 1
        st.session_state.encontradas = set()
        if st.session_state.fase_atual >= len(fases):
            st.balloons()
            st.markdown("🏁 Parabéns! Você finalizou todas as fases do jogo filosófico!")
            st.session_state.fase_atual = 0
            st.session_state.encontradas = set()

# Botão de reinício
st.sidebar.button("🔁 Reiniciar jogo", on_click=lambda: st.session_state.update(fase_atual=0, encontradas=set()))
