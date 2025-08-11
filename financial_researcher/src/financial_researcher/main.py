import os
import warnings

from financial_researcher.crew import FinancialResearcher

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the researcher crew.
    """
    inputs = {"company": "Tesla"}

    # Ensure output directory exists for tasks that write files
    os.makedirs("output", exist_ok=True)

    result = FinancialResearcher().crew().kickoff(inputs=inputs)
    try:
        # Print the result
        print("\n\n=== FINAL REPORT ===\n\n")
        print(result.raw)

        print("\n\nReport has been saved to output/report.md")
    except AttributeError:
        print(result)

if __name__ == "__main__":
    run()

