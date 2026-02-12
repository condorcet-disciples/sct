/**
 * SCT Voting Simulation Backend
 * Express server with in-memory storage (JSON file persistence)
 */

const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');
const { spawn } = require('child_process');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Data storage
const dataDir = path.join(__dirname, 'data');
const dataFile = path.join(dataDir, 'database.json');

// Ensure data directory exists
if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
}

// Load or initialize database
function loadDatabase() {
    try {
        if (fs.existsSync(dataFile)) {
            const data = fs.readFileSync(dataFile, 'utf8');
            return JSON.parse(data);
        }
    } catch (error) {
        console.error('Error loading database:', error);
    }
    return { sessions: {}, votes: {} };
}

function saveDatabase(db) {
    fs.writeFileSync(dataFile, JSON.stringify(db, null, 2));
}

let database = loadDatabase();

// Candidates configuration
const CANDIDATES = [
    { id: 1, name: 'Business-as-usual', emoji: '🚗💨', color: '#E21B3C' },
    { id: 2, name: 'Slow cars', emoji: '🚗', color: '#1368CE' },
    { id: 3, name: 'Few cars', emoji: '🚶', color: '#D89E00' },
    { id: 4, name: 'No cars', emoji: '⛔', color: '#26890C' }
];

const RATING_LABELS = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'];

// API Routes

// Get candidates
app.get('/api/candidates', (req, res) => {
    res.json({ candidates: CANDIDATES, ratingLabels: RATING_LABELS });
});

// Create a new voting session
app.post('/api/sessions', (req, res) => {
    const { seed, description } = req.body;
    const sessionId = uuidv4();
    
    database.sessions[sessionId] = {
        id: sessionId,
        created_at: new Date().toISOString(),
        seed: seed || null,
        description: description || null
    };
    database.votes[sessionId] = [];
    
    saveDatabase(database);
    
    res.json({ sessionId, seed, description });
});

// Get all sessions
app.get('/api/sessions', (req, res) => {
    const sessions = Object.values(database.sessions).map(session => ({
        ...session,
        vote_count: (database.votes[session.id] || []).length
    })).sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    
    res.json({ sessions });
});

// Get session details with votes
app.get('/api/sessions/:sessionId', (req, res) => {
    const { sessionId } = req.params;
    
    const session = database.sessions[sessionId];
    if (!session) {
        return res.status(404).json({ error: 'Session not found' });
    }
    
    const votes = database.votes[sessionId] || [];
    
    res.json({ session, votes });
});

// Cast a vote
app.post('/api/sessions/:sessionId/votes', (req, res) => {
    const { sessionId } = req.params;
    const { agentId, preferences, isSynthetic } = req.body;
    
    // Validate session exists
    const session = database.sessions[sessionId];
    if (!session) {
        return res.status(404).json({ error: 'Session not found' });
    }
    
    // Validate preferences
    if (!Array.isArray(preferences) || preferences.length !== 4) {
        return res.status(400).json({ error: 'Preferences must be an array of 4 ratings' });
    }
    
    for (const pref of preferences) {
        if (typeof pref !== 'number' || pref < 0 || pref > 4) {
            return res.status(400).json({ error: 'Each preference must be a number between 0 and 4' });
        }
    }
    
    const vote = {
        id: (database.votes[sessionId] || []).length + 1,
        session_id: sessionId,
        agent_id: agentId || uuidv4(),
        is_synthetic: isSynthetic ? 1 : 0,
        candidate_1: preferences[0],
        candidate_2: preferences[1],
        candidate_3: preferences[2],
        candidate_4: preferences[3],
        created_at: new Date().toISOString()
    };
    
    if (!database.votes[sessionId]) {
        database.votes[sessionId] = [];
    }
    database.votes[sessionId].push(vote);
    
    saveDatabase(database);
    
    res.json({ 
        voteId: vote.id,
        agentId: vote.agent_id,
        preferences 
    });
});

