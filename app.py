from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import pandas as pd

app = Flask(__name__)

def scrape_duunitori():
    url = "https://duunitori.fi/tyopaikat?haku=python"
    content = requests.get(url).text
    soup = BeautifulSoup(content, "lxml")

    jobs = soup.find_all('a', class_='job-box__hover gtm-search-result')
        
    for job in jobs:
        company = job['data-company']
        description = job.text
        # print(company, description)
        return jobs

# data = pd.DataFrame(scrape_duunitori())
# print(data)


# Home page with URL input
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url")
        jobs = scrape_duunitori(url)
        return render_template("results.html", filtered=jobs, count=len(jobs), skill="Custom Search")
    return render_template("home.html")

# Simulate sending request to selected companies
@app.route("/send_request", methods=["POST"])
def send_request():
    selected_ids = request.form.getlist("company")
    selected_companies = [c for c in session.get("jobs", []) if str(c["id"]) in selected_ids]
    return render_template("sent.html", selected=selected_companies)

if __name__ == "__main__":
    app.run(debug=True)
