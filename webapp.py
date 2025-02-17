import streamlit as st
import os
import load_answer as load_answer
import load_data as load_data
import pdfplumber
from fpdf import FPDF
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_store_dir = os.path.join(current_dir, "document")

st.title("Insurance Policy Recommendor")

file_uploaded = st.file_uploader("Upload pdf file..", type="pdf")
def read_pdf_text(file):
    all_text = []
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                lines = page.extract_text_lines()
                for line in lines:
                    all_text.append(line.get('text'))
    except:
         st.write("None")
    return all_text

# def read_pdf_tables(file):
#     all_tables = []
#     try:
#         with pdfplumber.open(file) as pdf:
#             for i in pdf.pages:
#                 all_text += i.extract_tables()
#     except:
#          st.write("None")
#     return all_tables

def create_and_store_pdf(new_pdf_dir,pdf_text):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font('helvetica', 'BIU', 8)
    
    for i in pdf_text:
        #Remove special character from string.
        clean_text = re.sub(r'[^a-zA-Z0-9 ,.]', '', i)
        pdf.cell(0, 10, clean_text, new_x="LEFT", new_y="NEXT")
        
    pdf.output(new_pdf_dir)
    

if file_uploaded is not None and file_uploaded.type == "application/pdf":
    
    new_pdf_dir = os.path.join(pdf_store_dir, file_uploaded.name)
    
    pdf_text = read_pdf_text(file_uploaded)
    # print("###################")
    # print(pdf_text)
    
    # pdf_tables = read_pdf_tables(file_uploaded)
    
    create_and_store_pdf(new_pdf_dir,pdf_text)
    
if st.button("Run Model"):
    load_data.load_pdf_data()
    st.write("Model executed.")
    

st.subheader("Enter policy requirements...")
    
with st.form("Select your plan."):
    
    coverage_amount = st.selectbox(
    "Coverage",
    ["$50,000 – $500,000", "$100,000 – $1,000,000", "$100,000 – $5,000,000", 
     "$150,000 – $1,500,000", "$200,000 – $2,000,000", "$250,000 – $2,000,000", 
     "$500,000 – $2,000,000", "$500,000 – $10,000,000", "$1,000,000 – $5,000,000", 
     "$2,000,000 – $10,000,000"]
    )
     
    policy_term = st.selectbox('Policy Term',
    ('10 – 30 years', '15 – 25 years', 'Lifetime coverage', '10 – 20 years', 'Until age 80',
     '0 - 25 years','Per trip annual coverage','10 – 25 years','Matches mortgage duration','Customizable'
     )
    )

    premium = st.selectbox(
    "Premium",
    ["Starts at $50/month", "Starts at $40/month", "Starts at $80/month", 
     "Starts at $25/month", "Starts at $60/month", "Based on business valuation", 
     "Starts at $30/month", "Starts at $70/month", "Starts at $45/month", 
     "Starts at $35/month"]
    )
   
    # List of additional benefits
    additional_benefits = [
    "Critical illness coverage",
    "Waiver of premium",
    "Accidental death benefit",
    "Disability income benefits",
    "Long-term care benefits",
    "Estate planning support",
    "Education fund",
    "Future insurability option",
    "Pension payouts",
    "Guaranteed income after retirement"
    ]

    # Streamlit multiselect widget
    selected_benefits = st.multiselect(
    "Select Additional Benefits:",
    options=additional_benefits,
    )   
    
    additional_benefits_string = "".join(str(x) for x in selected_benefits) 

    submitted = st.form_submit_button("Submit")
    
    query = (f"""Provide information about any existing one or more policy that most matches below details:
            Coverage Amount: {coverage_amount}, 
            Policy Term: {policy_term}, 
            Premiums: {premium}, 
            Additional Benefits: {additional_benefits_string}""")

    if submitted:
        result = load_answer.get_answer(query)
        # st.write("Coverage Amount: ", coverage_amount, "\n", "Policy Term: ", policy_term, "\n", "Premium: ", premium, "\n", "Additional Benefits: ", additional_benefits)
        st.divider()
        st.subheader("Recommended policy based on above selected values:")
        st.write(result)