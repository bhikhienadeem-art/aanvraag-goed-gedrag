import streamlit as st
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.id import ID

# --- PAGINA CONFIGURATIE ---
st.set_page_config(page_title="VOG Aanvraag Suriname", layout="centered")

# --- CSS STYLING VOOR HET ONTWERP ---
st.markdown("""
    <style>
    /* Achtergrondkleur */
    .stApp { background-color: #0d2538; }
    
    /* Header Banners */
    .banner { 
        background: linear-gradient(90deg, #004d4d 0%, #008080 100%); 
        color: white; 
        padding: 20px; 
        border-radius: 10px; 
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Formulier Container */
    .form-container { 
        background-color: #e6f2f2; 
        padding: 30px; 
        border-radius: 15px; 
        border: 2px solid #008080;
    }
    
    /* Knop Styling */
    .stButton>button { 
        background-color: #008080 !important; 
        color: white !important; 
        font-weight: bold; 
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- APPRWRITE CONNECTIE ---
client = Client()
(client.set_endpoint('https://cloud.appwrite.io/v1').set_project('6a35359b000c27a4ab88')) 
databases = Databases(client)
storage = Storage(client)

# --- UI OPBOUW ---
st.markdown('<div class="banner"><h1>ONLINE VOG AANVRAAG</h1></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; color:white;"><h3>AANVRAGEN IS EENVOUDIG EN SNEL</h3></div>', unsafe_allow_html=True)

st.markdown('<div class="form-container">', unsafe_allow_html=True)
with st.form("aanvraag_formulier"):
    st.subheader("ONLINE AANVRAAGFORMULIER")
    
    naam = st.text_input("Volledige Naam")
    bsn = st.text_input("BSN/ID-nummer")
    email = st.text_input("E-mailadres")
    
    uittreksel = st.file_uploader("Upload Paspoort/ID (pdf, jpg)", type=['pdf', 'jpg'])
    pasfoto = st.file_uploader("Upload Pasfoto (jpg, png)", type=['jpg', 'png'])
    betaling = st.file_uploader("Upload Betalingsbewijs (pdf, jpg)", type=['pdf', 'jpg'])
    
    submit = st.form_submit_button("AANVRAAG INDIENEN")

    if submit:
        # Hier de logica voor opslaan naar Appwrite (zoals voorheen)
        st.success("Uw aanvraag is succesvol verwerkt!")
st.markdown('</div>', unsafe_allow_html=True)
