# sct
A Python implementation of concepts from social choice theory

## How to run the App
```bash
uv venv # create a new virtual environment
source .venv/bin/activate # activate the virtual environment
uv sync

cd frontend
npm install
npm start
```

You should see this message on your terminal:
```bash
> sct-voting-frontend@1.0.0 start
> node server.js

🗳️  SCT Voting Server running at http://localhost:3000
📊 Database: /Users/as4623/sct/frontend/data/database.json
```

On the frontend, you should see a new session with a session ID.

Periodically, delete `frontend/data/database.json` to delete the data generated during test simulations.

## Preview
### Candidate View
Explore candidates. Click on the cards to reveal descriptions.
![alt text][candidate-view]

### Voting View
Place your preferences. Choose from Strongly Disagree to Strongly Agree. Cast your vote. Randomly generate some votes using various strategies.
![alt text][voting-view]

### Results View
View the winner candidates based on the Plurality, Borda, and Majority Judgement voting systems. Note the rank of the winner candidate(s) in the other systems to understand how they can differ.
![alt text][results-view]

[candidate-view]: https://github.com/condorcet-disciples/sct/blob/5979bf8fe8389a4540a6701908aa47e1c63c89a5/docs/screenshots/candidate-view.png
[voting-view]: https://github.com/condorcet-disciples/sct/blob/5979bf8fe8389a4540a6701908aa47e1c63c89a5/docs/screenshots/voting-view.png
[results-view]: https://github.com/condorcet-disciples/sct/blob/5979bf8fe8389a4540a6701908aa47e1c63c89a5/docs/screenshots/results-view.png