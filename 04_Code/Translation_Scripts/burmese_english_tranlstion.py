# === 1. Install Dependencies ===
# These commands are typically run in a Colab notebook cell or before running the script
# !pip install -q transformers sentencepiece sacrebleu argostranslate libretranslatepy googletrans==4.0.0-rc1 httpx>=0.28.1

# === 2. Import Libraries ===
import json, gzip, time
import xml.etree.ElementTree as ET
import torch
import sacrebleu
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from googletrans import Translator
from argostranslate import package, translate
from libretranslatepy import LibreTranslateAPI
import os 


# Adjust paths if your script is not run from the root of 'Internship_Project/'
tmx_file_path = os.path.join('..', '..', '05_Data', 'Burmese_English', 'en-my.tmx.gz')

# === 4. Parse TMX file (Burmese: 'my', English: 'en') ===
en_sentences = []
my_sentences = []

try:
    with gzip.open(tmx_file_path, "rb") as f:
        tree = ET.parse(f)
        root = tree.getroot()

    for tu in root.findall(".//tu"):
        langs = {}
        for tuv in tu.findall("tuv"):
            lang = tuv.attrib.get("{http://www.w3.org/XML/1998/namespace}lang")
            seg = tuv.find("seg")
            if lang and seg is not None and seg.text:
                langs[lang] = seg.text.strip()
        if "en" in langs and "my" in langs:
            en_sentences.append(langs["en"])
            my_sentences.append(langs["my"])
except FileNotFoundError:
    print(f"Error: {tmx_file_path} not found. Please ensure the dataset is in the correct path.")
    exit() # Exit if dataset is not found

# === 3. Limit to first 50 for quick benchmarking ===
en_sentences = en_sentences[:50]
my_sentences = my_sentences[:50]

print(f"✅ Loaded {len(en_sentences)} English and {len(my_sentences)} Burmese sentences.")
print("🔍 Example:")
if en_sentences and my_sentences:
    print("MY:", my_sentences[0])
    print("EN:", en_sentences[0])
else:
    print("No sentences loaded. Check dataset.")
    exit()


#=== 5. Argos Translate Setup (Skipped for Burmese in original script, keeping commented for consistency) ===
def translate_argos(sentences):
    #Need to install Burmese-English package if available
    available_packages = package.get_available_packages()
    my_en_package = next((p for p in available_packages if p.from_code == "my" and p.to_code == "en"), None)
    if my_en_package:
        package.install_from_path(my_en_package.download())
    installed_languages = translate.get_installed_languages()
    my_lang = next(filter(lambda x: x.code == "my", installed_languages))
    en_lang = next(filter(lambda x: x.code == "en", installed_languages))
    argos_translator = my_lang.get_translation(en_lang)
    return [argos_translator.translate(s) for s in sentences]


# === 6. Device Setup ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("🚀 Using device:", device)

# === 7. Load M2M100 Models ===
def load_m2m_model(model_name):
    print(f"Loading {model_name}...")
    tokenizer = M2M100Tokenizer.from_pretrained(model_name)
    model = M2M100ForConditionalGeneration.from_pretrained(model_name).to(device)
    print(f"Finished loading {model_name}.")
    return tokenizer, model

tokenizer_1b, model_1b = load_m2m_model("facebook/m2m100_1.2B")
tokenizer_418m, model_418m = load_m2m_model("facebook/m2m100_418M")

def translate_m2m(sentences, tokenizer, model, src_lang="my", tgt_lang="en", batch_size=4):
    tokenizer.src_lang = src_lang
    results = []
    for i in range(0, len(sentences), batch_size):
        batch = sentences[i:i+batch_size]
        if not batch: # Handle empty batch if remaining sentences are less than batch_size
            continue
        encoded = tokenizer(batch, return_tensors="pt", padding=True, truncation=True).to(device)
        generated = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id(tgt_lang))
        decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)
        results.extend(decoded)
    return results

