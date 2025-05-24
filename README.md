# Crypto-and-Translation-Projects
# Offline NMT Model Comparison (Internship Project 2025)

---

## Project Overview

This repository documents the work completed during an AI/ML internship focusing on two primary areas: an initial exploration of **cryptography concepts** and a subsequent deep dive into **offline language translation model**.

The core of this project is the comprehensive evaluation of various open-source, pre-trained neural machine translation (NMT) models for offline use. The goal was to identify suitable models for building a local, internet-independent language translation solution. We benchmarked these models against Google Translate across Hindi-English, Chinese-English, and Burmese-English language pairs using standard BLEU scores.

---

## Table of Contents

1.  [Project Overview](#project-overview)
2.  [Table of Contents](#table-of-contents)
3.  [Internship Phases](#internship-phases)
    * [Phase 1: Cryptography Exploration](#phase-1-cryptography-exploration)
    * [Phase 2: Offline Language Translation Model Comparison](#phase-2-offline-language-translation-model-comparison)
4.  [Models Explored](#models-explored)
5.  [Methodology](#methodology)
6.  [Accuracy Comparison Results (BLEU Scores)](#accuracy-comparison-results-bleu-scores)
7.  [Key Observations and Challenges](#key-observations-and-challenges)
8.  [Repository Structure](#repository-structure)
9.  [Setup and Usage (for Translation Benchmarking)](#setup-and-usage-for-translation-benchmarking)
10. [Future Work](#future-work)
11. [Contact](#contact)
12. [License](#license)

---

## Internship Phases

### Phase 1: Cryptography Exploration

The initial phase of the internship involved gaining foundational knowledge in **cryptography**. This covered essential concepts crucial for understanding secure data handling, which can be relevant for any future secure AI deployments.

**Key Topics Covered:**
* **Symmetric-key Cryptography:** AES (Advanced Encryption Standard), DES/3DES.
* **Asymmetric-key Cryptography (Public-key):** RSA, Elliptic Curve Cryptography (ECC).
* **Hashing Algorithms:** SHA-256, MD5.
* **Digital Signatures:** Principles of authenticity, integrity, and non-repudiation.
* **Key Exchange:** Diffie-Hellman protocol.

Detailed notes and summaries of these concepts are stored in the `02_Cryptography_Research/` directory.

### Phase 2: Offline Language Translation Model Comparison

Following the cryptography phase, the focus shifted to a practical machine learning project: evaluating pre-trained open-source models for **offline language translation**. The primary objective was to compare their accuracy against Google Translate and document their characteristics, performance, and limitations.

---

## Models Explored

The following translation models were explored and benchmarked:

* **M2M100 1.2B (from Hugging Face):** A large-scale multilingual neural machine translation model supporting direct translation between 100 languages.
* **M2M100 418M (from Hugging Face):** A smaller variant of the M2M100 model, also supporting 100 languages.
* **Argos Translate:** An open-source offline translation engine that uses neural machine translation.
* **LibreTranslate:** An open-source machine translation API that can be self-hosted. (Note: External API instance used for this project, leading to connection issues.)
* **Google Translate (Baseline):** Google's proprietary online service, used as a high-quality benchmark.

Detailed descriptions, characteristics, setup notes, and observations for each model can be found in the `03_Translation_Models_Exploration/` directory.

---

## Methodology

To ensure a fair and consistent evaluation, the following methodology was implemented:

* **Dataset:** Publicly available benchmark datasets were used for each language pair, with a subset of 50 sentence pairs selected for quick evaluation.
    * **Burmese-English:** `en-my.tmx.gz`
    * **Chinese-English:** A JSONL dataset with `english` and `chinese` fields.
    * **Hindi-English:** `IITB.en-hi.en` and `IITB.en-hi.hi` files.
* **Metric:** The **BLEU (Bilingual Evaluation Understudy) score** was chosen to quantify translation accuracy.
* **Environment:** All experiments were conducted using Python within a Google Colab environment, utilizing GPU acceleration where available.
* **Libraries:** Hugging Face `transformers` for M2M100, `argostranslate`, `libretranslatepy`, and `googletrans` were used for respective models.

---

## Accuracy Comparison Results (BLEU Scores)

The tables below summarize the BLEU scores obtained for each model across the tested language pairs. Higher BLEU scores indicate better translation quality.

### Burmese-English Translation (MY \(\rightarrow\) EN)

| Model                     | BLEU Score |
| :------------------------ | :--------- |
| Google Translate (Baseline) | 9.14       |
| M2M100 1.2B               | 1.42       |
| M2M100 418M               | 0.72       |
| LibreTranslate            | 0.00       |

### Chinese-English Translation (EN \(\rightarrow\) ZH)

| Model                     | BLEU Score |
| :------------------------ | :--------- |
| Google Translate (Baseline) | 8.88       |
| Argos Translate           | 1.98       |
| M2M100 1.2B               | 7.92       |
| M2M100 418M               | 3.88       |
| LibreTranslate            | 0.00       |

### Hindi-English Translation (EN \(\rightarrow\) HI)

| Model                     | BLEU Score |
| :------------------------ | :--------- |
| Google Translate (Baseline) | 8.86       |
| Argos Translate           | 5.56       |
| M2M100 1.2B               | 4.53       |
| M2M100 418M               | 5.51       |

**Note:** LibreTranslate showed a 0.00 BLEU score for Burmese-English and Chinese-English due to persistent `HTTP Error 400: Bad Request` from the external API instance used during testing. This indicates issues with the server or potential rate limits, not necessarily the model's inherent capability when self-hosted.

---

## Key Observations and Challenges

* **Google Translate Dominance:** Google Translate consistently achieved the highest accuracy, setting a strong benchmark for translation quality.
* **Offline Model Performance:** Among offline models, **M2M100 1.2B** performed best for Chinese-English, demonstrating its strength in well-resourced languages. However, all offline models struggled with low-resource languages like Burmese-English.
* **Resource Requirements:** Larger models like M2M100 1.2B are computationally intensive, requiring significant GPU memory for efficient inference.
* **API Instability:** Reliance on external APIs (like the LibreTranslate instance used) can introduce instability and hinder evaluation.
* **Dataset Limitations:** The limited dataset size (50 sentences per pair) provided a quick benchmark but might not capture real-world performance nuances.

---

## Repository Structure
```
Internship_Project/
├── 01_Reports/
│   ├── Fortnightly_Reports/
│   │   └── Fortnight_1_2025-05-10_to_2025-05-24.pdf
│   └── Final_Report/
├── 02_Cryptography_Research/
│   ├── Concepts_Notes.md
│   └── Code_Snippets_Crypto/
├── 03_Translation_Models_Exploration/
│   ├── Model_M2M100_1.2B/
│   │   └── Description.md
│   ├── Model_M2M100_418M/
│   ├── Model_Argos_Translate/
│   ├── Model_LibreTranslate/
│   ├── Model_Google_Translate/
│   └── Exploration_Log.md
├── 04_Code/
│   ├── Translation_Scripts/
│   │   ├── burmese_english_translation.py
│   │   ├── chinese_english_translation.py
│   │   └── hindi_english_translation.py
│   └── Data_Preprocessing_Scripts/
├── 05_DataSet/
│   ├── Burmese_English/
│   │   └── ReadMe.md
│   ├── Chinese_English/
│   │   └── ReadMe.md
│   └── Hindi_English/
│       └── ReadMe.md
├── 06_Results/
│   ├── Burmese_English_Results/
│   │   ├── burmese_english_raw_output_m2m1b.txt
│   │   └── burmese_english_bleu_scores.csv
│   ├── Chinese_English_Results/
│   ├── Hindi_English_Results/
│   └── Overall_Summary_Results.csv
├── .gitignore
└── README.md
```
---

## Setup and Usage (for Translation Benchmarking)

To replicate the translation benchmarking results:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[YourGitHubUsername]/[YourRepoName].git
    cd [YourRepoName]
    ```

2.  **Navigate to Code Directory:**
    ```bash
    cd 04_Code/Translation_Scripts/
    ```

3.  **Install Dependencies:**
    The scripts require various Python libraries. You can install them using pip:
    ```bash
    pip install -q transformers sentencepiece sacrebleu argostranslate libretranslatepy googletrans==4.0.0-rc1 httpx>=0.28.1
    ```
    *Note: `googletrans==4.0.0-rc1` is specified due to common issues with newer `googletrans` versions.*

4.  **Obtain Datasets:**
    * **Burmese-English:** The `en-my.tmx.gz` file should be uploaded to your Colab environment or placed in `05_Data/Burmese_English/`.
    * **Chinese-English:** A `.jsonl` dataset (e.g., from an online source) needs to be uploaded or placed in `05_Data/Chinese_English/`.
    * **Hindi-English:** `IITB.en-hi.en` and `IITB.en-hi.hi` files should be uploaded or placed in `05_Data/Hindi_English/`.
    *(The Python scripts expect these files to be available in the execution environment or in the specified data paths.)*

5.  **Run the Translation Scripts:**
    Execute each Python script individually:
    ```bash
    python burmese_english_translation.py
    python chinese_english_translation.py
    python hindi_english_translation.py
    ```
    *(Ensure you are running these in an environment with sufficient resources, especially for M2M100 models. Google Colab with GPU is recommended.)*

    *Remember to upload the dataset files to the Colab session or ensure their paths are correctly set in the scripts.*

---



## Contact

For any questions or further information, please feel free to reach out:

Harsh Tripathi
harsht@iitbhilai.ac.in
