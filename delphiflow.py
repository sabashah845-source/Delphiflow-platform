import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="✨ Delphi CVI Platform",
    page_icon="🧠",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.stApp {
    background: linear-gradient(
        to right,
        #eef2ff,
        #fdfbff
    );
}

h1, h2, h3 {
    color: #3b0764;
}

div[data-testid="stMetric"] {
    background-color: white;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
}

.stButton>button {
    background: linear-gradient(
        90deg,
        #7c3aed,
        #2563eb
    );
    color: white;
    border-radius: 12px;
    border: none;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
}

.stDownloadButton>button {
    background: linear-gradient(
        90deg,
        #059669,
        #10b981
    );
    color: white;
    border-radius: 12px;
    border: none;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
}

.css-1d391kg {
    background-color: #ffffff;
}

.block-container {
    padding-top: 2rem;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "responses" not in st.session_state:
    st.session_state.responses = []

# =====================================================
# HEADER
# =====================================================

st.markdown("""
# 🧠 AI Delphi Expert Consensus Platform

### 📊 Smart Questionnaire Validation & CVI Analytics
""")

st.info("""
✨ Features Included:
- Google Form Style Questionnaire
- CVI Calculation
- Delphi Consensus
- Expert Feedback
- Real-Time Analytics
- Excel Export
""")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    width=120
)

st.sidebar.title("⚙️ Settings")

consensus_threshold = st.sidebar.slider(
    "🎯 Consensus Threshold (%)",
    50,
    100,
    80
)

anonymous_mode = st.sidebar.checkbox(
    "🕶️ Anonymous Review",
    value=True
)

# =====================================================
# QUESTIONNAIRE SECTION
# =====================================================

st.markdown("""
<div class="card">
""", unsafe_allow_html=True)

st.header("📝 Create Questionnaire")

questionnaire_title = st.text_input(
    "📌 Questionnaire Title",
    "Medication Adherence Questionnaire"
)

questionnaire_description = st.text_area(
    "📖 Description",
    "Describe your study..."
)

st.subheader("✍️ Add Questions")

default_questions = """
The patient takes medication regularly.
The patient forgets medication doses.
The patient understands medication instructions.
"""

manual_questions = st.text_area(
    "Enter One Question Per Line",
    default_questions,
    height=200
)

st.subheader("📂 Upload Questionnaire CSV")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

uploaded_questions = []

if uploaded_file is not None:

    upload_df = pd.read_csv(uploaded_file)

    st.success("✅ File Uploaded Successfully")

    st.dataframe(upload_df)

    if "question" in upload_df.columns:

        uploaded_questions = (
            upload_df["question"]
            .dropna()
            .tolist()
        )

manual_question_list = [
    q.strip()
    for q in manual_questions.split("\n")
    if q.strip()
]

questions = (
    manual_question_list +
    uploaded_questions
)

questions = list(dict.fromkeys(questions))

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# QUESTIONNAIRE PREVIEW
# =====================================================

st.markdown("""
<div class="card">
""", unsafe_allow_html=True)

st.header("👀 Questionnaire Preview")

for i, q in enumerate(questions):
    st.write(f"**{i+1}.** {q}")

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# EXPERT INFO
# =====================================================

st.markdown("""
<div class="card">
""", unsafe_allow_html=True)

st.header("👨‍⚕️ Expert Information")

col1, col2 = st.columns(2)

with col1:
    expert_name = st.text_input(
        "👤 Expert Name"
    )

    expert_specialty = st.text_input(
        "🏥 Specialization"
    )

with col2:
    expert_email = st.text_input(
        "📧 Email"
    )

    years_experience = st.number_input(
        "📅 Years of Experience",
        1,
        50,
        5
    )

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# DELPHI FORM
# =====================================================

st.markdown("""
<div class="card">
""", unsafe_allow_html=True)

st.header("📋 Delphi Rating Form")

