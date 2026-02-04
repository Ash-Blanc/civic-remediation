"""
Civic Remediation System - Main Entry Point

Supports two modes:
1. Singleton Pipeline (NEW): Converging flow → ONE problem, ONE cause, ONE solution → Project Launch
2. Deep Team (Legacy): Intelligent delegation to 7-agent team
"""
from dotenv import load_dotenv
import sys

# Import both modes
from app.team import create_civic_team
from app.workflow import create_singleton_pipeline

load_dotenv()


def run_singleton_pipeline(query: str = "Pollution of the Ganga River"):
    """
    NEW: Singleton Pipeline mode.
    Converging flow: ONE problem → ONE cause → ONE department → ONE solution → ONE funding → Blueprint
    """
    print(f"--- Starting Singleton Pipeline for: {query} ---")
    print("Mode: Converging (ONE item per stage)")
    
    pipeline = create_singleton_pipeline()
    response = pipeline.run(query)
    
    return response


def run_team(query: str = "Pollution of the Ganga River") -> str:
    """
    Legacy: Team-based intelligent delegation mode.
    The coordinator (Deep Team) decides which agents to invoke and synthesizes results.
    """
    print(f"--- Starting Civic Remediation Deep Team for: {query} ---")
    print("Mode: Divergent (multiple items per agent)")
    
    team = create_civic_team()
    response = team.run(query)
    
    return response.content


# Alias for backward compatibility
run_pipeline = run_singleton_pipeline


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Pollution of the Ganga River"
    mode = sys.argv[2] if len(sys.argv) > 2 else "singleton"
    
    if mode == "team":
        print("Using Deep Team mode (intelligent delegation)")
        result = run_team(query)
    else:
        print("Using Singleton Pipeline mode (converging)")
        result = run_singleton_pipeline(query)
    
    print("\n--- Final Result ---")
    print(result)
