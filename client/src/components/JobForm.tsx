import React from "react";
import { useState, FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { Autocomplete, TextField, Button, Paper } from "@mui/material";
import Results from "./Results";

const jobOptions = [
  "Software Developer",
  "Data Analyst",
  "Designer",
  "Project Manager",
  "Marketing Specialist",
];

const providerOptions = ["duunitori"];

export const JobForm = () => {
  const [jobRole, setJobRole] = useState<string | null>(null);
  const [provider, setProvider] = useState<string | null>("duunitori");
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    console.log("Submitting form");
    console.log("Job Role:", jobRole);
    console.log("Provider:", provider);

    if (!jobRole) {
      alert("Please select a job role");
      return;
    }

    const title = jobRole;
    console.log("Title:", title);

    try {
      console.log("Fetching from backend...");
      const response = await fetch("http://localhost:5000/scrape", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ keyword: jobRole, provider: provider }),
      });
      console.log("Response status:", response.status);
      const data = await response.json();
      console.log("Response data:", data);

      if (response.ok) {
        console.log("Navigating to results");
        navigate("/results", {
          state: {
            jobs: data.jobs,
            skill: title,
            count: data.total_vacancies,
          },
        });
      } else {
        alert(data.error || "An error occurred");
      }
    } catch (err) {
      console.error("Fetch error:", err);
      alert("Failed to fetch jobs");
    }
  };

  return (
    <div
      style={{
        backgroundColor: "white",
        border: "1px solid #ddd",
        borderRadius: "8px",
        padding: "1rem",
        width: "100%",
        maxWidth: "400px",
      }}
    >
      <form onSubmit={handleSubmit}>
        <Autocomplete
          disablePortal
          options={jobOptions}
          value={jobRole}
          onChange={(event, newValue) => setJobRole(newValue)}
          sx={{ width: "100%", marginBottom: "1rem" }}
          renderInput={(params) => <TextField {...params} label="Job Role" />}
        />

        <Autocomplete
          disablePortal
          options={providerOptions}
          value={provider}
          onChange={(event, newValue) => setProvider(newValue)}
          sx={{ width: "100%", marginBottom: "1rem" }}
          renderInput={(params) => <TextField {...params} label="Provider" />}
        />

        <Button
          type="submit"
          variant="contained"
          fullWidth
          sx={{
            backgroundColor: "#FEDBD0",
            color: "#442C2E",
            border: "1px solid #442C2E",
            "&:hover": {
              backgroundColor: "#FEEAE6",
            },
          }}
        >
          To the list
        </Button>
      </form>
      <Paper sx={{ width: "100%", marginTop: "1rem", padding: "1rem" }}>
        <p>
          <strong>How it works:</strong>
        </p>
        <p>
          1. Select a position from the dropdown or choose "Other (Custom)" to
          enter your own
        </p>
        <p>2. Click "Search Jobs" to find available positions</p>
        <p>3. View company names, contact details, and send applications</p>
      </Paper>
    </div>
  );
};
export default JobForm;
