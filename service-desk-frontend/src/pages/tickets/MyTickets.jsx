import { useEffect, useState, useContext } from "react";
import { Link } from "react-router-dom";
import { getMyTickets } from "../../api/tickets.api";
import { AuthContext } from "../../context/AuthContext";

const MyTickets = () => {
  const { user } = useContext(AuthContext);

  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadTickets = async () => {
      try {
        const data = await getMyTickets();
        setTickets(data);
      } catch (err) {
        console.error("Failed to load tickets", err);
        setError("Unable to load tickets");
      } finally {
        setLoading(false);
      }
    };

    loadTickets();
  }, []);

  if (loading) {
    return <div className="container mt-4">Loading tickets...</div>;
  }

  if (error) {
    return <div className="container mt-4 text-danger">{error}</div>;
  }

  return (
    
    <div className="container mt-4">
      
      <h3 className="mb-3">
        My Tickets
        {user && (
          <span className="text-muted ms-2" style={{ fontSize: "0.9rem" }}>
            ({user.username})
          </span>
        )}
      </h3>
      <div className="d-flex justify-content-between align-items-center mb-3">

  <Link to="/tickets/create" className="btn btn-primary">
    + Create Ticket
  </Link>
</div>

      {tickets.length === 0 ? (
        <p>No tickets found.</p>
      ) : (
        <table className="table table-hover align-middle">
          <thead className="table-dark">
            <tr>
              <th>ID</th>
              <th>Subject</th>
              <th>Status</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {tickets.map((ticket) => (
              <tr key={ticket.id}>
                <td>{ticket.id}</td>
                <td>
                  <Link className="text-decoration-none" to={`/tickets/${ticket.id}`}>
                    {ticket.subject}
                  </Link>
                </td>
                <td>
                  <span className={`badge bg-${getStatusColor(ticket.status)}`}>
                    {ticket.status}
                  </span>
                </td>
                <td>
                  {new Date(ticket.created_at).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

const getStatusColor = (status) => {
  switch (status) {
    case "OPEN":
      return "secondary";
    case "IN_PROGRESS":
      return "warning";
    case "RESOLVED":
      return "primary";
    case "CLOSED":
      return "success";
    default:
      return "secondary";
  }
};

export default MyTickets;
