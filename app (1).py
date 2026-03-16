import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime, date
import openpyxl

st.set_page_config(
    page_title="GSTGenius AI — GST Compliance Platform",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #f8fafc !important;
    color: #1e293b !important;
}
.stApp { background-color: #f8fafc !important; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
    padding-top: 0 !important;
}
section[data-testid="stSidebar"] * { color: #1e293b !important; }
section[data-testid="stSidebar"] .stRadio label {
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 12px !important;
    border-radius: 6px !important;
    display: block !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: #f1f5f9 !important;
}

/* TOP HEADER BAR */
.top-header {
    background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
    padding: 20px 32px;
    border-radius: 12px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.top-header h1 {
    color: white !important;
    font-size: 24px !important;
    font-weight: 700 !important;
    margin: 0 !important;
}
.top-header p { color: rgba(255,255,255,0.8) !important; margin: 0 !important; font-size: 13px !important; }

/* METRIC CARDS */
[data-testid="metric-container"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    padding: 20px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
}
[data-testid="metric-container"] label {
    color: #64748b !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #1e3a5f !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}

/* BUTTONS */
.stButton > button {
    background: #2563eb !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #1d4ed8 !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.3) !important;
}

/* CARDS */
.card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.card-blue {
    background: linear-gradient(135deg, #1e3a5f, #2563eb);
    color: white;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
}

/* HEADINGS */
h1 { color: #1e3a5f !important; font-weight: 800 !important; font-size: 28px !important; }
h2 { color: #1e3a5f !important; font-weight: 700 !important; font-size: 22px !important; }
h3 { color: #334155 !important; font-weight: 600 !important; font-size: 16px !important; }

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background: #f8fafc !important;
    border: 2px dashed #cbd5e1 !important;
    border-radius: 10px !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background: #f1f5f9 !important;
    border-radius: 8px !important;
    padding: 4px !important;
    border: 1px solid #e2e8f0 !important;
}
.stTabs [data-baseweb="tab"] {
    color: #64748b !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #2563eb !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
}

/* INPUTS */
.stTextInput input, .stNumberInput input {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    color: #1e293b !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}

/* SELECTBOX */
[data-testid="stSelectbox"] > div > div {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}

/* SUCCESS / ERROR / WARNING */
.stSuccess { background: #f0fdf4 !important; border: 1px solid #bbf7d0 !important; border-radius: 8px !important; color: #166534 !important; }
.stError { background: #fef2f2 !important; border: 1px solid #fecaca !important; border-radius: 8px !important; color: #991b1b !important; }
.stWarning { background: #fffbeb !important; border: 1px solid #fde68a !important; border-radius: 8px !important; color: #92400e !important; }
.stInfo { background: #eff6ff !important; border: 1px solid #bfdbfe !important; border-radius: 8px !important; color: #1e40af !important; }

/* DIVIDER */
hr { border-color: #e2e8f0 !important; }

/* BADGE */
.badge-green { background:#dcfce7; color:#166534; padding:4px 12px; border-radius:99px; font-size:12px; font-weight:600; }
.badge-red { background:#fee2e2; color:#991b1b; padding:4px 12px; border-radius:99px; font-size:12px; font-weight:600; }
.badge-yellow { background:#fef9c3; color:#854d0e; padding:4px 12px; border-radius:99px; font-size:12px; font-weight:600; }
.badge-blue { background:#dbeafe; color:#1e40af; padding:4px 12px; border-radius:99px; font-size:12px; font-weight:600; }

/* SCROLLBAR */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>
""", unsafe_allow_html=True)

# ─── GST DATA ────────────────────────────────────────────────────────────────
GST_RULES = {
    "food": 0, "rice": 0, "wheat": 0, "milk": 0, "vegetables": 0,
    "fruits": 0, "eggs": 0, "meat": 0, "fish": 0, "salt": 0,
    "restaurant": 5, "transport": 5, "clothing": 5, "footwear": 5,
    "medicine": 5, "fertilizer": 5, "coal": 5,
    "electronics": 18, "mobile": 18, "laptop": 18, "software": 18,
    "furniture": 18, "insurance": 18, "banking": 18, "telecom": 18,
    "hotel": 18, "construction": 18, "it services": 18,
    "luxury": 28, "car": 28, "tobacco": 28, "alcohol": 28,
    "pan masala": 28, "aerated drinks": 28, "cement": 28,
    "textile": 12, "processed food": 12, "butter": 12, "cheese": 12,
    "ayurvedic": 12, "playing cards": 12
}

LATE_FEES = {"GSTR-1": 50, "GSTR-3B": 50, "GSTR-9": 200, "GSTR-4": 50}

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1e3a5f,#2563eb);padding:20px;margin:-1rem -1rem 1rem -1rem;'>
        <div style='color:white;font-size:20px;font-weight:800;'>🧾 GSTGenius AI</div>
        <div style='color:rgba(255,255,255,0.75);font-size:12px;margin-top:4px;'>Professional GST Compliance Platform</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("Navigation", [
        "📊 Dashboard",
        "✅ GST Rate Checker",
        "🧾 Invoice Validator",
        "💰 ITC Calculator",
        "📅 Filing Tracker",
        "⚠️ Late Fee Calculator",
        "📈 Analytics",
        "❓ GST FAQ Bot"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("<p style='font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:1px;'>Business Profile</p>", unsafe_allow_html=True)
    business_name = st.text_input("Business Name", "My Business", label_visibility="collapsed", placeholder="Business Name")
    gstin = st.text_input("GSTIN", "27AAAAA0000A1Z5", label_visibility="collapsed", placeholder="GSTIN")
    filing_period = st.selectbox("Filing Period", [
        "April 2025","May 2025","June 2025","July 2025","August 2025",
        "September 2025","October 2025","November 2025","December 2025",
        "January 2026","February 2026","March 2026"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
    <div style='background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:12px;'>
        <p style='font-size:12px;color:#1e40af;font-weight:600;margin:0;'>📞 Support</p>
        <p style='font-size:11px;color:#3b82f6;margin:4px 0 0;'>guptasanskar824@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def get_sample_data():
    return pd.DataFrame({
        "Invoice No": ["INV001","INV002","INV003","INV004","INV005","INV006","INV007","INV008","INV009","INV010"],
        "Item": ["Laptop","Rice","Restaurant Bill","Mobile Phone","Wheat","Car Insurance","Clothing","Software License","Butter","Tobacco"],
        "Category": ["electronics","food","restaurant","mobile","wheat","insurance","clothing","software","butter","tobacco"],
        "Amount (₹)": [50000,5000,2000,25000,3000,10000,1500,10000,500,2000],
        "GST Applied (%)": [18,5,5,18,0,18,12,18,12,28],
        "GSTIN of Supplier": ["27AAAAA0000A1Z5","29BBBBB1111B2Y6","07CCCCC2222C3X7","27AAAAA0000A1Z5","33DDDDD3333D4W8","29BBBBB1111B2Y6","07CCCCC2222C3X7","27AAAAA0000A1Z5","33DDDDD3333D4W8","29BBBBB1111B2Y6"],
        "Invoice Date": ["2025-01-05","2025-01-07","2025-01-10","2025-01-12","2025-01-15","2025-01-18","2025-01-20","2025-01-22","2025-01-25","2025-01-28"],
        "HSN Code": ["8471","1006","9963","8517","1001","9971","6203","8523","0401","2401"]
    })

def check_compliance(df):
    results = []
    for _, row in df.iterrows():
        category = str(row["Category"]).lower().strip()
        gst_applied = float(row["GST Applied (%)"])
        amount = float(row["Amount (₹)"])
        expected = GST_RULES.get(category, None)
        if expected is None: status, flag = "⚠️ Unknown Category", "unknown"
        elif gst_applied == expected: status, flag = "✅ Correct", "correct"
        else: status, flag = f"❌ Wrong — Should be {expected}%", "wrong"
        gst_amount = amount * gst_applied / 100
        results.append({"Invoice No": row.get("Invoice No","-"),"Item": row["Item"],"Amount (₹)": amount,"GST Applied (%)": gst_applied,"Expected GST (%)": expected if expected is not None else "Unknown","GST Amount (₹)": round(gst_amount,2),"Status": status,"Flag": flag})
    return pd.DataFrame(results)

def to_excel(df):
    output = BytesIO()
    df.to_excel(output, index=False)
    return output.getvalue()

def page_header(title, subtitle):
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#1e3a5f 0%,#2563eb 100%);padding:24px 32px;border-radius:12px;margin-bottom:24px;'>
        <h1 style='color:white!important;font-size:22px!important;font-weight:700!important;margin:0!important;'>{title}</h1>
        <p style='color:rgba(255,255,255,0.75);font-size:13px;margin:6px 0 0;'>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def color_rows(row):
    if "❌" in str(row["Status"]): return ["background-color:#fee2e2;color:#991b1b"]*len(row)
    elif "✅" in str(row["Status"]): return ["background-color:#dcfce7;color:#166534"]*len(row)
    else: return ["background-color:#fef9c3;color:#854d0e"]*len(row)

# ════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
if page == "📊 Dashboard":
    page_header(f"🧾 GSTGenius AI — {business_name}", f"GSTIN: {gstin}  |  Filing Period: {filing_period}  |  {date.today().strftime('%d %B %Y')}")

    col_l, col_r = st.columns([2,1])
    with col_l:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("#### 📤 Upload Transaction File")
        uploaded = st.file_uploader("Upload Excel / CSV file", type=["xlsx","csv"], key="dash", label_visibility="collapsed")
        sample_df = get_sample_data()
        st.download_button("⬇️ Download Sample File", to_excel(sample_df), "sample_transactions.xlsx", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#1e3a5f,#2563eb);border-radius:12px;padding:24px;color:white;'>
            <p style='font-size:12px;opacity:0.75;text-transform:uppercase;letter-spacing:1px;margin:0;'>Platform</p>
            <p style='font-size:28px;font-weight:800;margin:8px 0;'>GSTGenius AI</p>
            <p style='font-size:13px;opacity:0.8;margin:0;'>Professional GST Compliance<br>for Indian Businesses</p>
        </div>
        """, unsafe_allow_html=True)

    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith("xlsx") else pd.read_csv(uploaded)
        results_df = check_compliance(df)
        correct = len(results_df[results_df["Flag"]=="correct"])
        wrong = len(results_df[results_df["Flag"]=="wrong"])
        unknown = len(results_df[results_df["Flag"]=="unknown"])
        total_gst = results_df["GST Amount (₹)"].sum()
        score = int((correct/len(results_df))*100) if len(results_df) > 0 else 0

        st.markdown("#### 📊 Compliance Overview")
        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Compliance Score", f"{score}%")
        c2.metric("Total Transactions", len(results_df))
        c3.metric("✅ Correct", correct)
        c4.metric("❌ Errors", wrong)
        c5.metric("💰 Total GST", f"₹{total_gst:,.0f}")

        col1, col2 = st.columns(2)
        with col1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={"text":"Compliance Score","font":{"color":"#1e3a5f","size":14}},
                gauge={"axis":{"range":[0,100],"tickcolor":"#94a3b8"},"bar":{"color":"#2563eb"},"steps":[{"range":[0,50],"color":"#fee2e2"},{"range":[50,75],"color":"#fef9c3"},{"range":[75,100],"color":"#dcfce7"}]},
                number={"suffix":"%","font":{"color":"#1e3a5f","size":36}}
            ))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="#1e293b",height=280,margin=dict(t=40,b=20))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            status_counts = results_df["Flag"].value_counts().reset_index()
            status_counts.columns = ["Status","Count"]
            fig2 = px.pie(status_counts, values="Count", names="Status",
                color_discrete_map={"correct":"#2563eb","wrong":"#ef4444","unknown":"#f59e0b"},
                title="Transaction Status")
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="#1e293b",height=280,margin=dict(t=40,b=20))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("#### 📋 Transaction Report")
        display_df = results_df.drop("Flag", axis=1)
        st.dataframe(display_df.style.apply(color_rows, axis=1), use_container_width=True)
        st.download_button("⬇️ Download Compliance Report", to_excel(display_df), "gst_compliance_report.xlsx", use_container_width=True)

    else:
        st.markdown("#### 📌 Platform Modules")
        features = [
            ("✅","GST Rate Checker","Instantly validate GST rates on all transactions"),
            ("🧾","Invoice Validator","Verify invoices meet all GST legal requirements"),
            ("💰","ITC Calculator","Calculate exact Input Tax Credit claimable"),
            ("📅","Filing Tracker","Monitor all GST return deadlines"),
            ("⚠️","Late Fee Calculator","Calculate penalties and avoid late filing costs"),
            ("❓","GST FAQ Bot","Instant answers to all GST queries"),
        ]
        col1, col2, col3 = st.columns(3)
        for i,(icon,title,desc) in enumerate(features):
            with [col1,col2,col3][i%3]:
                st.markdown(f"""
                <div style='background:white;border:1px solid #e2e8f0;border-radius:10px;padding:20px;margin-bottom:16px;border-top:3px solid #2563eb;'>
                    <p style='font-size:24px;margin:0 0 8px;'>{icon}</p>
                    <p style='font-weight:700;color:#1e3a5f;font-size:14px;margin:0 0 6px;'>{title}</p>
                    <p style='color:#64748b;font-size:13px;margin:0;line-height:1.5;'>{desc}</p>
                </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# GST RATE CHECKER
# ════════════════════════════════════════════════════════════════════════════
elif page == "✅ GST Rate Checker":
    page_header("✅ GST Rate Checker", "Verify correct GST rates on individual items or bulk transactions")
    tab1, tab2 = st.tabs(["  Single Item Check  ", "  Bulk Excel Upload  "])

    with tab1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Item Details**")
            category = st.selectbox("Category", sorted(GST_RULES.keys()))
            gst_charged = st.number_input("GST Rate Charged (%)", 0, 28, 18)
            amount = st.number_input("Transaction Amount (₹)", 0, 10000000, 10000)
        with col2:
            st.markdown("**GST Rate Reference**")
            st.markdown(f"""
            <div style='background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:16px;'>
                <p style='font-size:13px;color:#1e40af;margin:0;'>Selected Category: <strong>{category.title()}</strong></p>
                <p style='font-size:28px;font-weight:800;color:#1e3a5f;margin:8px 0;'>{GST_RULES[category]}%</p>
                <p style='font-size:12px;color:#3b82f6;margin:0;'>Correct GST Rate as per Indian Tax Law</p>
            </div>""", unsafe_allow_html=True)

        if st.button("Verify GST Rate", use_container_width=True):
            expected = GST_RULES[category]
            gst_amount = amount * gst_charged / 100
            correct_amount = amount * expected / 100
            if gst_charged == expected:
                st.success(f"✅ Correct — GST rate of {expected}% is accurate for {category.title()}")
                st.metric("GST Amount", f"₹{gst_amount:,.2f}")
            else:
                st.error(f"❌ Incorrect — You charged {gst_charged}% but correct rate is {expected}%")
                c1,c2,c3 = st.columns(3)
                c1.metric("Charged", f"₹{gst_amount:,.2f}")
                c2.metric("Should Be", f"₹{correct_amount:,.2f}")
                c3.metric("Difference", f"₹{abs(gst_amount-correct_amount):,.2f}", delta="Overcharged" if gst_charged > expected else "Undercharged")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("#### 📋 Complete GST Rate Schedule")
        rate_df = pd.DataFrame([{"Category":k.title(),"GST Rate":f"{v}%","Slab":"Exempt" if v==0 else f"{v}% Slab"} for k,v in sorted(GST_RULES.items(),key=lambda x:x[1])])
        st.dataframe(rate_df, use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload Transaction File (Excel / CSV)", type=["xlsx","csv"], key="gst_bulk")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("⬇️ Download Sample File", to_excel(get_sample_data()), "sample.xlsx", use_container_width=True)
        if uploaded:
            df = pd.read_excel(uploaded) if uploaded.name.endswith("xlsx") else pd.read_csv(uploaded)
            results_df = check_compliance(df)
            display_df = results_df.drop("Flag", axis=1)
            errors = len(results_df[results_df["Flag"]=="wrong"])
            correct = len(results_df[results_df["Flag"]=="correct"])
            c1,c2,c3 = st.columns(3)
            c1.metric("Total Transactions", len(df))
            c2.metric("✅ Compliant", correct)
            c3.metric("❌ Errors Found", errors)
            st.dataframe(display_df.style.apply(color_rows,axis=1), use_container_width=True)
            st.download_button("⬇️ Download Report", to_excel(display_df), "gst_report.xlsx", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# INVOICE VALIDATOR
# ════════════════════════════════════════════════════════════════════════════
elif page == "🧾 Invoice Validator":
    page_header("🧾 Invoice Validator", "Validate GST invoices against all legal requirements")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Supplier Details**")
        inv_no = st.text_input("Invoice Number *", "INV-2025-001")
        inv_date = st.date_input("Invoice Date *", date.today())
        supplier_name = st.text_input("Supplier Name *", "ABC Traders")
        supplier_gstin = st.text_input("Supplier GSTIN *", "27AAAAA0000A1Z5")
        buyer_name = st.text_input("Buyer Name *", "XYZ Enterprises")
    with col2:
        st.markdown("**Transaction Details**")
        buyer_gstin = st.text_input("Buyer GSTIN", "29BBBBB1111B2Y6")
        place_of_supply = st.selectbox("Place of Supply *", ["Maharashtra","Karnataka","Delhi","Tamil Nadu","Gujarat","Rajasthan","Uttar Pradesh","West Bengal","Telangana","Kerala"])
        hsn_code = st.text_input("HSN / SAC Code *", "8471")
        taxable_value = st.number_input("Taxable Value (₹) *", 0, 10000000, 50000)
        gst_rate = st.selectbox("GST Rate *", [0,5,12,18,28])

    if st.button("Validate Invoice", use_container_width=True):
        errors, warnings, passed = [], [], []
        if not inv_no: errors.append("Invoice number is missing")
        else: passed.append("Invoice number present")
        if not supplier_gstin or len(supplier_gstin) != 15: errors.append("Supplier GSTIN must be 15 characters")
        else: passed.append("Supplier GSTIN format valid")
        if buyer_gstin and len(buyer_gstin) != 15: errors.append("Buyer GSTIN must be 15 characters")
        elif buyer_gstin: passed.append("Buyer GSTIN format valid")
        else: warnings.append("Buyer GSTIN missing — acceptable for B2C")
        if not hsn_code or len(hsn_code) < 4: errors.append("HSN/SAC code must be at least 4 digits")
        else: passed.append("HSN/SAC code valid")
        if not place_of_supply: errors.append("Place of supply is mandatory")
        else: passed.append("Place of supply mentioned")
        if taxable_value <= 0: errors.append("Taxable value must be greater than zero")
        else: passed.append("Taxable value valid")

        cgst = taxable_value * (gst_rate/2) / 100
        sgst = taxable_value * (gst_rate/2) / 100
        total = taxable_value + cgst + sgst

        if errors: st.error(f"❌ Invoice has {len(errors)} compliance error(s)")
        else: st.success("✅ Invoice is fully GST compliant")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Validation Results**")
            for p in passed: st.markdown(f"<p style='color:#166534;font-size:13px;margin:4px 0;'>✅ {p}</p>", unsafe_allow_html=True)
            for w in warnings: st.markdown(f"<p style='color:#92400e;font-size:13px;margin:4px 0;'>⚠️ {w}</p>", unsafe_allow_html=True)
            for e in errors: st.markdown(f"<p style='color:#991b1b;font-size:13px;margin:4px 0;'>❌ {e}</p>", unsafe_allow_html=True)
        with col_b:
            st.markdown("**Tax Breakdown**")
            st.markdown(f"""
            <div style='background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:16px;'>
                <div style='display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #e2e8f0;'><span style='color:#64748b;font-size:13px;'>Taxable Value</span><strong>₹{taxable_value:,.2f}</strong></div>
                <div style='display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #e2e8f0;'><span style='color:#64748b;font-size:13px;'>CGST ({gst_rate/2}%)</span><strong>₹{cgst:,.2f}</strong></div>
                <div style='display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #e2e8f0;'><span style='color:#64748b;font-size:13px;'>SGST ({gst_rate/2}%)</span><strong>₹{sgst:,.2f}</strong></div>
                <div style='display:flex;justify-content:space-between;padding:10px 0 0;'><span style='color:#1e3a5f;font-weight:700;'>Total Invoice Value</span><strong style='color:#2563eb;font-size:18px;'>₹{total:,.2f}</strong></div>
            </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# ITC CALCULATOR
# ════════════════════════════════════════════════════════════════════════════
elif page == "💰 ITC Calculator":
    page_header("💰 Input Tax Credit Calculator", "Calculate the exact ITC claimable from your purchases")
    tab1, tab2 = st.tabs(["  Manual Entry  ", "  Bulk Upload  "])
    with tab1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        n = st.number_input("Number of purchase entries", 1, 20, 3)
        purchases, total_itc = [], 0
        for i in range(int(n)):
            col1,col2,col3,col4 = st.columns(4)
            with col1: item = st.text_input(f"Item", f"Purchase {i+1}", key=f"i_{i}")
            with col2: amt = st.number_input(f"Amount (₹)", 0, 1000000, 10000, key=f"a_{i}")
            with col3: gst = st.selectbox(f"GST %", [0,5,12,18,28], index=3, key=f"g_{i}")
            with col4: elig = st.selectbox(f"ITC Eligible?", ["Yes","No"], key=f"e_{i}")
            gst_paid = amt * gst / 100
            if elig == "Yes": total_itc += gst_paid
            purchases.append({"Item":item,"Amount (₹)":amt,"GST %":gst,"GST Paid (₹)":round(gst_paid,2),"ITC Eligible":elig,"ITC Claimable (₹)":round(gst_paid,2) if elig=="Yes" else 0})

        if st.button("Calculate ITC", use_container_width=True):
            pur_df = pd.DataFrame(purchases)
            total_paid = sum(p["GST Paid (₹)"] for p in purchases)
            non_elig = total_paid - total_itc
            c1,c2,c3 = st.columns(3)
            c1.metric("Total GST Paid", f"₹{total_paid:,.2f}")
            c2.metric("ITC Claimable", f"₹{total_itc:,.2f}")
            c3.metric("Non-Eligible", f"₹{non_elig:,.2f}")
            st.success(f"✅ You can claim ₹{total_itc:,.2f} as Input Tax Credit")
            st.dataframe(pur_df, use_container_width=True, hide_index=True)
            fig = px.bar(pur_df, x="Item", y=["GST Paid (₹)","ITC Claimable (₹)"], barmode="group", title="GST Paid vs ITC Claimable", color_discrete_map={"GST Paid (₹)":"#94a3b8","ITC Claimable (₹)":"#2563eb"})
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#1e293b", plot_bgcolor="#f8fafc")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# FILING TRACKER
# ════════════════════════════════════════════════════════════════════════════
elif page == "📅 Filing Tracker":
    page_header("📅 GST Filing Tracker", "Monitor all return deadlines and never miss a filing date")
    st.markdown(f"<p style='color:#64748b;font-size:13px;'>Today: <strong>{date.today().strftime('%d %B %Y')}</strong></p>", unsafe_allow_html=True)

    deadlines = [
        {"Return Type":"GSTR-1","Due Date":"11th of every month","Description":"Outward supplies — Sales register","Penalty per day":"₹50","Status":"🟢 Active"},
        {"Return Type":"GSTR-3B","Due Date":"20th of every month","Description":"Monthly summary return","Penalty per day":"₹50","Status":"🟢 Active"},
        {"Return Type":"GSTR-2B","Due Date":"14th (auto-generated)","Description":"Auto-drafted ITC statement","Penalty per day":"N/A","Status":"✅ Auto"},
        {"Return Type":"GSTR-9","Due Date":"31st December annually","Description":"Annual consolidated return","Penalty per day":"₹200","Status":"🟡 Annual"},
        {"Return Type":"GSTR-9C","Due Date":"31st December annually","Description":"Reconciliation statement","Penalty per day":"₹200","Status":"🟡 Annual"},
        {"Return Type":"GSTR-4","Due Date":"30th April annually","Description":"Composition scheme return","Penalty per day":"₹50","Status":"🟢 Active"},
    ]
    st.dataframe(pd.DataFrame(deadlines), use_container_width=True, hide_index=True)

    st.markdown("#### ✅ Pre-Filing Compliance Checklist")
    checks = ["Sales invoices uploaded to GSTR-1","Purchase register reconciled with GSTR-2B","ITC claims verified and matched","GSTR-3B liability calculated","Tax payment made before filing","GSTR-3B filed before 20th","E-way bills reconciled","RCM entries accounted for"]
    col1, col2 = st.columns(2)
    for i, c in enumerate(checks):
        with [col1,col2][i%2]: st.checkbox(c, key=f"chk_{i}")

    st.markdown("#### 🔔 Filing Reminder Setup")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: ret = st.selectbox("Return Type", ["GSTR-1","GSTR-3B","GSTR-9"])
    with c2: days = st.number_input("Days before deadline", 1, 15, 3)
    with c3: email = st.text_input("Email Address", "your@email.com")
    if st.button("Set Reminder", use_container_width=True):
        st.success(f"✅ Reminder configured — You will be notified {days} days before {ret} deadline at {email}")
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# LATE FEE CALCULATOR
# ════════════════════════════════════════════════════════════════════════════
elif page == "⚠️ Late Fee Calculator":
    page_header("⚠️ Late Fee & Penalty Calculator", "Calculate GST penalties and understand the cost of delayed filing")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        return_type = st.selectbox("Return Type", ["GSTR-1","GSTR-3B","GSTR-9","GSTR-4"])
        due_date = st.date_input("Filing Due Date", date(2025,11,20))
        filing_date = st.date_input("Actual / Expected Filing Date", date.today())
        turnover = st.number_input("Annual Turnover (₹)", 0, 100000000, 5000000)
    with col2:
        tax_liability = st.number_input("Tax Liability (₹)", 0, 10000000, 50000)
        nil_return = st.checkbox("Nil Return (No transactions)")

    if st.button("Calculate Penalty", use_container_width=True):
        days_late = max(0, (filing_date - due_date).days)
        daily = 25 if nil_return else LATE_FEES.get(return_type, 50)
        total_fee = daily * 2 * days_late
        interest = tax_liability * 0.18 * days_late / 365 if days_late > 0 else 0
        max_fee = 5000 if turnover <= 1500000 else 10000
        actual_fee = min(total_fee, max_fee)

        if days_late == 0:
            st.success("✅ No penalty applicable — Filed within due date")
        else:
            st.error(f"⚠️ {days_late} days overdue — Penalty applicable")
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Days Late", days_late)
            c2.metric("Late Fee", f"₹{actual_fee:,.0f}")
            c3.metric("Interest @ 18%", f"₹{interest:,.0f}")
            c4.metric("Total Liability", f"₹{actual_fee+interest:,.0f}")
            if total_fee > max_fee:
                st.info(f"ℹ️ Late fee capped at ₹{max_fee:,} for your turnover bracket")
            days_range = list(range(0, days_late+30, 5))
            fees = [min(LATE_FEES.get(return_type,50)*2*d, max_fee)+(tax_liability*0.18*d/365) for d in days_range]
            fig = px.area(x=days_range, y=fees, title="Cumulative Penalty Over Time", labels={"x":"Days Late","y":"Total Penalty (₹)"}, color_discrete_sequence=["#ef4444"])
            fig.add_vline(x=days_late, line_dash="dash", line_color="#2563eb", annotation_text=f"Day {days_late}")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#1e293b", plot_bgcolor="#f8fafc")
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# ANALYTICS
# ════════════════════════════════════════════════════════════════════════════
elif page == "📈 Analytics":
    page_header("📈 GST Analytics", "Visual intelligence from your transaction data")
    uploaded = st.file_uploader("Upload transaction file for analysis", type=["xlsx","csv"])
    st.download_button("⬇️ Download Sample", to_excel(get_sample_data()), "sample.xlsx")
    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith("xlsx") else pd.read_csv(uploaded)
        results_df = check_compliance(df)
        col1,col2 = st.columns(2)
        with col1:
            fig = px.bar(df, x="Item", y="Amount (₹)", title="Transaction Amount by Item", color_discrete_sequence=["#2563eb"])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#1e293b", plot_bgcolor="#f8fafc")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            gst_sum = df.groupby("GST Applied (%)")["Amount (₹)"].sum().reset_index()
            fig2 = px.pie(gst_sum, values="Amount (₹)", names="GST Applied (%)", title="Revenue by GST Slab", color_discrete_sequence=["#1e3a5f","#2563eb","#60a5fa","#93c5fd","#bfdbfe"])
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#1e293b")
            st.plotly_chart(fig2, use_container_width=True)
        df["GST Amount"] = df["Amount (₹)"] * df["GST Applied (%)"] / 100
        fig3 = px.bar(df, x="Item", y="GST Amount", title="GST Amount per Transaction", color_discrete_sequence=["#1e3a5f"])
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#1e293b", plot_bgcolor="#f8fafc")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("📂 Upload a transaction file above to generate analytics")

# ════════════════════════════════════════════════════════════════════════════
# FAQ BOT
# ════════════════════════════════════════════════════════════════════════════
elif page == "❓ GST FAQ Bot":
    page_header("❓ GST Knowledge Base", "Instant answers to common GST compliance questions")
    faqs = {
        "What is GST?":"GST (Goods and Services Tax) is a comprehensive indirect tax on supply of goods and services in India. It replaced VAT, service tax, and excise duty. GST has slabs of 0%, 5%, 12%, 18%, and 28%.",
        "What is GSTIN?":"GSTIN is a 15-digit unique identification number for every GST-registered business. Format: 2-digit state code + 10-digit PAN + 1-digit entity number + Z + 1 check digit.",
        "What is Input Tax Credit (ITC)?":"ITC allows businesses to deduct GST paid on purchases from GST collected on sales. If you paid ₹18,000 on purchases and collected ₹25,000 on sales, you pay only ₹7,000 to the government.",
        "What is GSTR-1?":"GSTR-1 contains details of all outward supplies (sales). Filed by the 11th of the following month for monthly filers.",
        "What is GSTR-3B?":"GSTR-3B is a monthly summary return with outward supplies, ITC claimed, and tax payable. Due by 20th of every month.",
        "What is Reverse Charge Mechanism?":"Under RCM, the receiver of goods/services pays GST instead of the supplier. Applies to legal services, GTA, and other specified categories.",
        "What is the GST rate for restaurants?":"5% GST without ITC for most restaurants. 18% with ITC for AC restaurants in hotels with room tariff above ₹7,500.",
        "What is an E-way Bill?":"Electronic document required for movement of goods worth more than ₹50,000. Must be generated on the GST portal before transportation.",
        "What is the penalty for late filing?":"₹50 per day (₹25 CGST + ₹25 SGST) for returns with tax liability. ₹20 per day for nil returns. Maximum cap of ₹5,000 for small taxpayers.",
        "Who must register for GST?":"Businesses with annual turnover exceeding ₹40 lakhs (goods) or ₹20 lakhs (services). Special category states have ₹10 lakh threshold.",
    }
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    search = st.text_input("Search GST knowledge base...", "", placeholder="Type a question e.g. What is ITC?")
    if search:
        found = False
        for q, a in faqs.items():
            if any(w.lower() in q.lower() for w in search.split()):
                st.markdown(f"""
                <div style='background:#eff6ff;border:1px solid #bfdbfe;border-left:4px solid #2563eb;border-radius:8px;padding:16px;margin:8px 0;'>
                    <p style='font-weight:700;color:#1e3a5f;font-size:14px;margin:0 0 8px;'>{q}</p>
                    <p style='color:#334155;font-size:13px;line-height:1.7;margin:0;'>{a}</p>
                </div>""", unsafe_allow_html=True)
                found = True
        if not found: st.warning("No results found. Try different keywords.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### 📚 All FAQs")
    for q, a in faqs.items():
        with st.expander(q):
            st.markdown(f"<p style='color:#334155;font-size:13px;line-height:1.7;'>{a}</p>", unsafe_allow_html=True)

# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align:center;padding:16px;'>
    <p style='color:#94a3b8;font-size:12px;margin:0;'>
        GSTGenius AI © 2026 &nbsp;|&nbsp; Built by Sanskar Gupta &nbsp;|&nbsp;
        <span style='color:#2563eb;'>guptasanskar824@gmail.com</span> &nbsp;|&nbsp;
        Professional GST Compliance Platform for Indian Businesses
    </p>
</div>
""", unsafe_allow_html=True)
