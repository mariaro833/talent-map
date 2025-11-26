import React, { useState, FormEvent } from "react";
import { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import {
  Checkbox,
  FormControlLabel,
  Button,
  Typography,
  Box,
  TextField,
} from "@mui/material";

interface Job {
  id: number;
  name: string;
  title: string;
  workplace?: string;
  contact?: string;
  email?: string;
  phone?: string;
  url?: string;
}

interface LocationState {
  jobs: Job[];
  skill: string;
  count: number;
}

function Results() {
  const [selectedCompanies, setSelectedCompanies] = useState<number[]>([]);
  const [selectAll, setSelectAll] = useState(false);

  const navigate = useNavigate();
  const location = useLocation();
  const { jobs, skill, count } = (location.state as LocationState) || {
    jobs: [],
    skill: "",
    count: 0,
  };

  useEffect(() => {
    if (jobs.length === 0) {
      navigate("/");
    }
  }, [jobs, navigate]);

  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      setSelectedCompanies(jobs.map((job) => job.id));
    } else {
      setSelectedCompanies([]);
    }
    setSelectAll(checked);
  };

  const handleSelectCompany = (id: number, checked: boolean) => {
    if (checked) {
      setSelectedCompanies((prev) => [...prev, id]);
    } else {
      setSelectedCompanies((prev) =>
        prev.filter((companyId) => companyId !== id)
      );
    }
  };

  const handleSendRequest = () => {
    const selectedJobs = jobs.filter((job) =>
      selectedCompanies.includes(job.id)
    );
    navigate("/send", { state: { selected: selectedJobs } });
  };

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h4" gutterBottom>
        Search Results
      </Typography>
      <Typography variant="body1" gutterBottom>
        Found {count} job results
      </Typography>

      {jobs.length > 0 ? (
        <form onSubmit={handleSendRequest}>
          {jobs.map((job) => (
            <Box
              key={job.id}
              sx={{ border: "1px solid #ddd", padding: 2, marginBottom: 2 }}
            >
              <FormControlLabel
                control={
                  <Checkbox
                    name={`select-${job.id}`}
                    checked={selectedCompanies.includes(job.id)}
                    onChange={(e) =>
                      handleSelectCompany(job.id, e.target.checked)
                    }
                  />
                }
                label="Select this job"
              />
              <TextField
                label="Company Name"
                value={job.name}
                fullWidth
                margin="normal"
                InputProps={{ readOnly: true }}
              />
              <TextField
                label="Job Title"
                value={job.title}
                fullWidth
                margin="normal"
                InputProps={{ readOnly: true }}
              />
              <TextField
                label="Contact Info"
                value={job.contact || ""}
                fullWidth
                margin="normal"
                InputProps={{ readOnly: true }}
              />
              {job.url && (
                <TextField
                  label="Job URL"
                  value={job.url}
                  fullWidth
                  margin="normal"
                  InputProps={{ readOnly: true }}
                />
              )}
            </Box>
          ))}

          <Button
            type="submit"
            variant="contained"
            disabled={selectedCompanies.length === 0}
            sx={{ marginTop: 2 }}
          >
            Send Requests to Selected Jobs
          </Button>
        </form>
      ) : (
        <Typography>No jobs found</Typography>
      )}

      <Button
        variant="outlined"
        onClick={() => navigate("/")}
        sx={{ marginTop: 2 }}
      >
        Back to Search
      </Button>
    </Box>
  );
}

export default Results;
