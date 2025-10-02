import streamlit as st
import random

# Palavras e significados por fase
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
            "DEMOCRACIA": "Forma de governo baseada na soberania popular."
        }
    }
}

def cria_grid(palavras, size=10):
    """Cria um grid de caça-palavra com palavras escondidas"""
    grid = [[" " for _ in range(size)] for _ in range(size)]
    
    for palavra in palavras:
        palavra = palavra.upper()
        # Tentar posicionar palavra na horizontal ou vertical
        colocada = False
        tentativas = 0
        while not colocada and tentativas < 100:
            orientacao = random.choice(["horizontal", "vertical"])
            if orientacao == "horizontal":
                linha = random.randint(0, size-1)
                col = random.randint(0, size - len(palavra))
                # Checar se espaço está livre
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
    # Preencher espaços vazios com letras aleatórias
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÇ"
    for i in range(size):
        for j in range(size):
            if grid[i][j] == " ":
                grid[i][j] = random.choice(letras)
    return grid

def mostrar_grid(grid):
    """Mostra o grid como texto formatado com fonte monoespaçada"""
    st.write("### Caça-Palavras")
    texto = "\n".join(" ".join(linha) for linha in grid)
    st.markdown(f"```\n{texto}\n```")

def main():
    st.title("Caça-Palavras de Filosofia")
    
    fase_atual = st.session_state.get("fase", 1)
    palavras = list(fases[fase_atual]["words"].keys())
    significados = fases[fase_atual]["words"]
    
    # Criar grid e armazenar no estado para não mudar toda hora
    if "grid" not in st.session_state or st.session_state.get("fase") != fase_atual:
        st.session_state["grid"] = cria_grid(palavras)
        st.session_state["achadas"] = []
        st.session_state["fase"] = fase_atual
    
    grid = st.session_state["grid"]
    achadas = st.session_state["achadas"]
    
    mostrar_grid(grid)
    
    st.write(f"Fase {fase_atual} - Encontre as palavras relacionadas à Filosofia.")
    
    palavra_input = st.text_input("Digite a palavra que encontrou (em maiúsculas):").strip().upper()
    
    if st.button("Verificar"):
        if palavra_input in palavras and palavra_input not in achadas:
            achadas.append(palavra_input)
            st.success(f"Você encontrou: {palavra_input}!")
            st.info(f"Significado: {significados[palavra_input]}")
            
            # Salvar estado
            st.session_state["achadas"] = achadas
            
            # Verificar se completou todas palavras da fase
            if len(achadas) == len(palavras):
                st.balloons()
                st.success("Parabéns! Você completou esta fase!")
                if fase_atual < len(fases):
                    if st.button("Ir para a próxima fase"):
                        st.session_state["fase"] = fase_atual + 1
                        st.experimental_rerun()
                else:
                    st.success("Você completou todas as fases!")
        elif palavra_input in achadas:
            st.warning("Você já encontrou essa palavra.")
        else:
            st.error("Palavra incorreta ou não pertence à fase atual.")

if __name__ == "__main__":
    main()



