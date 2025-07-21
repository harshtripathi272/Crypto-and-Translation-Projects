Internship_Project/
├── 01_Reports/
│   ├── Fortnightly_Reports/
│   │   └── Fortnight_1_2025-05-10_to_2025-05-24.pdf
│   │   └── First_two_week_Project.pdf
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
├── .gitignore
└── README.md
```
---

## Setup and Usage (for Translation Benchmarking)

To replicate the translation benchmarking results:

1.  **Clone the Repository:**
```bash
git clone https://github.com/harshtripathi272/Crypto-and-Translation-Projects.git
cd Crypto-and-Translation-Projects
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
