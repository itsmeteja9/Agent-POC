import json
from rca_engine import run_rca

#read logs from file
with open("logs.txt","r") as f:
  logs = f.read()

results = run_rca(logs)

print("\n RCA RESULT:\n")
print(json.dumps(results,indent=2))
