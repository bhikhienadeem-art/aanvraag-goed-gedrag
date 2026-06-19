import streamlit as st
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID

# Appwrite configuratie
client = Client()
(client
  .set_endpoint('https://cloud.appwrite.io/v1') 
  .set_project('6a35359b000c27a4ab88')) 

databases = Databases(client)

st.title("Aanvraag Bewijs van Goed Gedrag")

with st.form("aanvraag"):
    naam = st.text_input("Volledige naam")
    id_nummer = st.text_input("ID-nummer")
    email = st.text_input("E-mailadres")
    
    submit = st.form_submit_button("Aanvraag indienen")

    if submit:
        try:
            databases.create_document(
                '6a3535e5000eb1eaa8ec', 
                'naam', 
                ID.unique(),
                {
                    'naam': naam,
                    'id_nummer': id_nummer,
                    'email': email,
                    'status': 'Nieuw'
                }
            )
            st.success("Aanvraag succesvol verzonden!")
        except Exception as e:
            st.error(f"Er ging iets mis: {e}")
