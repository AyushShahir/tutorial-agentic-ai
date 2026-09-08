import streamlit as st
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration to wide layout
st.set_page_config(
    page_title="Blood Work Analyzer",
    page_icon="🩸",
    layout="wide"
)

# Premium dark theme styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Main container styling */
    .stApp {
        background-color: #0d0f12;
        color: #f3f4f6;
    }
    html, body {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Title styling */
    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ff4d4d 0%, #f9ab20 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
    }
    
    /* Column headers */
    .column-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 10px;
        margin-bottom: 12px;
        border-bottom: 2px solid #2d3139;
        padding-bottom: 6px;
    }
    
    /* Styled scrollable text boxes */
    .output-box {
        height: 230px;
        overflow-y: auto;
        padding: 16px;
        border: 1px solid #2d3139;
        border-radius: 10px;
        background-color: #161a22;
        font-size: 0.95rem;
        line-height: 1.6;
        color: #d1d5db;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Custom style for empty outputs */
    .output-empty {
        color: #6b7280;
        font-style: italic;
    }
    
    /* Style the text area container */
    div[data-baseweb="textarea"] {
        border-color: #2d3139 !important;
        background-color: #161a22 !important;
        border-radius: 10px !important;
    }
    
    /* Style the text area input itself */
    textarea {
        color: #f3f4f6 !important;
        font-family: monospace !important;
        background-color: #161a22 !important;
    }
    
    /* Customize Primary Button style */
    div.stButton > button {
        background: linear-gradient(135deg, #ff4d4d 0%, #e02f2f 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 6px rgba(239, 68, 68, 0.2) !important;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #ff6666 0%, #ff4d4d 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 12px rgba(239, 68, 68, 0.3) !important;
    }

    /* Scrollbar styling */
    .output-box::-webkit-scrollbar {
        width: 6px;
    }
    .output-box::-webkit-scrollbar-track {
        background: #11141a;
        border-radius: 10px;
    }
    .output-box::-webkit-scrollbar-thumb {
        background: #374151;
        border-radius: 10px;
    }
    .output-box::-webkit-scrollbar-thumb:hover {
        background: #4b5563;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to convert basic markdown formatting to clean HTML for output boxes
def markdown_to_html(text):
    if not text:
        return ""
    # Convert bold (**text**) to <strong>text</strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Convert list items (- item or * item) to <li>
    lines = text.split('\n')
    in_list = False
    html_lines = []
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            continue
        if line_strip.startswith('- ') or line_strip.startswith('* '):
            if not in_list:
                html_lines.append('<ul style="margin-top: 5px; margin-bottom: 5px; padding-left: 20px;">')
                in_list = True
            html_lines.append(f'<li style="margin-bottom: 4px;">{line_strip[2:]}</li>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<p style="margin-top: 5px; margin-bottom: 5px;">{line_strip}</p>')
    if in_list:
        html_lines.append('</ul>')
    return "".join(html_lines)

# App Title
st.markdown('<h1 class="app-title">Blood Work Analyzer</h1>', unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.markdown('<div class="column-header">Blood Work Report</div>', unsafe_allow_html=True)
    blood_report = st.text_area(
        label="Paste your blood report",
        height=500,
        placeholder="Paste your blood work report here...",
        label_visibility="collapsed"
    )
    analyze_clicked = st.button("Analyze", type="primary", use_container_width=True)

with right_col:
    st.markdown('<div class="column-header">Health Summary</div>', unsafe_allow_html=True)
    health_box = st.empty()
    health_box.markdown('<div class="output-box output-empty">No summary generated yet. Enter report and click Analyze.</div>', unsafe_allow_html=True)

    st.markdown('<div class="column-header">Suggested Diet Plan</div>', unsafe_allow_html=True)
    diet_box = st.empty()
    diet_box.markdown('<div class="output-box output-empty">No diet plan generated yet. Enter report and click Analyze.</div>', unsafe_allow_html=True)

# Fetch API Key from Environment
api_key = os.environ.get("GOOGLE_API_KEY")

if analyze_clicked:
    if not blood_report.strip():
        st.warning("Please paste a blood work report before analyzing.")
    elif not api_key:
        st.error("Google API Key not found. Please set the GOOGLE_API_KEY environment variable.")
    else:
        with st.spinner("Analyzing your blood work..."):
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash",
                    google_api_key=api_key
                )
                
                # Stage 1: Extract and flag abnormal values
                extraction_prompt = f"""
You are a medical data extraction assistant.

From the blood report below, extract ALL test values and classify each one as HIGH, LOW, or NORMAL
based on the reference ranges provided in the report.

Format your response as:
- Test Name: value | Status: HIGH/LOW/NORMAL | Reference: range

Blood Report:
{blood_report}
"""
                extraction_response = llm.invoke(extraction_prompt)
                extracted_values = extraction_response.text

                # Stage 2: Health summary and Indian diet plan
                diet_prompt = f"""
You are a clinical nutritionist specializing in Indian dietary habits.

Based on the blood work analysis below, provide two clearly separated sections:

SECTION 1 - HEALTH SUMMARY:
Write 4-5 lines explaining the patient's condition in simple, non-technical language.

SECTION 2 - INDIAN DIET PLAN:
List foods to eat more of and foods to avoid, using commonly available Indian foods
like dal, sabzi, roti, rice, etc. Keep it practical and concise.

Blood Work Analysis:
{extracted_values}
"""
                diet_response = llm.invoke(diet_prompt)
                full_response = diet_response.text

                # Split response into two sections
                if "SECTION 2" in full_response:
                    parts = full_response.split("SECTION 2")
                    health_summary = parts[0].replace("SECTION 1 - HEALTH SUMMARY:", "").replace("SECTION 1", "").strip()
                    diet_plan = ("SECTION 2" + parts[1]).replace("SECTION 2 - INDIAN DIET PLAN:", "").replace("SECTION 2", "").strip()
                else:
                    health_summary = full_response
                    diet_plan = ""

                # Format outputs to clean HTML
                health_html = markdown_to_html(health_summary)
                diet_html = markdown_to_html(diet_plan if diet_plan else full_response)

                # Render into fixed-height scrollable boxes
                health_box.markdown(
                    f'<div class="output-box">{health_html}</div>',
                    unsafe_allow_html=True
                )
                diet_box.markdown(
                    f'<div class="output-box">{diet_html}</div>',
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
