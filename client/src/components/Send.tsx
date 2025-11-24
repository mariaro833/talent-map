import { useNavigate, useLocation } from 'react-router-dom';
// TODO: Import necessary MUI components
// import { ... } from '@mui/material';

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
  selected: Job[];
}

function Send() {
  const navigate = useNavigate();
  const location = useLocation();
  const { selected } = (location.state as LocationState) || { selected: [] };

  // TODO: Implement send functionality
  // - Display selected companies
  // - Show success message
  // - Provide next steps
  // - Navigation buttons

  return (
    <div>
      {/* TODO: Implement the Send component */}
      {/* - Show success message */}
      {/* - Display selected companies */}
      {/* - Provide next steps */}
      {/* - Navigation options */}
      <h1>Internship Requests Sent!</h1>

      {selected && selected.length > 0 ? (
        <div>
          <p>You selected {selected.length} companies:</p>
          {selected.map((company, index) => (
            <div key={index}>
              <h3>{company.name}</h3>
              <p>{company.title}</p>
              {company.contact && <p>Contact: {company.contact}</p>}
            </div>
          ))}

          <p>Next steps: Check your email for application templates.</p>
        </div>
      ) : (
        <p>No companies selected</p>
      )}

      <button onClick={() => navigate('/')}>Back to Home</button>
      <button onClick={() => navigate('/')}>New Search</button>
    </div>
  );
}

export default Send;