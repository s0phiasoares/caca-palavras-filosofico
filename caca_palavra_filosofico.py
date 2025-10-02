import streamlit as st
import random

fases = {
    1: {
        "words": {
            "ÉTICA": "Ramo da filosofia que estuda os valores morais e a conduta humana.",
            "LÓGICA": "Estudo dos princípios do raciocínio válido.",
            "SÓCRATES": "Filósofo grego fundador da filosofia moral."
        }
    },
    2: {
        "words": {
            "METAFÍSICA": "Estudo do ser e da realidade além do físico.",
            "EPISTEMOLOGIA": "Estudo do conhecimento e da sua validade.",
            " MILETO": ""
        }
    },
    3: {
        "words": {
            "EXISTENCIALISMO": "Filosofia que enfatiza a existência individual, liberdade e escolha.",
            "NIHILISMO": "Doutrina que nega a existência de valores objetivos.",
            "HEGEL": "Filósofo alemão conhecido pelo idealismo dialético."
        }
    },
    4: {
        "words": {
            "UTILITARISMO": "Doutrina ética que avalia ações pelo benefício ao maior número.",
            "DEONTOLOGIA": "Ética baseada no dever e nas regras morais.",
            "ARISTÓTELES": "Filósofo grego que estudou lógica, ética e política."
        }
    },
    5: {
        "words": {
            "PLATÃO": "Filósofo grego discípulo de Sócrates e fundador da Academia.",
            "IDEALISMO": "Doutrina que afirma a primazia da mente sobre a matéria.",
            "HEDONISMO": "Doutrina que busca o prazer como princípio da vida."
        }
    },
    6: {
        "words": {
            "CÉREBRO": "Órgão que processa informações e é sede da consciência.",
            "RAZÃO": "Capacidade humana de pensar, julgar e compreender.",
            "LIBERDADE": "Condição de agir segundo a própria vontade."
        }
    },
    7: {
        "words": {
            "DEMOCRACIA": "Sistema político onde o povo exerce o poder.",
            "ANÁLISE": "Exame detalhado de elementos e estrutura.",
            "ÉPISTEME": "Conhecimento científico, distinto da opinião."
        }
    },
    8: {
        "words": {
            "HUMANISMO": "Doutrina que valoriza o ser humano e suas capacidades.",
            "FENOMENOLOGIA": "Estudo da estrutura da experiência consciente.",
            "EMPIRISMO": "Teoria que afirma que o conhecimento vem da experiência."
        }
    },
    9: {
        "words": {
            "PRAGMATISMO": "Doutrina que valoriza a utilidade prática das ideias.",
            "ESTOICISMO": "Filosofia que ensina a aceitar o destino com serenidade.",
            "DEBATE": "Discussão estruturada para expor ideias contrárias."
        }
    },
    10: {
        "words": {
            "RAIZ": "Origem ou fundamento de algo.",
            "CONHECIMENTO": "Informação e compreensão adquiridas pelo estudo ou experiência.",
            "FILOSOFIA": "Amor à sabedoria e busca pelo conhecimento."
        }
    }
}

def cria_grid(palavras, size=12):
    grid = [[" " for _ in range(size)] for _ in range(size)]
    for palavra in palavras:
        palavra = palavra.upper()
        colocada = False
        tentativas = 0
        while not colocada and tentativas < 200:
            orientacao = random.choice(["horizontal", "vertical"])
            if orientacao == "horizontal":
                linha = random.randint(0, size-1)
                col = random.randint(0, size - len(palavra))
                if all(grid[linha][col+i] in [" ", palavra[i]] for i in range(len(palavra))):
                    for i in range(len(palavra)):
                        grid[linha][col+i] = palavra[i]
                    colocada = True
            else:
                linha = random.randint(0, size - len(palavra))
                col = random.randint(0, size-1)
                if all(grid[linha+i][col] in [" ", palavra[i]] for i in range(len(palavra))):
                    for i in range(len(palavra)):
                        grid[linha+i][col] = palavra[i]
                    colocada = True
            tentativas += 1
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÇ"
    for i in range(size):
        for j in range(size):
            if grid[i][j] == " ":
                grid[i][j] = random.choice(letras)
    return grid

def mostrar_grid(grid):
    st.write("🔍 Caça-Palavras ")
    texto = "\n".join(" ".join(linha) for linha in grid)
    st.markdown(f"```\n{texto}\n```")

def main():
    st.title("🧠 Caça-Palavras de Filosofia 🧩")

    # Inicializa a fase
    if "fase" not in st.session_state:
        st.session_state["fase"] = 1
        st.session_state["achadas"] = []
        st.session_state["grid"] = None

    fase_atual = st.session_state["fase"]
    palavras = list(fases[fase_atual]["words"].keys())
    significados = fases[fase_atual]["words"]

    # Inicializa o grid se necessário
    if st.session_state["grid"] is None:
        st.session_state["grid"] = cria_grid(palavras)

    mostrar_grid(st.session_state["grid"])

    st.write(f"🎯 **Fase {fase_atual}** - Encontre as palavras relacionadas à Filosofia.")

    if st.session_state["achadas"]:
        st.markdown("### ✅ Palavras encontradas:")
        for p in st.session_state["achadas"]:
            st.write(f"- **{p}**")

    palavra_input = st.text_input("Digite a palavra que encontrou (em maiúsculas) ✍️:").strip().upper()

    if st.button("🔎 Verificar"):
        if palavra_input in palavras and palavra_input not in st.session_state["achadas"]:
            st.session_state["achadas"].append(palavra_input)
            st.success(f"✅ Você encontrou: **{palavra_input}**!")
            st.info(f"📚 Significado: {significados[palavra_input]}")
        elif palavra_input in st.session_state["achadas"]:
            st.warning("⚠️ Você já encontrou essa palavra.")
        else:
            st.error("❌ Palavra incorreta ou não pertence à fase atual.")

    # Se completou a fase
    if len(st.session_state["achadas"]) == len(palavras):
        st.balloons()
        st.success("🎉 Parabéns! Você completou esta fase!")

        if fase_atual < len(fases):
            if st.button("➡️ Ir para a próxima fase"):
                # Atualiza a fase e reinicia o jogo
                st.session_state["fase"] = fase_atual + 1
                st.session_state["achadas"] = []
                st.session_state["grid"] = None  # para recriar o grid na nova fase
                st.experimental_rerun()
        else:
            st.success("🏆 Você completou todas as fases! 🎊")

if __name__ == "__main__":
    main()




