import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function CreateElection() {
  const [title, setTitle] = useState("");
  const [candidateName, setCandidateName] = useState("");
  const [candidates, setCandidates] = useState([]);
  const [voters, setVoters] = useState([]);
  const [voterName, setVoterName] = useState("");
  const [voterVotes, setVoterVotes] = useState(1);
  const [method, setMethod] = useState("plurality");
  const [results, setResults] = useState(null);

  const addCandidate = () => {
    if (candidateName && !candidates.includes(candidateName)) {
      setCandidates([...candidates, candidateName]);
      setCandidateName("");
    }
  };

  const removeCandidate = (name) => {
    setCandidates(candidates.filter((c) => c !== name));
  };

  const addVoter = () => {
    const shuffled = [...candidates].sort(() => 0.5 - Math.random());
    setVoters([
      ...voters,
      {
        name: voterName || `Voter ${voters.length + 1}`,
        votes: voterVotes,
        preferences: shuffled,
      },
    ]);
    setVoterName("");
    setVoterVotes(1);
  };

  const removeVoter = (index) => {
    setVoters(voters.filter((_, i) => i !== index));
  };

  const handleDrag = (e, fromVoter, fromIndex) => {
    e.dataTransfer.setData("fromVoter", fromVoter);
    e.dataTransfer.setData("fromIndex", fromIndex);
  };

  const handleDrop = (e, toVoter, toIndex) => {
    const fromVoter = e.dataTransfer.getData("fromVoter");
    const fromIndex = e.dataTransfer.getData("fromIndex");

    const updatedVoters = [...voters];
    const prefs = [...updatedVoters[fromVoter].preferences];
    const [moved] = prefs.splice(fromIndex, 1);
    prefs.splice(toIndex, 0, moved);
    updatedVoters[fromVoter].preferences = prefs;
    setVoters(updatedVoters);
  };

  const runElection = async () => {
    const payload = {
      candidates,
      ballots: voters.map((v) => [v.name, v.votes, v.preferences]),
      method,
      num_winners: 1,
    };
    try {
      const res = await axios.post("http://localhost:8000/vote/", payload);
      setResults(res.data);
    } catch (err) {
      console.error("Election error:", err);
      setResults(null);
    }
  };

  return (
    <div className="create-elections">
      <h2>Create New Election</h2>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Election Title"
      />

      <h3>Candidates</h3>
      <input
        value={candidateName}
        onChange={(e) => setCandidateName(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && addCandidate()}
        placeholder="Add a candidate"
      />
      <div className="candidate-boxes">
        {candidates.map((name) => (
          <div key={name} className="candidate-chip">
            {name}
            <span onClick={() => removeCandidate(name)}>&times;</span>
          </div>
        ))}
      </div>

      <h3>Voters</h3>
      <div className="add-voter-row">
        <label className="voter-label">
          Voter Name:
          <input
            value={voterName}
            onChange={(e) => setVoterName(e.target.value)}
            placeholder="Enter a name"
          />
        </label>
        <label className="votes-label">
          Num Votes:
          <input
            type="number"
            min="1"
            value={voterVotes}
            onChange={(e) => setVoterVotes(parseInt(e.target.value))}
          />
        </label>
        <button onClick={addVoter}>Add Voter</button>
      </div>

      {voters.map((v, idx) => (
        <div key={idx}>
          <div className="voter-header">
            <h4>
              {v.name} ({v.votes} vote{v.votes > 1 ? "s" : ""})
            </h4>
            <button onClick={() => removeVoter(idx)}>Remove</button>
          </div>
          <div className="voter-block">
            <ul>
              {v.preferences.map((cand, i) => (
                <li
                  key={i}
                  draggable
                  onDragStart={(e) => handleDrag(e, idx, i)}
                  onDrop={(e) => handleDrop(e, idx, i)}
                  onDragOver={(e) => e.preventDefault()}
                >
                  <span className="drag-arrow">⇅</span>
                  {cand}
                </li>
              ))}
            </ul>
          </div>
        </div>
      ))}

      <h3>Voting Method</h3>
      <select
        value={method}
        onChange={(e) => {
          setMethod(e.target.value);
          runElection();
        }}
      >
        <option value="plurality">Plurality</option>
        <option value="borda">Borda</option>
      </select>

      <button className="create-btn" onClick={runElection}>
        Run Election
      </button>

      {results && (
        <div className="results">
          <h3>Results</h3>
          <table>
            <thead>
              <tr>
                <th>Candidate</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(results.full_results).map(([name, score]) => (
                <tr key={name}>
                  <td>{name}</td>
                  <td>{score}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <h4>
            Winner{results.winners.length > 1 ? "s" : ""}:{" "}
            {results.winners.join(", ")}
          </h4>
        </div>
      )}
    </div>
  );
}

export default CreateElection;