
import DiamondIcon from "@mui/icons-material/Diamond";
import JobForm from "./JobForm";
import DataBox from "./DataBox";

function Home() {

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
