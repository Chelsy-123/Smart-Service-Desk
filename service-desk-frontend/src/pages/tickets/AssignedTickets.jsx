import { useEffect, useState } from "react";
import { getAssignedTickets, updateTicketStatus } from "../../api/tickets.api";
import { Link } from "react-router-dom";

const statusColors = {
  OPEN: "badge bg-secondary",
  IN_PROGRESS: "badge bg-warning",
  CLOSED: "badge bg-success",
};

const AssignedTickets = () => {
  const [tickets, setTickets] = useState([]);

  useEffect(() => {
    loadTickets();
  }, []);

  const loadTickets = async () => {
  const data = await getAssignedTickets();
  setTickets(data);
};


  const changeStatus = async (id, status) => {
    await updateTicketStatus(id, status);
    loadTickets(); // refresh → user sees update
  };

  return (
    <div className="container mt-4">
      <h4>Assigned Tickets</h4>

      <table className="table table-bordered">
        <thead>
          <tr>
            <th>ID</th>
            <th>Subject</th>
            <th>Status</th>
            <th>Change Status</th>
          </tr>
        </thead>
        <tbody>
          {tickets.map(t => (
            <tr key={t.id}>
              <td>{t.id}</td>
              <td>
                <Link to={`/tickets/${t.id}`}>{t.subject}</Link>
              </td>
              <td>
                <span className={statusColors[t.status]}>
                  {t.status}
                </span>
              </td>
              <td>
                <select
                  value={t.status}
                  onChange={e => changeStatus(t.id, e.target.value)}
                  className="form-select"
                >
                  <option value="OPEN">OPEN</option>
                  <option value="IN_PROGRESS">IN PROGRESS</option>
                  <option value="CLOSED">CLOSED</option>
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AssignedTickets;
