import "./upload-document.css";

export default function UploadDocument() {
  return (
    <div className="upload-card">
      <div className="upload-dropzone">
        <strong>Drag & Drop document here</strong>
        <div>or click to upload</div>
        <div className="upload-helper">
          Supported: Aadhaar, PAN, Salary Slip, PDF / Image
        </div>
      </div>

      <div className="upload-controls">
        <select>
          <option>Auto-detect document type</option>
          <option>Aadhaar</option>
          <option>PAN</option>
          <option>Salary Slip</option>
        </select>
      </div>

      <button className="upload-btn">Upload & Validate</button>
    </div>
  );
}
