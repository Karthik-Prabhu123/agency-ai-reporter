import streamlit as st
import pandas as pd
from groq import Groq

# Configure Page Styling
st.set_page_config(page_title="Agency AI Reporter", layout="wide", page_icon="📊")

st.markdown("""
    <style>
    .report-box { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6; }
    .metric-card { background-color: #ffffff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.title("📊 AI-Assisted Campaign Reporter (Powered by Groq)")
st.subheader("Transform messy Meta & Google ad exports into polished client briefs instantly.")

# --- SIDEBAR: SETUP & INPUTS ---
st.sidebar.header("🔑 Authentication")
api_key = st.sidebar.text_input("Enter Groq API Key", type="password", help="Get your key from console.groq.com")

st.sidebar.header("📁 Data Upload")
meta_file = st.sidebar.file_uploader("Upload Meta Ads CSV/XLSX", type=["csv", "xlsx"])
google_file = st.sidebar.file_uploader("Upload Google Ads CSV/XLSX", type=["csv", "xlsx"])

st.sidebar.header("⚙️ Report Details")
client_name = st.sidebar.text_input("Client Name", "Acme Corp")
date_range = st.sidebar.text_input("Reporting Period", "Past 7 Days")

# --- DATA PROCESSING FUNCTIONS ---
def parse_meta(file):
    try:
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        spend_col = [c for c in df.columns if 'spend' in c.lower() or 'amount spent' in c.lower()]
        roas_col = [c for c in df.columns if 'roas' in c.lower() or 'return on ad spend' in c.lower()]
        purch_col = [c for c in df.columns if 'purchase' in c.lower() or 'results' in c.lower()]
        
        # FIX: Appending .sum() twice flattens a dataframe/series into a clean native scalar float
        spend = float(df[spend_col].sum().sum()) if spend_col else 0.0
        purchases = int(df[purch_col].sum().sum()) if purch_col else 0
        roas = round(float(df[roas_col].mean().mean()), 2) if roas_col else 0.0
        return spend, purchases, roas
    except Exception as e:
        st.error(f"Error parsing Meta file: {e}")
        return 0.0, 0, 0.0

def parse_google(file):
    try:
        df = pd.read_csv(file, skiprows=0) if file.name.endswith('.csv') else pd.read_excel(file)
        if 'Cost' not in df.columns and len(df) > 1:
            df = pd.read_csv(file, skiprows=1) if file.name.endswith('.csv') else pd.read_excel(file, skiprows=1)
            
        spend_col = [c for c in df.columns if 'cost' in c.lower() or 'spend' in c.lower()]
        conv_col = [c for c in df.columns if 'conversions' in c.lower() or 'conv.' in c.lower()]
        val_col = [c for c in df.columns if 'value' in c.lower() or 'revenue' in c.lower()]
        
        # FIX: Flattening outputs safely via .sum().sum() to avoid parsing errors
        spend = float(df[spend_col].sum().sum()) if spend_col else 0.0
        conversions = float(df[conv_col].sum().sum()) if conv_col else 0.0
        conv_value = float(df[val_col].sum().sum()) if val_col else 0.0
        
        roas = round(conv_value / spend, 2) if spend > 0 else 0.0
        return spend, conversions, roas
    except Exception as e:
        st.error(f"Error parsing Google file: {e}")
        return 0.0, 0.0, 0.0

# --- MAIN APP ROUTINE ---
if st.sidebar.button("🚀 Generate Report"):
    if not api_key:
        st.warning("Please enter your Groq API key in the sidebar first.")
    elif not meta_file and not google_file:
        st.warning("Please upload at least one advertising data export file.")
    else:
        client = Groq(api_key=api_key)
        
        meta_spend, meta_purch, meta_roas = 0.0, 0, 0.0
        g_spend, g_conv, g_roas = 0.0, 0.0, 0.0
        
        if meta_file:
            meta_spend, meta_purch, meta_roas = parse_meta(meta_file)
        if google_file:
            g_spend, g_conv, g_roas = parse_google(google_file)
            
        total_spend = meta_spend + g_spend
        
        # Display Core Metric Dashboard Layer
        st.markdown("### 📈 Computed Blended Metrics")
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric("Total Blended Spend", f"${total_spend:,.2f}")
        with m_col2:
            if meta_file: st.metric("Meta Spend / ROAS", f"${meta_spend:,.2f}", f"{meta_roas}x ROAS")
        with m_col3:
            if google_file: st.metric("Google Spend / ROAS", f"${g_spend:,.2f}", f"{g_roas}x ROAS")
            
        # Build Groq Prompt Content Framework
        with st.spinner("Streaming analytical insights from Groq hardware engines..."):
            prompt = f"""
            You are a professional Account Manager at an elite growth marketing agency. 
            Write a data-backed performance update for our client '{client_name}' handling their reporting period '{date_range}'.
            
            Metrics Context:
            - Combined Ad Investment: ${total_spend:.2f}
            - Meta Ads Allocation: ${meta_spend:.2f} driving {meta_purch} conversions at a performance efficiency of {meta_roas}x ROAS.
            - Google Ads Allocation: ${g_spend:.2f} driving {g_conv} target conversion actions at an efficiency of {g_roas}x ROAS.
            
            Draft standard reporting text with:
            1. Executive Highlights: 2 highly professional sentences contextualising performance.
            2. Strategic Insights & Next Moves: Provide 3 clear bullet points highlighting platform shifts, margin performance adjustments, and optimization steps based on these numbers.
            
            Keep the tone clean, objective, ready to copy directly into emails. Do not include markdown code block containers.
            """
            
            try:
                # Call the standard Groq completion endpoint with the updated model string
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful expert marketing data assistant."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model="openai/gpt-oss-120b"  # Updated active production model identifier
                )
                
                                # FIX: Access the first element [0] of the choices list safely
                report_content = chat_completion.choices[0].message.content
                
                

                
                st.markdown("---")
                st.markdown("### 📝 Review & Edit Generated Draft")
                
                final_text = st.text_area("Interactive Editor", value=report_content, height=400)
                
                # --- NEW REPORTLAB PDF ENGINE ---
                import io
                from reportlab.lib.pagesizes import letter
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib import colors

                def create_pdf(text_content):
                    buffer = io.BytesIO()
                    # Setup clean document geometry setup
                    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
                    story = []
                    styles = getSampleStyleSheet()
                    
                    # Custom Executive Corporate Colors
                    primary_color = colors.HexColor("#1A365D")   # Deep Slate Blue
                    body_color = colors.HexColor("#2D3748")      # Charcoal Body Text
                    
                    # Define Typography Hierarchies
                    title_style = ParagraphStyle(
                        'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', 
                        fontSize=24, leading=28, textColor=primary_color, spaceAfter=8
                    )
                    meta_style = ParagraphStyle(
                        'DocMeta', parent=styles['Normal'], fontName='Helvetica-Oblique', 
                        fontSize=10, leading=14, textColor=colors.gray, spaceAfter=20
                    )
                    body_style = ParagraphStyle(
                        'DocBody', parent=styles['Normal'], fontName='Helvetica', 
                        fontSize=11, leading=18, textColor=body_color, spaceAfter=12
                    )

                    # Add Content Items to the compilation stream
                    story.append(Paragraph(f"📊 Performance Brief: {client_name}", title_style))
                    story.append(Paragraph(f"Reporting Windows: {date_range} | Generated by AI Agent Suite", meta_style))
                    story.append(Spacer(1, 10))
                    
                    # Format individual paragraph structures correctly safely inside lines
                    for paragraph in text_content.split('\n'):
                        if paragraph.strip():
                            story.append(Paragraph(paragraph.strip(), body_style))
                    
                    doc.build(story)
                    buffer.seek(0)
                    return buffer.getvalue()

                # Generate the compiled PDF bytes matrix
                pdf_data = create_pdf(final_text)

                st.download_button(
                    label="📄 Download Clean Client PDF",
                    data=pdf_data,
                    file_name=f"{client_name.lower().replace(' ', '_')}_brief.pdf",
                    mime="application/pdf"
                )

            except Exception as ai_err:
                st.error(f"Groq API Inference failed: {ai_err}. Check your token configuration.")
else:
    st.info("💡 To start, paste your Groq API Key (gsk_...), drag your CSV metrics dumps into the left sidebar, and click Generate Report.")
