import React, { useState } from "react";
import axios from "axios";

const JoinPage = () => {
  const [invitationCode, setInvitationCode] = useState("");

  const handleJoin = async () => {
    try {
      const response = await axios.post("/api/join-invitation", {
        invitationCode,
      });
      alert("Joined successfully!");
      console.log(response.data);
    } catch (error) {
      console.error("Error joining invitation:", error);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>Join Invitation</h1>
      <div style={styles.form}>
        <input
          type="text"
          placeholder="Invitation Code"
          value={invitationCode}
          onChange={(e) => setInvitationCode(e.target.value)}
          style={styles.input}
        />
        <button onClick={handleJoin} style={styles.button}>
          Join
        </button>
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
    fontSize: "2rem",
    color: "#333",
    marginBottom: "40px",
  },
  form: {
    maxWidth: "400px",
    margin: "0 auto",
  },
  input: {
    padding: "12px",
    margin: "10px 0",
    width: "100%",
    border: "1px solid #E0E0E0",
    borderRadius: "8px",
    fontSize: "1rem",
  },
  button: {
    padding: "12px 24px",
    backgroundColor: "#007AFF",
    color: "#FFF",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    fontSize: "1rem",
    width: "100%",
    marginTop: "20px",
  },
};

export default JoinPage;
