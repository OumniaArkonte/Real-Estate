import streamlit as st
import os
import json
from datetime import datetime

# Import des modules (assure-toi que tes agents sont bien définis dans module2.py)
try:
    import module2
except ImportError as e:
    st.error(f"Erreur lors de l'import de module2: {e}")
    st.stop()

# -------------------------------
# Config Streamlit
# -------------------------------
st.set_page_config(
    page_title="Real Estate - Property Valuation",
    page_icon="🏠",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f1f5f9;
    }
    .main-content {
        background: #1e293b;
        border-radius: 12px;
        padding: 2rem;
        border: 1px solid #334155;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# État de session
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# UI
# -------------------------------
st.title("🏠 Property Valuation Assistant")
st.write("Automated property assessment and market analysis")

# Historique
st.subheader("Conversation")
for role, text in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"**🧑 You:** {text}")
    else:
        st.markdown(f"**🤖 Assistant:** {text}")

# -------------------------------
# Orchestration des agents
# -------------------------------
st.subheader("New Question")
user_input = st.text_area("Posez votre question :", placeholder="Ex: Estimation pour une maison de 3 chambres...")

def parse_agent_output(agent_output):
    """
    Transforme l'output brut d'un agent (RunOutput ou JSON string) en dictionnaire lisible.
    """
    if hasattr(agent_output, "content"):
        content = agent_output.content
    else:
        content = agent_output
    try:
        # Si le contenu est un JSON string, convertir en dict
        if isinstance(content, str):
            return json.loads(content.replace("'", '"'))
        elif isinstance(content, dict):
            return content
        else:
            return str(content)
    except Exception:
        return str(content)

if st.button("Envoyer"):
    if user_input.strip():
        st.session_state.chat_history.append(("user", user_input))
        try:
            st.info("📥 DataCollectionAgent en cours...")
            data_result = parse_agent_output(module2.DataCollectionAgent.run(user_input))

            st.info("📚 KnowledgeBaseAgent en cours...")
            kb_result = parse_agent_output(module2.KnowledgeBaseAgent.run(data_result))

            st.info("💰 ValuationAgent en cours...")
            valuation_result = parse_agent_output(module2.ValuationAgent.run(kb_result))

            st.info("📊 MarketComparisonAgent en cours...")
            market_result = parse_agent_output(module2.MarketComparisonAgent.run(valuation_result))

            st.info("✅ ValidationAgent en cours...")
            validation_result = parse_agent_output(module2.ValidationAgent.run(market_result))

            st.info("📑 AdvisoryAgent en cours...")
            final_result = parse_agent_output(module2.AdvisoryAgent.run(validation_result))

            # Formatage pour affichage clair
            response = f"""
### Résultats de l'analyse

**Caractéristiques extraites :**  
{json.dumps(data_result, indent=2, ensure_ascii=False)}

**Base de connaissances enrichie :**  
{json.dumps(kb_result, indent=2, ensure_ascii=False)}

**Estimation initiale :**  
{json.dumps(valuation_result, indent=2, ensure_ascii=False)}

**Analyse marché :**  
{json.dumps(market_result, indent=2, ensure_ascii=False)}

**Validation et score de confiance :**  
{json.dumps(validation_result, indent=2, ensure_ascii=False)}

**Recommandations finales :**  
{json.dumps(final_result, indent=2, ensure_ascii=False)}
"""
        except Exception as e:
            response = f" Erreur dans l'orchestration : {e}"

        st.session_state.chat_history.append(("bot", response))
        st.rerun()

# -------------------------------
# Upload fichiers
# -------------------------------
st.subheader("Upload documents (optionnel)")
uploaded_file = st.file_uploader("Choisir un fichier", type=["pdf", "docx", "txt", "csv"])
if uploaded_file:
    documents_dir = os.path.join("documents2")
    os.makedirs(documents_dir, exist_ok=True)
    filepath = os.path.join(documents_dir, uploaded_file.name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Fichier enregistré : {filepath}")
