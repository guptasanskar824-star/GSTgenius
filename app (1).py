import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime, date
import openpyxl

st.set_page_config(
    page_title="GSTGenius — Professional GST Compliance Platform",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='12' fill='%231e3a5f'/><text y='.9em' font-size='80' x='10'>G</text></svg>",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, html, body { font-family: 'Inter', sans-serif !important; }
.stApp { background-color: #f0f2f5 !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: #1e3a5f !important;
    border-right: none !important;
    min-width: 260px !important;
}
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
section[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }
section[data-testid="stSidebar"] .stRadio label {
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 10px 14px !important;
    border-radius: 6px !important;
    display: block !important;
    color: #cbd5e1 !important;
    letter-spacing: 0.2px !important;
}
section[data-testid="stSidebar"] .stRadio label:hover { background: rgba(255,255,255,0.08) !important; color: #fff !important; }
section[data-testid="stSidebar"] input[type="text"] {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #fff !important;
    border-radius: 6px !important;
    font-size: 13px !important;
}
section[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #fff !important;
    border-radius: 6px !important;
}

/* ── MAIN CONTENT ── */
main .block-container { padding: 1.5rem 2rem !important; max-width: 100% !important; }

/* ── PAGE HEADER ── */
.page-header {
    background: #1e3a5f;
    padding: 22px 28px;
    border-radius: 10px;
    margin-bottom: 20px;
    border-left: 4px solid #3b82f6;
}
.page-header h1 {
    color: #ffffff !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    margin: 0 0 4px !important;
    letter-spacing: -0.3px !important;
}
.page-header p { color: #94a3b8 !important; font-size: 12px !important; margin: 0 !important; letter-spacing: 0.3px !important; }

/* ── METRIC CARDS ── */
[data-testid="metric-container"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    padding: 16px 20px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
[data-testid="metric-container"] label {
    color: #64748b !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #1e3a5f !important;
    font-size: 26px !important;
    font-weight: 700 !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: #1e3a5f !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 10px 20px !important;
    font-size: 13px !important;
    letter-spacing: 0.3px !important;
    transition: all 0.15s !important;
}
.stButton > button:hover { background: #2563eb !important; box-shadow: 0 4px 12px rgba(37,99,235,0.25) !important; }

/* ── CARDS ── */
.card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 24px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.card-section-title { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #64748b; margin-bottom: 16px; padding-bottom: 10px; border-bottom: 1px solid #f1f5f9; }

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { border: 1px solid #e2e8f0 !important; border-radius: 8px !important; }
.stDataFrame thead tr th { background: #f8fafc !important; color: #374151 !important; font-weight: 600 !important; font-size: 12px !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; }

/* ── TYPOGRAPHY ── */
h1 { color: #1e3a5f !important; font-weight: 800 !important; font-size: 24px !important; letter-spacing: -0.5px !important; }
h2 { color: #1e3a5f !important; font-weight: 700 !important; font-size: 18px !important; }
h3 { color: #334155 !important; font-weight: 600 !important; font-size: 14px !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; }
p { color: #475569 !important; font-size: 14px !important; line-height: 1.6 !important; }

/* ── INPUTS ── */
.stTextInput input, .stNumberInput input, textarea {
    background: #ffffff !important;
    border: 1px solid #d1d5db !important;
    color: #1e293b !important;
    border-radius: 6px !important;
    font-size: 13px !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.08) !important;
    outline: none !important;
}
[data-testid="stSelectbox"] > div > div {
    background: #ffffff !important;
    border: 1px solid #d1d5db !important;
    border-radius: 6px !important;
    font-size: 13px !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] { background: #f1f5f9 !important; border-radius: 6px !important; padding: 3px !important; border: 1px solid #e2e8f0 !important; }
.stTabs [data-baseweb="tab"] { color: #64748b !important; border-radius: 4px !important; font-size: 12px !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; padding: 8px 16px !important; }
.stTabs [aria-selected="true"] { background: #ffffff !important; color: #1e3a5f !important; box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important; }

/* ── STATUS BADGES ── */
.badge { display: inline-block; padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; letter-spacing: 0.3px; }
.badge-pass { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
.badge-fail { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
.badge-warn { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
.badge-info { background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }

/* ── ALERTS ── */
[data-testid="stAlert"] { border-radius: 6px !important; font-size: 13px !important; }

/* ── DIVIDER ── */
hr { border: none !important; border-top: 1px solid #e2e8f0 !important; margin: 16px 0 !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 99px; }

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] { background: #f8fafc !important; border: 1.5px dashed #cbd5e1 !important; border-radius: 8px !important; }

/* ── EXPANDER ── */
[data-testid="stExpander"] { background: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# GST MASTER DATA — Comprehensive Coverage
# ══════════════════════════════════════════════════════════════
GST_RULES = {
    # 0% — Exempt
    "food grains": 0, "rice": 0, "wheat": 0, "flour": 0, "maida": 0, "atta": 0,
    "milk": 0, "curd": 0, "lassi": 0, "buttermilk": 0, "paneer": 0,
    "vegetables": 0, "fruits": 0, "eggs": 0, "meat": 0, "fish": 0,
    "salt": 0, "jaggery": 0, "honey": 0, "bread": 0, "prasad": 0,
    "books": 0, "newspaper": 0, "maps": 0, "postal services": 0,
    "education services": 0, "healthcare": 0, "agriculture": 0,

    # 5%
    "restaurant": 5, "food delivery": 5, "transport": 5,
    "railways": 5, "economy air travel": 5, "supply of food": 5,
    "footwear under 1000": 5, "clothing under 1000": 5, "clothing": 5,
    "medicine": 5, "drugs": 5, "fertilizer": 5, "coal": 5,
    "domestic lpg": 5, "kerosene": 5, "agarbatti": 5,
    "renewable energy": 5, "handloom": 5, "handicraft": 5,

    # 12%
    "butter": 12, "cheese": 12, "ghee": 12, "packed food": 12,
    "processed food": 12, "fruit juice": 12, "namkeen": 12,
    "ayurvedic medicine": 12, "ayurvedic": 12,
    "textile": 12, "apparel above 1000": 12, "footwear above 1000": 12,
    "mobile phones": 12, "mobiles": 12,
    "construction residential": 12, "works contract": 12,
    "business class air travel": 12, "non ac restaurant": 12,
    "playing cards": 12, "chess board": 12, "carrom board": 12,

    # 18%
    "electronics": 18, "laptop": 18, "computer": 18, "monitor": 18,
    "software": 18, "it services": 18, "saas": 18,
    "furniture": 18, "steel furniture": 18,
    "insurance": 18, "banking": 18, "financial services": 18,
    "telecom": 18, "internet services": 18,
    "hotel above 2500": 18, "ac restaurant": 18, "hotel": 18,
    "construction commercial": 18,
    "paint": 18, "varnish": 18, "putty": 18,
    "refrigerator": 18, "washing machine": 18, "ac": 18,
    "bicycle": 18, "camera": 18, "speaker": 18,
    "advertising": 18, "consulting": 18, "legal services": 18,
    "accounting": 18, "audit": 18, "ca services": 18,
    "manpower services": 18, "security services": 18,
    "maintenance services": 18, "repair services": 18,
    "printing": 18, "packaging": 18,
    "iron": 18, "steel": 18, "aluminium": 18, "copper": 18,
    "plastic": 18, "rubber": 18, "paper": 18, "stationery": 18,

    # 28%
    "luxury cars": 28, "car": 28, "suv": 28, "motorcycle above 350cc": 28,
    "tobacco": 28, "cigarettes": 28, "pan masala": 28,
    "alcohol": 28, "aerated drinks": 28, "energy drinks": 28,
    "cement": 28, "luxury hotels": 28,
    "casino": 28, "betting": 28, "lottery": 28,
    "luxury goods": 28, "perfume": 28, "sunscreen": 28,
    "dishwasher": 28, "vacuum cleaner": 28,
    "aircraft": 28, "yacht": 28,
}

LATE_FEES = {"GSTR-1": 50, "GSTR-3B": 50, "GSTR-9": 200, "GSTR-4": 50, "GSTR-7": 200, "GSTR-8": 200}

GST_RETURNS = {
    "GSTR-1": {"freq": "Monthly / Quarterly", "due": "11th of next month (Monthly) / 13th of month after quarter", "desc": "Details of outward supplies (sales)", "filer": "All regular taxpayers"},
    "GSTR-2B": {"freq": "Monthly", "due": "14th of following month", "desc": "Auto-drafted ITC statement", "filer": "All regular taxpayers"},
    "GSTR-3B": {"freq": "Monthly", "due": "20th of following month", "desc": "Summary return with tax payment", "filer": "All regular taxpayers"},
    "GSTR-4": {"freq": "Annual", "due": "30th April", "desc": "Composition scheme annual return", "filer": "Composition taxpayers"},
    "GSTR-5": {"freq": "Monthly", "due": "20th of following month", "desc": "Return for non-resident foreign taxpayers", "filer": "Non-resident taxable persons"},
    "GSTR-6": {"freq": "Monthly", "due": "13th of following month", "desc": "Return for input service distributors", "filer": "Input Service Distributors"},
    "GSTR-7": {"freq": "Monthly", "due": "10th of following month", "desc": "Return for TDS deductors", "filer": "TDS deductors"},
    "GSTR-8": {"freq": "Monthly", "due": "10th of following month", "desc": "Return for TCS collectors (e-commerce)", "filer": "E-commerce operators"},
    "GSTR-9": {"freq": "Annual", "due": "31st December", "desc": "Annual return consolidating all monthly returns", "filer": "All regular taxpayers with turnover > 2Cr"},
    "GSTR-9C": {"freq": "Annual", "due": "31st December", "desc": "Reconciliation statement with audited financials", "filer": "Taxpayers with turnover > 5Cr"},
    "GSTR-10": {"freq": "Once", "due": "3 months from cancellation", "desc": "Final return on cancellation of registration", "filer": "Cancelled registration holders"},
    "GSTR-11": {"freq": "Monthly", "due": "28th of following month", "desc": "Return for UIN holders (embassies, UN bodies)", "filer": "UIN holders"},
}

ITC_BLOCKED = [
    "Motor vehicles for personal use (Section 17(5)(a))",
    "Food and beverages, outdoor catering (Section 17(5)(b))",
    "Health and life insurance for employees (Section 17(5)(b))",
    "Membership of clubs, health and fitness centres (Section 17(5)(b))",
    "Rent-a-cab services (Section 17(5)(b))",
    "Travel benefits to employees — LTA, vacation (Section 17(5)(b))",
    "Works contract services for immovable property (Section 17(5)(c))",
    "Goods/services used for personal consumption (Section 17(5)(g))",
    "Goods lost, stolen, destroyed or written off (Section 17(5)(h))",
    "Goods/services received by non-resident taxable person (Section 17(5)(i))",
]

# ── HELPERS ──────────────────────────────────────────────────
def get_sample():
    return pd.DataFrame({
        "Invoice No": [f"INV-2025-{str(i).zfill(3)}" for i in range(1,16)],
        "Supplier Name": ["Tech Solutions Pvt Ltd","Agro Traders","Hotel Marriott","MobileZone","FoodGrain Co","InsureCorp","Fashion House","CloudSoft India","Dairy Fresh","Tobacco Corp","Cement India","AC Services","Interior Design","Agarbatti Co","Consultancy Firm"],
        "Supplier GSTIN": ["27AAAAA0000A1Z5","29BBBBB1111B2Y6","07CCCCC2222C3X7","27AAAAA0000A1Z5","33DDDDD3333D4W8","29BBBBB1111B2Y6","07CCCCC2222C3X7","27AAAAA0000A1Z5","33DDDDD3333D4W8","29BBBBB1111B2Y6","27AAAAA0000A1Z5","29BBBBB1111B2Y6","07CCCCC2222C3X7","27AAAAA0000A1Z5","29BBBBB1111B2Y6"],
        "Item Description": ["Laptop","Rice","Hotel Stay","Mobile Phones","Wheat","Insurance Premium","Clothing","Software License","Butter","Tobacco","Cement","AC Unit","Furniture","Agarbatti","Consulting Services"],
        "Category": ["laptop","rice","hotel","mobiles","wheat","insurance","clothing","software","butter","tobacco","cement","ac","furniture","agarbatti","consulting"],
        "HSN / SAC Code": ["8471","1006","9963","8517","1001","9971","6203","8523","0401","2401","2523","8415","9403","3302","9983"],
        "Taxable Amount (Rs)": [50000,5000,8000,25000,3000,10000,1500,10000,500,2000,15000,35000,20000,1000,15000],
        "GST Applied (%)": [18,5,18,12,0,18,12,18,12,28,18,28,18,0,18],
        "Place of Supply": ["Maharashtra","Karnataka","Delhi","Maharashtra","Tamil Nadu","Maharashtra","Karnataka","Maharashtra","Gujarat","Delhi","Maharashtra","Karnataka","Delhi","Rajasthan","Maharashtra"],
        "Invoice Date": ["2025-01-05","2025-01-07","2025-01-10","2025-01-12","2025-01-15","2025-01-18","2025-01-20","2025-01-22","2025-01-25","2025-01-28","2025-02-01","2025-02-03","2025-02-05","2025-02-08","2025-02-10"],
        "ITC Eligible": ["Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","No","Yes","Yes","Yes","Yes","Yes"],
    })

def check_compliance(df):
    results = []
    VALID_RATES = [0, 5, 12, 18, 28]
    # Smart column detection
    amt_col = next((c for c in df.columns if any(x in c.lower() for x in ["taxable","amount","value"])), df.columns[5])
    gst_col = next((c for c in df.columns if "gst" in c.lower() and any(x in c.lower() for x in ["rate","_","%"])), df.columns[6])
    inv_col = next((c for c in df.columns if any(x in c.lower() for x in ["invoice","inv","bill","voucher"])), df.columns[0])
    party_col = next((c for c in df.columns if any(x in c.lower() for x in ["party","supplier","vendor","name","customer","buyer"])), df.columns[2])
    cat_col = next((c for c in df.columns if any(x in c.lower() for x in ["category","item","description","goods","product","service","particulars"])), None)
    state_col = next((c for c in df.columns if "state" in c.lower()), None)
    cgst_col = next((c for c in df.columns if c.upper() == "CGST" or c.lower() == "cgst"), None)
    sgst_col = next((c for c in df.columns if c.upper() == "SGST" or c.lower() == "sgst"), None)
    igst_col = next((c for c in df.columns if c.upper() == "IGST" or c.lower() == "igst"), None)
    total_col = next((c for c in df.columns if "total" in c.lower() and ("invoice" in c.lower() or "value" in c.lower())), None)

    for _, row in df.iterrows():
        try:
            gst = float(row[gst_col])
            amt = float(row[amt_col])
        except:
            continue

        inv = str(row[inv_col])
        party = str(row[party_col])
        state = str(row[state_col]) if state_col else "-"
        cat = str(row[cat_col]).lower().strip() if cat_col else None
        cgst_amt = float(row[cgst_col]) if cgst_col and pd.notna(row[cgst_col]) else 0
        sgst_amt = float(row[sgst_col]) if sgst_col and pd.notna(row[sgst_col]) else 0
        igst_amt = float(row[igst_col]) if igst_col and pd.notna(row[igst_col]) else 0
        total_declared = float(row[total_col]) if total_col and pd.notna(row[total_col]) else 0
        actual_tax = round(cgst_amt + sgst_amt + igst_amt, 2)
        expected_tax = round(amt * gst / 100, 2)
        expected_total = round(amt + expected_tax, 2)

        issues = []
        flag = "correct"

        # Check 1 — Invalid GST slab
        if gst not in VALID_RATES:
            issues.append(f"Invalid GST slab: {gst}% — Valid slabs are 0/5/12/18/28")
            flag = "wrong"

        # Check 2 — Tax math mismatch
        if actual_tax > 0 and abs(actual_tax - expected_tax) > 1:
            issues.append(f"Tax mismatch: Declared Rs {actual_tax:,.2f} vs Computed Rs {expected_tax:,.2f}")
            flag = "wrong"

        # Check 3 — Total invoice mismatch
        if total_declared > 0 and abs(total_declared - expected_total) > 1:
            issues.append(f"Invoice total mismatch: Declared Rs {total_declared:,.2f} vs Computed Rs {expected_total:,.2f}")
            flag = "wrong"

        # Check 4 — Both IGST and CGST charged
        if igst_amt > 0 and cgst_amt > 0:
            issues.append("Both IGST and CGST charged on same invoice — not permitted")
            flag = "wrong"

        # Check 5 — Category rate validation
        if cat and cat in GST_RULES:
            exp_rate = GST_RULES[cat]
            if gst != exp_rate:
                issues.append(f"Wrong rate for {cat.title()}: Applied {gst}% but correct rate is {exp_rate}%")
                flag = "wrong"

        if flag == "correct":
            status = "Tax Math Verified — Valid GST Slab" if not (cat and cat in GST_RULES) else "Fully Compliant"
        else:
            status = " | ".join(issues)

        results.append({
            "Invoice No": inv,
            "Party Name": party,
            "State": state,
            "Taxable Amount (Rs)": amt,
            "GST Rate (%)": gst,
            "Expected Tax (Rs)": expected_tax,
            "Actual Tax (Rs)": actual_tax if actual_tax > 0 else expected_tax,
            "Compliance Status": status,
            "Flag": flag
        })
    return pd.DataFrame(results)

def to_excel(df):
    out = BytesIO()
    df.to_excel(out, index=False)
    return out.getvalue()

def header(title, sub):
    st.markdown(f"""
    <div class='page-header'>
        <h1>{title}</h1>
        <p>{sub}</p>
    </div>""", unsafe_allow_html=True)

def color_rows(row):
    status = str(row.get("Compliance Status", row.get("Status", "")))
    if "Non-Compliant" in status or "Wrong" in status or "wrong" in status:
        return ["background-color:#fff1f2;color:#9f1239"] * len(row)
    elif "Compliant" in status and "Non" not in status:
        return ["background-color:#f0fdf4;color:#14532d"] * len(row)
    else:
        return ["background-color:#fffbeb;color:#78350f"] * len(row)

# ── LOGO & SIDEBAR ────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 16px 16px;border-bottom:1px solid rgba(255,255,255,0.1);margin-bottom:16px;'>
        <div style='display:flex;align-items:center;gap:12px;'>
            <div style='width:36px;height:36px;background:#3b82f6;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;'>
                <svg width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'>
                    <path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/>
                    <polyline points='14,2 14,8 20,8'/>
                    <line x1='16' y1='13' x2='8' y2='13'/>
                    <line x1='16' y1='17' x2='8' y2='17'/>
                    <polyline points='10,9 9,9 8,9'/>
                </svg>
            </div>
            <div>
                <div style='color:#ffffff;font-size:16px;font-weight:800;letter-spacing:-0.3px;'>GSTGenius</div>
                <div style='color:#64748b;font-size:11px;letter-spacing:0.3px;margin-top:1px;'>COMPLIANCE PLATFORM</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size:10px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:1.2px;padding:0 4px;margin-bottom:6px;'>Main Navigation</p>", unsafe_allow_html=True)

    page = st.radio("", [
        "Dashboard",
        "GST Rate Checker",
        "Invoice Validator",
        "ITC Calculator",
        "GST Returns Tracker",
        "Late Fee Calculator",
        "RCM Manager",
        "E-Way Bill Checker",
        "Analytics",
        "GST Knowledge Base"
    ], label_visibility="collapsed")

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:10px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:1.2px;padding:0 4px;margin-bottom:8px;'>Business Profile</p>", unsafe_allow_html=True)
    business_name = st.text_input("", "My Business Pvt Ltd", placeholder="Business Name", label_visibility="collapsed")
    gstin = st.text_input("", "27AAAAA0000A1Z5", placeholder="GSTIN (15 digits)", label_visibility="collapsed")
    filing_period = st.selectbox("", ["April 2025","May 2025","June 2025","July 2025","August 2025","September 2025","October 2025","November 2025","December 2025","January 2026","February 2026","March 2026"], label_visibility="collapsed")
    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px;color:#475569;padding:0 4px;'>v2.0 &nbsp;|&nbsp; Built by Sanskar Gupta<br><span style='color:#3b82f6;'>guptasanskar824@gmail.com</span></p>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════
if page == "Dashboard":
    header("Compliance Dashboard", f"{business_name}  |  GSTIN: {gstin}  |  Period: {filing_period}  |  {date.today().strftime('%d %B %Y')}")

    col_main, col_side = st.columns([3,1])
    with col_main:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<p class='card-section-title'>Upload Transaction Register</p>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload Excel or CSV file containing transaction data", type=["xlsx","csv"], key="dash", label_visibility="collapsed")
        c1,c2 = st.columns(2)
        with c1: st.download_button("Download Sample Transaction File", to_excel(get_sample()), "GSTGenius_Sample.xlsx", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_side:
        st.markdown("""
        <div style='background:#1e3a5f;border-radius:10px;padding:20px;height:100%;'>
            <div style='display:flex;align-items:center;gap:10px;margin-bottom:12px;'>
                <div style='width:32px;height:32px;background:#3b82f6;border-radius:6px;display:flex;align-items:center;justify-content:center;'>
                    <svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2.5'><path d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/></svg>
                </div>
                <div>
                    <p style='color:white;font-size:13px;font-weight:700;margin:0;'>GSTGenius</p>
                    <p style='color:#64748b;font-size:10px;margin:0;letter-spacing:0.5px;'>COMPLIANCE PLATFORM</p>
                </div>
            </div>
            <p style='color:#94a3b8;font-size:12px;line-height:1.6;margin:0;'>Professional GST compliance for Indian businesses and CA firms. Covering all provisions of the CGST Act 2017.</p>
        </div>""", unsafe_allow_html=True)

    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith("xlsx") else pd.read_csv(uploaded)
        results_df = check_compliance(df)
        correct = len(results_df[results_df["Flag"]=="correct"])
        wrong = len(results_df[results_df["Flag"]=="wrong"])
        unknown = len(results_df[results_df["Flag"]=="unknown"])
     total_gst = results_df["Actual Tax (Rs)"].sum()
        score = int((correct/len(results_df))*100) if len(results_df)>0 else 0

        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Compliance Score", f"{score}%")
        c2.metric("Total Records", len(results_df))
        c3.metric("Compliant", correct)
        c4.metric("Non-Compliant", wrong)
        c5.metric("Total GST (Rs)", f"{total_gst:,.0f}")

        col1, col2 = st.columns(2)
        with col1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=score,
                title={"text":"Compliance Score","font":{"color":"#1e3a5f","size":13,"family":"Inter"}},
                gauge={"axis":{"range":[0,100],"tickcolor":"#94a3b8","tickfont":{"size":10}},"bar":{"color":"#1e3a5f","thickness":0.3},"steps":[{"range":[0,50],"color":"#fee2e2"},{"range":[50,80],"color":"#fef3c7"},{"range":[80,100],"color":"#dcfce7"}],"threshold":{"line":{"color":"#2563eb","width":3},"thickness":0.8,"value":score}},
                number={"suffix":"%","font":{"color":"#1e3a5f","size":40,"family":"Inter"}}
            ))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",height=260,margin=dict(t=30,b=10,l=20,r=20))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            counts = pd.DataFrame({"Status":["Compliant","Non-Compliant","Unverified"],"Count":[correct,wrong,unknown]})
            fig2 = px.donut = px.pie(counts, values="Count", names="Status", hole=0.55,
                color_discrete_map={"Compliant":"#1e3a5f","Non-Compliant":"#ef4444","Unverified":"#f59e0b"},
                title="Transaction Status")
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="#1e293b",height=260,margin=dict(t=30,b=10),font=dict(family="Inter"))
            fig2.update_traces(textfont_size=12)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<p class='card-section-title'>Detailed Compliance Report</p>", unsafe_allow_html=True)
        display = results_df.drop("Flag", axis=1)
        st.dataframe(display.style.apply(color_rows, axis=1), use_container_width=True)
        st.download_button("Download Compliance Report", to_excel(display), "GSTGenius_Compliance_Report.xlsx", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("<p class='card-section-title' style='margin-top:8px;'>Platform Modules</p>", unsafe_allow_html=True)
        modules = [
            ("GST Rate Checker","Validate correct GST rates across all 1000+ HSN/SAC codes as per CGST Act"),
            ("Invoice Validator","Verify invoices against all mandatory fields under Section 31 of CGST Act"),
            ("ITC Calculator","Compute eligible ITC and identify blocked credits under Section 17(5)"),
            ("GST Returns Tracker","Monitor all 12 GST return types, deadlines, and filing compliance"),
            ("Late Fee Calculator","Calculate penalties, interest under Section 47 and Section 50"),
            ("RCM Manager","Identify and manage Reverse Charge Mechanism liabilities"),
            ("E-Way Bill Checker","Validate e-way bill requirements for goods movement"),
            ("Analytics","Visual intelligence and trend analysis on your GST data"),
        ]
        c1,c2 = st.columns(2)
        for i,(t,d) in enumerate(modules):
            with [c1,c2][i%2]:
                st.markdown(f"""
                <div style='background:white;border:1px solid #e2e8f0;border-radius:8px;padding:16px;margin-bottom:12px;border-left:3px solid #1e3a5f;'>
                    <p style='font-weight:700;color:#1e3a5f;font-size:13px;margin:0 0 4px;'>{t}</p>
                    <p style='color:#64748b;font-size:12px;margin:0;line-height:1.5;'>{d}</p>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# GST RATE CHECKER
# ══════════════════════════════════════════════════════════════
elif page == "GST Rate Checker":
    header("GST Rate Checker", "Verify applicable GST rates — CGST Act 2017 Schedule I through VI")
    tab1, tab2 = st.tabs(["  Single Item Verification  ", "  Bulk Transaction Upload  "])

    with tab1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<p class='card-section-title'>Item Details</p>", unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1: cat = st.selectbox("Category", sorted(GST_RULES.keys()))
        with c2: gst_charged = st.number_input("GST Rate Applied (%)", 0, 28, 18)
        with c3: amt = st.number_input("Transaction Value (Rs)", 0, 10000000, 10000)

        exp = GST_RULES[cat]
        st.markdown(f"""
        <div style='background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:16px;margin:12px 0;display:flex;gap:24px;align-items:center;'>
            <div><p style='font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;margin:0;font-weight:600;'>Category</p><p style='font-size:16px;font-weight:700;color:#1e3a5f;margin:4px 0 0;'>{cat.title()}</p></div>
            <div style='width:1px;height:40px;background:#e2e8f0;'></div>
            <div><p style='font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;margin:0;font-weight:600;'>Correct GST Rate</p><p style='font-size:28px;font-weight:800;color:#1e3a5f;margin:4px 0 0;'>{exp}%</p></div>
            <div style='width:1px;height:40px;background:#e2e8f0;'></div>
            <div><p style='font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;margin:0;font-weight:600;'>GST Slab</p><p style='font-size:16px;font-weight:700;color:#1e3a5f;margin:4px 0 0;'>{"Exempt" if exp==0 else f"{exp}% Slab"}</p></div>
        </div>""", unsafe_allow_html=True)

        if st.button("Verify Compliance", use_container_width=True):
            gst_amt = amt * gst_charged / 100
            correct_amt = amt * exp / 100
            if gst_charged == exp:
                st.success(f"Compliant — GST rate of {exp}% correctly applied on {cat.title()}")
                c1,c2 = st.columns(2)
                c1.metric("GST Amount (Rs)", f"{gst_amt:,.2f}")
                c2.metric("Taxable Value (Rs)", f"{amt:,.2f}")
            else:
                st.error(f"Non-Compliant — Rate applied: {gst_charged}% | Correct rate: {exp}% | Category: {cat.title()}")
                c1,c2,c3 = st.columns(3)
                c1.metric("GST Charged (Rs)", f"{gst_amt:,.2f}")
                c2.metric("Correct GST (Rs)", f"{correct_amt:,.2f}")
                c3.metric("Variance (Rs)", f"{abs(gst_amt-correct_amt):,.2f}", delta="Overcharged" if gst_charged>exp else "Undercharged")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<p class='card-section-title'>GST Rate Schedule — All Slabs</p>", unsafe_allow_html=True)
        for slab in [0,5,12,18,28]:
            items = [k.title() for k,v in GST_RULES.items() if v==slab]
            colors = {"0":"#dcfce7","5":"#dbeafe","12":"#fef3c7","18":"#e0e7ff","28":"#fee2e2"}
            tcol = {"0":"#166534","5":"#1e40af","12":"#92400e","18":"#3730a3","28":"#991b1b"}
            st.markdown(f"""
            <div style='background:{colors[str(slab)]};border-radius:6px;padding:12px 16px;margin-bottom:8px;'>
                <p style='font-weight:700;color:{tcol[str(slab)]};font-size:13px;margin:0 0 6px;'>{"Exempt (0%)" if slab==0 else f"{slab}% GST Slab"}</p>
                <p style='color:{tcol[str(slab)]};font-size:12px;margin:0;opacity:0.85;'>{" · ".join(items[:12])}{"..." if len(items)>12 else ""}</p>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<p class='card-section-title'>Bulk Transaction Verification</p>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload transaction register (Excel / CSV)", type=["xlsx","csv"], key="bulk")
        st.download_button("Download Sample File", to_excel(get_sample()), "sample.xlsx")
        if uploaded:
            df = pd.read_excel(uploaded) if uploaded.name.endswith("xlsx") else pd.read_csv(uploaded)
            results_df = check_compliance(df)
            display = results_df.drop("Flag",axis=1)
            wrong = len(results_df[results_df["Flag"]=="wrong"])
            correct = len(results_df[results_df["Flag"]=="correct"])
            c1,c2,c3 = st.columns(3)
            c1.metric("Total Transactions", len(df))
            c2.metric("Compliant", correct)
            c3.metric("Non-Compliant", wrong)
            st.dataframe(display, use_container_width=True)
            st.download_button("Download Report", to_excel(display), "compliance_report.xlsx")
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# INVOICE VALIDATOR
# ══════════════════════════════════════════════════════════════
elif page == "Invoice Validator":
    header("Invoice Validator", "Section 31, CGST Act 2017 — Mandatory fields for a valid tax invoice")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='card-section-title'>Invoice Details</p>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("**Supplier Information**")
        inv_no = st.text_input("Invoice Number *", "INV-2025-001")
        inv_date = st.date_input("Invoice Date *", date.today())
        supplier_name = st.text_input("Supplier Legal Name *", "ABC Traders Pvt Ltd")
        supplier_gstin = st.text_input("Supplier GSTIN *", "27AAAAA0000A1Z5")
        supplier_address = st.text_input("Supplier Address *", "123, MG Road, Mumbai")
    with c2:
        st.markdown("**Buyer & Transaction Details**")
        buyer_name = st.text_input("Buyer Legal Name *", "XYZ Enterprises")
        buyer_gstin = st.text_input("Buyer GSTIN (B2B)", "29BBBBB1111B2Y6")
        place_of_supply = st.selectbox("Place of Supply *", ["Maharashtra","Karnataka","Delhi","Tamil Nadu","Gujarat","Rajasthan","Uttar Pradesh","West Bengal","Telangana","Kerala","Andhra Pradesh","Punjab","Haryana","Bihar","Odisha"])
        hsn_code = st.text_input("HSN / SAC Code *", "8471")
        taxable_value = st.number_input("Taxable Value (Rs) *", 0, 10000000, 50000)
        gst_rate = st.selectbox("GST Rate *", [0,5,12,18,28])

    if st.button("Validate Invoice", use_container_width=True):
        errors, warnings, passed = [], [], []
        if not inv_no: errors.append("Invoice number — mandatory under Section 31(1)(a)")
        else: passed.append("Invoice number present")
        if not inv_date: errors.append("Invoice date — mandatory under Section 31(1)(b)")
        else: passed.append("Invoice date mentioned")
        if not supplier_name: errors.append("Supplier legal name — mandatory under Section 31(1)(c)")
        else: passed.append("Supplier name present")
        if not supplier_gstin or len(supplier_gstin) != 15: errors.append("Supplier GSTIN — must be 15 characters [Section 31(1)(c)]")
        else: passed.append("Supplier GSTIN valid — 15 characters")
        if not supplier_address: errors.append("Supplier address — mandatory under Section 31(1)(c)")
        else: passed.append("Supplier address present")
        if not buyer_name: errors.append("Buyer name — mandatory under Section 31(1)(d)")
        else: passed.append("Buyer name present")
        if buyer_gstin and len(buyer_gstin) != 15: errors.append("Buyer GSTIN — must be exactly 15 characters")
        elif buyer_gstin: passed.append("Buyer GSTIN valid — 15 characters")
        else: warnings.append("Buyer GSTIN absent — acceptable for B2C supplies only")
        if not place_of_supply: errors.append("Place of supply — mandatory under Section 31(1)(e)")
        else: passed.append("Place of supply mentioned")
        if not hsn_code or len(hsn_code) < 4: errors.append("HSN/SAC code — minimum 4 digits required")
        else: passed.append("HSN/SAC code valid")
        if taxable_value <= 0: errors.append("Taxable value must be greater than zero")
        else: passed.append("Taxable value valid")

        cgst = taxable_value * (gst_rate/2) / 100
        sgst = taxable_value * (gst_rate/2) / 100
        total = taxable_value + cgst + sgst

        if errors: st.error(f"Invoice Non-Compliant — {len(errors)} mandatory field(s) missing or incorrect under CGST Act 2017")
        else: st.success("Invoice is fully compliant with Section 31 of the CGST Act 2017")

        c1,c2 = st.columns(2)
        with c1:
            st.markdown("<p class='card-section-title'>Validation Results</p>", unsafe_allow_html=True)
            for p in passed: st.markdown(f"<p style='color:#166534;font-size:13px;margin:3px 0;padding:4px 8px;background:#f0fdf4;border-radius:4px;'>&#10003; {p}</p>", unsafe_allow_html=True)
            for w in warnings: st.markdown(f"<p style='color:#92400e;font-size:13px;margin:3px 0;padding:4px 8px;background:#fffbeb;border-radius:4px;'>&#9888; {w}</p>", unsafe_allow_html=True)
            for e in errors: st.markdown(f"<p style='color:#991b1b;font-size:13px;margin:3px 0;padding:4px 8px;background:#fff1f2;border-radius:4px;'>&#10007; {e}</p>", unsafe_allow_html=True)
        with c2:
            st.markdown("<p class='card-section-title'>Tax Computation</p>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;'>
                <div style='display:flex;justify-content:space-between;padding:10px 16px;border-bottom:1px solid #e2e8f0;'><span style='color:#64748b;font-size:13px;'>Taxable Value</span><strong style='color:#1e293b;'>Rs {taxable_value:,.2f}</strong></div>
                <div style='display:flex;justify-content:space-between;padding:10px 16px;border-bottom:1px solid #e2e8f0;'><span style='color:#64748b;font-size:13px;'>CGST @ {gst_rate/2}%</span><strong style='color:#1e293b;'>Rs {cgst:,.2f}</strong></div>
                <div style='display:flex;justify-content:space-between;padding:10px 16px;border-bottom:1px solid #e2e8f0;'><span style='color:#64748b;font-size:13px;'>SGST @ {gst_rate/2}%</span><strong style='color:#1e293b;'>Rs {sgst:,.2f}</strong></div>
                <div style='display:flex;justify-content:space-between;padding:12px 16px;background:#1e3a5f;'><span style='color:#94a3b8;font-size:13px;font-weight:600;'>Total Invoice Value</span><strong style='color:#ffffff;font-size:18px;'>Rs {total:,.2f}</strong></div>
            </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ITC CALCULATOR
# ══════════════════════════════════════════════════════════════
elif page == "ITC Calculator":
    header("Input Tax Credit Calculator", "Section 16 and Section 17(5), CGST Act 2017 — Eligible and Blocked Credits")
    tab1, tab2 = st.tabs(["  ITC Calculation  ", "  Blocked Credits — Section 17(5)  "])
    with tab1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        n = st.number_input("Number of purchase entries", 1, 20, 3)
        purchases, total_itc = [], 0
        for i in range(int(n)):
            c1,c2,c3,c4,c5 = st.columns(5)
            with c1: item = st.text_input("Description", f"Purchase {i+1}", key=f"i_{i}")
            with c2: amt = st.number_input("Amount (Rs)", 0, 1000000, 10000, key=f"a_{i}")
            with c3: gst = st.selectbox("GST %", [0,5,12,18,28], index=3, key=f"g_{i}")
            with c4: elig = st.selectbox("ITC Eligible", ["Yes","No"], key=f"e_{i}")
            with c5: purpose = st.selectbox("Purpose", ["Business","Personal","Mixed"], key=f"p_{i}")
            gst_paid = amt * gst / 100
            if elig == "Yes" and purpose == "Business": total_itc += gst_paid
            elif elig == "Yes" and purpose == "Mixed": total_itc += gst_paid * 0.5
            purchases.append({"Description":item,"Amount (Rs)":amt,"GST %":gst,"GST Paid (Rs)":round(gst_paid,2),"ITC Eligible":elig,"Purpose":purpose,"ITC Claimable (Rs)":round(gst_paid,2) if (elig=="Yes" and purpose=="Business") else round(gst_paid*0.5,2) if (elig=="Yes" and purpose=="Mixed") else 0})

        if st.button("Compute ITC", use_container_width=True):
            df = pd.DataFrame(purchases)
            total_paid = df["GST Paid (Rs)"].sum()
            non_elig = total_paid - total_itc
            c1,c2,c3 = st.columns(3)
            c1.metric("Total GST Paid (Rs)", f"{total_paid:,.2f}")
            c2.metric("ITC Claimable (Rs)", f"{total_itc:,.2f}")
            c3.metric("Non-Eligible (Rs)", f"{non_elig:,.2f}")
            st.success(f"Net ITC claimable: Rs {total_itc:,.2f} — Available for set-off against output tax liability")
            st.dataframe(df, use_container_width=True, hide_index=True)
            fig = px.bar(df, x="Description", y=["GST Paid (Rs)","ITC Claimable (Rs)"], barmode="group", title="GST Paid vs ITC Claimable", color_discrete_map={"GST Paid (Rs)":"#94a3b8","ITC Claimable (Rs)":"#1e3a5f"})
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#1e293b", plot_bgcolor="#f8fafc", font=dict(family="Inter"))
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<p class='card-section-title'>Blocked Input Tax Credits — Section 17(5), CGST Act 2017</p>", unsafe_allow_html=True)
        st.warning("ITC on the following categories CANNOT be claimed even if GST is paid. Claiming blocked credits is a serious compliance violation.")
        for item in ITC_BLOCKED:
            st.markdown(f"<div style='background:#fff1f2;border:1px solid #fecaca;border-left:3px solid #ef4444;border-radius:6px;padding:10px 14px;margin-bottom:8px;'><p style='color:#991b1b;font-size:13px;margin:0;font-weight:500;'>{item}</p></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# GST RETURNS TRACKER
# ══════════════════════════════════════════════════════════════
elif page == "GST Returns Tracker":
    header("GST Returns Tracker", "Complete return filing schedule — All 12 return types under CGST Act 2017")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='card-section-title'>Annual Return Filing Schedule</p>", unsafe_allow_html=True)
    rows = [{"Return":k,"Frequency":v["freq"],"Due Date":v["due"],"Description":v["desc"],"Applicable To":v["filer"]} for k,v in GST_RETURNS.items()]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='card-section-title'>Filing Status Tracker</p>", unsafe_allow_html=True)
    for rname in ["GSTR-1","GSTR-3B","GSTR-9","GSTR-9C"]:
        c1,c2,c3,c4 = st.columns([2,2,2,1])
        with c1: st.markdown(f"<p style='font-weight:700;color:#1e3a5f;font-size:13px;margin:8px 0;'>{rname}</p>", unsafe_allow_html=True)
        with c2: st.markdown(f"<p style='color:#64748b;font-size:12px;margin:8px 0;'>{GST_RETURNS[rname]['due']}</p>", unsafe_allow_html=True)
        with c3: status = st.selectbox("", ["Filed","Pending","Not Applicable"], key=f"ret_{rname}", label_visibility="collapsed")
        with c4:
            color = "#dcfce7" if status=="Filed" else "#fee2e2" if status=="Pending" else "#f1f5f9"
            tcolor = "#166534" if status=="Filed" else "#991b1b" if status=="Pending" else "#475569"
            st.markdown(f"<span class='badge' style='background:{color};color:{tcolor};border:none;margin-top:8px;display:inline-block;'>{status}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='card-section-title'>Pre-Filing Checklist</p>", unsafe_allow_html=True)
    checks = [
        "Sales invoices reconciled with books of accounts",
        "Purchase register reconciled with GSTR-2B auto-drafted statement",
        "ITC eligibility verified — blocked credits identified and excluded",
        "Output tax liability computed correctly",
        "Tax payment (DRC-03 or PMT-06) made prior to filing",
        "Reverse Charge entries identified and accounted for",
        "E-way bill data reconciled with invoice data",
        "Credit notes and debit notes accounted for correctly",
        "Export invoices with correct IGST treatment",
        "Inter-state and intra-state supply classification verified",
    ]
    c1,c2 = st.columns(2)
    for i,c in enumerate(checks):
        with [c1,c2][i%2]: st.checkbox(c, key=f"chk_{i}")
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# LATE FEE CALCULATOR
# ══════════════════════════════════════════════════════════════
elif page == "Late Fee Calculator":
    header("Late Fee & Interest Calculator", "Section 47 (Late Fee) and Section 50 (Interest) — CGST Act 2017")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        return_type = st.selectbox("Return Type", list(LATE_FEES.keys()))
        due_date = st.date_input("Filing Due Date", date(2025,11,20))
        filing_date = st.date_input("Actual / Expected Filing Date", date.today())
        turnover = st.number_input("Annual Turnover (Rs)", 0, 1000000000, 5000000)
    with c2:
        tax_liability = st.number_input("Unpaid Tax Liability (Rs) [for interest]", 0, 10000000, 50000)
        nil_return = st.checkbox("Nil Return (No outward supplies)")
        taxpayer_type = st.selectbox("Taxpayer Category", ["Regular Taxpayer","MSME / Small Taxpayer","Composition Dealer"])

    if st.button("Compute Penalty & Interest", use_container_width=True):
        days = max(0, (filing_date - due_date).days)
        daily = 10 if nil_return else LATE_FEES.get(return_type,50)
        fee = daily * 2 * days
        interest = tax_liability * 0.18 * days / 365 if days > 0 else 0
        max_cap = 500 if nil_return else (5000 if turnover<=15000000 else 10000)
        actual_fee = min(fee, max_cap)

        if days == 0:
            st.success("No late fee applicable — Return filed within due date")
        else:
            st.error(f"Late filing detected — {days} days overdue")
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Days Overdue", days)
            c2.metric("Late Fee (Rs)", f"{actual_fee:,.0f}")
            c3.metric("Interest @ 18% p.a. (Rs)", f"{interest:,.0f}")
            c4.metric("Total Liability (Rs)", f"{actual_fee+interest:,.0f}")
            if fee > max_cap:
                st.info(f"Late fee capped at Rs {max_cap:,} per return as per your turnover bracket and return type")
            st.markdown(f"""
            <div style='background:#fff1f2;border:1px solid #fecaca;border-radius:8px;padding:16px;margin-top:12px;'>
                <p style='font-weight:700;color:#991b1b;font-size:13px;margin:0 0 8px;'>Legal Reference</p>
                <p style='color:#991b1b;font-size:12px;margin:0;line-height:1.6;'>
                Section 47 — Late fee of Rs {daily} per day (CGST) + Rs {daily} per day (SGST) = Rs {daily*2}/day<br>
                Section 50 — Interest at 18% per annum on unpaid tax from due date to date of payment<br>
                Maximum late fee per return: Rs {max_cap:,} (as per CBIC notification for your turnover bracket)
                </p>
            </div>""", unsafe_allow_html=True)
            rng = list(range(0, days+31, max(1, days//10)))
            vals = [min(daily*2*d, max_cap) + tax_liability*0.18*d/365 for d in rng]
            fig = px.area(x=rng, y=vals, title="Cumulative Penalty & Interest Accrual", labels={"x":"Days Overdue","y":"Total Liability (Rs)"}, color_discrete_sequence=["#ef4444"])
            fig.add_vline(x=days, line_dash="dash", line_color="#1e3a5f", annotation_text=f"Current: Day {days}", annotation_font_color="#1e3a5f")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#1e293b", plot_bgcolor="#f8fafc", font=dict(family="Inter"))
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# RCM MANAGER
# ══════════════════════════════════════════════════════════════
elif page == "RCM Manager":
    header("Reverse Charge Mechanism Manager", "Section 9(3) and Section 9(4), CGST Act 2017 — RCM Liability Identification")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='card-section-title'>Notified Services under Section 9(3) — Mandatory RCM</p>", unsafe_allow_html=True)
    rcm_items = [
        {"Category":"Legal Services","Supplier":"Advocate / Firm of Advocates","Recipient":"Business Entity","GST Rate":"18%","Section":"Section 9(3)"},
        {"Category":"Goods Transport Agency (GTA)","Supplier":"GTA","Recipient":"Factory / Society / Registered Person","GST Rate":"5% or 12%","Section":"Section 9(3)"},
        {"Category":"Director Services","Supplier":"Director of a Company","Recipient":"Company / Body Corporate","GST Rate":"18%","Section":"Section 9(3)"},
        {"Category":"Import of Services","Supplier":"Foreign Service Provider","Recipient":"Indian Registered Person","GST Rate":"Applicable rate","Section":"Section 9(3)"},
        {"Category":"Renting of Motor Vehicle","Supplier":"Unregistered Person","Recipient":"Registered Business","GST Rate":"5%","Section":"Section 9(3)"},
        {"Category":"Security Services","Supplier":"Individual / HUF (unregistered)","Recipient":"Registered Business","GST Rate":"18%","Section":"Section 9(3)"},
        {"Category":"Insurance Agent","Supplier":"Insurance Agent","Recipient":"Insurance Company","GST Rate":"18%","Section":"Section 9(3)"},
        {"Category":"Sponsorship Services","Supplier":"Any person","Recipient":"Company / Partnership Firm","GST Rate":"18%","Section":"Section 9(3)"},
    ]
    st.dataframe(pd.DataFrame(rcm_items), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='card-section-title'>RCM Liability Calculator</p>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: rcm_cat = st.selectbox("Service Category", ["Legal Services","GTA","Director Services","Import of Services","Security Services","Insurance Agent","Sponsorship","Others"])
    with c2: rcm_amt = st.number_input("Invoice Value (Rs)", 0, 10000000, 50000)
    with c3: rcm_rate = st.selectbox("Applicable GST Rate (%)", [5,12,18,28])
    if st.button("Calculate RCM Liability", use_container_width=True):
        rcm_gst = rcm_amt * rcm_rate / 100
        st.success(f"RCM Liability: Rs {rcm_gst:,.2f} — To be paid by recipient in cash (ITC cannot offset RCM liability)")
        c1,c2,c3 = st.columns(3)
        c1.metric("Taxable Value", f"Rs {rcm_amt:,.2f}")
        c2.metric("RCM GST Payable", f"Rs {rcm_gst:,.2f}")
        c3.metric("CGST + SGST", f"Rs {rcm_gst/2:,.2f} each")
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# E-WAY BILL CHECKER
# ══════════════════════════════════════════════════════════════
elif page == "E-Way Bill Checker":
    header("E-Way Bill Compliance Checker", "Rule 138, CGST Rules 2017 — Validity, Requirements and Exemptions")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='card-section-title'>E-Way Bill Requirement Check</p>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        goods_value = st.number_input("Value of Goods (Rs)", 0, 100000000, 60000)
        distance = st.number_input("Distance of Transport (km)", 0, 5000, 150)
        transport_mode = st.selectbox("Mode of Transport", ["Road","Rail","Air","Ship"])
        supply_type = st.selectbox("Type of Supply", ["Outward Supply","Inward Supply","Import","Export","Job Work"])
    with c2:
        goods_type = st.selectbox("Goods Category", ["General Goods","Exempt Goods","Handicraft","Postal Goods","LPG for household","Defence formation","Railway equipment"])
        from_state = st.selectbox("Origin State", ["Maharashtra","Karnataka","Delhi","Tamil Nadu","Gujarat","Rajasthan","Uttar Pradesh"])
        to_state = st.selectbox("Destination State", ["Maharashtra","Karnataka","Delhi","Tamil Nadu","Gujarat","Rajasthan","Uttar Pradesh"])

    if st.button("Check E-Way Bill Requirement", use_container_width=True):
        inter_state = from_state != to_state
        exempt_cats = ["Exempt Goods","Handicraft","Postal Goods","LPG for household","Defence formation","Railway equipment"]
        required = goods_value >= 50000 and goods_type not in exempt_cats
        validity_days = max(1, distance // 200) if transport_mode == "Road" else max(1, distance // 400)

        if not required:
            st.success("E-Way Bill NOT required — Goods value below Rs 50,000 or category is exempt")
        else:
            st.warning("E-Way Bill REQUIRED before commencement of goods movement")
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("E-Way Bill Required", "Yes")
            c2.metric("Supply Type", "Inter-State" if inter_state else "Intra-State")
            c3.metric("Distance", f"{distance} km")
            c4.metric("Validity", f"{validity_days} day(s)")
            st.markdown(f"""
            <div style='background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:16px;margin-top:12px;'>
                <p style='font-weight:700;color:#92400e;font-size:13px;margin:0 0 6px;'>Compliance Requirements</p>
                <p style='color:#92400e;font-size:12px;margin:0;line-height:1.8;'>
                1. Generate E-Way Bill on ewaybillgst.gov.in before goods movement begins<br>
                2. E-Way Bill valid for {validity_days} day(s) from date of generation<br>
                3. Carry original copy of E-Way Bill during transportation<br>
                4. Update Part-B (vehicle details) if transporter changes<br>
                5. Penalty for non-compliance: Rs 10,000 or tax amount — whichever is higher [Section 129]
                </p>
            </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ANALYTICS
# ══════════════════════════════════════════════════════════════
elif page == "Analytics":
    header("GST Analytics", "Transaction intelligence and compliance trend analysis")
    uploaded = st.file_uploader("Upload transaction register for analysis", type=["xlsx","csv"])
    st.download_button("Download Sample File", to_excel(get_sample()), "sample.xlsx")
    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith("xlsx") else pd.read_csv(uploaded)
        results_df = check_compliance(df)
        amt_col = [c for c in df.columns if "Amount" in c][0]
        gst_col = next((c for c in df.columns if "GST" in c and "%" in c), df.columns[6])
        c1,c2 = st.columns(2)
        with c1:
            fig = px.bar(df, x=df.columns[3], y=amt_col, title="Transaction Value Distribution", color_discrete_sequence=["#1e3a5f"])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#1e293b", plot_bgcolor="#f8fafc", font=dict(family="Inter"))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            g = df.groupby(gst_col)[amt_col].sum().reset_index()
            fig2 = px.pie(g, values=amt_col, names=gst_col, title="Revenue by GST Slab", hole=0.5, color_discrete_sequence=["#1e3a5f","#2563eb","#60a5fa","#93c5fd","#bfdbfe"])
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#1e293b", font=dict(family="Inter"))
            st.plotly_chart(fig2, use_container_width=True)
        df["GST Amount"] = df[amt_col] * df[gst_col] / 100
        fig3 = px.bar(df, x=df.columns[3], y="GST Amount", title="GST Liability per Transaction", color_discrete_sequence=["#334155"])
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#1e293b", plot_bgcolor="#f8fafc", font=dict(family="Inter"))
        st.plotly_chart(fig3, use_container_width=True)
        stat = results_df["Flag"].value_counts()
        fig4 = px.bar(x=stat.index, y=stat.values, title="Compliance Status Summary", color=stat.index, color_discrete_map={"correct":"#1e3a5f","wrong":"#ef4444","unknown":"#f59e0b"})
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#1e293b", plot_bgcolor="#f8fafc", font=dict(family="Inter"))
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Upload a transaction register to generate analytics")

# ══════════════════════════════════════════════════════════════
# GST KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════
elif page == "GST Knowledge Base":
    header("GST Knowledge Base", "Comprehensive reference — CGST Act 2017, Rules, Notifications and Circulars")
    topics = {
        "What is GST and its structure?": "GST is a comprehensive, multi-stage, destination-based indirect tax levied on every value addition. India follows a dual GST structure — CGST (Central GST) and SGST (State GST) for intra-state transactions, and IGST (Integrated GST) for inter-state transactions. GST is governed by the CGST Act 2017, IGST Act 2017, and respective State GST Acts.",
        "GST Registration — Section 22 to Section 30": "Mandatory registration for businesses with annual aggregate turnover exceeding Rs 40 lakhs (goods) or Rs 20 lakhs (services). Threshold is Rs 10 lakhs for special category states. Voluntary registration is permitted. GSTIN is a 15-digit alphanumeric code: State code (2) + PAN (10) + Entity number (1) + Z (1) + Check digit (1).",
        "Input Tax Credit — Section 16 and 17": "ITC is available to registered persons on inward supplies used in the course or furtherance of business. Conditions: Tax invoice available, goods/services received, tax paid by supplier, return filed. Time limit: Earlier of due date of annual return for next financial year or actual date of filing annual return. Section 17(5) specifies blocked credits.",
        "Place of Supply — IGST Act Sections 10-13": "Determines whether a supply is intra-state (CGST+SGST) or inter-state (IGST). For goods: place of supply is location where goods are delivered. For services: generally place of recipient's establishment. Specific rules apply for immovable property, restaurants, event services, transportation, and digital services.",
        "Tax Invoice Requirements — Section 31": "A tax invoice must contain: supplier name, address, GSTIN; consecutive serial number; date of issue; recipient details (GSTIN for B2B); place of supply; HSN/SAC code; description, quantity and value of goods/services; taxable value and discounts; applicable tax rate and amount (CGST, SGST, IGST); and signature. E-invoicing mandatory for turnover above Rs 5 crores.",
        "Composition Scheme — Section 10": "Available to businesses with turnover up to Rs 1.5 crore (Rs 75 lakhs for special category states). Tax rates: 1% for manufacturers, 5% for restaurants, 6% for service providers. Cannot issue tax invoice, collect tax from customers, or claim ITC. File GSTR-4 annually instead of monthly returns.",
        "Time of Supply — Section 12 and 13": "For goods: earlier of date of invoice or date of receipt of payment. For services: earlier of date of invoice (if within 30 days of supply) or date of receipt of payment. For reverse charge: date of payment or 60th day from supplier's invoice, whichever is earlier.",
        "Annual Return — Section 44": "GSTR-9 is the annual return consolidating all monthly/quarterly returns. Mandatory for all regular taxpayers with turnover above Rs 2 crores. GSTR-9C (reconciliation statement) required for taxpayers with turnover above Rs 5 crores — must be certified by a CA or CMA.",
        "GST Audit — Section 65 and 66": "Section 65: Departmental audit by GST authorities. Section 66: Special audit ordered by the Commissioner if value not correctly declared or credit not within normal limits. Taxpayer must cooperate, maintain books of accounts for 6 years from due date of annual return.",
        "Penalties and Offences — Section 122 to 138": "Penalty for tax evasion: 100% of tax evaded or Rs 10,000, whichever is higher. Penalty for other offences: Rs 10,000 or 10% of tax. Late fee: Section 47. Interest on delayed payment: Section 50 — 18% p.a. (24% for excess ITC claims). Prosecution for offences above Rs 5 crores.",
    }
    search = st.text_input("Search knowledge base", "", placeholder="e.g. ITC blocked credits, place of supply, e-invoicing...")
    if search:
        found = False
        for q,a in topics.items():
            if any(w.lower() in q.lower() or w.lower() in a.lower() for w in search.split()):
                st.markdown(f"""
                <div style='background:#eff6ff;border:1px solid #bfdbfe;border-left:3px solid #1e3a5f;border-radius:6px;padding:16px;margin-bottom:10px;'>
                    <p style='font-weight:700;color:#1e3a5f;font-size:13px;margin:0 0 8px;'>{q}</p>
                    <p style='color:#334155;font-size:13px;line-height:1.7;margin:0;'>{a}</p>
                </div>""", unsafe_allow_html=True)
                found = True
        if not found: st.warning("No results found. Try different search terms.")

    st.markdown("<p class='card-section-title' style='margin-top:16px;'>Complete Reference Library</p>", unsafe_allow_html=True)
    for q,a in topics.items():
        with st.expander(q):
            st.markdown(f"<p style='color:#334155;font-size:13px;line-height:1.75;'>{a}</p>", unsafe_allow_html=True)

# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align:center;padding:8px;'>
    <p style='color:#94a3b8;font-size:11px;margin:0;letter-spacing:0.3px;'>
        GSTGenius &copy; 2026 &nbsp;&nbsp;|&nbsp;&nbsp; Built by Sanskar Gupta &nbsp;&nbsp;|&nbsp;&nbsp; guptasanskar824@gmail.com &nbsp;&nbsp;|&nbsp;&nbsp; Professional GST Compliance Platform &nbsp;&nbsp;|&nbsp;&nbsp; Covering CGST Act 2017
    </p>
</div>
""", unsafe_allow_html=True)
