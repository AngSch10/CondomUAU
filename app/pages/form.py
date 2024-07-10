import streamlit as st
import json

st.title('Fill the form')

# Example form fields
name = st.text_input("Name")
age = st.number_input("Age", step=1)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
feedback = st.text_area("Feedback")

if st.button("Submit"):
    form_data = {
        "Name": name,
        "Age": age,
        "Gender": gender,
        "Feedback": feedback
    }
    
    # Process the data as needed
    st.write("Form Submitted Successfully!")
    st.json(form_data)
    
    # Optionally, save the data to a file
    #with open("form_data.json", "w") as f:
    #    json.dump(form_data, f)