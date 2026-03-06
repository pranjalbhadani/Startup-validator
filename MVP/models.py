from pydantic import BaseModel

class StartupInput(BaseModel):
    startup_name: str
    idea_description: str
    target_market: str
    revenue_model: str | None = None