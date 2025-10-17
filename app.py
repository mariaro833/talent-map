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
    """Scrape job listings from Duunitori"""
    jobs = []
    
    try:
        search_url = f"https://duunitori.fi/tyopaikat?haku={quote(keyword)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try multiple selector strategies for Duunitori
        job_cards = soup.find_all('a', {'data-action': 'job-box-click'})
        
        if not job_cards:
            job_cards = soup.find_all('div', class_='job-box')
        
        if not job_cards:
            job_cards = soup.find_all(['article', 'div'], class_=re.compile(r'job|listing|vacancy', re.I))
        
        for card in job_cards[:20]:
            try:
                job_data = {
                    'id': len(jobs) + 1,
                    'name': 'N/A',
                    'title': 'N/A',
                    'workplace': None,
                    'contact': None,
                    'email': None,
                    'phone': None,
                    'url': None
                }
                
                # Extract job title
                title_elem = (card.find('h3', class_='job-box__title') or 
                             card.find('h2', class_='job-box__title') or
                             card.find(class_=re.compile(r'job.*title|title', re.I)) or
                             card.find(['h1', 'h2', 'h3', 'h4']))
                
                if title_elem:
                    job_data['title'] = title_elem.get_text(strip=True)
                
                # Extract company name
                company_elem = (card.find('div', class_='job-box__job-company') or
                               card.find(class_=re.compile(r'company|employer|organization', re.I)) or
                               card.find('span', class_='company'))
                
                if company_elem:
                    job_data['name'] = company_elem.get_text(strip=True)
                
                # Alternative: look for company in nearby elements
                if job_data['name'] == 'N/A':
                    info_divs = card.find_all('div', class_=re.compile(r'info|detail|meta'))
                    for div in info_divs:
                        text = div.get_text(strip=True)
                        if text and len(text) > 2 and len(text) < 100:
                            if not any(keyword in text.lower() for keyword in ['päivä', 'day', 'ago', 'sitten']):
                                job_data['name'] = text
                                break
                
                # Extract location
                location_elem = (card.find('div', class_='job-box__job-location') or
                                card.find(class_=re.compile(r'location|address|city', re.I)))
                if location_elem:
                    job_data['workplace'] = location_elem.get_text(strip=True)
                
                # Extract URL
                if card.name == 'a' and card.get('href'):
                    href = card.get('href')
                    if href.startswith('http'):
                        job_data['url'] = href
                    elif href.startswith('/'):
                        job_data['url'] = f"https://duunitori.fi{href}"
                    else:
                        job_data['url'] = f"https://duunitori.fi/{href}"
                
                # Extract contact information
                card_text = card.get_text()
                
                email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', card_text)
                if email_match:
                    job_data['email'] = email_match.group()
                    job_data['contact'] = email_match.group()
                
                phone_match = re.search(r'\+?358?\s*\(?0?\)?\s*\d{1,3}[\s-]?\d{3,4}[\s-]?\d{3,4}', card_text)
                if phone_match:
                    job_data['phone'] = phone_match.group().strip()
                    if not job_data['contact']:
                        job_data['contact'] = phone_match.group().strip()
                
                if job_data['title'] != 'N/A':
                    jobs.append(job_data)
                
            except Exception as e:
                continue
        
    except Exception as e:
        print(f"Scraping error: {e}")
    
    return jobs

# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         skill = request.form.get("skill", "").strip()
        
#         if not skill:
#             return render_template("home.html", error="Please enter a skill or position")
        
#         # Scrape jobs based on skill
#         jobs = scrape_duunitori(skill)
        
#         return render_template("result.html", 
#                              skill=skill, 
#                              filtered=jobs, 
#                              count=len(jobs))
    
#     return render_template("home.html")

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
    
    # GET request - MUST pass positions here!
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
    app.run(debug=True, host='0.0.0.0', port=5000)
