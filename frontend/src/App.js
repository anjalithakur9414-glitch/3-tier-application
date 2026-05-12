import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {

  const [items, setItems] = useState([]);

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    const response = await axios.get("http://localhost:8000/items");
    setItems(response.data);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>DevOps Full Stack Project</h1>

      <h2>Items List</h2>

      {items.map((item) => (
        <div key={item.id}>
          {item.id} - {item.name}
        </div>
      ))}
    </div>
  );
}

export default App;