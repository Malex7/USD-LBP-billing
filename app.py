if st.button("Calculate"):
    result, usd_owed, lbp_owed = calculate_split_change(bill_usd, paid_usd, paid_lbp, exchange_rate)
    st.markdown("### Result:")

    if usd_owed == 0 and lbp_owed == 0:
        st.markdown(result)
    else:
        usd_to_lbp = usd_owed * exchange_rate
        total_lbp = int(usd_to_lbp + lbp_owed)

        line_parts = []
        if usd_owed > 0:
            line_parts.append(f"**{usd_owed} USD**")
        if lbp_owed > 0:
            line_parts.append(f"**{lbp_owed:,} LBP**")
        
        owed_line = " and ".join(line_parts)
        st.markdown(f"- {owed_line}  **OR {total_lbp:,} LBP**")

    # Per person section
    if split_between > 1 and (usd_owed != 0 or lbp_owed != 0):
        st.markdown("### Per Person:")

        total_owed_usd = abs(usd_owed)
        total_owed_lbp = abs(lbp_owed)
        per_person_usd_float = total_owed_usd / split_between
        usd_part = int(per_person_usd_float)
        lbp_part = round((per_person_usd_float - usd_part) * exchange_rate + (total_owed_lbp / split_between))
        per_person_lbp_total = round((total_owed_usd * exchange_rate + total_owed_lbp) / split_between)

        pp_parts = []
        if usd_part > 0:
            pp_parts.append(f"**{usd_part} USD**")
        if lbp_part > 0:
            pp_parts.append(f"**{lbp_part:,} LBP**")

        st.markdown(f"- {' and '.join(pp_parts)}  **OR {per_person_lbp_total:,} LBP**")

