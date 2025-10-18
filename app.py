from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote
import json
import os


app = Flask(__name__)

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
    "Other (Custom)"
]


def scrape_duunitori(keyword):
    jobs = []
    try:
        search_url = f"https://duunitori.fi/tyopaikat?haku={keyword}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        job_cards = soup.select('a.job-box__hover.gtm-search-result')

        for card in job_cards[:20]:
            try:
                job_data = {
                    'id': len(jobs) + 1,
                    'name': card.get('data-company', 'N/A'),
                    'title': card.get_text(strip=True),
                    'workplace': None,
                    'contact': None,
                    'email': None,
                    'phone': None,
                    'url': f"https://duunitori.fi{card.get('href')}" if card.get('href') else None
                }
                # Try email in card text first
                card_text = card.get_text()
                email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', card_text)
                if email_match:
                    job_data['email'] = email_match.group()
                    job_data['contact'] = email_match.group()

                 # If email not found, try fetching the job page
                if not job_data['email'] and job_data['url']:
                   try:
                         resp2 = requests.get(job_data['url'], headers=headers, timeout=5)
                         page_text = BeautifulSoup(resp2.content, 'html.parser').get_text(separator="\n")
                         email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', page_text)
                         if email_match:
                          job_data['email'] = email_match.group()
                          job_data['contact'] = email_match.group()
                   except Exception:
                    pass

                 # Append job_data to list
                
                jobs.append(job_data)
            except Exception:
                continue
    except Exception as e:
        print(f"Scraping error: {e}")

    return jobs
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        position = request.form.get("position", "").strip()
        custom_skill = request.form.get("customSkill", "").strip()
        
        # Use custom skill if "Other (Custom)" is selected
        skill = custom_skill if position == "Other (Custom)" and custom_skill else position
        
        if not skill:
            return render_template("home.html", 
                                 positions=COMMON_POSITIONS,
                                 error="Please select or enter a position")
        
        # Scrape jobs based on skill
        jobs = scrape_duunitori(skill)
        
        return render_template("result.html", 
                             skill=skill, 
                             filtered=jobs, 
                             count=len(jobs))
    return render_template("home.html", positions=COMMON_POSITIONS)

@app.route('/scrape', methods=['POST'])
def scrape():
    """API endpoint for scraping"""
    try:
        data = request.get_json()
        keyword = data.get('keyword', '').strip()
        provider = data.get('provider', 'duunitori')
        
        if not keyword:
            return jsonify({'error': 'Keyword is required'}), 400
        
        jobs = scrape_duunitori(keyword)
        
        return jsonify({
            'total_vacancies': len(jobs),
            'keyword': keyword,
            'provider': provider,
            'jobs': jobs
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
            selected_companies.append({
                'name': f'Company {idx}',
                'contact': 'contact@company.com'
            })
        except (ValueError, IndexError):
            continue
    
    return render_template("send.html", selected=selected_companies)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
