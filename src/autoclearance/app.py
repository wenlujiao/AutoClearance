import streamlit as st
import PyPDF2
import pandas as pd
from io import BytesIO
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autoclearance.crew import AutoclearanceCrew

# 1. Page Config
st.set_page_config(page_title="AutoClearance AI", layout="wide")

# --- Password Protection ---
# Only allow access if password is correct
password = st.sidebar.text_input("Password", type="password")
if password != "123456":
    st.info("Please enter the password to access.")
    st.stop()

# 2. Sidebar: Input Area
with st.sidebar:
    st.header("Invoice Data Entry")

    # --- PDF Upload Section ---
    st.subheader("Upload Invoice (PDF)")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    invoice_text = ""  # Initialize variable

    if uploaded_file is not None:
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                invoice_text += page.extract_text()
            st.success("PDF read successfully!")
            
            # Optional: Show extracted text
            with st.expander("View Extracted Text"):
                st.text(invoice_text)
                
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

    # Fallback: Manual Text Input (if no PDF uploaded)
    if not invoice_text:
        invoice_text = st.text_area("Or paste invoice text here:", height=300)
    
    # Run Button
    run_btn = st.button("Start AI Audit", type="primary")

# 3. Main Interface
st.title("AutoClearance: AI Compliance Audit System")
st.markdown("---")

# 4. Main Logic
if run_btn:
    if not invoice_text:
        st.warning("Please upload a PDF or paste invoice text first.")
    else:
        with st.spinner("AI Agents are analyzing the invoice..."):
            try:
                # Initialize the crew
                crew_instance = AutoclearanceCrew()
                
                # Run the crew
                # Note: 'invoice_data' must match the variable in your Task description
                inputs = {'invoice_data': invoice_text}
                result = crew_instance.crew().kickoff(inputs=inputs)
                
                # Display Results
                st.success("Audit Complete!")
                st.subheader("Audit Report")
                st.markdown(result)
                
                # ... 在 AI 运行结束后 ...
                try:
                    # 假设 AI 返回的是结构化字符串，我们先把它转成表格
                    # 这里的 result 最好是经过 AI 处理后的干净数据
                    data = json.loads(result) # 这里的 result 需确保是 JSON 格式
                    df_items = pd.DataFrame(data['items'])

                    st.subheader("📦 自动化单证生成")
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        # 输出 3：CSV 导出
                        csv = df_items.to_csv(index=False).encode('utf-8')
                        st.download_button("下载结构化数据 (CSV)", csv, "clearance_data.csv", "text/csv")

                    with col2:
                        st.button("生成标准发票 (PDF) - 开发中")

                    with col3:
                        st.button("生成装箱单 (PDF) - 开发中")

                except:
                    st.warning("AI 返回的不是标准结构，正在尝试解析...")
                    st.markdown(result)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")