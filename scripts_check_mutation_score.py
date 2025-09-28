import sys
import argparse

def parse_mutmut_results(text: str):
    # This parser is intentionally simple; adapt as needed for your output format.
    survived = 0
    total = 0
    for line in text.splitlines():
        line = line.strip().lower()
        if line.startswith("survived"):
            parts = [p for p in line.split() if p.isdigit()]
            if parts:
                survived = int(parts[0])
        if line.startswith("total"):
            parts = [p for p in line.split() if p.isdigit()]
            if parts:
                total = int(parts[0])
    return survived, total

def main():
    parser = argparse.ArgumentParser(description="Check mutation score threshold.")
    parser.add_argument("results_file", help="Path to mutmut results text file")
    parser.add_argument("--threshold", type=float, default=85.0, help="Minimum required mutation score (killed%)")
    args = parser.parse_args()

    with open(args.results_file, "r", encoding="utf-8") as f:
        text = f.read()

    survived, total = parse_mutmut_results(text)
    killed = max(0, total - survived)
    score = 100.0 * killed / total if total else 0.0

    print(f"Mutation score: {score:.2f}% (killed {killed}/{total})")
    if score < args.threshold:
        print(f"Threshold not met: {args.threshold:.2f}%")
        sys.exit(1)
    print("Threshold met.")
    sys.exit(0)

if __name__ == "__main__":
    main()
