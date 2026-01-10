import streamlit as st
import PyPDF2  
from autoclearance.crew import AutoclearanceCrew

# 1. Page Config
st.set_page_config(page_title="AutoClearance AI", layout="wide")
# --- password seting
password = st.sidebar.text_input
if password != "123456":
    st.info("Please enter the password to access.")
    st.stop()
# -------------------------
st.title("AutoClearance: AI Compliance Audit System")
st.markdown("---")

# 2. Sidebar: Input Area
with st.sidebar:
    st.header("Invoice Data Entry")

    # --- PDF Upload Section ---
    st.subheader("Upload Invoice (PDF)")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    invoice_text = ""  # Initialize as empty string

    if uploaded_file is not None:
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                invoice_text += page.extract_text()
            st.success("PDF read successfully!")
            
            with st.expander("View Extracted Text"):
                st.text(invoice_text)
                
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

    # If no file uploaded, allow manual input
    if not invoice_text:
        invoice_text = st.text_area("Or paste invoice text here:", height=300)
    
    # Run Button
    run_btn = st.button("Start AI Audit", type="primary")
    
    # Run Button
    run_btn = st.button("Start AI Audit", type="primary")

# 3. Main Interface: Results
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Audit Logs")
    log_container = st.empty() # Placeholder for live logs

with col2:
    st.subheader("Final Report")
    result_container = st.empty()

# 4. Core Logic
if run_btn:
    with st.spinner('Processing invoice data...'):
        try:
            # Prepare inputs
            inputs = {'invoice_data': invoice_text}
            
            # --- Run Crew ---
            crew_output = AutoclearanceCrew().crew().kickoff(inputs=inputs)
            result_str = str(crew_output)
            
            # --- Check Results ---
            if "Risk Alert" in result_str or "FAILED" in result_str:
                # Error Box
                st.error("Compliance Risk Detected")
                
                with col2:
                    st.warning("System Intervention: Logical inconsistency found.")
                    st.text(result_str)
                    
                    # --- Manual Correction Form ---
                    st.markdown("### Action Required")
                    st.info("Weight discrepancy detected (GW < NW). Please correct below:")
                    
                    with st.form("correction_form"):
                        new_gw = st.text_input("Correct Gross Weight (GW):")
                        new_nw = st.text_input("Correct Net Weight (NW):")
                        submit_correction = st.form_submit_button("Submit & Re-run")
                        
                    if submit_correction:
                        st.write("Feature coming soon: Session State management needed for web loops...")
            
            else:
                # Success Box
                st.success("Audit Passed")
                result_container.markdown(result_str)

        except Exception as e:
            st.error(f"System Error: {e}")