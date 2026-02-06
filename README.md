# sct
A Python implementation of concepts from social choice theory

## How to run the frontend
```bash
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