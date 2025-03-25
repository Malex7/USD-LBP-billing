
import streamlit as st

def calculate_split_change(bill_usd, paid_usd, paid_lbp, exchange_rate):
    paid_lbp_usd = paid_lbp / exchange_rate
    total_paid_usd = paid_usd + paid_lbp_usd
    difference_usd = round(total_paid_usd - bill_usd, 2)

    if difference_usd < 0:
        owed_usd = abs(difference_usd)
        usd_owed = int(owed_usd)
        lbp_owed = round((owed_usd - usd_owed) * exchange_rate)

        result = "❌ Customer still owes:\n"
        if usd_owed > 0:
            result += f"- {usd_owed} USD\n"
        if lbp_owed > 0:
            result += f"- {lbp_owed:,} LBP"
        return result

    elif difference_usd > 0:
        usd_return = int(difference_usd)
        lbp_return = round((difference_usd - usd_return) * exchange_rate)

        result = "✅ Change to return:\n"
        if usd_return > 0:
            result += f"- {usd_return} USD\n"
        if lbp_return > 0:
            result += f"- {lbp_return:,} LBP"
        return result

    else:
        return "✅ Payment is exact. No change owed."

# Streamlit UI
st.title("💵 USD/LBP Mixed Payment POS Calculator")

exchange_rate = st.number_input("Exchange rate (LBP per 1 USD)", value=89000)
currency = st.selectbox("Currency of the bill", ["USD", "LBP"])
bill_amount = st.number_input("Total bill amount", value=0.0, min_value=0.0)
paid_usd = st.number_input("Paid in USD", value=0.0, min_value=0.0)
paid_lbp = st.number_input("Paid in LBP", value=0.0, min_value=0.0)

if currency == "USD":
    bill_usd = bill_amount
else:
    bill_usd = bill_amount / exchange_rate

if st.button("Calculate"):
    result = calculate_split_change(bill_usd, paid_usd, paid_lbp, exchange_rate)
    st.markdown(f"### Result:\n{result}")
