import streamlit as st
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.id import ID

# --- APPLICATIE CONFIGURATIE ---
st.set_page_config(page_title="VOG Aanvraag Portaal", layout="centered")

# --- CSS STYLING (Layout & Kleuren) ---
st.markdown("""
    <style>
    .stApp { background-color: #0a1f33; color: #ffffff; }
    .main-header { 
        background: linear-gradient(90deg, #004d4d 0%, #008080 100%); 
        padding: 20px; 
        text-align: center; 
        border-radius: 10px; 
        margin-bottom: 20px;
    }
    .form-container { 
        background-color: #f0f7f7; 
        padding: 30px; 
        border-radius: 15px; 
        color: #0a1f33; 
    }
    .stButton>button { 
        background-color: #008080; 
        color: white; 
        width: 100%; 
        font-weight: bold; 
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- APPRWRITE CONNECTIE ---
client = Client()
(client
  .set_endpoint('https://cloud.appwrite.io/v1') 
  .set_project('6a35359b000c27a4ab88')) 

databases = Databases(client)
storage = Storage(client)

# --- UI OPBOUW ---
st.markdown('<div class="main-header"><h1>ONLINE VOG AANVRAAG</h1></div>', unsafe_allow_html=True)

st.subheader("U HEEFT EEN VOG NODIG? AANVRAGEN IS EENVOUDIG EN SNEL")
st.markdown("---")

with st.markdown('<div class="form-container">', unsafe_allow_html=True):
    with st.form("aanvraag_formulier"):
        st.subheader("ONLINE AANVRAAGFORMULIER")
        
        naam = st.text_input("Volledige Naam")
        bsn = st.text_input("BSN/ID-nummer")
        email = st.text_input("E-mailadres")
        
        st.write("---")
        uittreksel = st.file_uploader("Upload Paspoort/ID (pdf, jpg)", type=['pdf', 'jpg'])
        pasfoto = st.file_uploader("Upload Pasfoto (jpg, png)", type=['jpg', 'png'])
        betaling = st.file_uploader("Upload Betalingsbewijs (pdf, jpg)", type=['pdf', 'jpg'])
        
        submit = st.form_submit_button("AANVRAAG INDIENEN")

        if submit:
            if all([naam, bsn, email, uittreksel, pasfoto, betaling]):
                try:
                    # Bestanden naar Storage
                    f1 = storage.create_file('documenten', ID.unique(), uittreksel)
                    f2 = storage.create_file('documenten', ID.unique(), pasfoto)
                    f3 = storage.create_file('documenten', ID.unique(), betaling)
                    
                    # Gegevens naar Database
                    databases.create_document(
                        '6a3535e5000eb1eaa8ec', 
                        'naam', 
                        ID.unique(),
                        {
                            'naam': naam,
                            'id_nummer': bsn,
                            'email': email,
                            'status': 'Nieuw',
                            'uittreksel_id': f1['$id'],
                            'pasfoto_id': f2['$id'],
                            'betaalbewijs_id': f3['$id']
                        }
                    )
                    st.success("Uw aanvraag is succesvol verzonden!")
                except Exception as e:
                    st.error(f"Er ging iets mis bij het verzenden: {e}")
            else:
                st.warning("Vul alle velden in en upload alle drie de documenten.")
st.markdown('</div>', unsafe_allow_html=True)
