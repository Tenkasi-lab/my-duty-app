import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Google Sheet CSV Link (Neenga kudutha link-ah CSV format-la mathiruken)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQaLlOSwTCkuUJSOxwaE_BgrO1j1D7vexky926Ufcju5H9t1PthxYEs9BcxyCTcxInosGvvKS_C_rIb/pubcsv?gid=1316908717"

st.set_page_config(page_title="Tenkasi Lab Smart Rota", layout="wide")
st.title("⚙️ Automated Duty Rotation System")

# 2. Date Selection
selected_date = st.date_input("Thethi-yai thervu seiyavum", datetime.now())
day_str = str(selected_date.day) # Sheet-la top row-la irukura date (3, 4, 5...)

try:
    # Google Sheet-ai read pannuvom
    df = pd.read_csv(SHEET_URL)
    
    # Column names-ah clean pannuvom (leading/trailing spaces remove panna)
    df.columns = df.columns.str.strip()
    
    # 3. Shift Selection
    selected_shift = st.selectbox("Shift-ai thervu seiyavum", ["A", "B", "C"])
    
    # Andha date column-la selected shift-la yaaru irukaanganu filter pannuvom
    if day_str in df.columns:
        present_staff = df[df[day_str] == selected_shift]['NAME'].tolist()
        
        if len(present_staff) > 0:
            st.subheader(f"📅 Date: {selected_date} | 🕒 Shift: {selected_shift}")
            
            # 4. Rotation Logic (Day offset vechu rotate pannuvom)
            points = [f"Duty Point {i}" for i in range(1, 14)]
            
            # Staff list-ah date-ai vechu rotate pannalam (Fairness-kaga)
            base_date = datetime(2024, 1, 1).date()
            offset = (selected_date - base_date).days
            
            # Staff sequence rotation
            n = len(present_staff)
            start_idx = offset % n
            rotated_staff = present_staff[start_idx:] + present_staff[:start_idx]
            
            # Display Result
            # 13 points-ku mela staff irundha list-ah cut pannuvom
            display_list = rotated_staff[:13]
            
            res_df = pd.DataFrame({
                "Point": points[:len(display_list)],
                "Staff Name": display_list
            })
            
            st.table(res_df)
            
            if len(rotated_staff) > 13:
                st.warning(f"Extra Staff (Reliever/Off): {', '.join(rotated_staff[13:])}")
        else:
            st.error(f"Inniku {selected_shift} shift-la yaarum illai!")
    else:
        st.error(f"Sheet-la '{day_str}' nu thethi column illai. Check pannunga.")

except Exception as e:
    st.error(f"Error: Sheet-ai read panna mudiyala. {e}")
