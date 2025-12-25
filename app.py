import streamlit as st
import pandas as pd
from simulation import calculate_risk, suggest_reassignment

st.set_page_config(page_title="Predictive SLA Simulation", layout="wide")

st.title("Predictive Process Simulation & SLA Forecasting")
st.write(
    "This prototype demonstrates how operational teams can proactively "
    "forecast SLA risks and simulate resource changes using current work-in-progress data."
)

st.subheader("Current Work in Progress")

try:
    df = pd.read_excel("data/demo_cases.xlsx")
except Exception:
    st.warning("Demo dataset not found. Please upload an Excel file.")
    uploaded_file = st.file_uploader("Upload WIP snapshot (.xlsx)", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
    else:
        st.stop()

st.dataframe(df, use_container_width=True)

df = calculate_risk(df)

st.subheader("Predicted SLA Risk Scores")
st.dataframe(
    df[["CaseID", "AssignedTo", "Team", "RiskScore"]],
    use_container_width=True
)

st.divider()

st.subheader("What-If Scenario Planning")

selected_case = st.selectbox("Select a case", df["CaseID"])
new_team = st.selectbox("Reassign to team", df["Team"].unique())

if st.button("Simulate Change"):
    df.loc[df["CaseID"] == selected_case, "Team"] = new_team
    df = calculate_risk(df)

    st.success("Scenario simulated successfully")

    st.dataframe(
        df[["CaseID", "AssignedTo", "Team", "RiskScore"]],
        use_container_width=True
    )

    st.subheader("System Suggestions")
    for suggestion in suggest_reassignment(df):
        st.write("•", suggestion)
