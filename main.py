import streamlit as st
import requests
import pandas as pd
import json
import base64

def main():
    st.set_page_config(layout="wide")
    st.title("DocInt")

    func_url = st.text_input("Enter the function URL")
    
    doc = st.text_input("Enter the type of the document (Telemach - ald, primus, indoma, indoma-rs, gros, spl, heva, petrol | Mladinska - pustis prazno)")


    link = st.text_input("Enter the link of the document")
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

   
    if st.button("Submit"):
        if link or pdf_file and doc:
            with st.spinner("Processing..."):
                response = None
                if pdf_file:
                    pdf_bytes = pdf_file.getvalue()
                    
                    # Encode the bytes to base64
                    b64_pdf = base64.b64encode(pdf_bytes).decode()
                    request_body = {
                        "file": b64_pdf,
                    }
                    response = requests.post(func_url, json=request_body, params={"doc": doc})
                elif link:
                    response = requests.get(func_url, params={"link": link, "doc": doc})


            try:
                data = json.loads(response.text) 
                items_df = pd.DataFrame(data['Items'])
                del data['Items']
                if data != {}:
                    st.write(data)
                st.table(items_df)
            except Exception as e:
                st.write(e)
                st.write(response)


if __name__ == "__main__":
    main()