with st.form("delphi_form"):

    all_responses = []

    for i, question in enumerate(questions):

        st.subheader(f"🧩 Question {i+1}")

        st.write(question)

        col1, col2, col3 = st.columns(3)

        with col1:
            relevance = st.radio(
                "⭐ Relevance",
                [1, 2, 3, 4],
                horizontal=True,
                key=f"rel_{i}"
            )

        with col2:
            clarity = st.radio(
                "💡 Clarity",
                [1, 2, 3, 4],
                horizontal=True,
                key=f"clar_{i}"
            )

        with col3:
            simplicity = st.radio(
                "✨ Simplicity",
                [1, 2, 3, 4],
                horizontal=True,
                key=f"simp_{i}"
            )

        comments = st.text_area(
            "🗨️ Expert Comments",
            key=f"comment_{i}"
        )

        st.markdown("---")

        all_responses.append({

            "title": questionnaire_title,
            "question": question,
            "expert_name": expert_name,
            "email": expert_email,
            "specialty": expert_specialty,
            "experience": years_experience,

            "relevance": relevance,
            "clarity": clarity,
            "simplicity": simplicity,

            "comments": comments,

            "timestamp": datetime.now()
        })

    submitted = st.form_submit_button(
        "🚀 Submit Expert Review"
    )

    if submitted:

        for r in all_responses:
            st.session_state.responses.append(r)

        st.success(
            "✅ Responses Submitted Successfully"
        )

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# ANALYTICS
# =====================================================

if len(st.session_state.responses) > 0:

    st.markdown("""
    <div class="card">
    """, unsafe_allow_html=True)

    st.header("📊 CVI Analytics Dashboard")

    df = pd.DataFrame(st.session_state.responses)

    cvi_results = []

    for question in questions:

        item_df = df[df["question"] == question]

        total_experts = len(item_df)

        if total_experts > 0:

            relevance_agree = len(
                item_df[item_df["relevance"] >= 3]
            )

            clarity_agree = len(
                item_df[item_df["clarity"] >= 3]
            )

            simplicity_agree = len(
                item_df[item_df["simplicity"] >= 3]
            )

            relevance_cvi = (
                relevance_agree / total_experts
            )

            clarity_cvi = (
                clarity_agree / total_experts
            )

            simplicity_cvi = (
                simplicity_agree / total_experts
            )

            avg_cvi = (
                relevance_cvi +
                clarity_cvi +
                simplicity_cvi
            ) / 3

            cvi_results.append({

                "Question": question,

                "Experts":
                total_experts,

                "Average I-CVI":
                round(avg_cvi, 2)
            })

    cvi_df = pd.DataFrame(cvi_results)

    st.dataframe(cvi_df)

    s_cvi = round(
        cvi_df["Average I-CVI"].mean(),
        2
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "📈 Scale-Level CVI",
            s_cvi
        )

    with col2:

        if s_cvi >= 0.80:
            st.success(
                "🎉 Excellent Content Validity"
            )
        else:
            st.warning(
                "⚠️ Needs Revision"
            )

    # =================================================
    # CHARTS
    # =================================================

    st.subheader("📉 CVI Visualization")

    fig = px.bar(
        cvi_df,
        x="Question",
        y="Average I-CVI",
        text="Average I-CVI",
        title="Average I-CVI Per Question"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =================================================
    # COMMENTS
    # =================================================

    st.subheader("💬 Expert Feedback")

    comments_df = df[
        df["comments"] != ""
    ]

    for _, row in comments_df.iterrows():

        if anonymous_mode:
            expert_display = "🕶️ Anonymous Expert"
        else:
            expert_display = row["expert_name"]

        st.info(f"""
        👤 {expert_display}

        📌 Question:
        {row['question']}

        💭 Comment:
        {row['comments']}
        """)

    # =================================================
    # EXPORT
    # =================================================

    st.subheader("📥 Export Reports")

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Responses",
            index=False
        )

        cvi_df.to_excel(
            writer,
            sheet_name="CVI Results",
            index=False
        )

    st.download_button(
        label="📊 Download Excel Report",
        data=output.getvalue(),
        file_name="delphi_cvi_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
<center>

### 🧠 AI Delphi Consensus Platform

Built with ❤️ using Streamlit

</center>
""", unsafe_allow_html=True)