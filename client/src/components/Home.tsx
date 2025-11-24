import { useState, FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import DiamondIcon from "@mui/icons-material/Diamond";
import JobForm from "./JobForm";
import DataBox from "./DataBox";

function Home() {
  // TODO: Add state for form inputs
  // const [position, setPosition] = useState('');
  // const [customSkill, setCustomSkill] = useState('');
  // const [provider, setProvider] = useState('duunitori');
  // const [error, setError] = useState('');
  // const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // TODO: Implement form submission
    // - Validate inputs
    // - Make API call to backend
    // - Handle response and navigate to results

    try {
      const response = await fetch("http://localhost:5000/scrape", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ keyword: skill, provider }),
      });
      const data = await response.json();
      if (response.ok) {
        navigate("/results", {
          state: { jobs: data.jobs, skill, count: data.total_vacancies },
        });
      } else {
        setError(data.error || "An error occurred");
      }
    } catch (err) {
      setError("Failed to fetch jobs");
    }
  };

  return (
    <div
      style={{
        display: "grid",
        gridTemplateAreas: '"header header" "left right"',
        gridTemplateColumns: "1fr 2fr",
        gridTemplateRows: "auto 1fr",
        height: "100vh",
        width: "100vw",
      }}
    >
      <div
        style={{
          gridArea: "header",
          backgroundColor: "#FEDBD0",
          color: "#443C2E",
          padding: "1rem",
          display: "flex",
          justifyContent: "flex-start",
          alignItems: "center",
        }}
      >
        <DiamondIcon
          style={{ fontSize: "2rem", color: "#443C2E", marginRight: "0.5rem" }}
        />
        <h2>TalentMap</h2>
      </div>
      <div
        style={{
          gridArea: "left",
          backgroundColor: "#FEEAE6",
          padding: "1rem",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <JobForm />
        <div class="info-box">
          <p>
            <strong>ℹHow it works:</strong>
          </p>
          <p>
            1. Select a position from the dropdown or choose "Other (Custom)" to
            enter your own
          </p>
          <p>2. Click "Search Jobs" to find available positions</p>
          <p>3. View company names, contact details, and send applications</p>
        </div>
      </div>
      <div
        style={{
          gridArea: "right",
          backgroundColor: "#f0f0f0",
          padding: "1rem",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <DataBox />
      </div>
    </div>
  );
}

export default Home;
