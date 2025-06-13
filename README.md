# BillSupport
Bill Support it is a clever USA Bill Analyzer, running in a container using Python 3.12 with FastAPI

# How works
This application runs in a container api, therefore needs to;
1 - run the command: docker build -t bill-support .
2 - run the command: docker docker run -p 8000:8000

# Alternatively, you can run a dev environment, this already with an active venv and inside the folder app
uvicorn app.main:app --reload

# Feature Support By Legislator
This feature, analyzes how a legislator voted by bills being supported or not. To access it, use your browser with a
local address http://localhost:8000/support/by_legislator

# Feature Support By Bill
This feature, analyzes how a legislator voted by bills being supported or not. To access it, use your browser with a
local address http://localhost:8000/support/by_bill