import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

from src.tooling import detect_tool
from src.calculos import juros_compostos, reserva_emergencia
from src.retrieval import retrieve_context
from src.agent import build_prompt, ask_gemini

load_dotenv()

st.set_page_config(page_title="FinMate AI", page_icon="💳", layout="centered")
st.title("💳 FinMate AI")
st.caption("Consultor amigável (educativo) para decisões financeiras com IA + base de conhecimento")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Chave não encontrada. Crie um arquivo .env com GEMINI_API_KEY.")
    st.stop()

# Cache seguro: cacheia somente strings e recria o client internamente
@st.cache_data(ttl=300)
def cached_ask(api_key: str, prompt: str) -> str:
    client_local = genai.Client(api_key=api_key)
    return ask_gemini(client_local, prompt)

# estado (memória)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Oi! Me diga seu objetivo (ex: guardar, quitar dívida, investir) e eu te ajudo com opções e próximo passo 🙂",
        }
    ]

# controle anti-repetição (evita chamadas duplicadas por re-run do Streamlit)
if "last_user_msg" not in st.session_state:
    st.session_state.last_user_msg = None

# painel lateral (debug/controle)
with st.sidebar:
    st.subheader("Configurações")
    show_sources = st.checkbox("Mostrar trechos usados da base", value=False)
    show_calc = st.checkbox("Mostrar resultado do cálculo (debug)", value=False)

    if st.button("Limpar conversa"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Conversa limpa ✅ Me diga seu objetivo e começamos de novo 🙂"}
        ]
        st.session_state.last_user_msg = None
        st.rerun()

# render do chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# input do usuário
user_msg = st.chat_input("Digite sua dúvida...")

if user_msg:
    # bloqueia processamento duplicado da mesma mensagem
    if user_msg == st.session_state.last_user_msg:
        st.stop()
    st.session_state.last_user_msg = user_msg

    # adiciona msg do usuário
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.write(user_msg)

    # busca contexto na base
    kb_context, scored = retrieve_context(user_msg, top_k=3)

    # --- Ferramentas (simulações) ---
    tool_info = detect_tool(user_msg)
    calc_result = None

    try:
        if tool_info["tool"] == "juros":
            args = tool_info["args"]

            if None in (args.get("aporte_inicial"), args.get("taxa_mensal"), args.get("meses")):
                calc_result = (
                    "Para simular **juros compostos**, preciso de 3 infos: **valor inicial**, **taxa mensal** e **meses**.\n"
                    "Exemplo: `Simule 1000 com 2% ao mês por 12 meses`."
                )
            else:
                r = juros_compostos(args["aporte_inicial"], args["taxa_mensal"], args["meses"])
                calc_result = (
                    f"- Simulação: juros compostos\n"
                    f"- Aporte inicial: R$ {args['aporte_inicial']:.2f}\n"
                    f"- Taxa mensal: {args['taxa_mensal']*100:.2f}%\n"
                    f"- Período: {args['meses']} meses\n"
                    f"- Montante estimado: R$ {r.montante:.2f}\n"
                    f"- Juros no período: R$ {r.juros:.2f}\n"
                )

        elif tool_info["tool"] == "reserva":
            args = tool_info["args"]

            if None in (args.get("gasto_mensal"), args.get("valor_reserva")):
                calc_result = (
                    "Para calcular **reserva de emergência**, preciso de: **gasto mensal** e **valor da reserva**.\n"
                    "Exemplo: `Reserva de emergência: gasto 2500 e tenho 8000`."
                )
            else:
                meses = reserva_emergencia(args["gasto_mensal"], args["valor_reserva"])
                calc_result = (
                    f"- Simulação: reserva de emergência\n"
                    f"- Gasto mensal: R$ {args['gasto_mensal']:.2f}\n"
                    f"- Reserva atual: R$ {args['valor_reserva']:.2f}\n"
                    f"- Cobertura estimada: {meses:.1f} meses\n"
                )

    except Exception as e:
        calc_result = f"Falha ao calcular (entrada inválida): {e}"

    # monta prompt (inclui calc_result se existir)
    prompt = build_prompt(
        user_msg,
        kb_context,
        st.session_state.messages,
        calc_result=calc_result
    )

    # chama IA
    with st.chat_message("assistant"):
        with st.spinner("Analisando..."):
            try:
                answer = cached_ask(api_key, prompt)
                st.write(answer)

                # debug cálculo
                if show_calc and calc_result:
                    st.markdown("#### Resultado do cálculo (debug)")
                    st.code(calc_result)

                # debug base
                if show_sources:
                    st.markdown("#### Trechos usados da base (debug)")
                    if scored:
                        for score, chunk in scored[:3]:
                            st.markdown(f"**Score {score}**")
                            st.code(chunk[:1200])
                    else:
                        st.write("Nenhum trecho relevante encontrado.")

            except Exception as e:
                msg = str(e)

                if "RESOURCE_EXHAUSTED" in msg or "429" in msg:
                    st.warning(
                        "⚠️ Limite da API gratuita atingido.\n\n"
                        "Aguarde cerca de 1 minuto e tente novamente.\n"
                        "Isso é uma limitação normal do plano free do Gemini."
                    )
                    answer = (
                        "No momento atingi o limite de uso da API gratuita.\n\n"
                        "👉 Aguarde cerca de **1 minuto** e tente novamente.\n"
                        "Enquanto isso, posso te ajudar a formular melhor a pergunta 🙂"
                    )
                else:
                    st.error("Erro ao chamar o Gemini.")
                    st.code(msg)
                    answer = "Tive um erro técnico aqui. Tenta novamente mais tarde."

                st.write(answer)

    # salva resposta
    st.session_state.messages.append({"role": "assistant", "content": answer})
