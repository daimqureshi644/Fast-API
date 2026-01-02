# app_streamlit.py
import streamlit as st
import requests
import pandas as pd

# FastAPI Backend ka URL
FASTAPI_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide") # Page ko thoda wide dikhane ke liye
st.title("🏥 Daim Qureshi's Patient Portal (Streamlit Frontend)")
st.subheader("FastAPI Backend se Data Manage Karein")

# --- Function to fetch all patients ---
def get_all_patients():
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/view-all")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching data: {response.status_code} - {response.text}")
            return {}
    except requests.exceptions.ConnectionError:
        st.error("FastAPI backend chal nahi raha hai! Pehle backend run karein.")
        return {}

# --- Display All Patients ---
st.header("📋 All Patients Data")
patients_data = get_all_patients()

if patients_data:
    # Dictionary ko list of dictionaries mein convert karein for DataFrame
    patients_list = [patient for patient_id, patient in patients_data.items()]
    df = pd.DataFrame(patients_list)
    st.dataframe(df, use_container_width=True) # Dataframe ko full width mein dikhayein
else:
    st.info("No patient data found or backend is not running.")

st.markdown("---")

# --- Add New Patient ---
st.header("➕ Add New Patient")
with st.form("add_patient_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        new_id = st.text_input("Patient ID (e.g., P003)", max_chars=10)
        new_name = st.text_input("Name (e.g., Ali)", max_chars=50)
        new_email = st.text_input("Email (e.g., ali@hdfc.com)")
    with col2:
        new_city = st.text_input("City (e.g., Lahore)")
        new_age = st.number_input("Age", min_value=1, max_value=119, value=30)
        new_gender = st.selectbox("Gender", ["male", "female", "other"])
    with col3:
        new_height = st.number_input("Height (meters)", min_value=0.5, max_value=2.5, value=1.70, step=0.01)
        new_weight = st.number_input("Weight (kgs)", min_value=1.0, max_value=300.0, value=70.0, step=0.1)

    submitted = st.form_submit_button("Add Patient")

    if submitted:
        patient_data = {
            "id": new_id,
            "name": new_name,
            "email": new_email,
            "city": new_city,
            "age": new_age,
            "gender": new_gender,
            "height": new_height,
            "weight": new_weight,
        }
        try:
            response = requests.post(f"{FASTAPI_BASE_URL}/add-patient", json=patient_data)
            if response.status_code == 200:
                st.success(f"Patient {new_name} added successfully!")
                st.rerun() # Page ko refresh karein naya data dikhane ke liye
            else:
                st.error(f"Error adding patient: {response.status_code} - {response.json().get('detail', response.text)}")
        except requests.exceptions.ConnectionError:
            st.error("FastAPI backend chal nahi raha hai! Pehle backend run karein.")

st.markdown("---")

# --- Search Patient by ID ---
st.header("🔍 Search Patient by ID")
search_id = st.text_input("Enter Patient ID to Search (e.g., P001)")
if st.button("Search"):
    if search_id:
        try:
            response = requests.get(f"{FASTAPI_BASE_URL}/search/{search_id}")
            if response.status_code == 200:
                st.json(response.json())
            elif response.status_code == 404:
                st.warning(f"Patient with ID '{search_id}' not found.")
            else:
                st.error(f"Error searching: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("FastAPI backend chal nahi raha hai! Pehle backend run karein.")
    else:
        st.warning("Please enter a Patient ID.")

st.markdown("---")

# --- Update Patient by ID ---
st.header("🔄 Update Patient Data")
update_id = st.text_input("Enter Patient ID to Update (e.g., P001)", key="update_id_input")

if update_id:
    # Existing data fetch karein pre-fill karne ke liye
    existing_patient = {}
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/search/{update_id}")
        if response.status_code == 200:
            existing_patient = response.json()
        elif response.status_code == 404:
            st.warning(f"Patient with ID '{update_id}' not found for update.")
    except requests.exceptions.ConnectionError:
        st.error("Backend connection error for update.")

    with st.form("update_patient_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            updated_name = st.text_input("Name", value=existing_patient.get("name", ""))
            updated_email = st.text_input("Email", value=existing_patient.get("email", ""))
        with col2:
            updated_city = st.text_input("City", value=existing_patient.get("city", ""))
            updated_age = st.number_input("Age", min_value=1, max_value=119, value=existing_patient.get("age", 30))
            updated_gender = st.selectbox("Gender", ["male", "female", "other"], index=["male", "female", "other"].index(existing_patient.get("gender", "male")))
        with col3:
            updated_height = st.number_input("Height (meters)", min_value=0.5, max_value=2.5, value=existing_patient.get("height", 1.70), step=0.01)
            updated_weight = st.number_input("Weight (kgs)", min_value=1.0, max_value=300.0, value=existing_patient.get("weight", 70.0), step=0.1)

        update_submitted = st.form_submit_button("Update Patient")

        if update_submitted:
            if not update_id:
                st.warning("Please enter a Patient ID to update.")
            else:
                patient_data_to_update = {
                    "id": update_id, # ID ko bhi send karna zaroori hai model validation ke liye
                    "name": updated_name,
                    "email": updated_email,
                    "city": updated_city,
                    "age": updated_age,
                    "gender": updated_gender,
                    "height": updated_height,
                    "weight": updated_weight,
                }
                try:
                    response = requests.put(f"{FASTAPI_BASE_URL}/update-patient/{update_id}", json=patient_data_to_update)
                    if response.status_code == 200:
                        st.success(f"Patient {update_id} updated successfully!")
                        st.rerun()
                    else:
                        st.error(f"Error updating patient: {response.status_code} - {response.json().get('detail', response.text)}")
                except requests.exceptions.ConnectionError:
                    st.error("FastAPI backend chal nahi raha hai! Pehle backend run karein.")
else:
    st.info("Enter a Patient ID above to load and update data.")


st.markdown("---")

# --- Delete Patient ---
st.header("🗑️ Delete Patient Data")
delete_id = st.text_input("Enter Patient ID to Delete (e.g., P001)", key="delete_id_input")
if st.button("Delete Patient"):
    if delete_id:
        try:
            response = requests.delete(f"{FASTAPI_BASE_URL}/delete-patient/{delete_id}")
            if response.status_code == 200:
                st.success(f"Patient {delete_id} deleted successfully!")
                st.rerun()
            elif response.status_code == 404:
                st.warning(f"Patient with ID '{delete_id}' not found.")
            else:
                st.error(f"Error deleting: {response.status_code} - {response.json().get('detail', response.text)}")
        except requests.exceptions.ConnectionError:
            st.error("FastAPI backend chal nahi raha hai! Pehle backend run karein.")
    else:
        st.warning("Please enter a Patient ID to delete.")

st.markdown("---")
st.caption("Developed by Daim Qureshi for FastAPI & Streamlit Practice")