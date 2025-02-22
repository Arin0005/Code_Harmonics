import React from "react";
import { useNavigate } from "react-router-dom";
import InvitationCard from "../components/InvitationCard";

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>Event Management</h1>
      <div style={styles.cardContainer}>
        <InvitationCard
          title="Create Invitation"
          description="Create a new event and invite others to join."
          buttonText="Create"
          onClick={() => navigate("/create")}
        />
        <InvitationCard
          title="Join Invitation"
          description="Join an existing event using an invitation code."
          buttonText="Join"
          onClick={() => navigate("/join")}
        />
      </div>
    </div>
  );
};

const styles = {
  container: {
    textAlign: "center",
    padding: "40px",
    minHeight: "100vh",
  },
  heading: {
    fontSize: "2.5rem",
    color: "#333",
    marginBottom: "40px",
  },
  cardContainer: {
    display: "flex",
    justifyContent: "center",
    gap: "40px",
    flexWrap: "wrap",
  },
};

export default HomePage;
