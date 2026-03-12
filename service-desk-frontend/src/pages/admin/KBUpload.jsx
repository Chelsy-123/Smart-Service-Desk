import { useState } from "react";
import axios from "../../api/axios";

export default function KBUpload() {
  const [form, setForm] = useState({
    title: "",
    category: "",
    priority: "",
    content: ""
    });

  const submit = async () => {
    await axios.post("/kb/upload/", form);
    alert("KB uploaded & ingested");
    setForm({ title: "", content: "", category: "IT", priority: "MEDIUM" });
  };

  return (
    <div className="container mt-4">
      <h4>Upload Knowledge Base</h4>

      <input
  type="text"
  placeholder="Title"
  value={form.title}
  onChange={e => setForm({ ...form, title: e.target.value })}
/>
<br /><br />
<select
  value={form.category}
  onChange={e => setForm({ ...form, category: e.target.value })}
>
  <option value="">Select Category</option>
  <option value="IT">IT</option>
  <option value="HR">HR</option>
  <option value="FINANCE">FINANCE</option>
</select>
<br /><br />
<select
  value={form.priority}
  onChange={e => setForm({ ...form, priority: e.target.value })}
>


  <option value="">Select Priority</option>
  <option value="LOW">LOW</option>
  <option value="MEDIUM">MEDIUM</option>
  <option value="HIGH">HIGH</option>
</select>
<br /><br />
      <textarea
        className="form-control mb-2"
        placeholder="KB Content"
        rows="6"
        value={form.content}
        onChange={(e) => setForm({ ...form, content: e.target.value })}
      />

      <button className="btn btn-success" onClick={submit}>
        Upload & Ingest
      </button>
    </div>
  );
}
