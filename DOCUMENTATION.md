# 🔒 AI Anonymizer Pro: The Ultimate Technical Manual

This documentation provides a comprehensive guide to the **AI Anonymizer Pro** project, covering its conception, technical stack, and deployment process.

---

## 1. The Idea (Privacy First)
The project aims to provide a secure environment for document sanitization. 
* **The Goal:** Detect and mask Personally Identifiable Information (PII) like names, IDs, and IBANs.
* **The Constraint:** Data must remain local. No generative AI or cloud-based processing is used to ensure compliance with privacy standards.

---

## 2. Project Planning & Modular Architecture
To ensure the code is professional and easy to maintain, we separated the logic into three main modules:
* **`app.py`**: The core frontend engine using Streamlit.
* **`config.py`**: Centralized configuration for URLs and project links (GitHub, Buy Me a Coffee, etc.).
* **`translations.py`**: A dictionary containing all UI strings in 5 languages (English, Catalan, Spanish, French, and German).

---

## 3. Selected Libraries & Tech Stack
We selected libraries that balance performance with local execution:

| Library | Purpose | Why? | Alternatives |
| :--- | :--- | :--- | :--- |
| **Streamlit** | Frontend | High-speed data dashboard creation. | Flask/React (High complexity). |
| **FastAPI** | Backend | High-performance API for file handling. | Django (Too heavy). |
| **Spacy/Presidio**| NLP Engine | Top-tier local detection of sensitive entities. | OpenAI API (Not local). |
| **Pandas** | Data Processing | Essential for Excel and CSV manipulation. | Openpyxl. |
| **python-docx** | Document Support| Precise parsing of Word files. | PDFMiner. |

---

## 4. How the Tool Works (Dummy-Proof Guide)
The workflow consists of two secure steps:

### Step A: Anonymize
1. Upload your `.xlsx`, `.csv`, or `.docx` file.
2. The system replaces sensitive data with placeholders (e.g., `USER_1`).
3. Download a `.zip` containing the anonymized file and a `decryption_keys.xlsx`.

### Step B: Deanonymize (Restore)
1. Upload the anonymized file.
2. Upload the `decryption_keys.xlsx` file.
3. The system restores the original values using the provided key.

---

## 5. Development & Trial-and-Error
During development in **January 2026**, we solved several critical issues:
* **2026 Syntax Update:** Replaced deprecated `use_container_width` with the new `width="stretch"` standard for images.
* **Security & Secrets:** GitHub Push Protection blocked a commit containing a Personal Access Token. We sanitized the code and switched to SSH authentication.
* **Nginx Port Conflicts:** Fixed `Address already in use` errors on port 80 by killing ghost processes before restarting Nginx.

---

## 6. Infrastructure & Public Deployment
The application is hosted at [anonymizerpro.thedepablos.com](https://anonymizerpro.thedepablos.com).

1. **DNS Management:** Linked the subdomain to the VPS IP.
2. **Nginx Reverse Proxy:** Configured to forward traffic to the internal port 8501.
3. **SSL/TLS Certificate:** Generated via **Let's Encrypt (Certbot)** to ensure an encrypted HTTPS connection.

---

## 7. Branding & Monetization
* **Banner:** A custom panoramic header created using **Gemini AI** to represent security and neural networks.
* **Buy Me a Coffee (BMC):** Integrated a donation system in the sidebar to help subsidize server costs.

---

## 8. GitHub Repository & Maintenance
The source code is managed via Git at [github.com/aortizdp/AnonymizerPro](https://github.com/aortizdp/AnonymizerPro).
* **MIT License:** Included to ensure open-source freedom.
* **README:** Updated with installation steps and project features.
* **Startup Script:** Created `run_all.sh` to launch both the Backend and Frontend with one command.

---
*© 2026 Project created by Albert Ortiz.*
