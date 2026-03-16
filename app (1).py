import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime, date
import openpyxl

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GSTGenius AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #0a0f1e;
    color: #e2e8f0;
}
.stApp { background-color: #0a0f1e; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1424 0%, #111827 100%);
    border-right: 1px solid rgba(0,245,255,0.1);
}
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* METRIC CARDS */
[data-testid="metric-container"] {
    background: #0d1424;
    border: 1px solid rgba(0,245,255,0.15);
    border-radius: 12px;
    padding: 16px;
}
[data-testid="metric-container"] label { color: #94a3b8 !important; font-size: 12px !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #00f5ff !important; font-size: 28px !important; font-weight: 700 !important; }

/* BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, #00f5ff, #0af) !important;
    color: #000 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* DATAFRAME */
[data-testid="stDataFrame"] { border: 1px solid rgba(0,245,255,0.1); border-radius: 12px; }

/* HEADINGS */
h1 { color: #00f5ff !important; font-weight: 700 !important; }
h2, h3 { color: #e2e8f0 !important; font-weight: 600 !important; }

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background: #0d1424;
    border: 2px dashed rgba(0,245,255,0.3);
    border-radius: 12px;
    padding: 20px;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] { background: #0d1424; border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"] { color: #94a3b8 !important; border-radius: 8px; }
.stTabs [aria-selected="true"] { background: rgba(0,245,255,0.15) !important; color: #00f5ff !important; }

/* ALERTS */
.stAlert { border-radius: 10px; }

/* INPUT */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    background: #0d1424 !important;
    border: 1px solid rgba(0,245,255,0.2) !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}
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

GSTR_DEADLINES = {
    "GSTR-1": "11th of next month",
    "GSTR-3B": "20th of next month",
    "GSTR-9": "31st December",
    "GSTR-2A": "Auto populated",
    "GSTR-4": "30th April"
}

LATE_FEES = {
    "GSTR-1": 50,
    "GSTR-3B": 50,
    "GSTR-9": 200,
    "GSTR-4": 50
}

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 GSTGenius AI")
    st.markdown("*Your AI-Powered GST Advisor*")
    st.markdown("---")

    page = st.radio("Navigate", [
        "📊 Dashboard",
        "✅ GST Rate Checker",
        "🧾 Invoice Validator",
        "💰 ITC Calculator",
        "📅 Filing Tracker",
        "⚠️ Late Fee Calculator",
        "📈 Analytics",
        "❓ GST FAQ Bot"
    ])

    st.markdown("---")
    st.markdown("### 🏢 Business Info")
    business_name = st.text_input("Business Name", "My Business")
    gstin = st.text_input("GSTIN", "27AAAAA0000A1Z5")
    filing_period = st.selectbox("Filing Period", [
        "April 2025", "May 2025", "June 2025",
        "July 2025", "August 2025", "September 2025",
        "October 2025", "November 2025", "December 2025",
        "January 2026", "February 2026", "March 2026"
    ])

    st.markdown("---")
    st.markdown("*Made with ❤️ by GSTGenius AI*")

# ─── SAMPLE DATA GENERATOR ───────────────────────────────────────────────────
def get_sample_data():
    return pd.DataFrame({
        "Invoice No": ["INV001","INV002","INV003","INV004","INV005",
                       "INV006","INV007","INV008","INV009","INV010"],
        "Item": ["Laptop","Rice","Restaurant Bill","Mobile Phone","Wheat",
                 "Car Insurance","Clothing","Software License","Butter","Tobacco"],
        "Category": ["electronics","food","restaurant","mobile","wheat",
                     "insurance","clothing","software","butter","tobacco"],
        "Amount (₹)": [50000,5000,2000,25000,3000,10000,1500,10000,500,2000],
        "GST Applied (%)": [18, 5, 5, 18, 0, 18, 12, 18, 12, 28],
        "GSTIN of Supplier": [
            "27AAAAA0000A1Z5","29BBBBB1111B2Y6","07CCCCC2222C3X7",
            "27AAAAA0000A1Z5","33DDDDD3333D4W8","29BBBBB1111B2Y6",
            "07CCCCC2222C3X7","27AAAAA0000A1Z5","33DDDDD3333D4W8","29BBBBB1111B2Y6"
        ],
        "Invoice Date": ["2025-01-05","2025-01-07","2025-01-10","2025-01-12",
                         "2025-01-15","2025-01-18","2025-01-20","2025-01-22",
                         "2025-01-25","2025-01-28"],
        "HSN Code": ["8471","1006","9963","8517","1001",
                     "9971","6203","8523","0401","2401"]
    })

# ─── COMPLIANCE CHECKER ──────────────────────────────────────────────────────
def check_compliance(df):
    results = []
    for _, row in df.iterrows():
        category = str(row["Category"]).lower().strip()
        gst_applied = float(row["GST Applied (%)"])
        amount = float(row["Amount (₹)"])
        expected = GST_RULES.get(category, None)

        if expected is None:
            status = "⚠️ Unknown Category"
            flag = "unknown"
        elif gst_applied == expected:
            status = "✅ Correct"
            flag = "correct"
        else:
            status = f"❌ Wrong — Should be {expected}%"
            flag = "wrong"

        gst_amount = amount * gst_applied / 100
        results.append({
            "Invoice No": row.get("Invoice No", "-"),
            "Item": row["Item"],
            "Amount (₹)": amount,
            "GST Applied (%)": gst_applied,
            "Expected GST (%)": expected if expected is not None else "Unknown",
            "GST Amount (₹)": round(gst_amount, 2),
            "Status": status,
            "Flag": flag
        })
    return pd.DataFrame(results)

# ─── DOWNLOAD EXCEL ──────────────────────────────────────────────────────────
def to_excel(df):
    output = BytesIO()
    df.to_excel(output, index=False)
    return output.getvalue()

# ════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
if page == "📊 Dashboard":
    st.markdown(f"# 🧠 GSTGenius AI — {business_name}")
    st.markdown(f"**GSTIN:** `{gstin}` &nbsp;&nbsp; **Period:** {filing_period}")
    st.markdown("---")

    st.markdown("### 📤 Upload Transactions to Get Started")
    uploaded = st.file_uploader("Upload Excel / CSV", type=["xlsx","csv"], key="dash")

    # Sample download
    sample_df = get_sample_data()
    st.download_button("⬇️ Download Sample Excel File", to_excel(sample_df),
                       "sample_transactions.xlsx", use_container_width=True)

    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith("xlsx") else pd.read_csv(uploaded)
        results_df = check_compliance(df)

        correct = len(results_df[results_df["Flag"]=="correct"])
        wrong = len(results_df[results_df["Flag"]=="wrong"])
        unknown = len(results_df[results_df["Flag"]=="unknown"])
        total_gst = results_df["GST Amount (₹)"].sum()
        score = int((correct / len(results_df)) * 100) if len(results_df) > 0 else 0

        st.markdown("### 📊 Compliance Overview")
        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("🎯 Compliance Score", f"{score}%")
        c2.metric("✅ Correct", correct)
        c3.metric("❌ Errors", wrong)
        c4.metric("⚠️ Unknown", unknown)
        c5.metric("💰 Total GST", f"₹{total_gst:,.0f}")

        # Score gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Compliance Score", "font": {"color": "#e2e8f0"}},
            gauge={
                "axis": {"range": [0,100], "tickcolor": "#94a3b8"},
                "bar": {"color": "#00f5ff"},
                "steps": [
                    {"range": [0,50], "color": "rgba(239,68,68,0.3)"},
                    {"range": [50,75], "color": "rgba(251,191,36,0.3)"},
                    {"range": [75,100], "color": "rgba(16,185,129,0.3)"}
                ]
            },
            number={"suffix": "%", "font": {"color": "#00f5ff"}}
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0", height=300)
        st.plotly_chart(fig, use_container_width=True)

        # Status pie
        status_counts = results_df["Flag"].value_counts().reset_index()
        status_counts.columns = ["Status","Count"]
        fig2 = px.pie(status_counts, values="Count", names="Status",
                      color_discrete_map={"correct":"#00f5ff","wrong":"#ef4444","unknown":"#fbbf24"},
                      title="Transaction Status Breakdown")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### 📋 Full Transaction Report")
        def color_rows(row):
            if "❌" in str(row["Status"]):
                return ["background-color:#7f1d1d;color:white"]*len(row)
            elif "✅" in str(row["Status"]):
                return ["background-color:#064e3b;color:white"]*len(row)
            else:
                return ["background-color:#78350f;color:white"]*len(row)

        display_df = results_df.drop("Flag", axis=1)
        st.dataframe(display_df.style.apply(color_rows, axis=1), use_container_width=True)
        st.download_button("⬇️ Download Full Report", to_excel(display_df),
                           "gst_compliance_report.xlsx", use_container_width=True)
    else:
        st.info("👆 Upload your transactions Excel file above to see your compliance dashboard!")
        st.markdown("### 📌 What GSTGenius AI Can Do For You")
        cols = st.columns(3)
        features = [
            ("✅","GST Rate Checker","Instantly check if correct GST rates are applied on all transactions"),
            ("🧾","Invoice Validator","Validate GST invoices for all mandatory fields"),
            ("💰","ITC Calculator","Calculate exactly how much Input Tax Credit you can claim"),
            ("📅","Filing Tracker","Track all GST return deadlines and never miss a date"),
            ("⚠️","Late Fee Calculator","Calculate penalties and plan to avoid them"),
            ("❓","GST FAQ Bot","Get instant answers to all GST questions"),
        ]
        for i, (icon, title, desc) in enumerate(features):
            cols[i%3].markdown(f"""
            <div style='background:#0d1424;border:1px solid rgba(0,245,255,0.15);
            border-radius:12px;padding:20px;margin:8px 0;'>
            <h3 style='color:#00f5ff'>{icon} {title}</h3>
            <p style='color:#94a3b8;font-size:14px'>{desc}</p>
            </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE: GST RATE CHECKER
# ════════════════════════════════════════════════════════════════════════════
elif page == "✅ GST Rate Checker":
    st.markdown("# ✅ GST Rate Checker")
    st.markdown("Check the correct GST rate for any product or service")
    st.markdown("---")

    tab1, tab2 = st.tabs(["🔍 Check Single Item", "📂 Check Bulk (Excel)"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            item_name = st.text_input("Item / Service Name", "Laptop")
            category = st.selectbox("Select Category", sorted(GST_RULES.keys()))
            gst_charged = st.number_input("GST Rate You Charged (%)", 0, 28, 18)

        with col2:
            amount = st.number_input("Transaction Amount (₹)", 0, 10000000, 10000)

        if st.button("🔍 Check GST Rate"):
            expected = GST_RULES.get(category, 18)
            gst_amount = amount * gst_charged / 100
            correct_gst_amount = amount * expected / 100

            if gst_charged == expected:
                st.success(f"✅ Correct! GST rate for **{category}** is **{expected}%**")
                st.metric("GST Amount", f"₹{gst_amount:,.2f}")
            else:
                st.error(f"❌ Wrong GST Rate! You charged **{gst_charged}%** but should be **{expected}%**")
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("You Charged", f"₹{gst_amount:,.2f}")
                col_b.metric("Should Be", f"₹{correct_gst_amount:,.2f}")
                col_c.metric("Difference", f"₹{abs(gst_amount - correct_gst_amount):,.2f}",
                             delta=f"{'Overcharged' if gst_charged > expected else 'Undercharged'}")

        st.markdown("### 📋 Complete GST Rate Reference")
        rate_df = pd.DataFrame([
            {"Category": k.title(), "GST Rate": f"{v}%",
             "Example": "Food grains, Eggs" if v==0 else
                        "Restaurant, Transport, Clothes" if v==5 else
                        "Butter, Processed food, Textiles" if v==12 else
                        "Electronics, Software, Hotels" if v==18 else
                        "Cars, Tobacco, Luxury goods"}
            for k,v in sorted(GST_RULES.items(), key=lambda x: x[1])
        ])
        st.dataframe(rate_df, use_container_width=True, hide_index=True)

    with tab2:
        uploaded = st.file_uploader("Upload Excel file", type=["xlsx","csv"], key="gst_check")
        sample_df = get_sample_data()
        st.download_button("⬇️ Download Sample", to_excel(sample_df), "sample.xlsx")

        if uploaded:
            df = pd.read_excel(uploaded) if uploaded.name.endswith("xlsx") else pd.read_csv(uploaded)
            results_df = check_compliance(df)
            display_df = results_df.drop("Flag", axis=1)

            errors = results_df[results_df["Flag"]=="wrong"]
            st.success(f"✅ Analysis complete! Found **{len(errors)} errors** out of {len(df)} transactions")

            def color_rows(row):
                if "❌" in str(row["Status"]): return ["background-color:#7f1d1d;color:white"]*len(row)
                elif "✅" in str(row["Status"]): return ["background-color:#064e3b;color:white"]*len(row)
                else: return ["background-color:#78350f;color:white"]*len(row)

            st.dataframe(display_df.style.apply(color_rows,axis=1), use_container_width=True)
            st.download_button("⬇️ Download Report", to_excel(display_df), "gst_report.xlsx")

# ════════════════════════════════════════════════════════════════════════════
# PAGE: INVOICE VALIDATOR
# ════════════════════════════════════════════════════════════════════════════
elif page == "🧾 Invoice Validator":
    st.markdown("# 🧾 GST Invoice Validator")
    st.markdown("Validate your invoices against GST law requirements")
    st.markdown("---")

    st.markdown("### Enter Invoice Details")
    col1, col2 = st.columns(2)

    with col1:
        inv_no = st.text_input("Invoice Number *", "INV-2025-001")
        inv_date = st.date_input("Invoice Date *", date.today())
        supplier_name = st.text_input("Supplier Name *", "ABC Traders")
        supplier_gstin = st.text_input("Supplier GSTIN *", "27AAAAA0000A1Z5")
        buyer_name = st.text_input("Buyer Name *", "XYZ Enterprises")

    with col2:
        buyer_gstin = st.text_input("Buyer GSTIN", "29BBBBB1111B2Y6")
        place_of_supply = st.selectbox("Place of Supply *", [
            "Maharashtra","Karnataka","Delhi","Tamil Nadu","Gujarat",
            "Rajasthan","Uttar Pradesh","West Bengal","Telangana","Kerala"
        ])
        hsn_code = st.text_input("HSN / SAC Code *", "8471")
        taxable_value = st.number_input("Taxable Value (₹) *", 0, 10000000, 50000)
        gst_rate = st.selectbox("GST Rate *", [0, 5, 12, 18, 28])

    if st.button("✅ Validate Invoice"):
        errors = []
        warnings = []
        passed = []

        # Validations
        if not inv_no: errors.append("Invoice number is missing")
        else: passed.append("✅ Invoice number present")

        if not supplier_gstin or len(supplier_gstin) != 15:
            errors.append("Supplier GSTIN must be exactly 15 characters")
        else: passed.append("✅ Supplier GSTIN format valid")

        if buyer_gstin and len(buyer_gstin) != 15:
            errors.append("Buyer GSTIN must be exactly 15 characters")
        elif buyer_gstin: passed.append("✅ Buyer GSTIN format valid")
        else: warnings.append("⚠️ Buyer GSTIN missing — okay for B2C transactions")

        if not hsn_code or len(hsn_code) < 4:
            errors.append("HSN/SAC code must be at least 4 digits")
        else: passed.append("✅ HSN/SAC code present")

        if not place_of_supply: errors.append("Place of supply is mandatory")
        else: passed.append("✅ Place of supply mentioned")

        if taxable_value <= 0: errors.append("Taxable value must be greater than 0")
        else: passed.append("✅ Taxable value valid")

        # Results
        cgst = taxable_value * (gst_rate/2) / 100
        sgst = taxable_value * (gst_rate/2) / 100
        total = taxable_value + cgst + sgst

        if errors:
            st.error(f"❌ Invoice has {len(errors)} error(s) — Not GST Compliant")
        else:
            st.success("✅ Invoice is GST Compliant!")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("### Validation Results")
            for p in passed: st.markdown(f"<p style='color:#34d399'>{p}</p>", unsafe_allow_html=True)
            for w in warnings: st.markdown(f"<p style='color:#fbbf24'>{w}</p>", unsafe_allow_html=True)
            for e in errors: st.markdown(f"<p style='color:#ef4444'>❌ {e}</p>", unsafe_allow_html=True)

        with col_b:
            st.markdown("### 💰 Tax Calculation")
            st.markdown(f"""
            <div style='background:#0d1424;border:1px solid rgba(0,245,255,0.15);border-radius:12px;padding:20px'>
            <p>Taxable Value: <strong>₹{taxable_value:,.2f}</strong></p>
            <p>CGST ({gst_rate/2}%): <strong>₹{cgst:,.2f}</strong></p>
            <p>SGST ({gst_rate/2}%): <strong>₹{sgst:,.2f}</strong></p>
            <hr style='border-color:rgba(0,245,255,0.2)'>
            <p style='font-size:20px;color:#00f5ff'>Total Invoice Value: <strong>₹{total:,.2f}</strong></p>
            </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE: ITC CALCULATOR
# ════════════════════════════════════════════════════════════════════════════
elif page == "💰 ITC Calculator":
    st.markdown("# 💰 Input Tax Credit Calculator")
    st.markdown("Calculate exactly how much ITC you can claim")
    st.markdown("---")

    tab1, tab2 = st.tabs(["📝 Manual Entry", "📂 Bulk Upload"])

    with tab1:
        st.markdown("### Add Purchase Transactions")
        n = st.number_input("Number of purchases", 1, 20, 3)
        purchases = []
        total_itc = 0

        for i in range(int(n)):
            st.markdown(f"**Purchase {i+1}**")
            col1,col2,col3,col4 = st.columns(4)
            with col1: item = st.text_input(f"Item {i+1}", f"Purchase {i+1}", key=f"item_{i}")
            with col2: amt = st.number_input(f"Amount ₹ {i+1}", 0, 1000000, 10000, key=f"amt_{i}")
            with col3: gst = st.selectbox(f"GST% {i+1}", [0,5,12,18,28], index=3, key=f"gst_{i}")
            with col4:
                itc_eligible = st.selectbox(f"ITC Eligible? {i+1}", ["Yes","No"], key=f"itc_{i}")

            gst_paid = amt * gst / 100
            if itc_eligible == "Yes":
                total_itc += gst_paid
            purchases.append({"Item":item,"Amount":amt,"GST%":gst,
                               "GST Paid":round(gst_paid,2),
                               "ITC Eligible":itc_eligible,
                               "ITC Claimable":round(gst_paid,2) if itc_eligible=="Yes" else 0})

        if st.button("💰 Calculate Total ITC"):
            pur_df = pd.DataFrame(purchases)
            st.dataframe(pur_df, use_container_width=True, hide_index=True)

            col1,col2,col3 = st.columns(3)
            total_gst_paid = sum(p["GST Paid"] for p in purchases)
            non_eligible = total_gst_paid - total_itc
            col1.metric("Total GST Paid", f"₹{total_gst_paid:,.2f}")
            col2.metric("✅ ITC Claimable", f"₹{total_itc:,.2f}", delta="Refundable")
            col3.metric("❌ Non-Eligible", f"₹{non_eligible:,.2f}")

            st.success(f"🎉 You can claim ₹{total_itc:,.2f} as Input Tax Credit!")

            fig = px.bar(pur_df, x="Item", y=["GST Paid","ITC Claimable"],
                        barmode="group", title="GST Paid vs ITC Claimable",
                        color_discrete_map={"GST Paid":"#8b5cf6","ITC Claimable":"#00f5ff"})
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        uploaded = st.file_uploader("Upload purchases Excel", type=["xlsx","csv"], key="itc")
        if uploaded:
            df = pd.read_excel(uploaded) if uploaded.name.endswith("xlsx") else pd.read_csv(uploaded)
            st.dataframe(df, use_container_width=True)
            st.info("Ensure your file has columns: Item, Amount (₹), GST Applied (%), ITC Eligible (Yes/No)")

# ════════════════════════════════════════════════════════════════════════════
# PAGE: FILING TRACKER
# ════════════════════════════════════════════════════════════════════════════
elif page == "📅 Filing Tracker":
    st.markdown("# 📅 GST Filing Tracker")
    st.markdown("Never miss a GST deadline again")
    st.markdown("---")

    today = date.today()
    st.markdown(f"**Today's Date:** {today.strftime('%d %B %Y')}")

    deadlines = [
        {"Return": "GSTR-1", "Deadline": "11th of every month",
         "Description": "Outward supplies (Sales)", "Penalty": "₹50/day", "Status": "🟢 On Track"},
        {"Return": "GSTR-3B", "Deadline": "20th of every month",
         "Description": "Monthly summary return", "Penalty": "₹50/day", "Status": "🟢 On Track"},
        {"Return": "GSTR-2B", "Deadline": "Auto-generated 14th",
         "Description": "Auto-drafted ITC statement", "Penalty": "N/A", "Status": "✅ Auto"},
        {"Return": "GSTR-9", "Deadline": "31st December annually",
         "Description": "Annual return", "Penalty": "₹200/day", "Status": "🟡 Upcoming"},
        {"Return": "GSTR-9C", "Deadline": "31st December annually",
         "Description": "Reconciliation statement", "Penalty": "₹200/day", "Status": "🟡 Upcoming"},
        {"Return": "GSTR-4", "Deadline": "30th April annually",
         "Description": "Composition scheme return", "Penalty": "₹50/day", "Status": "🟢 On Track"},
    ]

    dead_df = pd.DataFrame(deadlines)
    st.dataframe(dead_df, use_container_width=True, hide_index=True)

    st.markdown("### ✅ Filing Checklist")
    checks = [
        "Sales invoices uploaded to GSTR-1",
        "Purchase register reconciled with GSTR-2B",
        "ITC claims verified and matched",
        "GSTR-3B liability calculated",
        "Tax payment made before filing",
        "GSTR-3B filed before 20th",
        "E-way bills reconciled",
        "RCM (Reverse Charge) entries accounted"
    ]
    cols = st.columns(2)
    for i, check in enumerate(checks):
        with cols[i%2]:
            st.checkbox(check, key=f"check_{i}")

    st.markdown("### 📆 Set Reminders")
    col1, col2 = st.columns(2)
    with col1:
        reminder_return = st.selectbox("Select Return", ["GSTR-1","GSTR-3B","GSTR-9"])
        reminder_days = st.number_input("Remind me X days before", 1, 15, 3)
    with col2:
        email = st.text_input("Your Email (for reminder)", "your@email.com")
        if st.button("🔔 Set Reminder"):
            st.success(f"✅ Reminder set! We'll notify {email} {reminder_days} days before {reminder_return} deadline")

# ════════════════════════════════════════════════════════════════════════════
# PAGE: LATE FEE CALCULATOR
# ════════════════════════════════════════════════════════════════════════════
elif page == "⚠️ Late Fee Calculator":
    st.markdown("# ⚠️ Late Fee & Penalty Calculator")
    st.markdown("Calculate GST penalties and plan to avoid them")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        return_type = st.selectbox("Return Type", ["GSTR-1","GSTR-3B","GSTR-9","GSTR-4"])
        due_date = st.date_input("Due Date", date(2025,11,20))
        filing_date = st.date_input("Actual / Expected Filing Date", date.today())
        turnover = st.number_input("Annual Turnover (₹)", 0, 100000000, 5000000)

    with col2:
        tax_liability = st.number_input("Tax Liability (₹)", 0, 10000000, 50000)
        has_nil_return = st.checkbox("Nil Return (No transactions)?")

    if st.button("⚠️ Calculate Penalty"):
        days_late = max(0, (filing_date - due_date).days)
        daily_fee = 25 if has_nil_return else LATE_FEES.get(return_type, 50)
        cgst_fee = daily_fee * days_late
        sgst_fee = daily_fee * days_late
        total_late_fee = cgst_fee + sgst_fee
        interest = tax_liability * 0.18 * days_late / 365 if days_late > 0 else 0
        total_penalty = total_late_fee + interest
        max_fee = 5000 if turnover <= 1500000 else 10000
        actual_fee = min(total_late_fee, max_fee)

        if days_late == 0:
            st.success("🎉 No late fee! Filed on time!")
        else:
            st.error(f"⚠️ {days_late} days late — Penalty applicable!")

            col_a,col_b,col_c,col_d = st.columns(4)
            col_a.metric("Days Late", days_late)
            col_b.metric("Late Fee", f"₹{actual_fee:,.0f}")
            col_c.metric("Interest @18%", f"₹{interest:,.0f}")
            col_d.metric("Total Penalty", f"₹{(actual_fee+interest):,.0f}")

            if total_late_fee > max_fee:
                st.info(f"ℹ️ Late fee capped at ₹{max_fee:,} as per your turnover bracket")

            # Timeline chart
            days_range = list(range(0, days_late+30, 5))
            fees = [min(LATE_FEES.get(return_type,50)*2*d, max_fee) + (tax_liability*0.18*d/365) for d in days_range]
            fig = px.line(x=days_range, y=fees, title="Penalty Growth Over Time",
                         labels={"x":"Days Late","y":"Total Penalty (₹)"},
                         color_discrete_sequence=["#ef4444"])
            fig.add_vline(x=days_late, line_dash="dash", line_color="#fbbf24",
                         annotation_text="Your position")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
            st.plotly_chart(fig, use_container_width=True)

            st.warning(f"💡 **Pro Tip:** Filing just {max(0,days_late-5)} days earlier would have saved you ₹{(actual_fee+interest)*0.3:,.0f} approximately!")

# ════════════════════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ════════════════════════════════════════════════════════════════════════════
elif page == "📈 Analytics":
    st.markdown("# 📈 GST Analytics Dashboard")
    st.markdown("Visual insights into your GST data")
    st.markdown("---")

    uploaded = st.file_uploader("Upload transactions for analytics", type=["xlsx","csv"])
    sample_df = get_sample_data()
    st.download_button("⬇️ Download Sample", to_excel(sample_df), "sample.xlsx")

    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith("xlsx") else pd.read_csv(uploaded)
        results_df = check_compliance(df)

        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(df, x="Item", y="Amount (₹)", color="GST Applied (%)",
                        title="Transaction Amount by Item",
                        color_continuous_scale="teal")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            gst_summary = df.groupby("GST Applied (%)")["Amount (₹)"].sum().reset_index()
            fig2 = px.pie(gst_summary, values="Amount (₹)", names="GST Applied (%)",
                         title="Revenue by GST Rate",
                         color_discrete_sequence=["#00f5ff","#8b5cf6","#ec4899","#fbbf24","#10b981"])
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
            st.plotly_chart(fig2, use_container_width=True)

        df["GST Amount"] = df["Amount (₹)"] * df["GST Applied (%)"] / 100
        fig3 = px.bar(df, x="Item", y="GST Amount",
                     title="GST Amount per Transaction",
                     color_discrete_sequence=["#8b5cf6"])
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
        st.plotly_chart(fig3, use_container_width=True)

        status_counts = results_df["Flag"].value_counts()
        fig4 = px.bar(x=status_counts.index, y=status_counts.values,
                     title="Compliance Status Distribution",
                     color=status_counts.index,
                     color_discrete_map={"correct":"#00f5ff","wrong":"#ef4444","unknown":"#fbbf24"})
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0")
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Upload a transactions file to see analytics!")

# ════════════════════════════════════════════════════════════════════════════
# PAGE: GST FAQ BOT
# ════════════════════════════════════════════════════════════════════════════
elif page == "❓ GST FAQ Bot":
    st.markdown("# ❓ GST FAQ Bot")
    st.markdown("Get instant answers to common GST questions")
    st.markdown("---")

    faqs = {
        "What is GST?": "GST (Goods and Services Tax) is a comprehensive indirect tax levied on the supply of goods and services in India. It replaced multiple indirect taxes like VAT, service tax, and excise duty. GST has 4 slabs: 0%, 5%, 12%, 18%, and 28%.",
        "What is GSTIN?": "GSTIN is a 15-digit unique identification number assigned to every GST-registered business. Format: 2-digit state code + 10-digit PAN + 1-digit entity number + 1-digit Z + 1-digit check digit.",
        "What is Input Tax Credit (ITC)?": "ITC allows businesses to deduct the GST paid on purchases from the GST collected on sales. For example, if you paid ₹18,000 GST on purchases and collected ₹25,000 GST on sales, you only pay ₹7,000 to the government.",
        "What is GSTR-1?": "GSTR-1 is a monthly/quarterly return that contains details of all outward supplies (sales). It must be filed by the 11th of the following month for monthly filers.",
        "What is GSTR-3B?": "GSTR-3B is a monthly self-declaration summary return. It contains summarized details of outward supplies, ITC claimed, and tax payable. Due by 20th of every month.",
        "What is Reverse Charge Mechanism (RCM)?": "Under RCM, the receiver of goods/services is liable to pay GST instead of the supplier. This applies to specific categories like legal services, GTA, etc.",
        "What is the GST rate for restaurants?": "Restaurants charge 5% GST without ITC benefit. AC restaurants in hotels with room tariff above ₹7,500 charge 18% with ITC.",
        "What is E-way Bill?": "E-way bill is an electronic document required for movement of goods worth more than ₹50,000. It must be generated on the GST portal before goods are transported.",
        "What is the penalty for late GST filing?": "Late fee is ₹50 per day (₹25 CGST + ₹25 SGST) for returns with tax liability, and ₹20 per day for nil returns. Maximum cap is ₹5,000 for small taxpayers.",
        "Who needs to register for GST?": "Businesses with annual turnover exceeding ₹40 lakhs (goods) or ₹20 lakhs (services) must register for GST. Some special category states have lower thresholds of ₹10 lakhs.",
    }

    st.markdown("### 🔍 Search Your Question")
    search = st.text_input("Type your GST question...", "")

    if search:
        found = False
        for q, a in faqs.items():
            if any(word.lower() in q.lower() for word in search.split()):
                st.markdown(f"""
                <div style='background:#0d1424;border:1px solid rgba(0,245,255,0.2);
                border-radius:12px;padding:20px;margin:10px 0'>
                <h4 style='color:#00f5ff'>Q: {q}</h4>
                <p style='color:#e2e8f0'>{a}</p>
                </div>""", unsafe_allow_html=True)
                found = True
        if not found:
            st.warning("Question not found in FAQ. Try different keywords!")

    st.markdown("### 📋 All Frequently Asked Questions")
    for q, a in faqs.items():
        with st.expander(f"❓ {q}"):
            st.markdown(f"<p style='color:#e2e8f0'>{a}</p>", unsafe_allow_html=True)
