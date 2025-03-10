import json, os, dotenv
from api import get_submissions

dotenv.load_dotenv()

if __name__ == "__main__":
    contestants = json.load(open("contestants.json", "r"))
    problems = json.load(open("problems.json", "r"))
    
    neoSaris = {
        "contestMetadata": {
            "duration": 300,
            "frozenTimeDuration": 60,
            "name": os.getenv("CONTEST_NAME"),
            "type": "ICPC"
        },
        "problems": problems['problems'],
        "verdicts": {
            "accepted": ["AC"],
            "wrongAnswerWithPenalty": ["WA", "TLE", "MLE", "IR", "RTE"],
            "wrongAnswerWithoutPenalty": ["CE"]
        },
        "contestants": contestants['contestants'],
        "submissions": get_submissions(contestants['contestants'], problems['problems'])
    }
    
    os.makedirs("result", exist_ok=True)
    with open("result/neoSaris.json", "w") as f:
        json.dump(neoSaris, f, indent=4)