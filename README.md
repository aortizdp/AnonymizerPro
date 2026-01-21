# AI Anonymizer Pro
🔒 AI Anonymizer Pro
Professional-grade document anonymization using local, non-generative AI.

AI Anonymizer Pro is a corporate-ready tool designed to protect sensitive data within Excel, CSV, and Word documents. Unlike other tools, it operates as a "Simple Translator" using local Natural Language Processing (NLP), ensuring that your data never leaves your infrastructure.

🌟 Key Features
100% Local Processing: No data is sent to external APIs or Generative AI models. Your privacy is guaranteed.

Multi-format Support: Seamlessly handles .xlsx, .csv, and .docx files.

Multi-language Interface: Fully translated into English, Català, Español, Français, and Deutsch.

Intelligent Detection: Automatically identifies and masks:

Personal Names (NER)

National IDs (DNI/NIE)

IBAN & Banking information

Phone numbers and Emails

Reversible Process: Includes a secure decryption_keys.xlsx generation to restore original data when needed.

🚀 Quick Start
1. Prerequisites
Ensure you have Python 3.10+ installed. It is recommended to use a virtual environment.

Bash
# Clone the repository
git clone https://github.com/aortizdp/AnonymizerPro.git
cd AnonymizerPro

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download the NLP model
python -m spacy download es_core_news_lg
2. Running the Application
The project is split into a FastAPI backend and a Streamlit frontend.

Start the Backend:

Bash
uvicorn backend.main:app --host 0.0.0.0 --port 7000
Start the Frontend:

Bash
streamlit run frontend/app.py
🛡️ Privacy & Security First
This application follows a Zero-Data-Storage policy:

No Cookies: We do not track users or use any advertising cookies.

No Logs: Document contents are processed in volatile memory and never logged.

Local AI: We use spacy with local models. No Generative AI (like GPT) is used to prevent data leakage or "hallucinations".

[!IMPORTANT] Auditability: Because privacy is our core value, the entire source code is open for review. For corporate environments, we encourage running this tool in an air-gapped or restricted network.

💡 VIBE Coding & Development
This project was developed using the VIBE Coding methodology: a high-level intent-driven development process where the human acts as a "Thought Partner" with AI.

Architect: Albert Ortiz

Thought Partner: Gemini AI

☕ Support the Project
AI Anonymizer Pro is free and open-source. If this tool helps you or your company save time and improve security, please consider supporting the server costs:

📄 License
Distributed under the MIT License. See LICENSE for more information.

👤 Author
Albert Ortiz

Website: albert.thedepablos.com

GitHub: @aortizdp
