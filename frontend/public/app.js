/**
 * SCT Voting Frontend Application
 * Kahoot-inspired minimalistic design
 */

// API Configuration
const API_BASE = '';

// State
let currentSession = null;
let candidates = [];
let ratingLabels = [];

// DOM Elements
const candidatesContainer = document.getElementById('candidatesContainer');
const voteBtn = document.getElementById('voteBtn');
const newSessionBtn = document.getElementById('newSessionBtn');
const sessionInfo = document.getElementById('sessionInfo');
const generateBtn = document.getElementById('generateBtn');
const numAgentsInput = document.getElementById('numAgents');
const strategySelect = document.getElementById('strategy');
const seedInput = document.getElementById('seed');
const resultsContainer = document.getElementById('resultsContainer');
const showResultsBtn = document.getElementById('showResults');
const clearVotesBtn = document.getElementById('clearVotesBtn');
const manualVoteCount = document.getElementById('manualVoteCount');
const syntheticVoteCount = document.getElementById('syntheticVoteCount');
const toastContainer = document.getElementById('toastContainer');

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
    await loadCandidates();
    await createNewSession();
    setupEventListeners();
});

// Load candidates from API
async function loadCandidates() {
    try {
        const response = await fetch(`${API_BASE}/api/candidates`);
        const data = await response.json();
        candidates = data.candidates;
        ratingLabels = data.ratingLabels;
        renderCandidates();
    } catch (error) {
        console.error('Failed to load candidates:', error);
        showToast('Failed to load candidates', 'error');
    }
}

// Render candidate sliders
function renderCandidates() {
    candidatesContainer.innerHTML = '';
    
    candidates.forEach((candidate, index) => {
        const card = document.createElement('div');
        card.className = 'candidate-card';
        card.style.setProperty('--card-color', candidate.color);
        
        card.innerHTML = `
            <div class="candidate-header">
                <span class="candidate-emoji">${candidate.emoji}</span>
                <span class="candidate-name">${candidate.name}</span>
            </div>
            <div class="slider-container">
                <input type="range" 
                       class="vote-slider" 
                       id="slider-${candidate.id}" 
                       min="0" 
                       max="4" 
                       value="2"
                       data-candidate-id="${candidate.id}">
                <div class="slider-labels">
                    ${ratingLabels.map((label, i) => `
                        <span class="slider-label ${i === 2 ? 'active' : ''}" data-value="${i}">${getShortLabel(label)}</span>
                    `).join('')}
                </div>
                <div class="current-rating" id="rating-${candidate.id}">Neutral</div>
            </div>
        `;
        
        candidatesContainer.appendChild(card);
        
        // Setup slider event
        const slider = card.querySelector('.vote-slider');
        slider.addEventListener('input', (e) => updateSliderUI(e.target, candidate.id));
    });
}

// Get short label for mobile
function getShortLabel(label) {
    const shorts = {
        'Strongly Disagree': 'SD',
        'Disagree': 'D',
        'Neutral': 'N',
        'Agree': 'A',
        'Strongly Agree': 'SA'
    };
    return shorts[label] || label;
}

// Update slider UI on change
function updateSliderUI(slider, candidateId) {
    const value = parseInt(slider.value);
    const ratingDisplay = document.getElementById(`rating-${candidateId}`);
    const card = slider.closest('.candidate-card');
    const labels = card.querySelectorAll('.slider-label');
    
    // Update rating text
    ratingDisplay.textContent = ratingLabels[value];
    
    // Update active label
    labels.forEach((label, i) => {
        label.classList.toggle('active', i === value);
    });
    
    // Update slider color intensity
    const intensity = (value / 4) * 100;
    slider.style.setProperty('--fill-percent', `${(value / 4) * 100}%`);
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
        sessionInfo.textContent = `Session: ${currentSession.slice(0, 8)}...`;
        
        // Reset vote counts
        manualVoteCount.textContent = '0';
        syntheticVoteCount.textContent = '0';
        
        // Clear results
        resultsContainer.innerHTML = '<p class="no-results">No votes yet</p>';
        
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
            updateSliderUI(slider, candidate.id);
        }
    });
}

