import streamlit as st

from utils.workflow import run_workflow
from utils.clickhouse_agent import clickhouse_agent


st.set_page_config(
    page_title="Agentic Cinema",
    page_icon="🎬",
    layout="wide"
)


st.title("🎬 Agentic Cinema")
if "result" not in st.session_state:
    st.session_state.result = None

st.write(
    "Upload a screenplay and let our AI production crew "
    "analyze it and create a production plan."
)


uploaded_file = st.file_uploader(
    "Upload your screenplay",
    type=["pdf"]
)



if uploaded_file is not None:

    st.success("Screenplay uploaded successfully!")

    if st.button("🎬 Analyze Screenplay"):

        with st.spinner("AI production crew is working..."):
            st.session_state.result = run_workflow(uploaded_file)

    if st.session_state.result is not None:

        result = st.session_state.result

        st.success("Analysis complete!")

        # -------------------------
        # SCRIPT ANALYSIS
        # -------------------------

        st.header("📖 Script Analysis")

        script_analysis = result["script_analysis"]

        st.subheader(script_analysis["title"])

        st.write("### Characters")
        st.write(", ".join(script_analysis["characters"]))

        st.write("### Locations")
        st.write(", ".join(script_analysis["locations"]))

        st.write("### Summary")
        st.write(script_analysis["summary"])

        # -------------------------
        # PRODUCTION PLAN
        # -------------------------

        st.header("🎥 Production Plan")

        production = result["production_plan"]

        st.metric(
            "Shooting Complexity",
            production["shooting_complexity"]
        )

        st.metric(
            "Estimated Shooting Days",
            production["estimated_shooting_days"]
        )

        st.write("### Required Locations")

        for location in production["required_locations"]:

            st.write(
                f"📍 **{location.get('name', location.get('location', 'Unknown'))}**"
            )

            st.write(f"- Type: {location.get('type', 'N/A')}")
            st.write(f"- Complexity: {location.get('complexity', 'N/A')}")
            st.write(f"- Lighting: {location.get('lighting', 'N/A')}")

            st.write(
                f"- Permit Required: "
                f"{'Yes' if location.get('permit_required', False) else 'No'}"
            )

            st.divider()

        st.write("### Production Notes")

        notes = production["production_notes"]

        if isinstance(notes, list):
            for note in notes:
                st.write(f"• {note}")
        else:
            st.write(f"• {notes}")

        # -------------------------
        # SHOOTING SCHEDULE
        # -------------------------

        st.header("📅 Shooting Schedule")

        schedule = result["schedule"]

        st.write(
            f"Total shooting days: "
            f"**{schedule['total_shooting_days']}**"
        )

        for day in schedule["schedule"]:

            with st.expander(
                f"Day {day['day']} — {day['location']}"
            ):

                st.write("**Scenes:**")

                for scene in day["scenes"]:
                    st.write(f"• {scene}")

                st.write("**Notes:**")
                st.write(day["notes"])

        # -------------------------
        # PRODUCTION ASSISTANT
        # -------------------------

        st.header("🤖 Production Assistant")

        st.write(
            "Ask questions about production requirements, locations, "
            "shooting days, permits, lighting, or scene complexity."
        )

        question = st.text_input(
            "Ask a production question",
            placeholder="e.g. What are the production requirements for the Street scene?"
        )

        if st.button("🔍 Ask Production Assistant"):

            if question.strip():

                with st.spinner(
                    "Production agent is checking production data..."
                ):

                    answer = clickhouse_agent(question)

                st.subheader("🎬 Agent Response")
                st.write(answer)

            else:
                st.warning("Please enter a question.")