import { useEffect, useState } from "react";
import { getKBDocuments } from "../../api/kb.api";

export default function KBDocumentList() {
  const [docs, setDocs] = useState([]);

  useEffect(() => {
    getKBDocuments().then(setDocs);
  }, []);

  return (
    <div className="container mt-4">
      <h4>Knowledge Base Documents</h4>

      {docs.map((doc) => (
        <div key={doc.id} className="card mb-2">
          <div className="card-body">
            <strong>{doc.title}</strong>
            <p className="mb-0">
              Source: {doc.source_type}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}
