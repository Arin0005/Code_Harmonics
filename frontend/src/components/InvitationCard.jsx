import React from "react";

const InvitationCard = ({ title, description, buttonText, onClick }) => {
  return (
    <div style={styles.card}>
      <h2 style={styles.title}>{title}</h2>
      <p style={styles.description}>{description}</p>
      <button onClick={onClick} style={styles.button}>
        {buttonText}
      </button>
    </div>
  );
};

const styles = {
  card: {
    border: "1px solid #E0E0E0",
    borderRadius: "12px",
    padding: "30px",
    width: "320px",
    boxShadow: "0 4px 12px rgba(0, 0, 0, 0.1)",
    transition: "transform 0.2s, box-shadow 0.2s",
  },
  title: {
    fontSize: "1.5rem",
    color: "#333",
    marginBottom: "16px",
  },
  description: {
    fontSize: "1rem",
    color: "#666",
    marginBottom: "24px",
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
    transition: "background-color 0.2s",
  },
};

export default InvitationCard;
