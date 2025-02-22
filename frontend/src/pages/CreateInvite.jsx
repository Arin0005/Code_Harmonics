import React, { useState } from "react";
import axios from "axios";

const CreatePage = () => {
  const [eventName, setEventName] = useState("");
  const [description, setDescription] = useState("");

  const handleCreate = async () => {
    try {
      const response = await axios.post("/api/create-invitation", {
        eventName,
        description,
      });
      alert("Invitation created successfully!");
      console.log(response.data);
    } catch (error) {
      console.error("Error creating invitation:", error);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>Create Invitation</h1>
      <div style={styles.form}>
        <input
          type="text"
          placeholder="Event Name"
          value={eventName}
          onChange={(e) => setEventName(e.target.value)}
          style={styles.input}
        />
        <textarea
          placeholder="Event Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          style={styles.textarea}
        />
        <button onClick={handleCreate} style={styles.button}>
          Create
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
  textarea: {
    padding: "12px",
    margin: "10px 0",
    width: "100%",
    border: "1px solid #E0E0E0",
    borderRadius: "8px",
    fontSize: "1rem",
    height: "120px",
    resize: "vertical",
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

export default CreatePage;
