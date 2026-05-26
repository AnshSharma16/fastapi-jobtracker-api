from fastapi import APIRouter
router=APIRouter()

@router.get('/jobs')
def get_jobs():
    return [
    {
        "company": "OpenAI",
            "role": "Python Backend Intern"
    },
    {
         "company": "Anthropic",
            "role": "AI Automation Developer"
    }
    ]