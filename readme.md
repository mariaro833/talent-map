# TalentMap - Job Scraper & Application Tracker

This Flask web application was created as a fun training project to explore 
web scraping methodologies using **BeautifulSoup4**, **Requests**, and other 
Python libraries. 

The application automates the internship search process by:
- Scraping job listings from Finnish job portals (Duunitori.fi)
- Extracting and organizing company information
- Collecting contact details (emails, phone numbers)
- Streamlining the application workflow

**Built with:** Flask, BeautifulSoup4, Requests, and a passion for automation! 

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd talent-map-2
```

2. **Create a virtual environment**

**On Windows (PowerShell):**
```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

**On Linux/Mac/WSL:**
```bash
python3 -m venv env
source env/bin/activate
```

3. **Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
```
http://localhost:5000
```

## Project Structure

```
talent-map-2/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── companies.json         # Stored company data (auto-generated)
├── templates/
│   ├── home.html         # Homepage with search form
│   ├── result.html       # Search results page
│   └── send.html         # Confirmation page
└── README.md             # This file
```

## 🛠️ Technologies Used

- **Backend:** Flask 3.1.0
- **Web Scraping:** BeautifulSoup4, Requests
- **Data Processing:** Python, JSON
- **Frontend:** HTML5, CSS3, JavaScript
- **Styling:** Custom CSS with gradient designs

## Available Job Positions

The app comes pre-configured with common tech positions:

- Python Developer
- Data Analyst
- Data Scientist
- Software Engineer
- Frontend Developer
- Backend Developer
- Full Stack Developer
- DevOps Engineer
- Machine Learning Engineer
- Business Analyst
- Project Manager
- UX/UI Designer
- Quality Assurance
- System Administrator
- Database Administrator
- Custom position (user input)

## Features in Detail

### Home Page
- Dropdown menu with pre-defined positions
- Custom skill input for specialized searches
- Provider selection (currently supports Duunitori.fi)
- Informative help section

### Results Page
- Dynamic job scraping from Duunitori.fi
- Company cards with hover effects
- Checkbox selection for multiple companies
- "Select All" functionality
- Contact information display
- Link to original job postings

### Send Page
- Confirmation of selected companies
- Success animation
- Company list with contact details
- Navigation back to search

## 🔧 Configuration

### Modify Job Positions

Edit the `COMMON_POSITIONS` list in `app.py`:

```python
COMMON_POSITIONS = [
    "Your Position 1",
    "Your Position 2",
    # Add more positions
]
```

### Change Port

Modify the last line in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change port here
```

## Usage

1. **Select a Position**
   - Choose from dropdown or select "Other (Custom)" for custom input

2. **Search Jobs**
   - Click "Search Jobs" button
   - Wait for scraping to complete

3. **Select Companies**
   - Review the results
   - Check boxes next to companies you're interested in
   - Use "Select All" for bulk selection

4. **Send Requests**
   - Click "Send Request to Selected Companies"
   - View confirmation page

## 🐛 Troubleshooting

### Import Error: Flask not found
```bash
# Make sure virtual environment is activated
source env/bin/activate  # Linux/Mac
.\env\Scripts\Activate.ps1  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### No results found
- Try different search keywords
- Check your internet connection
- Duunitori.fi structure might have changed

### Port already in use
```bash
# Change port in app.py or kill the process
# Linux/Mac:
lsof -ti:5000 | xargs kill -9

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- **Maria Rohnonen, Tatiana Orlova**

## Support

If you have any questions or run into issues, please open an issue on GitHub.

## Future Enhancements

- [ ] Add more job providers (LinkedIn, Indeed, etc.)
- [ ] Email integration for sending applications
- [ ] Save favorite companies
- [ ] Export results to CSV/Excel
- [ ] User authentication and profiles
- [ ] Application tracking dashboard
- [ ] Email templates for applications
- [ ] Advanced filtering options

## Version History

- **v1.0.0** - Initial release
  - Basic job scraping functionality
  - Modern UI with gradient design
  - Company selection and tracking

---

Created with Love for job seekers in Finland
