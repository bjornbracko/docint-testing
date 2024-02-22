import streamlit as st
import requests
import pandas as pd
import json
import base64


def main():
    st.title("DocInt")

    func_url = st.text_input("Enter the function URL")
    

    link = st.text_input("Enter the link of the document")
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if link or pdf_file:
        response = None
        if pdf_file:
            pdf_bytes = pdf_file.getvalue()
            
            # Encode the bytes to base64
            b64_pdf = base64.b64encode(pdf_bytes).decode()
            request_body = {
                "file": b64_pdf,
            }
            response = requests.post(func_url, json=request_body)
        elif link:
            response = requests.get(func_url, params={"link": link})

        data = json.loads(response.text)
        # Display Total and Invoice Number
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"Invoice Number: {data['InvoiceNumber']}")
            
        with col2:
            st.write(f"Total: {data['Total']}")

        # Convert the items list to a pandas DataFrame and display it
        items_df = pd.DataFrame(data['Items'])
        st.table(items_df)



if __name__ == "__main__":
    main()