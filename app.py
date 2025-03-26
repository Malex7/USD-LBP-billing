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
        return result, usd_owed, lbp_owed

    elif difference_usd > 0:
        usd_return = int(difference_usd)
        lbp_return = round((difference_usd - usd_return) * exchange_rate)

        result = "✅ Change to return:\n"
        if usd_return > 0:
            result += f"- {usd_return} USD\n"
        if lbp_return > 0:
            result += f"- {lbp_return:,} LBP"
        return result, -usd_return, -lbp_return

    else:
        return "✅ Payment is exact. No change owed.", 0, 0

# Streamlit UI
st.title("💵 USD/LBP Payment Calculator")

exchange_rate = st.number_input("Exchange rate (LBP per 1 USD)", value=89000)
currency = st.selectbox("Currency of the bill", ["USD", "LBP"])
bill_amount = st.number_input("Total bill amount", value=0.0, min_value=0.0)
paid_usd = st.number_input("Paid in USD", value=0.0, min_value=0.0)
paid_lbp = st.number_input("Paid in LBP", value=0.0, min_value=0.0)
split_between = st.number_input("Split between how many people? (0 = no split)", min_value=0, value=0)

if currency == "USD":
    bill_usd = bill_amount
else:
    bill_usd = bill_amount / exchange_rate

if st.button("Calculate"):
    result, usd_owed, lbp_owed = calculate_split_change(bill_usd, paid_usd, paid_lbp, exchange_rate)
    st.markdown(f"### Result:\n{result}")

    # Optional OR full amount in LBP
    if usd_owed > 0 or lbp_owed > 0:
        usd_to_lbp = usd_owed * exchange_rate
        total_lbp = int(usd_to_lbp + lbp_owed)
        st.markdown("### OR")
        st.markdown(f"💰 **Pay full: {total_lbp:,} LBP**")

    # Per person split breakdown
    if split_between > 1 and (usd_owed != 0 or lbp_owed != 0):
        total_owed_usd = abs(usd_owed)
        total_owed_lbp = abs(lbp_owed)
        per_person_usd_float = total_owed_usd / split_between

        # Convert each person's share to USD + LBP
        usd_part = int(per_person_usd_float)
        lbp_part = round((per_person_usd_float - usd_part) * exchange_rate + (total_owed_lbp / split_between))

        st.markdown("### Per Person:")
        if usd_part > 0 or lbp_part > 0:
            per_person_str = []
            if usd_part > 0:
                per_person_str.append(f"{usd_part} USD")
            if lbp_part > 0:
                per_person_str.append(f"{lbp_part:,} LBP")
            st.markdown("- " + " and ".join(per_person_str))

