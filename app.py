import os
import io
import streamlit as st
from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()

st.set_page_config(
    page_title="Swasthya AI",
    page_icon="💚",
    layout="centered",
)

st.title("💚 Swasthya AI")
st.caption(
    "Your personal health companion — wellness, report understanding, "
    "medicine information, and voice assistance."
)

API_KEY = os.getenv("SARVAM_API_KEY", "").strip()

# Sidebar
with st.sidebar:
    st.header("Choose a module")
    module = st.radio(
        "What would you like help with?",
        [
            "Wellness Coach",
            "Understand My Reports",
            "Medicine Guide",
            "🎙️ Voice Health Assistant",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption(
        "Hackathon prototype • Not a substitute for professional medical advice"
    )


def get_client():
    if not API_KEY:
        st.error(
            "API key missing. Add SARVAM_API_KEY=your_key to your local "
            ".env file, then restart the app."
        )
        st.stop()

    return SarvamAI(api_subscription_key=API_KEY)


def ask_sarvam(system_prompt: str, user_prompt: str) -> str:
    client = get_client()

    response = client.chat.completions(
        model="sarvam-105b-conversations",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content


SAFETY = (
    "You are a cautious health-information assistant in a hackathon prototype. "
    "Do not diagnose, prescribe medicines, recommend a personalized supplement dose, "
    "or tell users to start, stop, or change prescribed treatment. Explain uncertainty. "
    "For concerning symptoms or abnormal results, advise contacting a qualified healthcare "
    "professional. For emergencies, advise seeking local emergency care. Be concise, practical, "
    "non-judgmental, and use plain language. Do not claim to replace a clinician. "
    "Respond in the same language as the user's question whenever possible."
)


# 1. Wellness Coach
if module == "Wellness Coach":
    st.subheader("🌱 Build healthier habits")
    st.write(
        "Tell us about your goal and routine to get general, realistic wellness suggestions."
    )

    goal = st.selectbox(
        "Your goal",
        [
            "Improve general fitness",
            "Build strength",
            "Improve sleep",
            "Eat more balanced meals",
            "Lose weight gradually",
            "Build a consistent routine",
        ],
    )
    routine = st.text_area(
        "Describe your usual day",
        placeholder=(
            "Example: I sit for classes most of the day, walk 15 minutes, "
            "and usually sleep around midnight."
        ),
    )
    preferences = st.text_input(
        "Preferences or constraints (optional)",
        placeholder="e.g. vegetarian meals, limited time, no gym",
    )

    if st.button(
        "Create my wellness plan",
        type="primary",
        use_container_width=True,
    ):
        if not routine.strip():
            st.warning("Please describe your usual day first.")
        else:
            with st.spinner("Creating suggestions..."):
                prompt = (
                    f"Goal: {goal}\nUsual day: {routine}\n"
                    f"Preferences/constraints: {preferences}\n\n"
                    "Give a simple plan for the next day with 3-5 achievable actions "
                    "and one gentle progress check-in. Avoid extreme dieting, calorie "
                    "prescriptions, and unsupported medical claims."
                )
                try:
                    st.markdown(ask_sarvam(SAFETY, prompt))
                except Exception:
                    st.error(
                        "API request failed. Check your API key, account access, "
                        "model availability, and internet connection."
                    )


# 2. Understand My Reports
elif module == "Understand My Reports":
    st.subheader("🧾 Understand a lab result")
    st.write("Enter a result exactly as shown on your report. This demo does not read uploaded files.")

    test_name = st.text_input("Test name", placeholder="e.g. Vitamin B12")
    result = st.text_input("Result and unit", placeholder="e.g. 180 pg/mL")
    reference = st.text_input(
        "Lab's reference range (if shown)",
        placeholder="Enter the range printed on your report",
    )
    report_date = st.text_input(
        "Report date (optional)",
        placeholder="e.g. 15 Oct 2026",
    )

    if st.button(
        "Explain this result",
        type="primary",
        use_container_width=True,
    ):
        if not test_name.strip() or not result.strip():
            st.warning("Please enter at least the test name and result.")
        else:
            with st.spinner("Preparing a plain-language explanation..."):
                prompt = (
                    f"Explain this lab result in plain language without diagnosing:\n"
                    f"Test: {test_name}\nResult: {result}\n"
                    f"Lab reference range: {reference or 'not provided'}\n"
                    f"Report date: {report_date or 'not provided'}\n\n"
                    "Structure the response as: (1) what the test generally measures, "
                    "(2) what can and cannot be inferred from this value, "
                    "(3) useful questions to ask a clinician, "
                    "(4) whether interpretation depends on symptoms, age, medical history, "
                    "or other tests. Do not recommend starting supplements or medication. "
                    "If the range or units are missing, say interpretation is limited."
                )
                try:
                    st.markdown(ask_sarvam(SAFETY, prompt))
                except Exception:
                    st.error(
                        "API request failed. Check your API key, account access, "
                        "model availability, and internet connection."
                    )


# 3. Medicine Guide
elif module == "Medicine Guide":
    st.subheader("💊 Understand existing medicines")
    st.write(
        "Ask general questions about a medicine or an existing prescription. "
        "Do not enter personal identifiers."
    )

    medicine = st.text_input(
        "Medicine name and strength (if known)",
        placeholder="e.g. medicine name as printed on the label",
    )
    question = st.text_area(
        "What would you like to understand?",
        placeholder="e.g. What questions should I ask my pharmacist about this medicine?",
    )

    if st.button(
        "Get medicine information",
        type="primary",
        use_container_width=True,
    ):
        if not medicine.strip() or not question.strip():
            st.warning("Please enter the medicine name and your question.")
        else:
            with st.spinner("Preparing general information..."):
                prompt = (
                    f"Medicine as entered by user: {medicine}\n"
                    f"Question: {question}\n\n"
                    "Provide general educational information only. Do not infer a dose, "
                    "prescribe, or advise starting/stopping/changing medication. "
                    "If the name is ambiguous, ask the user to confirm the exact name "
                    "and strength with a pharmacist. Encourage checking the package leaflet "
                    "and consulting a qualified professional."
                )
                try:
                    st.markdown(ask_sarvam(SAFETY, prompt))
                except Exception:
                    st.error(
                        "API request failed. Check your API key, account access, "
                        "model availability, and internet connection."
                    )


# 4. Voice Health Assistant
elif module == "🎙️ Voice Health Assistant":
    st.subheader("🎙️ Voice Health Assistant")
    st.write(
        "Ask your health-information question by speaking. "
        "Automatic language detection is enabled for supported languages."
    )
    st.info(
        "Speak in a supported language, including Hindi or English. "
        "Short recordings work best. Avoid sharing your name, address, "
        "or other identifying information."
    )

    audio = st.audio_input(
        "Tap to record your question",
        sample_rate=16000,
        key="voice_health_audio",
    )

    if audio is not None:
        st.audio(audio, format="audio/wav")

        if st.button(
            "Transcribe and get guidance",
            type="primary",
            use_container_width=True,
            key="voice_health_submit",
        ):
            try:
                client = get_client()

                with st.spinner("Transcribing your speech..."):
                    audio_bytes = audio.getvalue()
                    transcription = client.speech_to_text.transcribe(file=("voice_question.wav", audio_bytes, "audio/wav"),
                    model="saaras:v4", language_code="unknown", mode="transcribe",
                    )


                transcript = getattr(transcription, "transcript", "") or ""
                detected_language = (
                    getattr(transcription, "language_code", None)
                    or getattr(transcription, "language", None)
                    or "Not returned by the API"
                )

                if not transcript.strip():
                    st.warning(
                        "No speech was detected. Please record your question again."
                    )
                else:
                    st.markdown("### 📝 Your transcribed question")
                    st.write(transcript)

                    st.caption(f"Detected language: {detected_language}")

                    with st.spinner("Preparing your health-information response..."):
                        answer = ask_sarvam(SAFETY, transcript)

                    st.markdown("### 💚 Swasthya AI response")
                    st.markdown(answer)

            except Exception as exc:
                st.error(
                    "Voice processing failed. Check your internet connection, "
                    "Sarvam API access, and supported audio format."
                )
                st.caption(f"Technical detail: {exc}")


# Footer
st.divider()
st.caption(
    "Privacy note: This demo does not intentionally save your inputs to a database. "
    "Avoid entering names, addresses, IDs, or other identifying details. "
    "AI-generated information may be inaccurate; verify medical decisions with "
    "a qualified professional."
)
