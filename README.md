# Internship Project: Cryptography and Offline Translation

## Lunor Translator 🔮

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React"/>
  <img src="https://img.shields.io/badge/Tauri-FFC131?style=for-the-badge&logo=tauri&logoColor=black" alt="Tauri"/>
  <img src="https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white" alt="Rust"/>
</p>

<p align="center">
  <img src="[INSERT YOUR APP SCREENSHOT OR LOGO HERE]" alt="Lunor Translator Screenshot" width="700"/>
</p>

<p align="center">
  <strong>A cross-platform, offline, AI-powered translation application for fast, private, and accurate multilingual communication. Developed as part of an internship project at DRDO.</strong>
</p>

---

## Table of Contents

1.  [Project Overview](#project-overview)
2.  [Internship Phases](#internship-phases)
    * [Phase 1: Cryptography Exploration](#phase-1-cryptography-exploration)
    * [Phase 2: From Model Comparison to Application Development](#phase-2-from-model-comparison-to-application-development)
3.  [Models Explored & Key Findings](#models-explored--key-findings)
4.  [The Final Application: Lunor Translator](#the-final-application-lunor-translator)
    * [Key Features](#key-features)
    * [Technology Stack](#technology-stack)
5.  [Repository Structure](#repository-structure)
6.  [Installation and Usage (Lunor Translator)](#installation-and-usage-lunor-translator)
    * [Prerequisites](#prerequisites)
    * [Backend Setup](#backend-setup)
    * [Frontend Setup](#frontend-setup)
7.  [Future Work](#future-work)
8.  [Contact](#contact)

---

## Internship Phases

### Phase 1: Cryptography Exploration

The initial phase of the internship involved gaining foundational knowledge in **cryptography**. This covered essential concepts crucial for understanding secure data handling, which is a vital prerequisite for any secure AI deployment.

**Key Topics Covered:**
* **Symmetric & Asymmetric-key Cryptography:** AES, RSA, ECC.
* **Hashing Algorithms & Digital Signatures:** SHA-256, principles of integrity and non-repudiation.
* **Key Exchange:** Diffie-Hellman protocol.

### Phase 2: From Model Comparison to Application Development

Following the cryptography phase, the focus shifted to a practical machine learning project. This phase had two stages:

1.  **Model Comparison:** The first stage involved a rigorous evaluation of pre-trained open-source models for **offline language translation**. The primary objective was to compare their accuracy against Google Translate using the BLEU score and identify the most capable model, especially for low-resource languages like Burmese.

2.  **Application Development:** Based on the conclusive results from the comparison, the project evolved. The winning model, **NLLB-200**, was chosen as the core engine to build a functional, cross-platform desktop application prototype named **Lunor Translator**.

---

## Models Explored & Key Findings

The following translation models were explored and benchmarked during the initial research phase:

* **M2M100 (1.2B & 418M variants)**
* **Argos Translate**
* **LibreTranslate**
* **NLLB-200** (Added during later testing)
* **Google Translate** (As an online baseline)

#### Accuracy Comparison Results (BLEU Scores)

The initial benchmarking revealed a clear performance gap, especially in the challenging Burmese-to-English pair.

| Model                 | Burmese-English BLEU Score |
| :-------------------- | :------------------------- |
| Google Translate      | 9.14                       |
| M2M100 1.2B           | 1.42                       |
| **NLLB-200 1.3B** | **25.02** |

#### Key Finding

The results were definitive: **NLLB-200 drastically outperformed all other tested models**, including the online baseline, for Burmese translation. This outstanding performance made it the clear and obvious choice for the core technology of the final application.

---

## The Final Application: Lunor Translator

Lunor Translator is the culmination of this research—a desktop application that brings the power of NLLB-200 to users in a secure, offline environment.

### Key Features

* 🔒 **Completely Offline:** All translation is processed locally. No data ever leaves your computer.
* ⚡ **State-of-the-Art Accuracy:** Powered by the NLLB-200 model for high-quality translation.
* 🌐 **Cross-Platform:** Designed to run natively on Windows, macOS, and Linux.
* ✨ **Modern UI:** A clean, intuitive, and responsive user interface built with React and Tauri.
* 📂 **Custom Model Support:** Load any compatible Hugging Face model from your local filesystem.

### Technology Stack

| Category          | Technology                                   |
| :---------------- | :------------------------------------------- |
| **AI/ML Model** | Facebook NLLB-200                            |
| **Backend** | Python, FastAPI, Hugging Face `transformers` |
| **Frontend** | React.js, Next.js, shadcn/ui                 |
| **Desktop Framework**| Tauri (with Rust Core)                       |

---

## Repository Structure

The final project is organized with a clear separation between the frontend application and the backend scripts.


nllb/
├── app/                  # The React/Tauri frontend application
│   ├── components/
│   └── ...
├── scripts/
│   └── backend/          # The Python backend server
│       ├── main.py
│       ├── run_server.py
│       └── requirements.txt
└── ... (other config files)


---

## Installation and Usage (Lunor Translator)

Follow these instructions to set up and run the application from the source code.

### Prerequisites

Ensure you have the following installed on your system:
* **Python** (version 3.10 or higher)
* **Node.js** (LTS version)
* **Rust** (stable toolchain, installed via `rustup`)
* **Git**

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd nllb/scripts/backend
    ```
2.  **(Recommended) Create and activate a virtual environment:**
    * **Windows:** `python -m venv venv` followed by `.\venv\Scripts\activate`
    * **macOS / Linux:** `python3 -m venv venv` followed by `source venv/bin/activate`
3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the backend server:**
    ```bash
    python run_server.py
    ```
    The server will start on `http://localhost:8000`. **Keep this terminal window open.**

### Frontend Setup

Open a **new terminal window**.

1.  **Navigate to the frontend directory:**
    ```bash
    cd nllb/app
    ```
2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```
3.  **Launch the Lunor Translator application:**
    ```bash
    npm run tauri dev
    ```
    The desktop application window will launch. You can now load a model via the settings panel and start translating.

---

## Future Work

* **Standalone Executable:** Solve the Tauri sidecar challenge to bundle the Python backend into a single, double-clickable application.
* **Model Fine-Tuning:** Create a larger, cleaner corpus for specific language pairs and fine-tune NLLB to reduce errors like named entity hallucinations.
* **Feature Expansion:** Add more features, such as full document translation and expanding Text-to-Speech (TTS) support.

---

## Contact

Harsh Tripathi - [harsht@iitbhilai.ac.in](mailto:harsht@iitbhilai.ac.in)
