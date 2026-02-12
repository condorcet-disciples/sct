/**
 * SCT Voting Frontend Application
 * Minimalist design with three tabs
 */

const API_BASE = '';

// State
let currentSession = null;
let candidates = [];
let candidateDescriptions = {};
let ratingLabels = [];

// DOM Elements
const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const candidatesGrid = document.getElementById('candidatesGrid');
const votingTableBody = document.getElementById('votingTableBody');
const voteBtn = document.getElementById('voteBtn');
const newSessionBtn = document.getElementById('newSessionBtn');
const generateBtn = document.getElementById('generateBtn');
const numAgentsInput = document.getElementById('numAgents');
const strategySelect = document.getElementById('strategy');
const seedInput = document.getElementById('seed');
const clearVotesBtn = document.getElementById('clearVotesBtn');
const resultsContainer = document.getElementById('resultsContainer');
const toastContainer = document.getElementById('toastContainer');

// Vote count elements
const totalVoteCount = document.getElementById('totalVoteCount');
const manualVoteCount = document.getElementById('manualVoteCount');
const syntheticVoteCount = document.getElementById('syntheticVoteCount');
const resultsVoteCount = document.getElementById('resultsVoteCount');

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
    await loadCandidates();
    await loadCandidateDescriptions();
    await createNewSession();
    setupEventListeners();
    renderCandidatesGrid();
    renderVotingTable();
});

// Load candidates from API
async function loadCandidates() {
    try {
        const response = await fetch(`${API_BASE}/api/candidates`);
        const data = await response.json();
        candidates = data.candidates;
        ratingLabels = data.ratingLabels;
    } catch (error) {
        console.error('Failed to load candidates:', error);
        showToast('Failed to load candidates', 'error');
    }
}

// Load candidate descriptions from JSON
async function loadCandidateDescriptions() {
    try {
        const response = await fetch(`${API_BASE}/data/candidates.json`);
        candidateDescriptions = await response.json();
    } catch (error) {
        console.error('Failed to load candidate descriptions:', error);
    }
}

// Render candidates grid (Tab 1 - flip cards)
function renderCandidatesGrid() {
    candidatesGrid.innerHTML = '';
    
    candidates.forEach(candidate => {
        const desc = candidateDescriptions[`candidate_${candidate.id}`] || {};
        
        const card = document.createElement('div');
        card.className = 'candidate-flip-card';
        card.innerHTML = `
            <div class="candidate-flip-inner">
                <div class="candidate-front">
                    <span class="candidate-emoji-large">${candidate.emoji}</span>
                    <span class="candidate-name-large">${candidate.name}</span>
                </div>
                <div class="candidate-back">
                    <span class="candidate-back-title">${desc.title || candidate.name}</span>
                    <p class="candidate-back-desc">${desc.description || 'No description available.'}</p>
                </div>
            </div>
        `;
        
        card.addEventListener('click', () => {
            card.classList.toggle('flipped');
        });
        
        candidatesGrid.appendChild(card);
    });
}

// Render voting table (Tab 2)
function renderVotingTable() {
    votingTableBody.innerHTML = '';
    
    candidates.forEach(candidate => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="candidate-col">
                <div class="candidate-cell">
                    <span class="candidate-emoji">${candidate.emoji}</span>
                    <span class="candidate-name">${candidate.name}</span>
                </div>
            </td>
            <td colspan="5" class="slider-cell">
                <input type="range" 
                       class="vote-slider" 
                       id="slider-${candidate.id}" 
                       min="0" 
                       max="4" 
                       value="2"
                       data-candidate-id="${candidate.id}">
                <div class="slider-value" id="value-${candidate.id}">Neutral</div>
            </td>
        `;
        
        votingTableBody.appendChild(row);
        
        const slider = row.querySelector('.vote-slider');
        slider.addEventListener('input', (e) => updateSliderValue(e.target, candidate.id));
    });
}

// Update slider value display
function updateSliderValue(slider, candidateId) {
    const value = parseInt(slider.value);
    const valueDisplay = document.getElementById(`value-${candidateId}`);
    valueDisplay.textContent = ratingLabels[value];
}

// Tab switching
function switchTab(tabName) {
    tabButtons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });
    
    tabContents.forEach(content => {
        const isActive = content.id === `tab-${tabName}`;
        content.classList.toggle('active', isActive);
    });
    
    // Load results when switching to results tab
    if (tabName === 'results') {
        loadResults();
    }
}

// Create a new voting session
async function createNewSession() {
    try {
        const response = await fetch(`${API_BASE}/api/sessions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                description: `Session created at ${new Date().toLocaleString()}`
            })
        });
        
        const data = await response.json();
        currentSession = data.sessionId;
        
        // Reset vote counts
        updateVoteCounts(0, 0);
        
        // Reset sliders
        resetSliders();
        
        showToast('New session created!', 'success');
    } catch (error) {
        console.error('Failed to create session:', error);
        showToast('Failed to create session', 'error');
    }
}

