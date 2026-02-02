import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Corrected Google Sheet CSV Link
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQaLlOSwTCkuUJSOxwaE_BgrO1j1D7vexky926Ufcju5H9t1PthxYEs9BcxyCTcxInosGvvKS_C_rIb/pub?gid=1316908717&output=csv"

st.set_page_config(page_title="Tenkasi Lab Smart Rota", layout="wide")
st.title("🛡️ Automated Duty Rotation System")

# 2. Date Selection
selected_date = st.date_input("Thethi-yai thervu seiyavum", datetime.now())
# Sheet-la top row-la numbers (3, 4, 5...) dhaan date-ah irukku
day_str = str(selected_date.day) 

try:
    # Google Sheet data-vai read pannuvom
    df = pd.read_csv(SHEET_URL)
    
    # Headers-la irukira extra spaces-ah remove pannuvom
    df.columns = df.columns.astype(str).str.strip()
    
    # Shift Selection
    selected_shift = st.selectbox("Shift-ai thervu seiyavum", ["A", "B", "C"])
    
    # Selected date column sheet-la irukkanu check pannuvom
    if day_str in df.columns:
        # 'NAME' column-la irundhu selected shift staff-ah edukkum
        # Sheet-la unga column header 'NAME' nu irukanum
        present_staff = df[df[day_str] == selected_shift]['NAME'].dropna().tolist()
        
        if len(present_staff) > 0:
            st.success(f"📅 Date: {selected_date} | 🕒 Shift: {selected_shift} | 👥 Total: {len(present_staff)}")
            
            # Rotation Logic (Day offset to ensure fairness)
            points = [f"Duty Point {i}" for i in range(1, 14)]
            base_date = datetime(2024, 1, 1).date()
            offset = (selected_date - base_date).days
            
            n = len(present_staff)
            start_idx = offset % n
            rotated_staff = present_staff[start_idx:] + present_staff[:start_idx]
            
            # Table display
            display_count = min(len(rotated_staff), 13)
            res_df = pd.DataFrame({
                "Duty Point": points[:display_count],
                "Staff Name": rotated_staff[:display_count]
            })
            
            st.table(res_df)
            
            # Extra staff details
            if len(rotated_staff) > 13:
                st.info(f"🏖️ **Extra/Reliever Today:** {', '.join(rotated_staff[13:])}")
        else:
            st.warning(f"⚠️ Inniku {day_str}-am thethi {selected_shift} shift-la yaarum illai.")
    else:
        st.error(f"❌ Sheet-la '{day_str}' nu thethi column illai. Sheet-ah check pannunga.")

except Exception as e:
    st.error(f"⚠️ Error: Sheet-ai read panna mudiyala. Reason: {e}")
    st.info("Check: Google Sheet-la Column header 'NAME' nu irukannu paarunga.")
