import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Unga Staff List (Exactly 43 members)
staff_list = [
    "SUTHAKAR", "VASANTH", "KANAGARAJ", "SURYA PRAKASH", "JEBASTIN", 
    "RAJA ALIAS PRADEEP KUMAR", "SUBASH", "DEEPA SELVIN", "KAVITHA", 
    "KUMAR.T", "MUGESH", "KARUVELAN", "SATHYA JOTHY", "MANIKANDA PRABHU", 
    "GANESAN", "MUTHURAJ", "V.SARAVANAN", "MUTHU MAHA PRABHU", "NAVEEN", 
    "MUTHU GANESH", "CHITTIBABU", "HARISH KUMAR", "BAVITH", "SAKTHI", 
    "MUTHUVADIVU", "MAHESH", "IMMANUVEL", "SUBHASHINI", "THINAGARAJ", 
    "MARIDURAI", "RAJA", "JOHN GUNASEELAN", "PACKIYA SELVAN", "VALLIRAJ", 
    "PARAMASIVAM", "PARTHIBAN RAJ", "VINOTH", "USHARAJA", "GUNAM", 
    "SAKTHI MANO", "SORIMUTHU", "MERLIN NIRMALA", "ESAKKIRAJA"
]

# Note: List-la 43 per irukaanga. Neenga kudutha 'JAY BABU', 'PETCHIYAMMAL' etc. 
# extra names irundhalum, rotation 43 vechu handle aagum.

points = [f"Duty Point {i}" for i in range(1, 14)]

st.set_page_config(page_title="Office Duty Rota", layout="wide")
st.title("🛡️ Daily Duty Rotation System")

# 2. Date Selection (Inniku date automatic-aa select aagum)
selected_date = st.date_input("Thethi-yai thervu seiyavum", datetime.now())

# Fixed starting point (Base date: Jan 1, 2024)
base_date = datetime(2024, 1, 1).date()
day_offset = (selected_date - base_date).days

# 3. Fair Rotation Logic
# Ovvoru naalum list 1 position rotate aagum. 
# Adhunala Point 1-la irukuravar nalaiku Point 2-ku povaaru.
n = len(staff_list)
shift_start = day_offset % n
rotated_staff = staff_list[shift_start:] + staff_list[:shift_start]

# 4. Shift Assignments
s1 = rotated_staff[0:13]
s2 = rotated_staff[13:26]
s3 = rotated_staff[26:39]
off = rotated_staff[39:43]

# 5. Display
col1, col2, col3 = st.columns(3)

with col1:
    st.header("🕒 Shift 1")
    st.table(pd.DataFrame({"Point": points, "Staff": s1}))

with col2:
    st.header("🕒 Shift 2")
    st.table(pd.DataFrame({"Point": points, "Staff": s2}))

with col3:
    st.header("🕒 Shift 3")
    st.table(pd.DataFrame({"Point": points, "Staff": s3}))

st.divider()
st.info(f"🏖️ **Today Off Duty:** {', '.join(off)}")
