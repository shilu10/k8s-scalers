// src/Visualizer.jsx
import React, { useState, useRef } from "react";

const generatePodPositions = (centerX, centerY, count, baseRadius = 80) => {
  const angleStep = (2 * Math.PI) / count;
  const dynamicRadius = baseRadius + Math.min(300, count * 1.2);
  return Array.from({ length: count }, (_, i) => {
    const angle = i * angleStep;
    const x = centerX + dynamicRadius * Math.cos(angle);
    const y = centerY + dynamicRadius * Math.sin(angle);
    return { x, y, id: i }; // include ID for dummy data lookup
  });
};

const getDummyPodDetails = (podId) => {
  return {
    name: `pod-${podId}`,
    status: podId % 2 === 0 ? "Running" : "Pending",
    cpu: `${(Math.random() * 0.5 + 0.1).toFixed(2)} cores`,
    memory: `${(Math.random() * 100 + 50).toFixed(0)} MB`,
  };
};

const DeploymentNode = ({ deployment, onDrag }) => {
  const [expanded, setExpanded] = useState(false);
  const [position, setPosition] = useState({
    x: deployment.cx,
    y: deployment.cy,
  });
  const isDragging = useRef(false);
  const [selectedPod, setSelectedPod] = useState(null);
  const [stress, setStress] = useState(50);
  const [timeout, setTimeoutVal] = useState(10);

  const handleMouseDown = () => {
    isDragging.current = true;
  };

  const handleMouseMove = (e) => {
    if (isDragging.current) {
      const svg = e.target.ownerSVGElement;
      if (!svg || !svg.createSVGPoint) return;
      const pt = svg.createSVGPoint();
      pt.x = e.clientX;
      pt.y = e.clientY;
      const cursorpt = pt.matrixTransform(svg.getScreenCTM().inverse());
      setPosition({ x: cursorpt.x, y: cursorpt.y });
      onDrag(deployment.name, cursorpt.x, cursorpt.y);
    }
  };

  const handleMouseUp = () => {
    isDragging.current = false;
  };

  const podPositions = expanded
    ? generatePodPositions(position.x, position.y, deployment.replicas)
    : [];

  return (
    <g
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      onClick={() => setExpanded(!expanded)}
      style={{ cursor: "move" }}
    >
      <circle
        cx={position.x}
        cy={position.y}
        r={40}
        fill={deployment.color}
        stroke="black"
        strokeWidth={2}
      />
      <text
        x={position.x}
        y={position.y}
        textAnchor="middle"
        dy=".3em"
        fill="white"
        fontWeight="bold"
      >
        {deployment.replicas}
      </text>
      <text
        x={position.x}
        y={position.y + 60}
        textAnchor="middle"
        fill="black"
        fontSize="14"
      >
        {deployment.name}
      </text>
      <text
        x={position.x}
        y={position.y + 75}
        textAnchor="middle"
        fill="gray"
        fontSize="12"
      >
        Deployment
      </text>
      {podPositions.map((pod) => (
        <circle
          key={pod.id}
          cx={pod.x}
          cy={pod.y}
          r={8}
          fill="gray"
          stroke="black"
          onClick={(e) => {
            e.stopPropagation();
            setSelectedPod(getDummyPodDetails(pod.id));
          }}
        />
      ))}
      {selectedPod && (
        <foreignObject x={position.x + 50} y={position.y - 20} width={260} height={220}>
          <div
            xmlns="http://www.w3.org/1999/xhtml"
            style={{
              background: "white",
              border: "1px solid black",
              padding: "0.5rem",
              fontSize: "12px",
              borderRadius: "5px",
              boxShadow: "0 2px 5px rgba(0,0,0,0.3)",
              width: "250px",
              height: "210px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div>
              <strong>{selectedPod.name}</strong>
              <div>Status: {selectedPod.status}</div>
              <div>CPU: {selectedPod.cpu}</div>
              <div>Memory: {selectedPod.memory}</div>
              <div style={{ marginTop: "0.5rem" }}>
                <label>Stress (%): </label>
                <input
                  type="number"
                  value={stress}
                  onChange={(e) => setStress(e.target.value)}
                  min={0}
                  max={100}
                  style={{ width: "60px" }}
                />
                <br />
                <label>Timeout (s): </label>
                <input
                  type="number"
                  value={timeout}
                  onChange={(e) => setTimeoutVal(e.target.value)}
                  min={1}
                  max={300}
                  style={{ width: "60px" }}
                />
              </div>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <button
                style={{ marginTop: "0.5rem" }}
                onClick={(e) => {
                  e.stopPropagation();
                  alert(`Stress ${selectedPod.name} at ${stress}% for ${timeout}s`);
                }}
              >
                Apply
              </button>
              <button
                style={{ marginTop: "0.5rem" }}
                onClick={(e) => {
                  e.stopPropagation();
                  setSelectedPod(null);
                }}
              >
                Close
              </button>
            </div>
          </div>
        </foreignObject>
      )}
    </g>
  );
};

const Arrow = ({ from, to }) => {
  const dx = to.cx - from.cx;
  const dy = to.cy - from.cy;
  const angle = Math.atan2(dy, dx);
  const offset = 40;
  const startX = from.cx + offset * Math.cos(angle);
  const startY = from.cy + offset * Math.sin(angle);
  const endX = to.cx - offset * Math.cos(angle);
  const endY = to.cy - offset * Math.sin(angle);

  return (
    <line
      x1={startX}
      y1={startY}
      x2={endX}
      y2={endY}
      stroke="black"
      strokeWidth={2}
      markerEnd="url(#arrowhead)"
    />
  );
};

const DeploymentVisualizer = () => {
  const [services, setServices] = useState({
    svc1: { name: "svc1", cx: 150, cy: 200, replicas: 10, color: "#4f46e5" },
    rabbitmq: { name: "rabbitmq", cx: 350, cy: 200, replicas: 1, color: "#f97316" },
    svc2: { name: "svc2", cx: 550, cy: 200, replicas: 10, color: "#10b981" },
  });

  const [connections, setConnections] = useState([
    { from: "svc1", to: "rabbitmq" },
    { from: "rabbitmq", to: "svc2" },
  ]);

  const [newSvcName, setNewSvcName] = useState("");
  const [newReplicas, setNewReplicas] = useState(1);

  const handleAddService = () => {
    if (!newSvcName.trim()) return;
    const id = newSvcName.toLowerCase();
    const offsetX = 200 + Object.keys(services).length * 100;
    setServices((prev) => ({
      ...prev,
      [id]: {
        name: newSvcName,
        cx: offsetX,
        cy: 400,
        replicas: newReplicas,
        color: "#94a3b8",
      },
    }));
    setNewSvcName("");
    setNewReplicas(1);
  };

  const handleDrag = (name, newX, newY) => {
    setServices((prev) => ({
      ...prev,
      [name]: {
        ...prev[name],
        cx: newX,
        cy: newY,
      },
    }));
  };

  return (
    <div>
      <form
        style={{
          display: "flex",
          gap: "1rem",
          padding: "1rem",
          alignItems: "center",
          borderBottom: "1px solid #ccc",
        }}
        onSubmit={(e) => {
          e.preventDefault();
          handleAddService();
        }}
      >
        <input
          type="text"
          placeholder="Deployment Name"
          value={newSvcName}
          onChange={(e) => setNewSvcName(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Replicas"
          min={1}
          value={newReplicas}
          onChange={(e) => setNewReplicas(Number(e.target.value))}
          required
        />
        <button type="submit">Add Deployment</button>
      </form>
      <svg width="100%" height="600" style={{ border: "1px solid lightgray" }}>
        <defs>
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="7"
            refX="10"
            refY="3.5"
            orient="auto"
          >
            <polygon points="0 0, 10 3.5, 0 7" fill="black" />
          </marker>
        </defs>
        {connections.map(({ from, to }, i) => (
          <Arrow key={i} from={services[from]} to={services[to]} />
        ))}
        {Object.values(services).map((svc) => (
          <DeploymentNode key={svc.name} deployment={svc} onDrag={handleDrag} />
        ))}
      </svg>
    </div>
  );
};

export default DeploymentVisualizer;
