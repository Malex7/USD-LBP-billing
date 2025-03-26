import streamlit as st
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(page_title="USD/LBP Calculator", page_icon="💵", layout="centered")

# --- Calculation logic ---
def calculate_split_change(bill_usd, paid_usd, paid_lbp, exchange_rate):
    paid_lbp_usd = paid_lbp / exchange_rate
    total_paid_usd = paid_usd + paid_lbp_usd
    difference_usd = round(total_paid_usd - bill_usd, 2)

    if difference_usd < 0:
        owed_usd = abs(difference_usd)
        usd_owed = int(owed_usd)
        lbp_owed = round((owed_usd - usd_owed) * exchange_rate)
        result = f"❌ Customer still owes:\n\n- **{usd_owed} USD** and **{lbp_owed:,} LBP**  \n**OR {round(owed_usd * exchange_rate):,} LBP**"
        return result, owed_usd
    elif difference_usd > 0:
        usd_return = int(difference_usd)
        lbp_return = round((difference_usd - usd_return) * exchange_rate)
        result = f"✅ Change to return:\n\n- **{usd_return} USD** and **{lbp_return:,} LBP**  \n**OR {round(difference_usd * exchange_rate):,} LBP**"
        return result, -difference_usd
    else:
        result = "✅ **Payment is exact. No change owed.**"
        return result, 0.0

# --- UI Layout ---
st.markdown("""
    <h1 style='text-align: center;'>💵 USD/LBP Payment Calculator</h1>
""", unsafe_allow_html=True)

with stylable_container("exchange_box", css="padding: 1rem; background-color: #f9f9f9; border-radius: 1rem; margin-bottom: 1rem;"):
    exchange_rate = st.number_input("💱 Exchange rate (LBP per 1 USD)", value=89000, step=1000)

with stylable_container("bill_info", css="padding: 1rem; background-color: #f0f4ff; border-radius: 1rem; margin-bottom: 1rem;"):
    currency = st.selectbox("🧾 Currency of the bill", ["USD", "LBP"])
    bill_amount = st.number_input("Total bill amount", value=0.0, min_value=0.0, step=0.01)

with stylable_container("payment_info", css="padding: 1rem; background-color: #fff0f0; border-radius: 1rem; margin-bottom: 1rem;"):
    paid_usd = st.number_input("💵 Paid in USD", value=0.0, min_value=0.0, step=0.01)
    paid_lbp = st.number_input("🇱🇧 Paid in LBP", value=0.0, min_value=0.0, step=1000.0)
    split_people = st.number_input("👥 Split between how many people?", min_value=0, value=0, step=1)

# --- Conversion logic ---
bill_usd = bill_amount if currency == "USD" else bill_amount / exchange_rate

if st.button("🧮 Calculate"):
    result, remaining_usd = calculate_split_change(bill_usd, paid_usd, paid_lbp, exchange_rate)

    with stylable_container("result_box", css="padding: 1rem; background-color: #eafbe7; border-radius: 1rem; margin-top: 1rem;"):
        st.markdown(f"### 💡 Result:\n{result}")

    if split_people > 0 and remaining_usd != 0:
        per_person_usd = abs(remaining_usd) / split_people
        per_usd = int(per_person_usd)
        per_lbp = round((per_person_usd - per_usd) * exchange_rate)
        full_lbp = round(per_person_usd * exchange_rate)

        with stylable_container("split_result", css="padding: 1rem; background-color: #fef7e0; border-radius: 1rem; margin-top: 1rem;"):
            st.markdown("### 👥 Per Person:")
            st.markdown(f"- **{per_usd} USD** and **{per_lbp:,} LBP**  \n**OR {full_lbp:,} LBP**")
