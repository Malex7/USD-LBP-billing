import streamlit as st
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(page_title="USD/LBP Calculator", page_icon="💵", layout="wide")

# --- Language toggle ---
lang = st.selectbox("🌐 Language / Langue / اللغة", ["English", "Français", "العربية"])

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
        "Français": "Taux de change (LBP pour 1 USD)",
        "العربية": "سعر الصرف (ل ل مقابل 1 دولار)"
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
        "Français": "Payé en LBP",
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
    "share": {
        "English": "Share of bill",
        "Français": "Part de la facture",
        "العربية": "النسبة من الفاتورة"
    },
    "equivalent": {
        "English": "Total LBP equivalent",
        "Français": "Équivalent total en LBP",
        "العربية": "المعادل الإجمالي بالليرة"
    }
}

# Now this dictionary can be used in the rest of your interface like:
# st.number_input(TEXT["exchange_rate"][lang], ...)
# This replaces all static text with language-aware labels.

# When rendering per-person info, use:
# st.markdown(f"- 💵 {TEXT['equivalent'][lang]}: ...")
# st.markdown(f"- 📊 {TEXT['share'][lang]}: ...")
# So LBP total appears before percentage as requested.

# ✅ You can now keep the Calculate button active even if bill = 0.
