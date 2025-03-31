# sct
A Python implementation of concepts from social choice theory

## Setting Up the Backend

To run the FastAPI backend locally:

```bash
cd backend
python -m venv sct-venv
source sct-venv/bin/activate
pip install -r requirements.txt
```

## Run webapp locally
For backend:
```
cd backend
uvicorn main:app --reload
```

For frontend:
```
cd frontend
npm start
```