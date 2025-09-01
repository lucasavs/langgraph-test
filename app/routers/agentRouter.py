from fastapi import APIRouter
from ..schemas.agentQuerySchema import PostAgentQuery
from ..controllers.agentController import agent_query_response

agentRouter = APIRouter()


@agentRouter.post("/query/", tags=["agent"])
async def post_agent(post_agent_query: PostAgentQuery):
    return {"answer": agent_query_response(post_agent_query)}
