from pydantic import BaseModel


class PostAgentQuery(BaseModel):
    query: str
