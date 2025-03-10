from datetime import datetime
import os
import requests

def api_get_submissions(page: int, problem: str) -> list | None:
    """
    Get submissions from the API.
    """
    
    url = f"https://coder.husc.edu.vn/api/v2/submissions?problem={problem}&page={page}"
    headers = {
        'Authorization': f"Bearer {os.getenv('API_KEY')}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data["data"]["objects"]
        else:
            return None
    except Exception as e:
        print(e)
        return None
    
def get_submissions(contestants: list, problems: list) -> list:
    """
    Get filtered submissions.
    """
    begin_time = datetime.fromisoformat(os.getenv("CONTEST_BEGIN_DATETIME"))
    contestants_name = [contestant['name'] for contestant in contestants]
    
    def check_submission(submission: dict) -> bool:
        time_submitted = (datetime.fromisoformat(submission['date']) - begin_time).seconds
        return (time_submitted >= 0) and (time_submitted <= 300 * 60) and submission['user'] in contestants_name
    
    result = []
    for problem in problems: 
        page = 1
        while True:
            submissions_page = api_get_submissions(page, problem['name'])
            if (submissions_page is None) or (len(submissions_page) == 0):
                break
            
            result.extend(filter(check_submission, submissions_page))
            page += 1

    return [{
        "timeSubmitted": (datetime.fromisoformat(submission['date']) - begin_time).seconds // 60,
        "contestantName": submission['user'],
        "problemIndex": list(filter(lambda problem: problem['name'] == submission['problem'], problems))[0]['index'],
        "verdict": submission['result']
    } for submission in result]