# === 8. LibreTranslate ===
def translate_libre(sentences, src_lang="my", tgt_lang="en"):
    # Ensure this URL is stable or run a local LibreTranslate server
    lt = LibreTranslateAPI("https://b458-49-43-7-49.ngrok-free.app") # Use your own LibreTranslate API as i locally ran it and then hosted it publicly 
    translations = []
    for text in sentences:
        try:
            if not text.strip():
                translations.append("")
                continue
            translated = lt.translate(text, source=src_lang, target=tgt_lang)
            translations.append(translated)
        except Exception as e:
            print(f"❌ LibreTranslate error for '{text[:50]}...': {e}")
            translations.append("[ERROR]") # Append an error placeholder
            time.sleep(1) # Be respectful to the API
    return translations

# === 9. Google Translate ===
translator = Translator()
def translate_google(sentences, src_lang="my", tgt_lang="en"):
    results = []
    for s in sentences:
        try:
            translated_text = translator.translate(s, src=src_lang, dest=tgt_lang).text
            results.append(translated_text)
        except Exception as e:
            print(f"❌ Google Translate error for '{s[:50]}...': {e}")
            results.append("[ERROR]")
            time.sleep(1) # Avoid hitting rate limits
    return results

# === 10. BLEU Score ===
def compute_bleu(hypotheses, references):
    # Ensure all hypotheses are strings. Replace any non-string errors with an empty string.
    hypotheses = [str(h) if isinstance(h, str) else "" for h in hypotheses]
    # sacrebleu expects references as a list of lists of references, e.g., [['ref1'], ['ref2']]
    references = [[ref] for ref in references]
    bleu = sacrebleu.corpus_bleu(hypotheses, references)
    return bleu.score

# === 11. Run Translations and Save Raw Outputs ===
output_dir = os.path.join('..', '..', '06_Results', 'Burmese_English_Results')
os.makedirs(output_dir, exist_ok=True) # Ensure output directory exists

# --- M2M100 1.2B ---
print("M2M100 1.2B...")
m2m100_1b_translations = translate_m2m(my_sentences, tokenizer_1b, model_1b)
with open(os.path.join(output_dir, 'burmese_english_raw_output_m2m1b.txt'), 'w', encoding='utf-8') as f:
    for s in m2m100_1b_translations:
        f.write(s + '\n')

# --- M2M100 418M ---
print("M2M100 418M...")
m2m100_418m_translations = translate_m2m(my_sentences, tokenizer_418m, model_418m)
with open(os.path.join(output_dir, 'burmese_english_raw_output_m2m418m.txt'), 'w', encoding='utf-8') as f:
    for s in m2m100_418m_translations:
        f.write(s + '\n')

# --- Google Translate ---
print("Google Translate...")
google_translations = translate_google(my_sentences)
with open(os.path.join(output_dir, 'burmese_english_raw_output_google.txt'), 'w', encoding='utf-8') as f:
    for s in google_translations:
        f.write(s + '\n')

# --- LibreTranslate ---
print("LibreTranslate...")
libre_translations = translate_libre(my_sentences)
with open(os.path.join(output_dir, 'burmese_english_raw_output_libretranslate.txt'), 'w', encoding='utf-8') as f:
    for s in libre_translations:
        f.write(s + '\n')

# === 12. Report BLEU Scores and Save to CSV ===
bleu_scores = {
    "Google Translate": compute_bleu(google_translations, en_sentences),
    "M2M100 1.2B": compute_bleu(m2m100_1b_translations, en_sentences),
    "M2M100 418M": compute_bleu(m2m100_418m_translations, en_sentences),
    "LibreTranslate": compute_bleu(libre_translations, en_sentences)
}

print("\n=== BLEU SCORES (MY → EN) ===")
for model_name, score in bleu_scores.items():
    print(f"{model_name}: {score:.2f}")

# Save to CSV
csv_path = os.path.join(output_dir, 'burmese_english_bleu_scores.csv')
with open(csv_path, 'w', encoding='utf-8') as f:
    f.write("Model,BLEU_Score\n")
    for model_name, score in bleu_scores.items():
        f.write(f"{model_name},{score:.2f}\n")
print(f"\n✅ BLEU scores saved to {csv_path}")