import streamlit as st
from autoclearance.crew import AutoclearanceCrew

# 1. Page Config
st.set_page_config(page_title="AutoClearance AI", layout="wide")
# --- 🔐 简单的密码保护锁 ---
password = st.sidebar.text_input("🔑 访问密码 (Password)", type="password")
if password != "123456":
    st.info("请输入密码以解锁 AI 功能 | Please enter the password to access.")
    st.stop()
# -------------------------
st.title("AutoClearance: AI Compliance Audit System")
st.markdown("---")

# 2. Sidebar: Input Area
with st.sidebar:
    st.header("Invoice Data Entry")
    
    # Default test data (with intentional errors)
    default_invoice = """
    INVOICE #001
    Desc: Plastic Toys (Kids)
    Qty: 100 pcs
    Unit Price: $5.00
    Total: $400.00
    GW: 50kg
    NW: 60kg
    """
    
    # Input Text Area
    invoice_input = st.text_area("Paste Invoice Text / OCR Output", value=default_invoice, height=300)
    
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
            inputs = {'invoice_data': invoice_input}
            
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