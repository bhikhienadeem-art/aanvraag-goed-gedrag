import streamlit as st
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.id import ID

# Appwrite configuratie
client = Client()
(client
  .set_endpoint('https://cloud.appwrite.io/v1') 
  .set_project('6a35359b000c27a4ab88')) 

databases = Databases(client)
storage = Storage(client)

st.title("Online VOG Aanvraag (Bewijs van Goed Gedrag)")

# Uitleg sectie (zoals in het ontwerp)
st.info("### Voorbereiding: Dit heeft u nodig")
st.markdown("- **1. Uittreksel:** Geldig burgerlijkheidsuittreksel (.pdf, .jpg)")
st.markdown("- **2. Pasfoto:** Recente pasfoto (.jpg, .png)")
st.markdown("- **3. Betalingsbewijs:** Bewijs van bankoverschrijving (.pdf, .jpg)")

with st.form("aanvraag_formulier"):
    naam = st.text_input("Volledige Naam")
    bsn = st.text_input("BSN-nummer")
    email = st.text_input("E-mailadres")
    
    uittreksel = st.file_uploader("Upload Uittreksel", type=['pdf', 'jpg'])
    pasfoto = st.file_uploader("Upload Pasfoto", type=['jpg', 'png'])
    betaling = st.file_uploader("Upload Betalingsbewijs", type=['pdf', 'jpg'])
    
    submit = st.form_submit_button("Indienen voor verwerking")

    if submit:
        if uittreksel and pasfoto and betaling:
            try:
                # Bestanden uploaden naar Storage bucket 'documenten'
                f1 = storage.create_file('documenten', ID.unique(), uittreksel)
                f2 = storage.create_file('documenten', ID.unique(), pasfoto)
                f3 = storage.create_file('documenten', ID.unique(), betaling)
                
                # Gegevens opslaan in database
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
                st.error(f"Fout bij opslaan: {e}")
        else:
            st.warning("Zorg dat u alle documenten heeft geüpload.")
