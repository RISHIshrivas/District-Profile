import streamlit as st
import pandas as pd
import os
import base64

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(page_title="जिला प्रोफाइल", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "DistrictMapping.xlsx")
IMAGE_DIR = os.path.join(BASE_DIR, "images")

# =================================================
# BACKGROUND IMAGE SETUP
# =================================================
def set_background(img_path):
    with open(img_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        table {{
            width:100%;
        }}
        th, td {{
            text-align:center !important;
            vertical-align:top;
            white-space:normal;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

bg = os.path.join(IMAGE_DIR, "BJP_BG.png")
if os.path.exists(bg):
    set_background(bg)

# =================================================
# LOAD EXCEL
# =================================================
sheet1 = pd.read_excel(EXCEL_PATH, sheet_name="District Mapping")
sheet2 = pd.read_excel(EXCEL_PATH, sheet_name="इन्‍फ्लुऐंशर लिस्‍ट MP")

# =================================================
# CLEAN DATA (CRITICAL)
# =================================================
def clean_df(df):
    df.columns = (
        df.columns.astype(str)
        .str.replace("\u00a0", " ", regex=False)
        .str.replace("\n", "", regex=False)
        .str.replace("\r", "", regex=False)
        .str.strip()
    )
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = (
                df[col].astype(str)
                .str.replace("\u00a0", " ", regex=False)
                .str.strip()
            )
    return df

sheet1 = clean_df(sheet1)
sheet2 = clean_df(sheet2)

def safe(val):
    if pd.isna(val):
        return "No Info"
    text = str(val).strip()
    if text.lower() in ["", "none", "---"]:
        return "No Info"
    return text


# =================================================
# SIDEBAR (NO IMAGE – FINAL)
# =================================================
st.sidebar.markdown(
    "<h3 style='text-align:center'>जिला चुनें</h3>",
    unsafe_allow_html=True
)

districts = sheet1["जिले का नाम"].dropna().unique()
selected_district = st.sidebar.selectbox("Choose District", districts)

# =================================================
# FILTER DATA (IMPORTANT FIX)
# =================================================
district_data = sheet1[
    sheet1["जिले का नाम"].str.strip() == selected_district.strip()
].iloc[0]

influencers = sheet2[
    sheet2["जिले का नाम"]
        .astype(str)
        .str.strip()
        .str.contains(selected_district.strip(), regex=False)
]

# =================================================
# IMAGE NAME MAP (FINAL)
# =================================================
IMAGE_MAP = {
    "भोपाल": "Bhopal",
    "सीहोर": "Sehore",
    "Bhopal": "Bhopal",
    "Sehore": "Sehore"
}

key = IMAGE_MAP.get(selected_district)

# =================================================
# MAIN BAR CONTENT (EXACT ORDER)
# =================================================

# ---------- HEADING ----------
st.markdown("<h1 style='text-align:center'>जिला प्रोफाइल</h1>", unsafe_allow_html=True)

# ---------- IMAGE 1 ----------
if key:
    img1 = os.path.join(IMAGE_DIR, f"{key}.png")
    if os.path.exists(img1):
        st.image(img1, use_container_width=True)

# ---------- DISTRICT NAME ----------
st.markdown(f"<h2 style='text-align:center'>{selected_district}</h2>", unsafe_allow_html=True)
st.markdown(
    f"<h4 style='text-align:center'>संभाग : {safe(district_data['संभाग'])}</h4>",
    unsafe_allow_html=True
)

# ---------- IMAGE 2 ----------
if key:
    img2 = os.path.join(IMAGE_DIR, f"{key}2.png")
    if os.path.exists(img2):
        st.image(img2, use_container_width=True)

# ---------- DESCRIPTION ----------
st.markdown("<h3 style='text-align:center'>जिले का विवरण</h3>", unsafe_allow_html=True)
st.markdown(
    f"<p style='text-align:center'>{safe(district_data['जिले का विवरण'])}</p>",
    unsafe_allow_html=True
)

# ---------- DARSHANIYA | TOURISM ----------
st.markdown("<h3 style='text-align:center'>दर्शनीय स्थल | पर्यटन स्थल</h3>", unsafe_allow_html=True)
t1 = pd.DataFrame({
    "दर्शनीय स्थल (मंदिर एवं धार्मिक महत्व के क्षेत्र)": [
        safe(district_data["दर्शनीय स्थल (मंदिर एवं धार्मिक महत्व के क्षेत्र)"])
    ],
    "पर्यटन स्थल": [safe(district_data["पर्यटन स्थल"])]
})
st.markdown(t1.to_html(index=False), unsafe_allow_html=True)

# ---------- FOOD | INNOVATION ----------
st.markdown(
    "<h3 style='text-align:center'>व्यंजन एवं मशहूर खान पान स्थल | जिला स्तर पर किए जा रहे विशेष नवाचार</h3>",
    unsafe_allow_html=True
)
t2 = pd.DataFrame({
    "व्यंजन एवं मशहूर खान पान स्थल": [
        safe(district_data["व्यंजन एवं मशहूर खान पान स्थल"])
    ],
    "जिला स्तर पर किए जा रहे विशेष नवाचार": [
        safe(district_data["जिला स्तर पर किए जा रहे विशेष नवाचार"])
    ]
})
st.markdown(t2.to_html(index=False), unsafe_allow_html=True)

# ---------- ODOP ----------
if safe(district_data["ODOP उत्पाद"]):
    st.markdown("<h3 style='text-align:center'>ODOP उत्पाद</h3>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='text-align:center'>{safe(district_data['ODOP उत्पाद'])}</p>",
        unsafe_allow_html=True
    )

# ---------- IDEAL | RIVER | PERSON ----------
st.markdown(
    "<h3 style='text-align:center'>आदर्श ग्राम | नदी एवं घाट | प्रमुख हस्ती</h3>",
    unsafe_allow_html=True
)
t3 = pd.DataFrame({
    "आदर्श ग्राम": [safe(district_data["आदर्श ग्राम"])],
    "नदी एवं घाट": [safe(district_data["नदी एवं घाट"])],
    "प्रमुख हस्ती (भारत रत्न, पद्म श्री, पद्म विभूषण या अन्य सम्मान से सम्मानित)": [
        safe(district_data["प्रमुख हस्ती (भारत रत्न, पद्म श्री, पद्म विभूषण या अन्य सम्मान से सम्मानित)"])
    ]
})
st.markdown(t3.to_html(index=False), unsafe_allow_html=True)

# ---------- INFLUENCER LIST (ALL ROWS) ----------
st.markdown("<h3 style='text-align:center'>इन्‍फ्लुऐंशर लिस्‍ट</h3>", unsafe_allow_html=True)

if influencers.empty:
    st.markdown("<p style='text-align:center'>कोई इन्फ्लुएंसर उपलब्ध नहीं</p>", unsafe_allow_html=True)
else:
    inf_df = influencers[
        ["इन्फ्लुएंसर्स नाम", "इंस्‍टाग्राम अकाउंट", "यूट्यूब अकाउंट", "मोबाइल नम्‍बर"]
    ].fillna("")

    st.markdown(inf_df.to_html(index=False), unsafe_allow_html=True)
