# Swasthya AI 💚

A 30-minute hackathon prototype for a personal health companion with three modules:
- **Wellness Coach** — general, achievable habit suggestions.
- **Understand My Reports** — plain-language explanations of manually entered lab results.
- **Medicine Guide** — general information about existing medicines and questions to ask a pharmacist/clinician.
- **Voice Assitant** _ AI assitant that understands any recognised Indian Language.

Powered by Sarvam AI chat completions.

## Run locally

Requires Python 3.10+ (recommended).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a local `.env` file in this folder with:

```text
SARVAM_API_KEY=your_actual_sarvam_api_key
```

Do not commit `.env`. It is excluded by `.gitignore`.

Run:

```powershell
python -m streamlit run app.py
```

## Safety and scope

This is a hackathon demo, not a medical device or clinical decision-support system. It does not diagnose conditions, prescribe medicines, or recommend personalized supplement doses. Report explanations depend on the information entered and may be wrong. Verify medical decisions with a qualified healthcare professional. Do not enter personal identifiers or real patient information in a public demo.

## Tech stack

- Python
- Streamlit
- Sarvam AI Python SDK (`sarvamai`)
- `python-dotenv`
