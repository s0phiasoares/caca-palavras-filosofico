import streamlit as st
import random
import numpy as np
import time

# --------------------------
# Configurações
# --------------------------
TEMPO_POR_FASE = 120  # segundos (2 minutos)

fases = [
    ["PLATAO", "ETICA", "SOCRATES", "VIRTUDE", "RAZAO"],
    ["NIETZSCHE", "VALORES", "ETERNORETORNO", "MORAL", "SUPERHOMEM"],
    ["BEAUVOIR", "EXISTENCIA", "LIBERDADE", "OPRESSAO", "FEMINISMO"],
    ["KANT", "CATEGORIA", "IMPERATIVO", "AUTONOMIA", "DEVER"],
    ["HEGEL", "DIALETICA", "TESE", "ANTITESE", "SINTESE"],
]

significados = {
    "PLATAO": "Filósofo grego, discípulo de Sócrates e mestre de Aristóteles. Fundador da Academia.",
    "ETICA": "Ramo da filosofia que estuda os princípios morais que governam o comportamento humano.",
    "SOCRATES": "Filósofo grego conhecido pelo método socrático e pela frase 'só sei que nada sei'.",
    "VIRTUDE": "Excelência moral; qualidade que leva o indivíduo a agir corretamente.",
    "RAZAO": "Capacidade humana de pensar, argumentar e chegar ao conhecimento lógico.",

    "NIETZSCHE": "Filósofo alemão que criticou a moral tradicional e propôs o conceito de 'além-do-homem'.",
    "VALORES": "Conceitos que orientam comportamentos e decisões; centrais na ética e moral.",
    "ETERNORETORNO": "Ideia nietzschiana de que tudo retorna infinitamente; desafio ao sentido da vida.",
    "MORAL": "Conjunto de regras e valores que orientam a conduta humana em sociedade.",
    "SUPERHOMEM": "Figura ideal de Nietzsche: o indivíduo que cria seus próprios valores.",

    "BEAUVOIR": "Filósofa existencialista e feminista francesa, autora de 'O Segundo Sexo'.",
    "EXISTENCIA": "Foco da filosofia existencialista: a experiência concreta do ser humano.",
    "LIBERDADE": "Condição de agir conforme a própria vontade; central no existencialismo.",
    "OPRESSAO": "Estado de dominação ou restrição à liberdade individual ou coletiva.",
    "FEMINISMO": "Movimento que busca igualdade de direitos e oportunidades entre os gêneros.",

    "KANT": "Filósofo alemão que fundou o idealismo transcendental e propôs o imperativo categórico.",
    "CATEGORIA": "Conceito kantiano: estrutura do entendimento humano da realidade.",
    "IMPERATIVO": "Regra moral universal. O imperativo categórico ordena agir como se sua ação fosse uma lei universal.",
    "AUTONOMIA": "Capacidade de agir segundo a própria razão moral, sem imposições externas.",
    "DEVER": "Para Kant, a base da moralidade: agir por respeito à lei moral.",

    "HEGEL": "Filósofo alemão que propôs a dialética como estrutura do pensamento e da história.",
    "DIALETICA": "Método filosófico baseado na contradição e superação de opostos.",
    "TESE": "Afirmação inicial em um processo dialético.",
    "ANTITESE": "Afirmação contrária à tese.",
    "SINTESE": "Superação entre tese e antítese; novo patamar de conhecimento."
}

# --------------------------
# Funções auxiliares
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

def resetar_fase():
    st.session_state.encontradas = set()
    st.session_state.tempo_inicial = time.time()

# --------------------------
# Streamlit App
# --------------------------

st.set_page_config(page_title="Caça-palavras Filosófico", layout="centered")
st.title("🧠 Caça-palavras Filosófico")
st.markdown("Encontre os filósofos e conceitos escondidos na grade!")

# Inicializa estado da sessão
if "fase_atual" not in st.session_state:
    st.session_state.fase_atual = 0
    st.session_state.encontradas = set()
    st.session_state.tempo_inicial = time.time()
    st.session_state.ultima_fase = 0

# Reseta timer se mudou de fase
if st.session_state.fase_atual != st.session_state.ultima_fase:
    resetar_fase()
    st.session_state.ultima_fase = st.session_state.fase_atual

# Calcula tempo restante
tempo_passado = time.time() - st.session_state.tempo_inicial
tempo_restante = max(0, TEMPO_POR_FASE - int(tempo_passado))
minutos = tempo_restante // 60
segundos = tempo_restante % 60

st.markdown(f"⏰ **Tempo restante:** {minutos:02d}:{segundos:02d}")

fase_palavras = fases[st.session_state.fase_atual]
grade = gerar_grade(fase_palavras)

if tempo_restante == 0:
    st.error("⏳ O tempo acabou! Você perdeu essa fase.")
    if st.button("🔄 Tentar novamente"):
        resetar_fase()
        st.experimental_rerun()
else:
    # Exibe fase
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
                if palpite in significados:
                    st.info(f"📖 *{significados[palpite]}*")
            else:
                st.info("Você já marcou essa palavra.")
        else:
            st.error("Essa palavra não está na lista.")

    # Verifica se completou a fase
    if set(fase_palavras) == st.session_state.encontradas:
        st.success("🎉 Fase completa!")
        if st.button("➡️ Próxima fase"):
            st.session_state.fase_atual += 1
            if st.session_state.fase_atual >= len(fases):
                st.balloons()
                st.markdown("🏁 Parabéns! Você finalizou todas as fases!")
                st.session_state.fase_atual = 0
            resetar_fase()

# Botão de reinício
st.sidebar.button("🔁 Reiniciar jogo", on_click=lambda: (
    st.session_state.update(fase_atual=0, encontradas=set(), tempo_inicial=time.time())
))


