import streamlit as st
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(page_title="USD/LBP Calculator", page_icon="💵", layout="wide")

# --- Language toggle ---
with st.container():
    col1, col2 = st.columns([8, 1])
    with col2:
        lang = st.selectbox("", ["English", "Français", "العربية"], index=0, label_visibility="collapsed", key="language_select")

# --- Arabic RTL support ---
if lang == "العربية":
    st.markdown("""<style>body { direction: rtl; text-align: right; }</style>""", unsafe_allow_html=True)

# --- Multi-language dictionary ---
TEXT = {
    "title": {
        "English": "USD/LBP Payment Calculator",
        "Français": "Calculateur de paiement USD/LBP",
        "العربية": "حاسبة الدفع بالدولار/الليرة"
    },
    "exchange_rate": {
        "English": "Exchange rate (LBP per 1 USD)",
        "Français": "Taux de change (LL pour 1 USD)",
        "العربية": "سعر الصرف (ل.ل مقابل 1 دولار)"
    },
    "currency_of_bill": {
        "English": "Currency of the bill",
        "Français": "Devise de la facture",
        "العربية": "عملة الفاتورة"
    },
    "total_bill": {
        "English": "Total bill amount",
        "Français": "Montant total de la facture",
        "العربية": "المبلغ الإجمالي للفاتورة"
    },
    "paid_usd": {
        "English": "Paid in USD",
        "Français": "Payé en USD",
        "العربية": "مدفوع بالدولار"
    },
    "paid_lbp": {
        "English": "Paid in LBP",
        "Français": "Payé en LL",
        "العربية": "مدفوع بالليرة"
    },
    "split_people": {
        "English": "Split between how many people?",
        "Français": "Diviser entre combien de personnes ?",
        "العربية": "تقسيم بين كم شخصًا؟"
    },
    "calculate": {
        "English": "Calculate",
        "Français": "Calculer",
        "العربية": "احسب"
    },
    "result": {
        "English": "Result",
        "Français": "Résultat",
        "العربية": "النتيجة"
    },
    "per_person": {
        "English": "Per Person Breakdown",
        "Français": "Détail par personne",
        "العربية": "حصة كل شخص"
    },
    "owes": {
        "English": "Owes",
        "Français": "Doit",
        "العربية": "ما يجب دفعه"
    },
    "change_return": {
        "English": "Change to return",
        "Français": "Monnaie à rendre",
        "العربية": "المبلغ المعاد"
    },
    "payment_exact": {
        "English": "Payment is exact. No change owed.",
        "Français": "Paiement exact. Pas de monnaie à rendre.",
        "العربية": "الدفع مطابق. لا يوجد مبلغ معاد."
    },
    "share": {
        "English": "Share of bill",
        "Français": "Part de la facture",
        "العربية": "النسبة من الفاتورة"
    },
    "equivalent": {
        "English": "Total LBP equivalent",
        "Français": "Équivalent total en LL",
        "العربية": "المعادل الإجمالي بالليرة"
    }
}

# --- Calculation logic ---
def calculate_split_change(bill_usd, paid_usd, paid_lbp, exchange_rate):
    paid_lbp_usd = paid_lbp / exchange_rate
    total_paid_usd = paid_usd + paid_lbp_usd
    difference_usd = round(total_paid_usd - bill_usd, 2)

    if difference_usd < 0:
        owed_usd = abs(difference_usd)
        usd_owed = int(owed_usd)
        lbp_owed = round((owed_usd - usd_owed) * exchange_rate)
        result = f"❌ {TEXT['owes'][lang]}:\n\n- **{usd_owed} USD** and **{lbp_owed:,} ل.ل**  \n**OR {round(owed_usd * exchange_rate):,} ل.ل**"
        return result, owed_usd
    elif difference_usd > 0:
        usd_return = int(difference_usd)
        lbp_return = round((difference_usd - usd_return) * exchange_rate)
        result = f"✅ {TEXT['change_return'][lang]}:\n\n- **{usd_return} USD** and **{lbp_return:,} ل.ل**  \n**OR {round(difference_usd * exchange_rate):,} ل.ل**"
        return result, -difference_usd
    else:
        result = f"✅ **{TEXT['payment_exact'][lang]}**"
        return result, 0.0

# --- UI Layout ---
st.markdown(f"""
    <h1 style='text-align: center;'>{TEXT['title'][lang]}</h1>
""", unsafe_allow_html=True)

with stylable_container(key="exchange_box", css="padding: 1rem; background-color: #f9f9f9; border-radius: 1rem; margin-bottom: 1rem;"):
    exchange_rate = st.number_input(TEXT["exchange_rate"][lang], value=89000, step=1000)

with stylable_container(key="currency_box", css="padding: 1rem; background-color: #f0f4ff; border-radius: 1rem; margin-bottom: 1rem;"):
    currency = st.selectbox(TEXT["currency_of_bill"][lang], ["USD", "LBP"])
    bill_amount = st.number_input(TEXT["total_bill"][lang], value=0.0, step=0.01)

with stylable_container(key="payment_box", css="padding: 1rem; background-color: #fff0f0; border-radius: 1rem; margin-bottom: 1rem;"):
    paid_usd = st.number_input(TEXT["paid_usd"][lang], value=0.0, step=0.01)
    paid_lbp = st.number_input(TEXT["paid_lbp"][lang], value=0.0, step=1000.0)
    split_people = st.number_input(TEXT["split_people"][lang], min_value=0, value=0, step=1)

bill_usd = bill_amount if currency == "USD" else bill_amount / exchange_rate

if st.button(TEXT["calculate"][lang]):
    result, remaining_usd = calculate_split_change(bill_usd, paid_usd, paid_lbp, exchange_rate)

    with stylable_container(key="result_box", css="padding: 1rem; background-color: #eafbe7; border-radius: 1rem; margin-top: 1rem;"):
        st.markdown(f"### 💡 {TEXT['result'][lang]}:\n{result}")

    if split_people > 0:
        per_person_usd = abs(remaining_usd) / split_people
        per_usd = int(per_person_usd)
        per_lbp = round((per_person_usd - per_usd) * exchange_rate)
        full_lbp = round(per_person_usd * exchange_rate)
        percentage = round((per_person_usd / bill_usd) * 100, 2) if bill_usd > 0 else 0

        with stylable_container(key="person_breakdown_box", css="padding: 1rem; background-color: #fef7e0; border-radius: 1rem; margin-top: 1rem;"):
            st.markdown(f"### 👥 {TEXT['per_person'][lang]}:")
            st.markdown(f"- 💵 **{per_usd} USD** and **{per_lbp:,} ل.ل**")
            st.markdown(f"- 📊 {TEXT['equivalent'][lang]}: **{full_lbp:,} ل.ل**")
            st.markdown(f"- 📊 {TEXT['share'][lang]}: **{percentage}%**")

