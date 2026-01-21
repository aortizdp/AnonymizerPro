# 🔒 AI Anonymizer Pro

**AI Anonymizer Pro** is a powerful, locally-hosted tool designed to protect data privacy. It identifies and masks sensitive information (names, IDs, IBANs, etc.) from documents using Natural Language Processing (NLP) without relying on generative AI, ensuring your data never leaves your server.

🚀 **Live Demo:** [anonymizerpro.thedepablos.com](https://anonymizerpro.thedepablos.com)

---

## ✨ Key Features

* **Multi-language Support:** Fully localized in English, Catalan, Spanish, French, and German.
* **Privacy First:** All processing is done locally via NLP (non-generative AI). Zero data storage policy.
* **Multiple Formats:** Supports `.xlsx`, `.csv`, and `.docx` files.
* **Secure Workflow:**
    1. **Anonymize:** Upload your file and get a masked version plus an encryption key file.
    2. **Deanonymize:** Use the key file to restore the original data whenever you need it.
* **No Cookies:** Respects user privacy with a strictly no-cookie policy.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Python-based web framework).
* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) for high-performance API processing.
* **NLP Engine:** Local Python libraries for PII (Personally Identifiable Information) detection.
* **Server:** Nginx as a reverse proxy with Let's Encrypt SSL.

---

## 🏗️ Project Architecture

The project is built with a modular and scalable approach:
* `frontend/app.py`: Main application logic.
* `frontend/config.py`: Centralized configuration for URLs and project links.
* `frontend/translations.py`: Translation dictionaries for multi-language support.
* `backend/`: Core engine for data anonymization.

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/aortizdp/AnonymizerPro.git](https://github.com/aortizdp/AnonymizerPro.git)
   cd AnonymizerPro
Run the startup script: We've included a helper script to launch both the backend and frontend simultaneously:

Bash
chmod +x run_all.sh
./run_all.sh
⚖️ License
Distributed under the MIT License. See LICENSE for more information.

☕ Support
Created by Albert Ortiz. If you find this tool useful, consider buying me a coffee!
https://buymeacoffee.com/aortizdp

Buy Me A Coffee
