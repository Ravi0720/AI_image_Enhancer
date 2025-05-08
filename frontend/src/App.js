import React, { useState } from "react";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [style, setStyle] = useState("anime");

  const handleFileChange = (e) => {
    setImage(e.target.files[0]);
    setPreviewUrl(URL.createObjectURL(e.target.files[0]));
  };

  const handleEnhance = async () => {
    const formData = new FormData();
    formData.append("file", image);
    formData.append("style", style);

    const res = await fetch("http://127.0.0.1:8000/enhance", {
      method: "POST",
      body: formData,
    });

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    setPreviewUrl(url);
  };

  return (
    <div className="container">
      <h1>AI Image Enhancer</h1>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <select onChange={(e) => setStyle(e.target.value)}>
        <option value="anime">Anime</option>
      </select>
      <button onClick={handleEnhance}>Enhance</button>

      {previewUrl && (
        <div className="image-box">
          <img src={previewUrl} alt="Preview" className="image-3d" />
        </div>
      )}
    </div>
  );
}

export default App;
