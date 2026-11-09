const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// --- MOCK DATABASES ---
// Represents the output from the Multi-Agent Swarm (State 4)
let flaggedAnomalies = [
  { 
    id: 1, 
    rowId: 42, 
    column: "Education", 
    value: "PhD", 
    context: "Age = 7", 
    reason: "Logical contradiction: Age 7 cannot hold a PhD.", 
    suggestedFix: "Flag for manual age verification.", 
    status: "pending" 
  },
  { 
    id: 2, 
    rowId: 89, 
    column: "Village", 
    value: null, 
    context: "Rural/Urban = Rural", 
    reason: "Conditional dependency: Rural addresses require a Village.", 
    suggestedFix: "Request missing Village data.", 
    status: "pending" 
  }
];

// Represents the Vector Database (Pinecone/Weaviate)
let organizationalMemory = [
  "If Education is PhD, Age must be > 22",
  "If Rural/Urban is Rural, Village cannot be NULL"
];

// --- API ROUTES ---

// 1. Fetch flagged records for the React Dashboard
app.get('/api/anomalies', (req, res) => {
  const pendingAnomalies = flaggedAnomalies.filter(a => a.status === 'pending');
  res.status(200).json({ 
    count: pendingAnomalies.length, 
    data: pendingAnomalies 
  });
});

// 2. Handle HITL Decisions (Accept Fix or Override & Learn)
app.post('/api/remediation', (req, res) => {
  const { anomalyId, action, customRule } = req.body;
  
  const anomalyIndex = flaggedAnomalies.findIndex(a => a.id === anomalyId);
  if (anomalyIndex === -1) {
    return res.status(404).json({ error: "Anomaly not found" });
  }

  if (action === 'accept_fix') {
    flaggedAnomalies[anomalyIndex].status = 'resolved';
    console.log(`[Dashboard] Fix accepted for Row ${flaggedAnomalies[anomalyIndex].rowId}`);
  } 
  
  else if (action === 'override_and_learn') {
    flaggedAnomalies[anomalyIndex].status = 'overridden';
    
    // Update the Organizational Memory Engine
    if (customRule) {
      // In a production environment, you would generate an embedding here 
      // (e.g., via OpenAI text-embedding-3-small) and upsert it to your Vector DB.
      organizationalMemory.push(customRule);
      console.log(`[Memory Engine Updated] New Rule Learned: "${customRule}"`);
    }
  }

  res.status(200).json({ 
    success: true, 
    message: `Anomaly ${anomalyId} processed successfully.`,
    totalRules: organizationalMemory.length 
  });
});

// --- SERVER START ---
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`AI Data Quality Backend running on port ${PORT}`);
  console.log(`Organizational Memory Engine initialized with ${organizationalMemory.length} rules.`);
});