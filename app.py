import streamlit as st
import os
import PyPDF2 as pdf
import google.generativeai as genai

#for environment variable
from dotenv import load_dotenv
load_dotenv() 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Gemini pro response
def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in reader.pages:
        text += page.extract_text()
    return text     
    # for page in reader(len(reader.pages)):
    #     page=reader.pages[page]
    #     text+=str(page.extract_text())
       

#prompt template
input_prompt="""
Act like a skilled or very experienced ATS(Application Tracking System) with a deep understanding of 
tech field, software engineering, data science, data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide best assistance for improving th resume.
Assign percentage matching based on JD and the missing keywords with high accuracy.
resume:{text}
description:{jd}

I want the response in one single string having the structure 
{{"JD Match":"%","MissingKeywords:[]", "Profile Summary":""}}

"""


#streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload your resume", type="pdf", help="Please upload the pdf file")


submit=st.button("Submit")

if submit:
    if uploaded_file is not None:
       text=input_pdf_text(uploaded_file)
       response=get_gemini_response(input_prompt) 
       st.subheader(response)