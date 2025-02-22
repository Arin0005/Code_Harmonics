import React from "react";

const Header = ({ username }) => {
  return (
    <div style={styles.header}>
      <h2>Welcome, {username}!</h2>
    </div>
  );
};

const styles = {
  header: {
    backgroundColor: "#f0f0f0",
    padding: "10px",
    textAlign: "right",
  },
};

export default Header;