// Reset all sliders to neutral
function resetSliders() {
    candidates.forEach(candidate => {
        const slider = document.getElementById(`slider-${candidate.id}`);
        if (slider) {
            slider.value = 2;
            updateSliderValue(slider, candidate.id);
        }
    });
}

// Update vote counts across tabs
function updateVoteCounts(manual, synthetic) {
    const total = manual + synthetic;
    if (totalVoteCount) totalVoteCount.textContent = total;
    if (manualVoteCount) manualVoteCount.textContent = manual;
    if (syntheticVoteCount) syntheticVoteCount.textContent = synthetic;
    if (resultsVoteCount) resultsVoteCount.textContent = total;
}

// Cast a vote
async function castVote() {
    if (!currentSession) {
        showToast('Please create a session first', 'warning');
        return;
    }
    
    const preferences = candidates.map(candidate => {
        const slider = document.getElementById(`slider-${candidate.id}`);
        return parseInt(slider.value);
    });
    
    try {
        voteBtn.disabled = true;
        voteBtn.textContent = 'Voting...';
        
        const response = await fetch(`${API_BASE}/api/sessions/${currentSession}/votes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ preferences, isSynthetic: false })
        });
        
        if (!response.ok) throw new Error('Failed to cast vote');
        
        // Update counts
        const manual = parseInt(manualVoteCount.textContent) + 1;
        const synthetic = parseInt(syntheticVoteCount.textContent);
        updateVoteCounts(manual, synthetic);
        
        showToast('Vote cast successfully!', 'success');
        resetSliders();
        
    } catch (error) {
        console.error('Failed to cast vote:', error);
        showToast('Failed to cast vote', 'error');
    } finally {
        voteBtn.disabled = false;
        voteBtn.textContent = 'Vote';
    }
}

// Generate random votes
async function generateRandomVotes() {
    if (!currentSession) {
        showToast('Please create a session first', 'warning');
        return;
    }
    
    const numAgents = parseInt(numAgentsInput.value) || 10;
    const strategy = strategySelect.value;
    const seed = seedInput.value ? parseInt(seedInput.value) : 0;
    
    try {
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
        
        const response = await fetch(`${API_BASE}/api/sessions/${currentSession}/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ numAgents, strategy, seed })
        });
        
        if (!response.ok) throw new Error('Failed to generate votes');
        
        const data = await response.json();
        
        // Update counts
        const manual = parseInt(manualVoteCount.textContent);
        const synthetic = parseInt(syntheticVoteCount.textContent) + data.generated;
        updateVoteCounts(manual, synthetic);
        
        showToast(`Generated ${data.generated} votes!`, 'success');
        
    } catch (error) {
        console.error('Failed to generate votes:', error);
        showToast('Failed to generate votes. Check Python setup.', 'error');
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate';
    }
}

