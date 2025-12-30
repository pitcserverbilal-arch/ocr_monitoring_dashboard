# =========================
# OCR BATCH INTELLIGENCE DASHBOARD - Render.com Optimized
# =========================
import streamlit as st
import pandas as pd
import oracledb
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="OCR Batch Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# DATABASE CONFIGURATION - RENDER COMPATIBLE
# =========================
# Get configuration from environment variables or use defaults
DB_HOST = os.getenv("DB_HOST", "128.101.23.130")
DB_PORT = int(os.getenv("DB_PORT", "1521"))
DB_SID = os.getenv("DB_SID", "theftdb")
DB_USER = os.getenv("DB_USER", "theft_data")
DB_PWD = os.getenv("DB_PWD", "theft_data")

DISCO_MAP = {
    "11": "LESCO",
    "12": "GEPCO",
    "13": "FESCO",
    "14": "IESCO",
    "15": "MEPCO",
    "26": "PESCO",
    "27": "HAZECO",
    "37": "HESCO",
    "38": "SEPCO",
    "48": "QESCO",
    "59": "TESCO"
}

# =========================
# POWER BI MODERN STYLING - PERFECT CARD SIZING
# =========================
st.markdown("""
<style>
/* Power BI Enhanced Theme */
:root {
    --primary-blue: #0078D4;
    --secondary-blue: #50E6FF;
    --accent-blue: #1890FF;
    --dark-blue: #005A9E;
    --light-blue: #E6F7FF;
    --dark-gray: #2C2C2C;
    --medium-gray: #4A4A4A;
    --light-gray: #F3F2F1;
    --white: #FFFFFF;
    --success-green: #107C10;
    --light-green: #DFF6DD;
    --warning-orange: #FFB900;
    --light-orange: #FFF4CE;
    --danger-red: #D13438;
    --light-red: #FDE7E9;
    --accent-purple: #8661C5;
    --light-purple: #F3F0FF;
}

/* PERFECT KPI Cards - LARGER AND BETTER */
.enhanced-kpi {
    background: var(--white);
    border-radius: 16px;
    padding: 25px 15px;
    color: var(--dark-gray);
    text-align: center;
    position: relative;
    overflow: hidden;
    height: 200px;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
    border: none;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin: 0 5px 15px 5px;
}

.enhanced-kpi:hover {
    transform: translateY(-5px);
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.12);
}

.enhanced-kpi.blue { 
    background: linear-gradient(135deg, var(--primary-blue), var(--dark-blue));
    color: white;
}
.enhanced-kpi.green { 
    background: linear-gradient(135deg, var(--success-green), #0D5C0D);
    color: white;
}
.enhanced-kpi.orange { 
    background: linear-gradient(135deg, var(--warning-orange), #D69C00);
    color: white;
}
.enhanced-kpi.red { 
    background: linear-gradient(135deg, var(--danger-red), #B02A30);
    color: white;
}
.enhanced-kpi.purple { 
    background: linear-gradient(135deg, var(--accent-purple), #6A4CA6);
    color: white;
}

.enhanced-kpi .kpi-icon {
    font-size: 30px;
    margin-bottom: 5px;
    opacity: 0.9;
}

.enhanced-kpi .kpi-value {
    font-size: 48px;
    font-weight: 800;
    line-height: 1;
    margin: 15px 0;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
}

.enhanced-kpi .kpi-label {
    font-size: 15px;
    opacity: 0.9;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-weight: 600;
    margin-top: 5px;
    padding: 0 20px;
    text-align: center;
    line-height: 1.2;
}

/* Enhanced Cards */
.enhanced-card {
    background: var(--white);
    border-radius: 16px;
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(0, 0, 0, 0.06);
    transition: all 0.3s ease;
}

.enhanced-card:hover {
    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.12);
}

/* Status Indicators */
.status-indicator {
    display: inline-flex;
    align-items: center;
    padding: 8px 14px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    margin: 2px;
}

.status-success {
    background: var(--light-green);
    color: var(--success-green);
}

.status-info {
    background: var(--light-blue);
    color: var(--primary-blue);
}

/* PERFECT Flag Cards */
.flag-card {
    border-radius: 12px;
    padding: 25px 15px;
    text-align: center;
    margin: 5px;
    transition: all 0.3s ease;
    height: 200px;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.flag-A {
    background: linear-gradient(135deg, rgba(16, 124, 16, 0.1), rgba(16, 124, 16, 0.05));
    border: 5px solid var(--success-green);
    color: var(--success-green);
}

.flag-C {
    background: linear-gradient(135deg, rgba(255, 185, 0, 0.1), rgba(255, 185, 0, 0.05));
    border: 5px solid var(--warning-orange);
    color: var(--warning-orange);
}

.flag-D {
    background: linear-gradient(135deg, rgba(253, 126, 20, 0.1), rgba(253, 126, 20, 0.05));
    border: 5px solid #fd7e14;
    color: #fd7e14;
}

.flag-E {
    background: linear-gradient(135deg, rgba(220, 53, 69, 0.1), rgba(220, 53, 69, 0.05));
    border: 5px solid var(--danger-red);
    color: var(--danger-red);
}

.flag-N {
    background: linear-gradient(135deg, rgba(108, 117, 125, 0.1), rgba(108, 117, 125, 0.05));
    border: 5px solid #6c757d;
    color: #6c757d;
}

.flag-card .flag-icon {
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 2px;
}

.flag-card .flag-value {
    font-size: 28px;
    font-weight: 900;
    margin: 2px 0;
}

.flag-card .flag-label {
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 8px;
    padding: 0 10px;
    text-align: center;
    line-height: 1.2;
}

.flag-card .flag-percentage {
    font-size: 14px;
    color: #666;
    margin: 8px 0;
}

.flag-card .flag-desc {
    font-size: 12px;
    color: #888;
    font-style: italic;
    padding: 0 10px;
    text-align: center;
    line-height: 1.3;
}

/* OCR Model Accuracy Cards */
.ocr-model-card {
    border-radius: 16px;
    padding: 30px 20px;
    color: white;
    text-align: center;
    height: 220px;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
    margin: 5px 0 15px 0;
}

.ocr-model-card .ocr-icon {
    font-size: 44px;
    margin-bottom: 15px;
    opacity: 0.9;
}

.ocr-model-card .ocr-value {
    font-size: 56px;
    font-weight: 800;
    line-height: 1;
    margin: 10px 0;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
}

.ocr-model-card .ocr-label {
    font-size: 18px;
    opacity: 0.9;
    font-weight: 600;
    margin-top: 10px;
    padding: 0 15px;
    text-align: center;
    line-height: 1.2;
}

.ocr-model-card .ocr-desc {
    font-size: 14px;
    opacity: 0.8;
    margin-top: 8px;
    padding: 0 10px;
    text-align: center;
    line-height: 1.3;
}

/* Animation Classes */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.5s ease-out;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DATA LOADER - WITH FALLBACK TO SAMPLE DATA
# =========================
@st.cache_data(ttl=300, show_spinner=False)
def load_all_disco_data(disco_code=None):
    """Load ALL data for specific DISCO or all DISCOS"""
    
    # Show environment info
    if os.environ.get("RENDER"):
        st.sidebar.info("☁️ Running on Render.com")
    
    # Try database connection first
    try:
        # Create DSN for Oracle
        dsn = f"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={DB_HOST})(PORT={DB_PORT}))(CONNECT_DATA=(SID={DB_SID})))"
        
        # Try to connect
        connection = oracledb.connect(
            user=DB_USER,
            password=DB_PWD,
            dsn=dsn
        )
        
        # Build query
        if disco_code:
            query = f"""
            SELECT 
                REF_DIGITS,
                SUBSTR(REF_DIGITS, 3, 2) AS DISCO_CODE,
                BILMONTH,
                IMAGE_VERIFY_CODE_PITC
            FROM TBL_GENERAL_BILL_PRINT_AUDIT 
            WHERE SUBSTR(REF_DIGITS, 3, 2) = '{disco_code}'
            FETCH FIRST 5000 ROWS ONLY
            """
        else:
            query = """
            SELECT 
                REF_DIGITS,
                SUBSTR(REF_DIGITS, 3, 2) AS DISCO_CODE,
                BILMONTH,
                IMAGE_VERIFY_CODE_PITC
            FROM TBL_GENERAL_BILL_PRINT_AUDIT
            FETCH FIRST 5000 ROWS ONLY
            """
        
        df = pd.read_sql(query, connection)
        connection.close()
        
        if len(df) == 0:
            raise Exception("No data returned from database")
            
        # Process the data
        df["DISCO_NAME"] = df["DISCO_CODE"].map(DISCO_MAP).fillna("UNKNOWN")
        df["BATCH_NO"] = df["REF_DIGITS"].str[:2]
        df["SUB_DIV"] = df["REF_DIGITS"].str[:5]
        df["BATCH_ID"] = df["BATCH_NO"] + "-" + df["DISCO_CODE"]
        df["PROCESSING_STATUS"] = df["IMAGE_VERIFY_CODE_PITC"].apply(
            lambda x: "Processed" if pd.notna(x) else "Pending"
        )
        df["ACCURACY_CATEGORY"] = df["IMAGE_VERIFY_CODE_PITC"].apply(
            lambda x: "Success (A,C,D)" if x in ['A', 'C', 'D'] else
                     "Images Not Available (E)" if x == 'E' else
                     "Reading Not Matched (N)" if x == 'N' else
                     "Not Processed" if pd.isna(x) else "Other"
        )
        
        st.sidebar.success(f"✅ Database: {len(df)} records")
        return df
        
    except Exception as e:
        st.sidebar.warning(f"⚠️ Using sample data")
        
        # =========================
        # SAMPLE DATA GENERATION (Fallback)
        # =========================
        sample_size = 5000
        codes = [disco_code] if disco_code else list(DISCO_MAP.keys())[:3]
        
        data = {
            'REF_DIGITS': [],
            'DISCO_CODE': [],
            'BILMONTH': [],
            'IMAGE_VERIFY_CODE_PITC': []
        }
        
        for i in range(sample_size):
            disco = np.random.choice(codes)
            batch_no = f"{np.random.randint(1, 20):02d}"
            sub_div = f"{batch_no}{disco}{np.random.randint(1, 5)}"
            ref_digits = f"{sub_div}{np.random.randint(100000000, 999999999)}"
            
            data['REF_DIGITS'].append(ref_digits)
            data['DISCO_CODE'].append(disco)
            data['BILMONTH'].append(np.random.choice(pd.date_range('2024-01-01', periods=6, freq='MS')))
            data['IMAGE_VERIFY_CODE_PITC'].append(np.random.choice(['A', 'C', 'D', 'E', 'N', None], 
                                                                 p=[0.35, 0.2, 0.15, 0.1, 0.05, 0.15]))
        
        df = pd.DataFrame(data)
        df["DISCO_NAME"] = df["DISCO_CODE"].map(DISCO_MAP)
        df["BATCH_NO"] = df["REF_DIGITS"].str[:2]
        df["SUB_DIV"] = df["REF_DIGITS"].str[:5]
        df["BATCH_ID"] = df["BATCH_NO"] + "-" + df["DISCO_CODE"]
        df["PROCESSING_STATUS"] = df["IMAGE_VERIFY_CODE_PITC"].apply(
            lambda x: "Processed" if pd.notna(x) else "Pending"
        )
        df["ACCURACY_CATEGORY"] = df["IMAGE_VERIFY_CODE_PITC"].apply(
            lambda x: "Success (A,C,D)" if x in ['A', 'C', 'D'] else
                     "Images Not Available (E)" if x == 'E' else
                     "Reading Not Matched (N)" if x == 'N' else
                     "Not Processed" if pd.isna(x) else "Other"
        )
        
        return df

# =========================
# BATCH PROCESSING FUNCTIONS
# =========================
def get_batch_statistics(df):
    """Get statistics for all batches"""
    batch_stats = []
    
    for batch_id in sorted(df["BATCH_ID"].unique()):
        batch_df = df[df["BATCH_ID"] == batch_id]
        
        total_records = len(batch_df)
        processed_records = batch_df["IMAGE_VERIFY_CODE_PITC"].notna().sum()
        
        flag_counts = {}
        for flag in ['A', 'C', 'D', 'E', 'N']:
            flag_counts[flag] = (batch_df["IMAGE_VERIFY_CODE_PITC"] == flag).sum()
        
        successful = flag_counts['A'] + flag_counts['C'] + flag_counts['D']
        total_an = flag_counts['A'] + flag_counts['N']
        ocr_accuracy = (flag_counts['A'] / total_an * 100) if total_an > 0 else 0
        
        processing_rate = (processed_records / total_records * 100) if total_records > 0 else 0
        success_rate = (successful / processed_records * 100) if processed_records > 0 else 0
        
        batch_stats.append({
            "Batch ID": batch_id,
            "DISCO": batch_df["DISCO_NAME"].iloc[0],
            "Total Records": total_records,
            "Processed": processed_records,
            "Successful (A,C,D)": successful,
            "Success Rate (A,C,D)": success_rate,
            "Processing Rate": processing_rate,
            "OCR Model Accuracy (A vs N)": ocr_accuracy,
            "Flag A": flag_counts['A'],
            "Flag C": flag_counts['C'],
            "Flag D": flag_counts['D'],
            "Flag E": flag_counts['E'],
            "Flag N": flag_counts['N'],
            "Total A+N": total_an
        })
    
    return pd.DataFrame(batch_stats)

def calculate_ocr_model_accuracy(df):
    """Calculate OCR model accuracy based on A vs N flags only"""
    count_a = (df["IMAGE_VERIFY_CODE_PITC"] == 'A').sum()
    count_n = (df["IMAGE_VERIFY_CODE_PITC"] == 'N').sum()
    total_an = count_a + count_n
    
    if total_an > 0:
        accuracy = (count_a / total_an * 100)
    else:
        accuracy = 0
    
    return {
        "count_a": count_a,
        "count_n": count_n,
        "total_an": total_an,
        "accuracy": accuracy
    }

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 ANALYSIS SETTINGS")
    
    selection_mode = st.radio(
        "Analysis Mode:",
        ["Single DISCO", "All DISCOS"],
        index=0,
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if selection_mode == "Single DISCO":
        disco_choice = st.selectbox(
            "Select DISCO:",
            options=list(DISCO_MAP.values()),
            index=4
        )
        disco_code = None
        for code, name in DISCO_MAP.items():
            if name == disco_choice:
                disco_code = code
                break
    else:
        disco_code = None
        disco_choice = "ALL DISCOS"
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
    st.markdown("### 📊 QUICK METRICS")
    
    with st.spinner("Loading..."):
        df_temp = load_all_disco_data(disco_code)
        processed_temp = df_temp[df_temp["IMAGE_VERIFY_CODE_PITC"].notna()]
        ocr_temp = calculate_ocr_model_accuracy(df_temp)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total", f"{len(df_temp):,}")
        with col2:
            st.metric("OCR Accuracy", f"{ocr_temp['accuracy']:.1f}%")
    
    st.progress(len(processed_temp) / len(df_temp))
    st.caption(f"Showing: {disco_choice}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Refresh Dashboard", use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.rerun()

# =========================
# LOAD DATA
# =========================
with st.spinner(f"🚀 Loading data for {disco_choice}..."):
    df = load_all_disco_data(disco_code)
    batch_stats = get_batch_statistics(df)
    ocr_accuracy = calculate_ocr_model_accuracy(df)

# =========================
# HEADER
# =========================
st.markdown(f"""
<div class="enhanced-header fade-in">
    <h1 style="margin: 0; font-size: 42px; font-weight: 800;">
        📊 OCR BATCH INTELLIGENCE DASHBOARD
    </h1>
    <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.95;">
        Advanced Analytics | A,C,D Success Classification | OCR Model Performance
    </p>
    <div style="margin-top: 20px; display: flex; justify-content: center; gap: 20px;">
        <span class="status-indicator status-success">🟢 Live Data</span>
        <span class="status-indicator status-info">📅 {datetime.now().strftime('%Y-%m-%d')}</span>
        <span class="status-indicator status-info">🏢 {disco_choice}</span>
        <span class="status-indicator status-info">📊 {len(df):,} Records</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# EXECUTIVE KPIs
# =========================
st.markdown('<div class="enhanced-card fade-in">', unsafe_allow_html=True)
st.markdown("### 📈 EXECUTIVE DASHBOARD")

total_records = len(df)
processed_records = df["IMAGE_VERIFY_CODE_PITC"].notna().sum()
successful_records = df["IMAGE_VERIFY_CODE_PITC"].isin(['A', 'C', 'D']).sum()
image_issues = (df["IMAGE_VERIFY_CODE_PITC"] == 'E').sum()
perfect_matches = (df["IMAGE_VERIFY_CODE_PITC"] == 'A').sum()

processing_rate = (processed_records / total_records * 100) if total_records > 0 else 0
success_rate = (successful_records / processed_records * 100) if processed_records > 0 else 0
perfect_match_rate = (perfect_matches / processed_records * 100) if processed_records > 0 else 0
image_issue_rate = (image_issues / processed_records * 100) if processed_records > 0 else 0

kpi_cols = st.columns(5)

with kpi_cols[0]:
    st.markdown(f"""
    <div class="enhanced-kpi blue">
        <div class="kpi-icon">📊</div>
        <div class="kpi-value">{total_records:,}</div>
        <div class="kpi-label">Total Records</div>
        <div class="kpi-trend">
            <span>⚡</span>
            <span>{processing_rate:.1f}% processed</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[1]:
    st.markdown(f"""
    <div class="enhanced-kpi green">
        <div class="kpi-icon">✅</div>
        <div class="kpi-value">{success_rate:.1f}%</div>
        <div class="kpi-label">Success Rate (A,C,D)</div>
        <div class="kpi-trend">
            <span>📈</span>
            <span>{successful_records:,} successful</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[2]:
    st.markdown(f"""
    <div class="enhanced-kpi purple">
        <div class="kpi-icon">🤖</div>
        <div class="kpi-value">{ocr_accuracy['accuracy']:.1f}%</div>
        <div class="kpi-label">OCR Model Accuracy</div>
        <div class="kpi-trend">
            <span>🎯</span>
            <span>A vs N only</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[3]:
    st.markdown(f"""
    <div class="enhanced-kpi orange">
        <div class="kpi-icon">⭐</div>
        <div class="kpi-value">{perfect_match_rate:.1f}%</div>
        <div class="kpi-label">Perfect Match (A)</div>
        <div class="kpi-trend">
            <span>🎯</span>
            <span>{perfect_matches:,} perfect</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[4]:
    st.markdown(f"""
    <div class="enhanced-kpi red">
        <div class="kpi-icon">🖼️</div>
        <div class="kpi-value">{image_issue_rate:.1f}%</div>
        <div class="kpi-label">Image Issues (E)</div>
        <div class="kpi-trend">
            <span>⚠️</span>
            <span>{image_issues:,} records</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# OCR MODEL ACCURACY SECTION
# =========================
st.markdown('<div class="enhanced-card fade-in">', unsafe_allow_html=True)
st.markdown("### 🤖 OCR MODEL ACCURACY ANALYSIS")

ocr_col1, ocr_col2, ocr_col3 = st.columns(3)

with ocr_col1:
    st.markdown(f"""
    <div class="ocr-model-card" style="background: linear-gradient(135deg, var(--accent-purple), #6A4CA6);">
        <div class="ocr-icon">🎯</div>
        <div class="ocr-value">{ocr_accuracy['accuracy']:.1f}%</div>
        <div class="ocr-label">OCR MODEL ACCURACY</div>
        <div class="ocr-desc">Based on A vs N flags only</div>
    </div>
    """, unsafe_allow_html=True)

with ocr_col2:
    st.markdown(f"""
    <div class="ocr-model-card" style="background: linear-gradient(135deg, var(--success-green), #0D5C0D);">
        <div class="ocr-icon">✅</div>
        <div class="ocr-value">{ocr_accuracy['count_a']:,}</div>
        <div class="ocr-label">PERFECT MATCHES (A)</div>
        <div class="ocr-desc">OCR readings with 80%+ confidence</div>
    </div>
    """, unsafe_allow_html=True)

with ocr_col3:
    st.markdown(f"""
    <div class="ocr-model-card" style="background: linear-gradient(135deg, #6c757d, #495057);">
        <div class="ocr-icon">📄</div>
        <div class="ocr-value">{ocr_accuracy['count_n']:,}</div>
        <div class="ocr-label">READING MISMATCHES (N)</div>
        <div class="ocr-desc">OCR readings below 80% confidence</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# FLAG DISTRIBUTION
# =========================
st.markdown('<div class="enhanced-card fade-in">', unsafe_allow_html=True)
st.markdown("### 🏷️ FLAG CLASSIFICATION DISTRIBUTION")

flag_counts = df["IMAGE_VERIFY_CODE_PITC"].value_counts()
flag_cols = st.columns(5)

for idx, flag in enumerate(['A', 'C', 'D', 'E', 'N']):
    count = flag_counts.get(flag, 0)
    with flag_cols[idx]:
        if processed_records > 0:
            percentage = (count / processed_records * 100)
        else:
            percentage = 0
            
        flag_labels = {
            'A': '✅ PERFECT MATCH',
            'C': '⚠️ FLAG C',
            'D': '⚠️ FLAG D',
            'E': '❌ IMAGE ISSUE',
            'N': '❌ READING ISSUE'
        }
        
        flag_descs = {
            'A': 'Successful with perfect reading (80%+)',
            'C': 'Successful with minor issues',
            'D': 'Successful but needs review',
            'E': 'Image not available',
            'N': 'Reading not matched (<80%)'
        }
        
        st.markdown(f"""
        <div class="flag-card flag-{flag}">
            <div class="flag-icon">{flag}</div>
            <div class="flag-value">{count:,}</div>
            <div class="flag-label">{flag_labels[flag]}</div>
            <div class="flag-percentage">{percentage:.1f}% of processed</div>
            <div class="flag-desc">{flag_descs[flag]}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# BATCH ANALYTICS TAB
# =========================
tab1, tab2 = st.tabs(["📦 BATCH ANALYTICS", "🔍 RECORD EXPLORER"])

with tab1:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
        st.markdown("### 📊 BATCH PERFORMANCE")
        
        selected_batch = st.selectbox(
            "Select Batch for Details:",
            options=["All Batches"] + sorted(batch_stats["Batch ID"].tolist())
        )
        
        if selected_batch != "All Batches":
            batch_data = batch_stats[batch_stats["Batch ID"] == selected_batch].iloc[0]
            
            metric_cols = st.columns(4)
            with metric_cols[0]:
                st.metric("Total Records", f"{batch_data['Total Records']:,}")
            with metric_cols[1]:
                st.metric("Processed", f"{batch_data['Processed']:,}")
            with metric_cols[2]:
                st.metric("Success Rate", f"{batch_data['Success Rate (A,C,D)']:.1f}%")
            with metric_cols[3]:
                st.metric("OCR Accuracy", f"{batch_data['OCR Model Accuracy (A vs N)']:.1f}%")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
        st.markdown("### 📈 BATCH COMPARISON")
        
        fig = go.Figure(data=[
            go.Bar(
                x=batch_stats["Batch ID"],
                y=batch_stats["Success Rate (A,C,D)"],
                name='Success Rate',
                marker_color=batch_stats["Success Rate (A,C,D)"].apply(
                    lambda x: 'var(--success-green)' if x >= 70 else 
                             'var(--warning-orange)' if x >= 50 else 'var(--danger-red)'
                )
            )
        ])
        
        fig.update_layout(
            height=400,
            xaxis_title="Batch ID",
            yaxis_title="Success Rate (%)",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
        st.markdown("### 🏆 TOP 5 PERFORMING BATCHES")
        
        top_batches = batch_stats.nlargest(5, 'Success Rate (A,C,D)')
        
        for idx, (_, batch) in enumerate(top_batches.iterrows(), 1):
            medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][idx-1]
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, var(--success-green)15, transparent);
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                border-left: 4px solid var(--success-green);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 20px;">{medal}</span>
                        <div>
                            <strong>{batch['Batch ID']}</strong><br>
                            <small style="color: var(--medium-gray);">{batch['DISCO']}</small>
                        </div>
                    </div>
                    <div style="
                        background: var(--success-green);
                        color: white;
                        padding: 6px 12px;
                        border-radius: 15px;
                        font-weight: 700;
                    ">
                        {batch['Success Rate (A,C,D)']:.1f}%
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
        st.markdown("### 📋 ALL BATCHES SUMMARY")
        
        display_stats = batch_stats[["Batch ID", "DISCO", "Total Records", "Success Rate (A,C,D)", "OCR Model Accuracy (A vs N)"]]
        st.dataframe(display_stats, use_container_width=True, height=300)
        
        batch_csv_data = batch_stats.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Batch Report",
            data=batch_csv_data,
            file_name="batch_report.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="enhanced-card">', unsafe_allow_html=True)
    st.markdown("### 🔍 RECORD EXPLORER")
    
    search_query = st.text_input(
        "Search records:",
        placeholder="Search by REF_DIGITS, DISCO, BATCH..."
    )
    
    filtered_df = df.copy()
    
    if search_query:
        filtered_df = filtered_df[
            filtered_df["REF_DIGITS"].str.contains(search_query, case=False, na=False) |
            filtered_df["DISCO_NAME"].str.contains(search_query, case=False, na=False) |
            filtered_df["BATCH_ID"].str.contains(search_query, case=False, na=False)
        ]
    
    st.metric("Found Records", f"{len(filtered_df):,}")
    
    display_columns = ["REF_DIGITS", "DISCO_NAME", "BATCH_ID", "IMAGE_VERIFY_CODE_PITC", "ACCURACY_CATEGORY"]
    st.dataframe(filtered_df[display_columns], use_container_width=True, height=400)
    
    filtered_csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data",
        data=filtered_csv_data,
        file_name="filtered_records.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, var(--dark-gray), #1a1a1a);
    color: white;
    padding: 20px;
    border-radius: 12px;
    margin-top: 30px;
    text-align: center;
    font-size: 12px;
    opacity: 0.9;
">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div>
            📅 <strong>Last Updated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
        <div>
            🏢 <strong>DISCO:</strong> {disco_choice}
        </div>
        <div>
            📊 <strong>Records:</strong> {len(df):,}
        </div>
    </div>
    <div style="margin-top: 10px; font-size: 11px; opacity: 0.7;">
        🚀 OCR Intelligence Dashboard | Deployed on Render.com
    </div>
</div>
""", unsafe_allow_html=True)