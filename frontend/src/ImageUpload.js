import React, { useState } from 'react';

const ImageUpload = () => {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [enhanced, setEnhanced] = useState(null);
    const [operation, setOperation] = useState("grayscale");
    const [value, setValue] = useState("1.0");

    const handleFileChange = (e) => {
        const selected = e.target.files[0];
        setFile(selected);
        setPreview(URL.createObjectURL(selected));
    };

    const handleUpload = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);
        formData.append("operation", operation);
        formData.append("value", value);  // always send, backend handles default

        try {
            const response = await fetch("http://localhost:8000/enhance", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) throw new Error("Enhancement failed");

            const blob = await response.blob();
            setEnhanced(URL.createObjectURL(blob));
        } catch (err) {
            console.error("Enhancement failed:", err);
        }
    };

    return (
        <div style={{ padding: 20 }}>
            <h2>Image Enhancer</h2>

            <input type="file" accept="image/*" onChange={handleFileChange} />

            <select onChange={(e) => setOperation(e.target.value)} value={operation}>
                <option value="grayscale">Grayscale</option>
                <option value="sharpen">Sharpen</option>
                <option value="contrast">Increase Contrast</option>
                <option value="rotate">Rotate</option>
                <option value="thumbnail">Thumbnail</option>
                <option value="ghibli">Ghibli Art</option>
                <option value="sketch">Pencil Sketch</option>
                <option value="cartoon">Cartoon</option>
                <option value="paint">Paint Style</option>
            </select>


            {(operation === "contrast" || operation === "rotate") && (
                <input
                    type="number"
                    step="0.1"
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                    placeholder="Enter value"
                    style={{ marginLeft: 10 }}
                />
            )}

            <button onClick={handleUpload}>Enhance</button>

            {preview && <div><h4>Original:</h4><img src={preview} alt="original" width={200} /></div>}
            {enhanced && <div><h4>Enhanced:</h4><img src={enhanced} alt="enhanced" width={200} /></div>}
        </div>
    );
};

export default ImageUpload;