// Load and display results
async function loadResults() {
    if (!currentSession) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/sessions/${currentSession}/results`);
        const data = await response.json();
        
        // Update vote counts
        const manual = data.manualVotes || 0;
        const synthetic = data.syntheticVotes || 0;
        updateVoteCounts(manual, synthetic);
        
        if (data.totalVotes === 0) {
            resultsContainer.innerHTML = '<p class="no-results">No votes have been cast yet</p>';
            return;
        }
        
        // Render results with winners and disappointment indices
        renderResults(data);
        
    } catch (error) {
        console.error('Failed to load results:', error);
        resultsContainer.innerHTML = '<p class="no-results">Failed to load results</p>';
    }
}

// Render results grid
function renderResults(data) {
    const results = data.results || {};
    
    // Helper to find candidate by name pattern
    function findCandidate(winnerName) {
        if (!winnerName) return null;
        return candidates.find(c => 
            winnerName.toLowerCase().includes(c.name.toLowerCase()) ||
            winnerName.toLowerCase().includes(`candidate_${c.id}`)
        );
    }
    
    // Get winners
    const pluralityWinner = findCandidate(results.plurality?.winner);
    const bordaWinner = findCandidate(results.borda?.winner);
    const majorityWinner = findCandidate(results.majority?.winner);
    
    // Format disappointment index
    function formatDisappointment(di) {
        if (!di || typeof di !== 'object') return 'N/A';
        return Object.entries(di)
            .map(([k, v]) => `${k.replace('candidate_', 'C')}: ${v.toFixed(1)}`)
            .join(', ');
    }
    
    resultsContainer.innerHTML = `
        <!-- Plurality Column -->
        <div class="results-column">
            <h3>Plurality</h3>
            <div class="winner-card">
                <span class="winner-emoji">${pluralityWinner?.emoji || '?'}</span>
                <span class="winner-name">${pluralityWinner?.name || 'Unknown'}</span>
            </div>
            <div class="disappointment-section">
                <div class="disappointment-index">
                    <div class="disappointment-label">Disappointment Index</div>
                    <div class="disappointment-value">${formatDisappointment(results.plurality?.disappointment)}</div>
                </div>
            </div>
            <div class="disappointment-placeholder"></div>
            <div class="disappointment-placeholder"></div>
        </div>
        
        <!-- Borda Column -->
        <div class="results-column">
            <h3>Borda</h3>
            <div class="winner-card">
                <span class="winner-emoji">${bordaWinner?.emoji || '?'}</span>
                <span class="winner-name">${bordaWinner?.name || 'Unknown'}</span>
            </div>
            <div class="disappointment-placeholder"></div>
            <div class="disappointment-section">
                <div class="disappointment-index">
                    <div class="disappointment-label">Disappointment Index</div>
                    <div class="disappointment-value">${formatDisappointment(results.borda?.disappointment)}</div>
                </div>
            </div>
            <div class="disappointment-placeholder"></div>
        </div>
        
        <!-- Majority Judgment Column -->
        <div class="results-column">
            <h3>Majority Judgment</h3>
            <div class="winner-card">
                <span class="winner-emoji">${majorityWinner?.emoji || '?'}</span>
                <span class="winner-name">${majorityWinner?.name || 'Unknown'}</span>
            </div>
            <div class="disappointment-placeholder"></div>
            <div class="disappointment-placeholder"></div>
            <div class="disappointment-section">
                <div class="disappointment-index">
                    <div class="disappointment-label">Disappointment Index</div>
                    <div class="disappointment-value">${formatDisappointment(results.majority?.disappointment)}</div>
                </div>
            </div>
        </div>
    `;
}

// Clear all votes
async function clearVotes() {
    if (!currentSession) return;
    
    if (!confirm('Are you sure you want to clear all votes?')) return;
    
    try {
        await fetch(`${API_BASE}/api/sessions/${currentSession}/votes`, {
            method: 'DELETE'
        });
        
        updateVoteCounts(0, 0);
        showToast('All votes cleared', 'info');
        
    } catch (error) {
        console.error('Failed to clear votes:', error);
        showToast('Failed to clear votes', 'error');
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    toastContainer.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 10);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Setup event listeners
function setupEventListeners() {
    // Tab navigation
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });
    
    // Voting actions
    voteBtn.addEventListener('click', castVote);
    newSessionBtn.addEventListener('click', createNewSession);
    generateBtn.addEventListener('click', generateRandomVotes);
    clearVotesBtn.addEventListener('click', clearVotes);
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey) {
            const activeTab = document.querySelector('.tab-btn.active');
            if (activeTab?.dataset.tab === 'voting') {
                castVote();
            }
        }
    });
}
