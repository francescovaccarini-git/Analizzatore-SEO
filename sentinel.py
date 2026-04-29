# pip install streamlit requests beautifulsoup4 nltk
# streamlit run app.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import time
import nltk
from collections import Counter

# --- CONFIGURAZIONE INIZIALE ---
st.set_page_config(
    page_title="SEO Sentinel MVP",
    page_icon="🚀",
    layout="wide"
)

# Download risorse NLTK se non presenti (per stop words)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
    
from nltk.corpus import stopwords

# --- FUNZIONI DI LOGICA (BACKEND) ---

def get_google_results(keyword, api_key=None):
    """
    Simula o esegue la ricerca su Google.
    NOTA: Per produzione reale, usare API come Serper.dev.
    Qui usiamo una simulazione robusta per demo senza costi immediati,
    ma includo il commento su come integrare l'API vera.
    """
    
    # --- OPZIONE A: SIMULAZIONE PER DEMO (Funziona subito senza API Key) ---
    # In un ambiente reale, sostituiresti questo blocco con una chiamata API a Serper.dev
    
    if not api_key:
        # Generiamo dati fittizi realistici basati sulla keyword per dimostrare la UI
        base_urls = [
            "https://example.com/blog/1", "https://competitor-a.com/guide", 
            "https://top-site.net/article", "https://wiki-info.org/page", 
            "https://news-daily.com/report"
        ]
        
        mock_titles = [
            f"Guida Completa a {keyword}: Tutto quello che devi sapere",
            f"I migliori consigli per {keyword} nel 2024",
            f"{keyword}: Errori da evitare e strategie vincenti",
            f"Come iniziare con {keyword}: Tutorial passo-passo",
            f"Recensione approfondita su {keyword}"
        ]
        
        return [
            {"title": t, "link": u, "snippet": f"Ecco cosa dicono gli esperti su {keyword}..."} 
            for t, u in zip(mock_titles, base_urls)
        ]

    # --- OPZIONE B: INTEGRAZIONE REALE SERPER.DEV (De-commentare per uso reale) ---
    """
    url = "https://google.serper.dev/search"
    payload = {"q": keyword, "gl": "it", "hl": "it"}
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get('organic', [])[:5]
    else:
        return []
    """

def scrape_page_content(url):
    """Scarica e pulisce il testo di una pagina web."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Rimuovi script, style, nav, footer
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
            
        text = soup.get_text(separator=' ', strip=True)
        # Pulizia extra spazi
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except Exception as e:
        return ""

def analyze_text(texts_list):
    """Analizza NLP sui testi raccolti."""
    combined_text = " ".join(texts_list).lower()
    
    # Tokenizzazione semplice
    words = re.findall(r'\b[a-z]{4,}\b', combined_text) # Solo parole > 3 char
    
    # Stop words italiane + inglesi comuni
    stop_words_set = set(stopwords.words('italian') + stopwords.words('english'))
    # Aggiungiamo parole generiche web
    generic_words = {'http', 'https', 'www', 'com', 'org', 'net', 'cookie', 'privacy', 'termini', 'condizioni'}
    stop_words_set.update(generic_words)
    
    filtered_words = [w for w in words if w not in stop_words_set]
    
    word_counts = Counter(filtered_words)
    return word_counts.most_common(20), len(combined_text.split())

# --- INTERFACCIA UTENTE (FRONTEND) ---

st.title("🚀 SEO Sentinel: Content Gap Analyzer")
st.markdown("""
<style>
    .report-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.header("1. Inserisci i Dati")
    keyword = st.text_input("Keyword Target (es. 'dieta chetogenica')", placeholder="Scrivi qui la tua keyword...")
    
    # Campo opzionale per API Key (nascosto inizialmente o usato per versione pro)
    with st.expander("⚙️ Impostazioni Avanzate (Opzionale)"):
        api_key = st.text_input("Serper.dev API Key (Lascia vuoto per Demo)", type="password")
        st.caption("Senza API Key, il tool userà dati simulati per mostrarti il funzionamento.")

with col2:
    st.header("2. Azione")
    st.info("💡 Questo tool analizza i top 5 risultati Google e ti dice cosa manca nel tuo contenuto.")
    
    analyze_btn = st.button("🔍 Analizza Competitor", type="primary", use_container_width=True)

# --- ELABORAZIONE DATI ---

