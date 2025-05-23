# Translation Models Exploration Log

This log details the journey of exploring and selecting models for the offline language translation comparison.

## 2025-05-XX: Initial Research & Tool Discovery

* **Received guidance from supervisor** regarding the scope of translation tasks and the importance of offline capability.
* Began by broadly researching "offline machine translation Python libraries" and "open source NMT models."
* **Explored "Awesome Machine Translation" tools/lists (as suggested by supervisor):** This was a valuable resource for identifying established and emerging translation tools and models. Key takeaways from this exploration included:
    * Recognition of the dominance of Transformer-based models.
    * Understanding the distinction between online APIs and locally deployable models.
    * Identifying potential candidates for offline use, such as various OpenNMT-based systems.
    * Gained insights into common evaluation metrics like BLEU.
* From this initial research and the "Awesome Machine Translation" list, identified several promising candidates for deeper investigation, including:
    * **Hugging Face Transformers:** Specifically, the M2M100 family (1.2B and 418M) due to its extensive multilingual support and pre-trained availability.
    * **Argos Translate:** Appeared to be a strong contender for true offline, privacy-focused desktop applications.
    * **LibreTranslate:** Interesting for its self-hostable API concept, offering control over data.

## 2025-05-YY: Setup Challenges and Initial Impressions of Candidates

* **M2M100 1.2B:**
    * **Setup:** Straightforward using Hugging Face `transformers` library.
    * **Observations:** Noted the substantial download size (~4.7GB) and high GPU memory requirements (approx. 9-10GB VRAM) for efficient inference. CPU inference was very slow. Initial quality impressions were high for well-resourced languages.
* **M2M100 418M:**
    * **Setup:** Identical to the 1.2B version, but with a smaller download (~1.8GB).
    * **Observations:** Lower memory footprint (approx. 3-4GB VRAM) and faster inference than 1.2B, but with a trade-off in perceived translation quality.
* **Argos Translate:**
    * **Setup:** Simple `pip` install, followed by downloading specific language packages (e.g., `en-zh`, `en-hi`).
    * **Observations:** Performed well as a truly offline solution with manageable resource usage. Quality seemed decent for common pairs, but might vary significantly across less common ones.
* **LibreTranslate:**
    * **Setup:** Attempted to use a public `ngrok` tunnel for testing its API functionality with `libretranslatepy`.
    * **Observations:** Encountered persistent `HTTP Error 400: Bad Request` errors. This severely hindered comprehensive testing and reliable quality assessment. Concluded that a self-hosted instance would be necessary for a proper evaluation of this model's capabilities and stability.
* **Google Translate:**
    * **Setup:** Utilized the unofficial `googletrans` library.
    * **Observations:** Served as the high-quality online baseline. Very fast and accurate. Occasional transient connection issues due to the unofficial API.

## 2025-05-ZZ: Dataset Selection and Metric Finalization

* Researched and selected publicly available benchmark datasets for the target language pairs: Hindi-English (IITB), Chinese-English (custom JSONL), and Burmese-English (TMX).
* Decided to extract a subset of 50 sentence pairs from each dataset for initial, quick benchmarking to manage computational resources and time.
* Confirmed **BLEU score** as the primary quantitative evaluation metric for translation quality, given its widespread use in MT research.
* Established a workflow for saving raw translated outputs and calculated BLEU scores for each model and language pair.

## Ongoing Reflections:

* The challenge of finding truly high-quality offline models, especially for low-resource languages, is significant.
* Resource management (GPU memory, CPU cycles) is a major factor when deploying large NMT models locally.
* Reliability of public API endpoints for open-source services can be a bottleneck for robust evaluation; self-hosting provides more control.
* The "Awesome Machine Translation" list was a great starting point for understanding the landscape.