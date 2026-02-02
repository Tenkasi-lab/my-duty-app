import streamlit as st
import pandas as pd
from datetime import datetime

# Corrected Google Sheet CSV Link
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQaLlOSwTCkuUJSOxwaE_BgrO1j1D7vexky926Ufcju5H9t1PthxYEs9BcxyCTcxInosGvvKS_C_rIb/pub?gid=1316908717&output=csv"

st.set_page_config(page_title="Tenkasi Lab Smart Rota", layout="wide")
st.title("🛡️ Automated Duty Rotation System")

# Date Selection
selected_date = st.date_input("Thethi-yai thervu seiyavum", datetime.now())
day_str = str(selected_date.day) 

try:
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.astype(str).str.strip()
    
    selected_shift = st.selectbox("Shift-ai thervu seiyavum", ["A", "B", "C"])
    
    if day_str in df.columns:
        present_staff = df[df[day_str] == selected_shift]['NAME'].dropna().tolist()
        
        if len(present_staff) > 0:
            st.success(f"📅 Date: {selected_date} | 🕒 Shift: {selected_shift} | 👥 Total: {len(present_staff)}")
            points = [f"Duty Point {i}" for i in range(1, 14)]
            
            # Rotation Logic
            base_date = datetime(2024, 1, 1).date()
            offset = (selected_date - base_date).days
            n = len(present_staff)
            start_idx = offset % n
            rotated_staff = present_staff[start_idx:] + present_staff[:start_idx]
            
            display_count = min(len(rotated_staff), 13)
            res_df = pd.DataFrame({
                "Duty Point": points[:display_count],
                "Staff Name": rotated_staff[:display_count]
            })
            st.table(res_df)
            
            if len(rotated_staff) > 13:
                st.info(f"🏖️ **Extra Staff:** {', '.join(rotated_staff[13:])}")
        else:
            st.warning(f"⚠️ Inniku {day_str}-am thethi '{selected_shift}' shift-la yaarum illai.")
    else:
        st.error(f"❌ Unga sheet-la '{day_str}' nu column header illai. Feb 3-ku mela date select pannunga.")

except Exception as e:
    st.error(f"⚠️ Connection Error: {e}")
