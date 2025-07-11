import streamlit as st
import pandas as pd

# --- Page config ---
st.set_page_config(
    page_title="Property Investment Insights",
    page_icon="🏠",
    layout="wide"
)

# --- Load pre-calculated data for sector list only ---
@st.cache_data
def load_data():
    return pd.read_csv("datasets/roi_analysis_file2.csv")

df = load_data()

# --- Market Defaults for Gurgaon ---
def get_market_defaults(sector, price):
    if sector in ['Sector 23', 'Sector 47', 'Sector 56', 'Sector 62']:
        yield_pct = 5.0
    elif 'Golf Course' in sector or price > 2.0:
        yield_pct = 4.0
    else:
        yield_pct = 4.5
    down_payment_pct = 20
    return yield_pct, down_payment_pct

# --- EMI Calculation ---
def calculate_emi(principal, rate, years):
    r = rate / 12
    n = years * 12
    emi = (principal * r * (1 + r)**n) / ((1 + r)**n - 1)
    return emi

# --- Page Title ---
st.markdown("<h1 style='text-align: center; color: #30cfcf;'>Property Investment Insights</h1>", unsafe_allow_html=True)

# --- Input Form ---
with st.form("property_form"):
    st.markdown("### Enter Property Details")

    col1, col2 = st.columns(2)
    with col1:
        sector = st.selectbox("Select Sector", sorted(df['sector'].unique()))
        built_up_area = st.number_input("Built-up Area (sq ft)", min_value=200, max_value=10000, value=1000, step=10)
    with col2:
        price = st.number_input("Price/budget (in Cr)", min_value=0.1, max_value=10.0, value=1.2, step=0.01)
        bhk = st.selectbox("Number of BHK (Bedrooms)", sorted(df['bedRoom'].dropna().unique()))

    submitted = st.form_submit_button("Show Insights")

# --- Constants ---
loan_interest = 8.5 / 100
loan_term_years = 20
insurance = 8000
misc_expenses = 7000

# --- Logic ---
if submitted:
    # Filter dataset to match user's sector and BHK (optional, if you want to show sample data)
    matched_data = df[(df['sector'] == sector) & (df['bedRoom'] == bhk)]  # Use 'bhk' NOT 'col2'[1]
    if matched_data.empty:
        st.error("No matching properties found in the dataset for this Sector and BHK. Showing insights based on your inputs.")
    else:
        # You can optionally use matched_data for something, but calculations are based on user input
        pass

    yield_pct, down_payment_pct = get_market_defaults(sector, price)
    price_rupees = price * 1e7
    estimated_annual_rent = price_rupees * (yield_pct / 100)
    maintenance = built_up_area * 4 * 12
    property_tax = price_rupees * 0.0025
    loan_amount = price_rupees * (1 - down_payment_pct / 100)
    emi = calculate_emi(loan_amount, loan_interest, loan_term_years)
    annual_emi = emi * 12
    total_expenses = maintenance + property_tax + insurance + misc_expenses
    annual_cash_flow = estimated_annual_rent - annual_emi - total_expenses
    total_investment = price_rupees * (down_payment_pct / 100) + total_expenses
    roi = (annual_cash_flow / total_investment) * 100

    # --- UI Metrics ---
    st.markdown("<h2 style='color: #30cfcf;'>Summary</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Sector", sector)
    with col2:
        st.metric("Price (₹)", f"{price_rupees:,.0f}")
    with col3:
        st.metric("Area (sq ft)", f"{built_up_area:,}")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Estimated Rent (₹/yr)", f"{estimated_annual_rent:,.0f}")
    with col5:
        st.metric("Annual Cash Flow", f"₹{annual_cash_flow:,.0f}", delta_color="inverse" if annual_cash_flow < 0 else "normal")
    with col6:
        st.metric("ROI (%)", f"{roi:.2f}%", delta_color="inverse" if roi < 0 else "normal")

    # --- Assumptions ---
    st.markdown("### Market Assumptions")
    st.markdown(f"""
- **Rental Yield**: {yield_pct:.1f}%
- **Down Payment**: {down_payment_pct}%
- **Loan Interest**: 8.5%, Tenure: 20 years
- **Maintenance**: ₹{maintenance:,.0f} / year
- **Property Tax**: ₹{property_tax:,.0f} / year
""")

    # --- Insights ---
    st.markdown("<h2 style='color: #30cfcf;'>Investment Analysis</h2>", unsafe_allow_html=True)
    monthly_rent = estimated_annual_rent / 12
    if annual_cash_flow < 0:
        st.error(f"""
**Summary:**  
This property gives good rent — ₹{monthly_rent:,.0f}/month — but due to EMI, maintenance, and taxes, you'll lose around ₹{abs(annual_cash_flow):,.0f} per year in the first few years.
""")
    else:
        st.success(f"""
**Summary:**  
Cash flow positive! Annual income: ₹{annual_cash_flow:,.0f}  
This property gives you a rental income of ₹{monthly_rent:,.0f}/month with a cash surplus of ₹{annual_cash_flow:,.0f} per year — a good long-term hold opportunity.
""")
