from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote
import json
import os
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_FILE = "companies.json"

# Load data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        companies = json.load(f)
else:
    companies = []


# Save helper
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(companies, f, ensure_ascii=False, indent=4)


# Common job positions for dropdown
COMMON_POSITIONS = [
    "Python Developer",
    "Data Analyst",
    "Data Scientist",
    "Software Engineer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "DevOps Engineer",
    "Machine Learning Engineer",
    "Business Analyst",
    "Project Manager",
    "UX/UI Designer",
    "Quality Assurance",
    "System Administrator",
    "Database Administrator",
    "Other (Custom)",
]


def scrape_duunitori(keyword: str) -> list:
    jobs = []
    try:
        logger.info(f"Scraping jobs for keyword: {keyword}")
        search_url = f"https://duunitori.fi/tyopaikat?haku={quote(keyword)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        job_cards = soup.select("a.job-box__hover.gtm-search-result")
        logger.info(f"Found {len(job_cards)} job cards")

        for i, card in enumerate(job_cards[:20]):
            try:
                job_data = {
                    "id": i + 1,
                    "name": card.get("data-company", "N/A"),
                    "title": card.get_text(strip=True),
                    "workplace": None,
                    "contact": None,
                    "email": None,
                    "phone": None,
                    "url": f"https://duunitori.fi{card.get('href')}"
                    if card.get("href")
                    else None,
                }
                # Try email in card text first
                card_text = card.get_text()
                email_match = re.search(
                    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", card_text
                )
                if email_match:
                    job_data["email"] = email_match.group()
                    job_data["contact"] = email_match.group()

                # If email not found, try fetching the job page
                if not job_data["email"] and job_data["url"]:
                    try:
                        resp2 = requests.get(
                            job_data["url"], headers=headers, timeout=5
                        )
                        resp2.raise_for_status()
                        page_text = BeautifulSoup(
                            resp2.content, "html.parser"
                        ).get_text(separator="\n")
                        email_match = re.search(
                            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                            page_text,
                        )
                        if email_match:
                            job_data["email"] = email_match.group()
                            job_data["contact"] = email_match.group()
                    except requests.RequestException as e:
                        logger.warning(
                            f"Failed to fetch job page {job_data['url']}: {e}"
                        )

                jobs.append(job_data)
            except Exception as e:
                logger.error(f"Error processing job card {i}: {e}")
                continue
    except requests.RequestException as e:
        logger.error(f"Scraping error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during scraping: {e}")

    logger.info(f"Scraped {len(jobs)} jobs")
    return jobs


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        position = request.form.get("position", "").strip()
        custom_skill = request.form.get("customSkill", "").strip()

        # Use custom skill if "Other (Custom)" is selected
        skill = (
            custom_skill if position == "Other (Custom)" and custom_skill else position
        )

        if not skill:
            return render_template(
                "home.html",
                positions=COMMON_POSITIONS,
                error="Please select or enter a position",
            )

        # Scrape jobs based on skill
        jobs = scrape_duunitori(skill)

        return render_template(
            "result.html", skill=skill, filtered=jobs, count=len(jobs)
        )
    return render_template("home.html", positions=COMMON_POSITIONS)


@app.route("/scrape", methods=["POST"])
def scrape():
    """API endpoint for scraping"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON payload required"}), 400

        keyword = data.get("keyword", "").strip()
        provider = data.get("provider", "duunitori")

        if not keyword:
            return jsonify({"error": "Keyword is required"}), 400

        if len(keyword) > 100:
            return jsonify({"error": "Keyword too long"}), 400

        if provider not in ["duunitori"]:
            return jsonify({"error": "Invalid provider"}), 400

        jobs = scrape_duunitori(keyword)

        return jsonify(
            {
                "total_vacancies": len(jobs),
                "keyword": keyword,
                "provider": provider,
                "jobs": jobs,
            }
        )

    except Exception as e:
        logger.error(f"Scrape API error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/send_request", methods=["POST"])
def send_request():
    """Handle sending internship requests"""
    selected_indices = request.form.getlist("company")

    # Load the companies data to get full details
    selected_companies = []

    for idx in selected_indices:
        try:
            # Find company by ID
            company_id = int(idx)
            # In a real app, you'd fetch from database or session
            # For now, create a mock response
            selected_companies.append(
                {"name": f"Company {idx}", "contact": "contact@company.com"}
            )
        except (ValueError, IndexError):
            continue

    return render_template("send.html", selected=selected_companies)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