// Generate random votes using Python backend
app.post('/api/sessions/:sessionId/generate', (req, res) => {
    const { sessionId } = req.params;
    const { numAgents, strategy, seed } = req.body;
    
    // Validate session exists
    const session = database.sessions[sessionId];
    if (!session) {
        return res.status(404).json({ error: 'Session not found' });
    }
    
    // Call Python script to generate preferences
    const pythonScript = path.join(__dirname, 'scripts', 'generate_votes.py');
    const args = [
        pythonScript,
        '--num-agents', numAgents || 10,
        '--strategy', strategy || 'biased'
    ];
    
    if (seed !== undefined && seed !== null) {
        args.push('--seed', seed);
    }
    
    const python = spawn('python3', args);
    
    let output = '';
    let errorOutput = '';
    
    python.stdout.on('data', (data) => {
        output += data.toString();
    });
    
    python.stderr.on('data', (data) => {
        errorOutput += data.toString();
    });
    
    python.on('close', (code) => {
        if (code !== 0) {
            console.error('Python script error:', errorOutput);
            return res.status(500).json({ error: 'Failed to generate votes', details: errorOutput });
        }
        
        try {
            const generatedAgents = JSON.parse(output);
            
            // Insert generated votes into database
            if (!database.votes[sessionId]) {
                database.votes[sessionId] = [];
            }
            
            const startId = database.votes[sessionId].length + 1;
            
            for (let i = 0; i < generatedAgents.length; i++) {
                const agent = generatedAgents[i];
                database.votes[sessionId].push({
                    id: startId + i,
                    session_id: sessionId,
                    agent_id: agent.id,
                    is_synthetic: 1,
                    candidate_1: agent.preferences[0],
                    candidate_2: agent.preferences[1],
                    candidate_3: agent.preferences[2],
                    candidate_4: agent.preferences[3],
                    created_at: new Date().toISOString()
                });
            }
            
            saveDatabase(database);
            
            res.json({ 
                generated: generatedAgents.length,
                agents: generatedAgents 
            });
        } catch (e) {
            console.error('Parse error:', e, output);
            res.status(500).json({ error: 'Failed to parse generated votes' });
        }
    });
});

// Get aggregated results for a session
app.get('/api/sessions/:sessionId/results', (req, res) => {
    const { sessionId } = req.params;
    
    const session = database.sessions[sessionId];
    if (!session) {
        return res.status(404).json({ error: 'Session not found' });
    }
    
    const votes = database.votes[sessionId] || [];
    
    if (votes.length === 0) {
        return res.json({ 
            totalVotes: 0, 
            syntheticVotes: 0,
            manualVotes: 0,
            results: {}
        });
    }
    
    // Run election with session ID
    const pythonScript = path.join(__dirname, 'scripts', 'run_election.py');
    const python = spawn('python3', [pythonScript, '--session-id', sessionId]);

    let output = '';
    let errorOutput = '';

    python.stdout.on('data', (data) => {
        output += data.toString();
    });

    python.stderr.on('data', (data) => {
        errorOutput += data.toString();
    });

    python.on('close', (code) => {
        if (code !== 0) {
            console.error('Election script error:', errorOutput);
            return res.status(500).json({ error: 'Election script failed', details: errorOutput });
        }
        
        try {
            const electionResults = JSON.parse(output);
            res.json({
                totalVotes: votes.length,
                syntheticVotes: votes.filter(v => v.is_synthetic).length,
                manualVotes: votes.filter(v => !v.is_synthetic).length,
                results: electionResults
            });
        } catch (e) {
            console.error('Failed to parse election results:', e, output);
            res.status(500).json({ error: 'Failed to parse election results' });
        }
    });
});

// Delete a session
app.delete('/api/sessions/:sessionId', (req, res) => {
    const { sessionId } = req.params;
    
    delete database.votes[sessionId];
    delete database.sessions[sessionId];
    
    saveDatabase(database);
    
    res.json({ deleted: true });
});

// Clear all votes from a session
app.delete('/api/sessions/:sessionId/votes', (req, res) => {
    const { sessionId } = req.params;
    
    const deletedCount = (database.votes[sessionId] || []).length;
    database.votes[sessionId] = [];
    
    saveDatabase(database);
    
    res.json({ deleted: deletedCount });
});

// Serve frontend
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start server
app.listen(PORT, () => {
    console.log(`🗳️  SCT Voting Server running at http://localhost:${PORT}`);
    console.log(`📊 Database: ${dataFile}`);
});
