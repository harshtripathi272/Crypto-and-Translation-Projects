# === 1. Install Dependencies ===
# !pip install -q transformers sentencepiece sacrebleu argostranslate libretranslatepy googletrans==4.0.0-rc1

# === 2. Import Libraries ===
import os
import sacrebleu
import torch # Import torch for device handling
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from googletrans import Translator
# from libretranslatepy import LibreTranslateAPI # Commented out as in original script
from argostranslate import package, translate

# === 3. Assuming Data Files are in '05_Data/Hindi_English/' ===
en_file_path = os.path.join('..', '..', '05_Data', 'Hindi_English', 'IITB.en-hi.en')
hi_file_path = os.path.join('..', '..', '05_Data', 'Hindi_English', 'IITB.en-hi.hi')

# Read the files
try:
    with open(en_file_path, encoding='utf-8') as f:
        en_sentences = [line.strip() for line in f.readlines() if line.strip()]
    with open(hi_file_path, encoding='utf-8') as f:
        hi_references = [line.strip() for line in f.readlines() if line.strip()]
except FileNotFoundError:
    print(f"Error: Dataset files ({en_file_path}, {hi_file_path}) not found. Please ensure datasets are in the correct path.")
    exit()

# Limit number for fast testing
en_sentences = en_sentences[:50]
hi_references = hi_references[:50]

print(f"Loaded {len(en_sentences)} English and {len(hi_references)} Hindi sentences.")
print("🔍 Example:")
if en_sentences and hi_references:
    print("EN:", en_sentences[0])
    print("HI:", hi_references[0])
else:
    print("No sentences loaded. Check dataset.")
    exit()


# === 4. Argos Translate Setup ===
print("Setting up Argos Translate (en -> hi)...")
try:
    package.update_package_index() # Update index to find packages
    available_packages = package.get_available_packages()
    # Find the correct package: from English to Hindi
    en_hi_package = next((p for p in available_packages if p.from_code == "en" and p.to_code == "hi"), None)

    if en_hi_package:
        if not package.is_installed(en_hi_package): # Check if already installed
            print("Installing Argos Translate en-hi package...")
            package.install_from_path(en_hi_package.download())
            print("Argos Translate en-hi package installed.")
        else:
            print("Argos Translate en-hi package already installed.")
    else:
        print("Warning: Argos Translate en-hi package not found in available packages.")
        argos_translator = None

    if en_hi_package and package.is_installed(en_hi_package):
        installed_languages = translate.get_installed_languages()
        en_lang = next(filter(lambda x: x.code == "en", installed_languages))
        hi_lang = next(filter(lambda x: x.code == "hi", installed_languages))
        argos_translator = en_lang.get_translation(hi_lang)
    else:
        argos_translator = None
        print("Argos Translate en-hi translation not available or not installed.")

except Exception as e:
    print(f"Error setting up Argos Translate: {e}")
    argos_translator = None


def translate_argos(sentences):
    if not argos_translator:
        print("Argos Translate not initialized. Skipping.")
        return ["[ERROR]" for _ in sentences]
    results = []
    for s in sentences:
        try:
            translated = argos_translator.translate(s)
            results.append(translated)
        except Exception as e:
            print(f" Argos Translate error for '{s[:50]}...': {e}")
            results.append("[ERROR]")
    return results


# === 5. Device Setup ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(" Using device:", device)

# === 6. HuggingFace M2M100 (1.2B) ===
def load_m2m_model(model_name):
    print(f"Loading {model_name}...")
    tokenizer = M2M100Tokenizer.from_pretrained(model_name)
    model = M2M100ForConditionalGeneration.from_pretrained(model_name).to(device)
    print(f"Finished loading {model_name}.")
    return tokenizer, model

tokenizer_1b, model_1b = load_m2m_model("facebook/m2m100_1.2B")
tokenizer_418m, model_418m = load_m2m_model("facebook/m2m100_418M")

def translate_m2m(sentences, tokenizer, model, src_lang="en", tgt_lang="hi", batch_size=4):
    tokenizer.src_lang = src_lang
    results = []
    for i in range(0, len(sentences), batch_size):
        batch = sentences[i:i+batch_size]
        if not batch:
            continue
        encoded = tokenizer(batch, return_tensors="pt", padding=True, truncation=True).to(device)
        generated = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id(tgt_lang))
        decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)
        results.extend(decoded)
    return results


