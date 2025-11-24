# TalentMap

A full-stack application for finding internship opportunities in Finland. The backend scrapes job listings from Duunitori.fi, and the frontend provides a modern React interface to search and select companies for internship applications.

## Features

- **Job Scraping**: Search for job positions and scrape contact information from Duunitori.fi
- **Modern UI**: React frontend with TypeScript for a smooth user experience
- **Docker Ready**: Easily deployable with Docker Compose
- **Database Integration**: MongoDB for storing company data

## Tech Stack

- **Backend**: Python Flask with BeautifulSoup for scraping
- **Frontend**: React with TypeScript and Vite
- **Database**: MongoDB
- **Deployment**: Docker & Docker Compose

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd talent-map
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - MongoDB: localhost:27017

## Development

### Backend

```bash
cd talent-map
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd client
npm install
npm run dev
```

## API Endpoints

- `POST /scrape`: Scrape jobs for a given keyword
  - Body: `{"keyword": "Python Developer", "provider": "duunitori"}`
  - Returns: Job listings with contact information

## Environment Variables

- `MONGO_URI`: MongoDB connection string (default: localhost)

## License

MIT