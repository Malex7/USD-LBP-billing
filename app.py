import streamlit as st

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

# Streamlit UI
st.title("💵 USD/LBP Payment Calculator")

exchange_rate = st.number_input("Exchange rate (LBP per 1 USD)", value=89000)
currency = st.selectbox("Currency of the bill", ["USD", "LBP"])
bill_amount = st.number_input("Total bill amount", value=0.0, min_value=0.0)
paid_usd = st.number_input("Paid in USD", value=0.0, min_value=0.0)
paid_lbp = st.number_input("Paid in LBP", value=0.0, min_value=0.0)
split_people = st.number_input("Split between how many people?", min_value=0, value=0, step=1)

if currency == "USD":
    bill_usd = bill_amount
else:
    bill_usd = bill_amount / exchange_rate

if st.button("Calculate"):
    result, remaining_usd = calculate_split_change(bill_usd, paid_usd, paid_lbp, exchange_rate)
    st.markdown(f"### Result:\n{result}")

    if split_people > 0 and remaining_usd != 0:
        per_person_usd = abs(remaining_usd) / split_people
        per_usd = int(per_person_usd)
        per_lbp = round((per_person_usd - per_usd) * exchange_rate)
        full_lbp = round(per_person_usd * exchange_rate)

        st.markdown("### Per Person:")
        st.markdown(f"- **{per_usd} USD** and **{per_lbp:,} LBP**  \n**OR {full_lbp:,} LBP**")