if analyze_btn:
    if not keyword:
        st.warning("⚠️ Per favore inserisci una keyword.")
    else:
        with st.spinner('Sto scansionando i risultati di Google...'):
            # 1. Ottieni risultati SERP
            results = get_google_results(keyword, api_key if api_key else None)
            
            if not results:
                st.error("Nessun risultato trovato o errore API.")
            else:
                st.success(f"Trovati {len(results)} competitor principali.")
                
                # 2. Scarica contenuti (Simulato o Reale)
                contents = []
                titles = []
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, res in enumerate(results):
                    status_text.text(f"Analizzando: {res['title'][:50]}...")
                    # In demo mode, generiamo testo finto coerente
                    if not api_key:
                        fake_text = f"Questo è un testo simulato relativo a {keyword}. Parliamo di benefici, rischi, strategie e {keyword} tips. Importante menzionare {keyword} spesso." * 50
                        contents.append(fake_text)
                    else:
                        # Se c'è API key, proviamo a scrapare davvero (con cautela)
                        content = scrape_page_content(res['link'])
                        contents.append(content if content else "Testo non disponibile")
                    
                    titles.append(res['title'])
                    progress_bar.progress((i + 1) / len(results))
                    time.sleep(0.5) # Pausa per effetto visivo e rispetto server
                
                status_text.text("Elaborazione linguistica in corso...")
                
                # 3. Analisi NLP
                top_keywords, total_word_count_estimate = analyze_text(contents)
                avg_length = total_word_count_estimate // len(results) if results else 0
                
                # --- VISUALIZZAZIONE RISULTATI ---
                
                st.divider()
                st.header("📊 Report Strategico")
                
                tab1, tab2, tab3 = st.tabs(["🎯 Brief Contenuto", "🔑 Keyword Cloud", "📝 Titoli Competitor"])
                
                with tab1:
                    st.subheader("Linee Guida per il Tuo Articolo")
                    st.metric("Lunghezza Media Consigliata", f"{avg_length} parole", delta="Basato sui Top 5")
                    
                    st.markdown("#### Struttura Suggerita (H2/H3)")
                    st.markdown("""
                    - **Introduzione**: Definisci chiaramente cos'è **[KEYWORD]**.
                    - **Benefici Principali**: Elenca i vantaggi (usa bullet points).
                    - **Come Fare**: Guida passo-passo pratica.
                    - **Errori Comuni**: Cosa evitare quando si usa **[KEYWORD]**.
                    - **Conclusione**: Call to Action chiara.
                    """.replace("[KEYWORD]", keyword.upper()))
                    
                    st.info("💡 **Consiglio Pro:** I competitor usano molto la parola chiave nel primo paragrafo. Fallo anche tu.")

                with tab2:
                    st.subheader("Parole Chiave Semantiche (LSI)")
                    st.caption("Queste parole appaiono frequentemente nei top risultati. Usale nel tuo testo.")
                    
                    # Creiamo una visualizzazione semplice
                    for word, count in top_keywords[:10]:
                        # Normalizziamo la barra per visualizzazione
                        max_c = top_keywords[0][1]
                        percent = int((count / max_c) * 100)
                        st.progress(percent, text=f"{word.capitalize()} ({count} occorrenze)")

                with tab3:
                    st.subheader("Analisi Titoli Competitor")
                    for title in titles:
                        st.markdown(f"- `{title}`")
                    
                    st.markdown("---")
                    st.subheader("💡 Idea Titolo Virale per Te:")
                    st.success(f"🔥 '{keyword.capitalize()}: La Guida Definitiva che Nessuno Ti Ha Mai Detto'")

                # --- SEZIONE MONETIZZAZIONE (SIMULATA) ---
                st.divider()
                st.subheader("🔒 Vuoi il Report Completo PDF?")
                st.markdown("La versione gratuita mostra solo l'analisi base. Sblocca l'export PDF e l'analisi dei backlink.")
                
                col_pay1, col_pay2 = st.columns(2)
                with col_pay1:
                    if st.button("💳 Acquista Report Completo (€9)", type="secondary"):
                        st.balloons()
                        st.success("Grazie! (In un'app reale, qui si aprirebbe Stripe Checkout)")
                with col_pay2:
                    st.caption("Pagamento sicuro tramite Stripe. Accesso immediato.")

else:
    # Stato iniziale
    st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", caption="Analizza. Ottimizza. Domina.")