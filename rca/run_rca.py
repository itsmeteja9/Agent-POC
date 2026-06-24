import json
import sys
import os
from rca_engine import run_rca

def main():
    """Main entry point for RCA analysis."""
    log_file = "logs.txt"
    
    if not os.path.exists(log_file):
        print(f"Error: {log_file} not found")
        sys.exit(1)
    
    try:
        # Read logs from file
        with open(log_file, "r") as f:
            logs = f.read()
        
        if not logs.strip():
            print("Error: Log file is empty")
            sys.exit(1)
        
        # Run RCA analysis
        results = run_rca(logs)
        
        # Display results
        print("\n" + "="*50)
        print("   RCA ANALYSIS RESULTS")
        print("="*50 + "\n")
        print(json.dumps(results, indent=2))
        print("\n" + "="*50)
        
        # Exit with appropriate code based on confidence
        sys.exit(0)
        
    except Exception as e:
        print(f"Error during RCA analysis: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
