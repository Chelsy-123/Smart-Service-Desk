import { useEffect, useState } from "react";
import { fetchAgents } from "../../api/auth.api";

const AgentsList = () => {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchAgents()
      .then((res) => {
        setAgents(res.data);
      })
      .catch(() => {
        setError("Failed to load agents");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) return <p className="text-center mt-4">Loading agents...</p>;
  if (error) return <p className="text-danger text-center">{error}</p>;

  return (
    <div className="container mt-4">
      <h4 className="mb-3">Agents</h4>

      <table className="table table-bordered table-sm">
        <thead className="table-dark">
          <tr>
            <th>Agent Name</th>
            <th>Username</th>
            <th>Email</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {agents.map((agent) => (
            <tr key={agent.id}>
              <td>{agent.agent_name}</td>
              <td>{agent.user.username}</td>
              <td>{agent.user.email}</td>
              <td>
                {agent.is_active ? (
                  <span className="badge bg-success">Active</span>
                ) : (
                  <span className="badge bg-danger">Inactive</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AgentsList;