// Cast a vote
async function castVote() {
    if (!currentSession) {
        showToast('Please create a session first', 'warning');
        return;
    }
    
    // Collect preferences
    const preferences = candidates.map(candidate => {
        const slider = document.getElementById(`slider-${candidate.id}`);
        return parseInt(slider.value);
    });
    
    try {
        voteBtn.disabled = true;
        voteBtn.innerHTML = '<span class="btn-icon">⏳</span> Voting...';
        
        const response = await fetch(`${API_BASE}/api/sessions/${currentSession}/votes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                preferences,
                isSynthetic: false
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to cast vote');
        }
        
        // Update vote count
        manualVoteCount.textContent = parseInt(manualVoteCount.textContent) + 1;
        
        // Show success animation
        showVoteSuccess();
        
        // Reset sliders
        resetSliders();
        
        // Refresh results
        await loadResults();
        
    } catch (error) {
        console.error('Failed to cast vote:', error);
        showToast('Failed to cast vote', 'error');
    } finally {
        voteBtn.disabled = false;
        voteBtn.innerHTML = '<span class="btn-icon">✓</span> Vote';
    }
}

// Show vote success animation
function showVoteSuccess() {
    showToast('Vote cast successfully! 🎉', 'success');
    
    // Add pulse animation to vote button
    voteBtn.classList.add('success-pulse');
    setTimeout(() => voteBtn.classList.remove('success-pulse'), 500);
}

// Generate random votes
async function generateRandomVotes() {
    if (!currentSession) {
        showToast('Please create a session first', 'warning');
        return;
    }
    
    const numAgents = parseInt(numAgentsInput.value) || 10;
    const strategy = strategySelect.value;
    const seed = seedInput.value ? parseInt(seedInput.value) : null;
    
    try {
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span class="btn-icon">⏳</span> Generating...';
        
        const response = await fetch(`${API_BASE}/api/sessions/${currentSession}/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                numAgents,
                strategy,
                seed
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to generate votes');
        }
        
        const data = await response.json();
        
        // Update synthetic vote count
        syntheticVoteCount.textContent = parseInt(syntheticVoteCount.textContent) + data.generated;
        
        showToast(`Generated ${data.generated} random votes! 🎲`, 'success');
        
        // Refresh results
        await loadResults();
        
    } catch (error) {
        console.error('Failed to generate votes:', error);
        showToast('Failed to generate votes. Make sure Python is set up.', 'error');
    } finally {
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<span class="btn-icon">⚡</span> Generate';
    }
}

// Load and display results
async function loadResults() {
    if (!currentSession) return;
    try {
        const response = await fetch(`${API_BASE}/api/sessions/${currentSession}/results`);
        const data = await response.json();
        // Update vote counts
        manualVoteCount.textContent = data.manualVotes || 0;
        syntheticVoteCount.textContent = data.syntheticVotes || 0;
        if (data.totalVotes === 0) {
            resultsContainer.innerHTML = '<p class="no-results">No votes yet</p>';
            return;
        }
        // Render results
        resultsContainer.innerHTML = data.results.map((result, rank) => `
            <div class="result-card" style="--card-color: ${result.color}">
                <div class="result-rank">#${rank + 1}</div>
                <div class="result-info">
                    <span class="result-emoji">${result.emoji}</span>
                    <span class="result-name">${result.name}</span>
                </div>
                <div class="result-stats">
                    <div class="result-average">${result.averageRating.toFixed(2)}</div>
                    <div class="result-bar-container">
                        <div class="result-bar" style="width: ${(result.averageRating / 4) * 100}%"></div>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load results:', error);
    }
}

// Clear all votes
async function clearVotes() {
    if (!currentSession) return;
    
    if (!confirm('Are you sure you want to clear all votes?')) return;
    
    try {
        await fetch(`${API_BASE}/api/sessions/${currentSession}/votes`, {
            method: 'DELETE'
        });
        
        manualVoteCount.textContent = '0';
        syntheticVoteCount.textContent = '0';
        resultsContainer.innerHTML = '<p class="no-results">No votes yet</p>';
        
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
    
    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Remove after delay
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Setup event listeners
function setupEventListeners() {
    voteBtn.addEventListener('click', castVote);
    newSessionBtn.addEventListener('click', createNewSession);
    generateBtn.addEventListener('click', generateRandomVotes);
    refreshResultsBtn.addEventListener('click', () => {
        resultsContainer.style.display = 'block';
        loadResults();
    });
    clearVotesBtn.addEventListener('click', clearVotes);
    showResultsBtn.addEventListener('click', () => {
        resultsContainer.style.display = 'block';
        loadResults();
    });
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey) {
            castVote();
        }
    });
}
