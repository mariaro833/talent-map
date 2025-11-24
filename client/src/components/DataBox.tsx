import React from "react";
import { Box, Grid } from "@mui/material";
// import { SparkLineChart } from "@mui/x-charts/SparkLineChart";
// import { ScatterChart } from "@mui/x-charts/ScatterChart";
// import { Heatmap } from "@mui/x-charts/Heatmap";
// import { BarChart } from "@mui/x-charts/BarChart";

const DataBox = () => {
  return (
    <Grid container spacing={2}>
      <Grid item xs={6} md={8}>
        <Box>
          <div
            style={{
              height: "100px",
              backgroundColor: "#e0e0e0",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            Spark Line Chart
          </div>
        </Box>
      </Grid>
      <Grid item xs={6} md={4}>
        <Box>
          <div
            style={{
              height: "100px",
              backgroundColor: "#e0e0e0",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            Spark Bar Chart
          </div>
        </Box>
      </Grid>
      <Grid item xs={6} md={4}>
        <Box>
          <div
            style={{
              height: "300px",
              backgroundColor: "#e0e0e0",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            Bar Chart Placeholder
          </div>
        </Box>
      </Grid>
      <Grid item xs={6} md={8}>
        <Box>
          <div
            style={{
              height: "300px",
              backgroundColor: "#f0f0f0",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            Heatmap Placeholder
          </div>
        </Box>
      </Grid>
    </Grid>
  );
};

export default DataBox;
