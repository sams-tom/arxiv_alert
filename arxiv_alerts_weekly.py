import feedparser
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import os
from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_abstract(abstract):
    summary = summarizer(abstract, max_length=80, min_length=20, do_sample=False)
    return summary[0]['summary_text']


keywords = [
    "marine robotics", "underwater", "AUV", "side scan", "bathymetry",
    "multimodal fusion", "multimodal machine learning", "knowledge distillation",
    "uncertainty quantification", "BNN", "hyperspectral", "SWIR", "bayesian neural network", 
    "Autonomous Underwater Vehicle", "Uncertainty", "Computer Vision"
]
# ----------------
# SETTINGS
# ----------------
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")

# ----------------
# ARXIV QUERY
# ----------------
search_query = "cat:cs.RO+OR+cat:cs.CV+OR+cat:stat.ML"
base_url = "http://export.arxiv.org/api/query?"
search_query = "cat:cs.RO+OR+cat:cs.CV+OR+cat:stat.ML"
url = f"{base_url}search_query={search_query}&start=0&max_results=5000&sortBy=submittedDate&sortOrder=descending"

feed = feedparser.parse(url)

# ----------------
# FILTER LAST 7 DAYS + KEYWORD SCORE
# ----------------
one_week_ago = datetime.utcnow() - timedelta(days=7)

recent_entries = []

for entry in feed.entries:
    pub_date = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ")
    if pub_date < one_week_ago:
        continue

    text = (entry["title"] + " " + entry["summary"]).lower()
    score = sum(1 for kw in keywords if kw.lower() in text)
    
    if score > 0:
       full_summary = entry["summary"].replace("\n", " ").strip()
       summary = summarize_abstract(full_summary)
       recent_entries.append({
    "title": entry["title"],
    "link": entry["link"],
    "authors": entry["authors"],
    "summary": summary, 
    "published": pub_date.strftime("%Y-%m-%d"),
    "score": score
})



print(f"Found {len(recent_entries)} new papers this week.")

# ----------------
# CATEGORY COLORS
# ----------------
category_colors = {
    "cs.RO": "#1f77b4",     # blue
    "cs.CV": "#ff7f0e",     # orange
    "stat.ML": "#2ca02c"    # green
}

# ----------------
# BUILD HTML CONTENT
# ----------------
today = datetime.today().strftime("%Y-%m-%d")
html_content = f"""
<html>
<head>
<style>
body {{ font-family: Arial, sans-serif; }}
h1 {{ color: #333; }}
h2 {{ margin-top: 20px; }}
.summary {{ margin-bottom: 15px; }}
details {{ margin-bottom: 10px; }}
</style>
</head>
<body>
<h1>arXiv Weekly Digest – {today}</h1>
<p>Filtered by categories: cs.RO, cs.CV, stat.ML | Keywords: marine, underwater, multimodal</p>
<hr>
<h2>Table of Contents</h2>
<ul>
"""

# Build TOC
for i, entry in enumerate(recent_entries):
    title = entry["title"]
    html_content += f'<li><a href="#paper{i}">{title}</a></li>\n'

# Add papers with collapsible abstracts
for i, entry in enumerate(recent_entries):
    title = entry["title"]
    if "authors" in entry and entry["authors"]:
        authors = ", ".join(author.get("name", "Unknown") for author in entry["authors"])
    else:
        authors = "Unknown"
    link = entry["link"]
    summary = entry["summary"].replace("\n", " ").strip()
    main_cat = entry["tags"][0]["term"] if "tags" in entry and entry["tags"] else "cs.RO"
    color = category_colors.get(main_cat, "#000000")

    html_content += f"""
    <h2 id="paper{i}" style="color:{color};"><a href="{link}">{title}</a> [{main_cat}]</h2>
    <p><strong>Authors:</strong> {authors}</p>
    <details>
      <summary>Abstract (click to expand)</summary>
      <p class="summary">{summary}</p>
    </details>
    <hr>
    """


if not recent_entries:
    html_content += "<p>No new papers this week.</p>"

html_content += "</body></html>"

# ----------------
# SEND EMAIL
# ----------------
msg = MIMEMultipart("alternative")
msg["From"] = EMAIL_ADDRESS
msg["To"] = TO_EMAIL
msg["Subject"] = f"Weekly arXiv Digest – {today}"
msg.attach(MIMEText(html_content, "html"))

try:
   with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        print(f"Weekly newsletter sent to {TO_EMAIL} with {len(recent_entries)} papers.")
except Exception as e:
    print("Error sending email:", e)