# === 7. Google Translate ===
translator = Translator()
def translate_google(sentences, src_lang="en", tgt_lang="hi"):
    results = []
    for s in sentences:
        try:
            translated_text = translator.translate(s, src=src_lang, dest=tgt_lang).text
            results.append(translated_text)
        except Exception as e:
            print(f" Google Translate error for '{s[:50]}...': {e}")
            results.append("[ERROR]")
            time.sleep(1) # Avoid hitting rate limits
    return results


# === 8. LibreTranslate (Commented out as in original script, keep this way if not testing) ===
lt = LibreTranslateAPI("https://b458-49-43-7-49.ngrok-free.app")    # or your local server
def translate_libre(sentences, src_lang="en", tgt_lang="hi"):
   translations = []
   for text in sentences:
       try:
           if not text.strip():
               translations.append("")
               continue
           translated = lt.translate(text, source=src_lang, target=tgt_lang)
           translations.append(translated)
       except Exception as e:
           print(f"ibreTranslate failed for: {text[:30]}... | Error: {e}")
           translations.append("[ERROR]")
           time.sleep(1)
   return translations

# === 9. BLEU Score Function ===
def compute_bleu(hypotheses, references):
    hypotheses = [str(h) if isinstance(h, str) else "" for h in hypotheses]
    references = [[ref] for ref in references]
    bleu = sacrebleu.corpus_bleu(hypotheses, references)
    return bleu.score

# === 10. Run Translations and Save Raw Outputs ===
output_dir = os.path.join('..', '..', '06_Results', 'Hindi_English_Results')
os.makedirs(output_dir, exist_ok=True) # Ensure output directory exists

# --- Argos Translate ---
print("🔄 Translating with Argos...")
argos_translations = translate_argos(en_sentences)
with open(os.path.join(output_dir, 'hindi_english_raw_output_argos.txt'), 'w', encoding='utf-8') as f:
    for s in argos_translations:
        f.write(s + '\n')

# --- M2M100 1.2B ---
print("🔄 Translating with M2M100 1.2B...")
m2m100_1b_translations = translate_m2m(en_sentences, tokenizer_1b, model_1b)
with open(os.path.join(output_dir, 'hindi_english_raw_output_m2m1b.txt'), 'w', encoding='utf-8') as f:
    for s in m2m100_1b_translations:
        f.write(s + '\n')

# --- M2M100 418M ---
print("🔄 Translating with M2M100 418M...")
m2m100_418m_translations = translate_m2m(en_sentences, tokenizer_418m, model_418m)
with open(os.path.join(output_dir, 'hindi_english_raw_output_m2m418m.txt'), 'w', encoding='utf-8') as f:
    for s in m2m100_418m_translations:
        f.write(s + '\n')

# --- Google Translate ---
print("🔄 Translating with Google Translate...")
google_translations = translate_google(en_sentences)
with open(os.path.join(output_dir, 'hindi_english_raw_output_google.txt'), 'w', encoding='utf-8') as f:
    for s in google_translations:
        f.write(s + '\n')

# --- LibreTranslate (if uncommented and used) ---
print("🔄 Translating with LibreTranslate...")
libre_translations = translate_libre(en_sentences)
with open(os.path.join(output_dir, 'hindi_english_raw_output_libretranslate.txt'), 'w', encoding='utf-8') as f:
    for s in libre_translations:
        f.write(s + '\n')


# === 11. BLEU Comparison and Save to CSV ===
bleu_scores = {
    "Google Translate": compute_bleu(google_translations, hi_references),
    "Argos Translate": compute_bleu(argos_translations, hi_references),
    "M2M100 1.2B": compute_bleu(m2m100_1b_translations, hi_references),
    "M2M100 418M": compute_bleu(m2m100_418m_translations, hi_references)
    # "LibreTranslate": compute_bleu(libre_translations, hi_references) # Uncomment if used
}

print("\n=== BLEU SCORES (EN → HI) ===")
for model_name, score in bleu_scores.items():
    print(f"{model_name}: {score:.2f}")

# Save to CSV
csv_path = os.path.join(output_dir, 'hindi_english_bleu_scores.csv')
with open(csv_path, 'w', encoding='utf-8') as f:
    f.write("Model,BLEU_Score\n")
    for model_name, score in bleu_scores.items():
        f.write(f"{model_name},{score:.2f}\n")
print(f"\nBLEU scores saved to {csv_path}")