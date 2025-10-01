
# Weekly arXiv Newsletter

Automatically generate a **weekly newsletter of arXiv papers** in your research areas, summarize abstracts using a small transformer model, and email it to yourself. 

---

## Features

- Queries **arXiv categories**: `cs.RO` (Robotics), `cs.CV` (Computer Vision), `stat.ML` (Machine Learning). (This can be change to include other arXivs.  
- Filters papers from the **last 7 days**.  
- Scores papers based on your **keywords**.  
- Keeps only the **top 20 papers** per week. (top defined as those with the most keyword hits)  
- Summarizes abstracts into **1–2 sentence summaries** using a transformer model (`sshleifer/distilbart-cnn-12-6`).  
- Generates an **HTML newsletter** with collapsible abstracts.  
- Sends the newsletter via **email**.

---

## Getting Started (Fork & Setup)

### 1. Fork the Repository

Click **Fork** to create your own copy. All your changes (keywords, emails) will be private to your fork.

### 2. Add GitHub Secrets

Go to your fork → **Settings → Secrets and variables → Actions → New repository secret**. Add:

| Secret Name       | Description |
|------------------|------------|
| `EMAIL_ADDRESS`   | The email that will send an email ( This must be a gmail account unless you edit the code). |
| `EMAIL_PASSWORD`  | Your **app password**, not your normal login password. [Gmail App Passwords] Go down to "create and use App passwords, copy the password when shown as youre only shown it once: (https://support.google.com/accounts/answer/185833?hl=en) |
| `TO_EMAIL`        | Where to send the newsletter (can be the same as `EMAIL_ADDRESS`). |

> ⚠️ Never include passwords or API keys directly in the code.

### 3. Customize Keywords & Categories

Edit `arxiv_alerts_weekly.py`:

- **Keywords**: Focus on your interests (e.g., robotics, marine sensing, ML). I suggest you give chatgpt a couple of paragraphs about your work and get it to spam keywords back at you. 
- **Categories**: Default: `cs.RO`, `cs.CV`, `stat.ML`. You can add more from [arXiv category list](https://arxiv.org/category_taxonomy).  
- **Top papers**: Default keeps the top 20; adjust if you want more.
Current keywords are:
```python 
keywords = [
    # Robotics & marine vehicles
    "marine robotics", "underwater robotics", "AUV", "autonomous underwater vehicle",
    "ROV", "remotely operated vehicle", "glider", "surface vehicle", "drone",
    
    # Sensing modalities
    "side scan sonar", "multibeam sonar", "bathymetry", "imagery", "photogrammetry",
    "multimodal sensing", "multimodal fusion", "hyperspectral", "SWIR", "thermal imaging",
    "optical imagery", "lidar", "acoustic imaging", "sonar imaging",
    
    # Machine learning & modeling
    "multimodal machine learning", "knowledge distillation", "deep learning",
    "bayesian neural network", "BNN", "uncertainty quantification", "probabilistic model",
    "computer vision", "image processing", "feature extraction", "sensor fusion",
    
    # Applications
    "benthic habitat mapping", "carbon mapping", "intertidal sediments",
    "environmental monitoring", "marine ecology", "seafloor mapping",
    
    # Techniques & methods
    "model robustness", "data augmentation", "simulation", "domain adaptation",
    "transfer learning", "predictive modeling", "sensor degradation", "noise robustness",
    
    # Keywords variations
    "uncertainty", "bayesian inference", "posterior predictive", "error estimation",
    "confidence estimation", "probabilistic prediction", "multimodal integration"
]
```
4. Workflow

The workflow .github/workflows/arxiv_newsletter.yml:

Runs every Monday at 09:00 UTC.

Can also be manually triggered from GitHub Actions.

Automatically installs dependencies (feedparser, transformers, torch) and runs the script.

5. Output

Sends an HTML email containing:

Table of contents linking to papers

Collapsible abstracts

Summarized abstracts

Authors, categories, and arXiv links

6. Tips

Regularly update keywords to capture new research trends.

Use ChatGPT to generate large lists of allied keywords.

Adjust max_results in the arXiv query to fetch more papers:
(its the 5000 in the url below, increase this if required)

url = f"{base_url}search_query={search_query}&start=0&max_results=5000&sortBy=submittedDate&sortOrder=descending"

7. Support / Contributions

Fork, customize, and submit pull requests if you improve keywords, add categories, or enhance formatting.



---

