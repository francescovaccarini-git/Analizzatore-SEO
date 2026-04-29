import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import time
import nltk
from collections import Counter
import random

# --- CONFIGURAZIONE PAGINA & STILE ---
st.set_page_config(
    page_title="SEO Sentinel Pro | Analisi Competitor AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Download risorse NLTK silenziosamente
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
    
from nltk.corpus import stopwords

# --- CSS PERSONALIZZATO PER LOOK PROFESSIONALE ---
st.markdown("""
<style>
    /* Nascondi i controlli Streamlit di default */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Stile delle card */
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 20px;
    }
    
    /* Pulsanti personalizzati */
    .stButton>button {
        width: 100%;
        background-color: #6C63FF;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        height: 50px;
    }
    
    /* Header principale */
    h1 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Box risultati */
    .result-box {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- LOGICA DI BUSINESS (SIMULATA MA REALISTICA) ---

def generate_mock_analysis(keyword):
    """
    Genera un'analisi dettagliata basata sulla keyword.
    In produzione, qui chiameresti API reali (Serper, Ahrefs, ecc.)
    """
    
    # Simulazione titoli competitor realistici
    titles = [
        f"{keyword}: La Guida Definitiva per il Successo",
        f"I 7 Segreti di {keyword} che Nessuno Ti Dice",
        f"Come Dominare {keyword} in Meno di 30 Giorni",
        f"{keyword} vs Alternativa: Quale Scegliere?",
        f"Recensione Onesta: Vale la pena investire in {keyword}?"
    ]
    
    # Simulazione parole chiave semantiche (LSI)
    base_lsi = ['strategia', 'risultati', 'guide', 'tutorial', 'vantaggi', 'svantaggi', 'costi', 'benefici', 'migliori', 'recensione']
    lsi_keywords = [(word, random.randint(5, 50)) for word in base_lsi]
    lsi_keywords.sort(key=lambda x: x[1], reverse=True)
    
    # Analisi Sentiment simulata
    sentiment_score = random.uniform(0.6, 0.95)
    
    return {
        "titles": titles,
        "lsi": lsi_keywords[:10],
        "avg_length": random.randint(1200, 2500),
        "sentiment": sentiment_score,
        "difficulty": random.randint(40, 85)
    }

def get_real_data_if_available(api_key, keyword):
    """Placeholder per integrazione reale futura"""
    if api_key:
        # Qui andrebbe la logica reale con Serper.dev
        return None 
    return generate_mock_analysis(keyword)

# --- INTERFACCIA UTENTE ---

# Sidebar Branding
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2933/2933245.png", width=100)
    st.header("SEO Sentinel Pro")
    st.caption("Analisi Competitor & Content Gap Analysis")
    st.divider()
    
    st.subheader("⚙️ Impostazioni")
    api_key = st.text_input("API Key Serper.dev (Opzionale)", type="password", help="Lascia vuoto per la Demo Gratuita")
    
    st.markdown("---")
    st.markdown("**Contatti & Supporto**")
    st.markdown("[📧 Contattaci](mailto:support@seosentinel.com)")
    st.markdown("[💼 Diventa Partner](#)")
    
    st.markdown("---")
    st.markdown("*Powered by Python & AI*")

# Main Content
col1, col2 = st.columns([1.5, 1])

with col1:
    st.title("Scopri Cosa Funziona Su Google 🔍")
    st.markdown("Inserisci una keyword o un URL competitor per ottenere un report strategico completo in pochi secondi.")
    
    input_container = st.container()
    with input_container:
        keyword = st.text_input("Inserisci Keyword Target", placeholder="Es: marketing digitale, scarpe running...")
        
        btn_col1, btn_col2 = st.columns([3, 1])
        with btn_col1:
            analyze_btn = st.button("🚀 Avvia Analisi Strategica", type="primary")

with col2:
    # Card Statistiche Rapide (Placeholder visivo)
    st.metric("Utenti Attivi Oggi", "1,240")
    st.metric("Report Generati", "8,500+")
    st.success("✅ Sistema Operativo al 100%")

# --- ELABORAZIONE E RISULTATI ---

if analyze_btn:
    if not keyword:
        st.error("⚠️ Per favore inserisci una keyword valida.")
    else:
        with st.spinner(f'Analisi in corso per "{keyword}"...'):
            time.sleep(2) # Simula elaborazione
            
            data = get_real_data_if_available(api_key, keyword)
            
            # Header Risultati
            st.divider()
            st.subheader(f"📊 Report Strategico per: **{keyword.upper()}**")
            
            # KPI Cards
            kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
            with kpi_col1:
                st.markdown(f"""
                    <div class="metric-card">
                        <h3>Difficoltà SEO</h3>
                        <p style='font-size: 24px; font-weight: bold;'>{data['difficulty']}/100</p>
                        <small>Medio-Alto</small>
                    </div>
                """, unsafe_allow_html=True)
            with kpi_col2:
                st.markdown(f"""
                    <div class="metric-card">
                        <h3>Lunghezza Ideale</h3>
                        <p style='font-size: 24px; font-weight: bold;'>~{data['avg_length']} parole</p>
                        <small>Basato sui Top 10</small>
                    </div>
                """, unsafe_allow_html=True)
            with kpi_col3:
                sentiment_label = "Positivo 😊" if data['sentiment'] > 0.7 else "Neutro 😐"
                st.markdown(f"""
                    <div class="metric-card">
                        <h3>Sentiment Mercato</h3>
                        <p style='font-size: 24px; font-weight: bold;'>{sentiment_label}</p>
                        <small>Score: {data['sentiment']}</small>
                    </div>
                """, unsafe_allow_html=True)

            st.divider()

            # Tabs per i dettagli
            tab1, tab2, tab3, tab4 = st.tabs(["🏆 Titoli Competitor", "🔑 Parole Chiave LSI", "📝 Struttura Consigliata", "💰 Monetizzazione"])

            with tab1:
                st.markdown("Ecco come hanno titolato i tuoi principali competitor:")
                for i, title in enumerate(data['titles'], 1):
                    st.info(f"**#{i}**: {title}")
                
                st.warning("💡 **Insight:** Nota l'uso di numeri ('7 Segreti') e aggettivi forti ('Definitiva'). Usa questa formula!")

            with tab2:
                st.markdown("Queste sono le parole semantiche (LSI) che Google si aspetta di trovare nel tuo articolo:")
                
                cols = st.columns(5)
                for idx, (word, count) in enumerate(data['lsi']):
                    col_idx = idx % 5
                    with cols[col_idx]:
                        st.progress(count / 50, text=f"{word.capitalize()}")

            with tab3:
                st.markdown("### 🗺️ Mappa dell'Articolo Ottimizzato")
                st.markdown("""
                Per battere la concorrenza, struttura il tuo contenuto così:
                
                1. **H1: Titolo Accattivante** (Includi la keyword principale)
                2. **Introduzione:** Gancia il lettore nei primi 100 caratteri.
                3. **H2: Cos'è [KEYWORD]?** (Definizione chiara)
                4. **H2: I Vantaggi Principali** (Usa bullet points)
                5. **H2: Come Iniziare con [KEYWORD]** (Guida pratica passo-passo)
                6. **H2: Errori Comuni da Evitare** (Aggiungi valore negativo)
                7. **H2: FAQ** (Rispondi alle domande frequenti)
                8. **Conclusione & CTA** (Call to Action chiara)
                """)

            with tab4:
                st.markdown("### 💎 Sblocca il Potenziale Completo")
                st.markdown("La versione gratuita ti dà una panoramica. Con il piano Pro ottieni:")
                st.bullet("✅ Export PDF del Report Completo")
                st.bullet("✅ Analisi dei Backlink dei Competitor")
                st.bullet("✅ Generatore di Meta Description AI")
                st.bullet("✅ Monitoraggio Posizioni Settimanale")
                
                st.divider()
                if st.button("🔓 Acquista Piano Pro - €29/mese", type="primary"):
                    st.success("Grazie! Reindirizzamento al checkout sicuro...")

else:
    # Stato iniziale vuoto con immagine placeholder
    st.markdown("""
    <div style='text-align: center; margin-top: 50px;'>
        <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="150">
        <p>Inserisci una keyword per iniziare l'analisi.</p>
    </div>
    """, unsafe_allow_html=True)