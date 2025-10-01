from flask import Flask, render_template, request, redirect, url_for, jsonify
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

# Home page: input skill/position
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        skill = request.form.get("skill").lower()
        # Filter companies by skill/workplace
        filtered = [c for c in companies if skill in c.get("workplace", "").lower()]
        count = len(filtered)
        return render_template("results.html", skill=skill, filtered=filtered, count=count)
    return render_template("home.html")

# Send request to selected companies (mock)
@app.route("/send_request", methods=["POST"])
def send_request():
    selected_ids = request.form.getlist("company")
    selected_companies = [c for c in companies if str(c["id"]) in selected_ids]
    # Here you could implement actual sending via email/API
    return render_template("sent.html", selected=selected_companies)

if __name__ == "__main__":
    app.run(debug=True)
