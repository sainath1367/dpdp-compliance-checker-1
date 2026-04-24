import streamlit as st
from fpdf import FPDF
import spacy

def generate_pdf(result, issues):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="DPDP Compliance Report", ln=True)
    pdf.cell(200, 10, txt=f"Result: {result}", ln=True)
    
    pdf.cell(200, 10, txt="Issues Found:", ln=True)
    
    for issue in issues:
        pdf.cell(200, 10, txt=f"- {issue}", ln=True)
    
    pdf.output("report.pdf")

st.title("DPDP Compliance Checker")

uploaded_file = st.file_uploader("Upload a file")

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    
    st.subheader("File Content:")
    st.text(content[:500])

    issues = []

    if "@" in content:
        issues.append("Email detected")

    if "phone" in content:
        issues.append("Phone number detected")

    try:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(content)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                issues.append(f"Person detected: {ent.text}")
    except:
        st.warning("ML model not loaded, skipping advanced detection")

    compliance_score = max(0, 100 - len(issues) * 25)
    st.metric("Compliance Score", f"{compliance_score}%")
    st.progress(compliance_score / 100)

    if issues:
        st.error("⚠️ Sensitive Data Found")
        generate_pdf("Non-Compliant", issues)
        
        with open("report.pdf", "rb") as f:
            st.download_button("Download Report", f, file_name="report.pdf")
    else:
        st.success("✅ Compliant")