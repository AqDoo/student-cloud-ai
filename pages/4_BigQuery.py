import json

import pandas as pd
import plotly.express as px
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

st.set_page_config(
    page_title="BigQuery Analytics",
    page_icon="☁️",
    layout="wide",
)

st.title("☁️ Google BigQuery бұлттық аналитикасы")
st.caption("BigQuery Sandbox ортасында сақталған студенттер деректері")


@st.cache_data(ttl=300)
def load_bigquery_data() -> pd.DataFrame:
    service_account_info = json.loads(
        st.secrets["gcp_service_account_json"]
    )

    credentials = (
        service_account.Credentials.from_service_account_info(
            service_account_info
        )
    )

    project_id = st.secrets["bigquery"]["project_id"]
    dataset_id = st.secrets["bigquery"]["dataset_id"]
    table_id = st.secrets["bigquery"]["table_id"]

    client = bigquery.Client(
        project=project_id,
        credentials=credentials,
    )

    query = f"""
        SELECT
            student_id,
            attendance,
            practice_score,
            activity,
            missed_tasks,
            final_score,
            risk_level
        FROM `{project_id}.{dataset_id}.{table_id}`
        ORDER BY final_score DESC
    """

    rows = client.query(query).result()
    return pd.DataFrame([dict(row) for row in rows])


try:
    data = load_bigquery_data()
except Exception as error:
    st.error("BigQuery деректерін жүктеу кезінде қате пайда болды.")
    st.exception(error)
    st.stop()

high_risk = int((data["risk_level"] == "Жоғары").sum())
average_score = float(data["final_score"].mean())

col1, col2, col3 = st.columns(3)

col1.metric("BigQuery жазбалары", len(data))
col2.metric("Орташа нәтиже", f"{average_score:.2f}")
col3.metric("Жоғары тәуекел", high_risk)

summary = (
    data.groupby("risk_level", as_index=False)
    .agg(
        student_count=("student_id", "count"),
        average_score=("final_score", "mean"),
    )
)

summary["average_score"] = summary["average_score"].round(2)

left, right = st.columns(2)

with left:
    figure = px.pie(
        summary,
        names="risk_level",
        values="student_count",
        hole=0.5,
        title="Тәуекел деңгейлерінің үлесі",
        color="risk_level",
        color_discrete_map={
            "Жоғары": "#ef476f",
            "Орташа": "#ffd166",
            "Төмен": "#06d6a0",
        },
    )
    st.plotly_chart(figure, width="stretch")

with right:
    st.subheader("BigQuery нәтижелері")
    st.dataframe(summary, width="stretch", hide_index=True)

st.subheader("Бұлттағы студенттер деректері")
st.dataframe(data, width="stretch", hide_index=True)

if st.button("BigQuery деректерін жаңарту"):
    st.cache_data.clear()
    st.rerun()