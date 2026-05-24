import streamlit as st
from chatbot.generator import generate_assignment
from chatbot.exporter import export_word, export_pdf
from datetime import date

st.set_page_config(page_title="SZABIST Assignment Bot", page_icon="📝", layout="centered")

st.markdown("""
<style>
    .stButton>button {
        background-color: #003366;
        color: white;
        width: 100%;
        font-size: 16px;
        padding: 10px;
        border-radius: 8px;
    }
    h1 { color: #003366; }
</style>
""", unsafe_allow_html=True)

st.title("📝 SZABIST Assignment Generator")
st.markdown("Fill in your details and topic — get a ready-to-submit formatted assignment!")

with st.form("assignment_form"):
    col1, col2 = st.columns(2)
    with col1:
        student_name  = st.text_input("Student Name", placeholder="e.g. Manan")
        reg_number    = st.text_input("Registration Number", placeholder="e.g. 25108312")
        batch         = st.text_input("Batch / Section", value="BSAI-2D")
    with col2:
        submitted_to    = st.text_input("Submitted To (Teacher)", placeholder="e.g. Mr Mujtaba")
        dept_abbr       = st.text_input("Department Abbreviation (header right cell)", value="AI", help="Short code shown in grey cell e.g. AI, CS, SE")
        dept_code       = st.text_input("Footer Department Code", value="DR&AI", help="e.g. DR&AI shown in footer")

    col3, col4, col5 = st.columns(3)
    with col3:
        subject = st.text_input("Subject", placeholder="e.g. PAK.STUDIES")
    with col4:
        assignment_no = st.text_input("Assignment No.", value="01")
    with col5:
        total_marks = st.text_input("Total Marks", value="06")

    submission_date = st.text_input("Last Date of Submission", value=date.today().strftime("%d/%m/%Y"))
    topic  = st.text_area("Assignment Topic / Question", placeholder="e.g. Pakistan's relationship with USA and China", height=100)
    pages  = st.slider("Approximate Pages", min_value=1, max_value=10, value=3)

    submitted = st.form_submit_button("🚀 Generate Assignment")

if submitted:
    if not all([student_name, reg_number, submitted_to, subject, topic]):
        st.error("Please fill in all required fields.")
    else:
        with st.spinner("Generating your assignment... please wait ⏳"):
            info = {
                "student_name":    student_name,
                "reg_number":      reg_number,
                "submitted_to":    submitted_to,
                "batch":           batch,
                "department":      "AI AND ROBOTICS",
                "dept_abbr":       dept_abbr,
                "dept_code":       dept_code,
                "subject":         subject,
                "assignment_no":   assignment_no,
                "submission_date": submission_date,
                "total_marks":     total_marks,
                "topic":           topic,
                "pages":           pages,
            }
            content = generate_assignment(info)

        if content:
            st.success("✅ Assignment generated!")
            st.text_area("Preview", content, height=400)

            word_bytes = export_word(info, content)
            pdf_bytes  = export_pdf(info, content)

            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button(
                    label="📄 Download Word (.docx)",
                    data=word_bytes,
                    file_name=f"Assignment_{subject.replace(' ','_').replace('.','')}_No{assignment_no}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            with col_b:
                st.download_button(
                    label="📑 Download PDF",
                    data=pdf_bytes,
                    file_name=f"Assignment_{subject.replace(' ','_').replace('.','')}_No{assignment_no}.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("Something went wrong. Check your .env file has a valid GITHUB_TOKEN.")
