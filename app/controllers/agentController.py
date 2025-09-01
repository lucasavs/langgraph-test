from ..schemas.agentQuerySchema import PostAgentQuery

# from ..service.agentService import AgentService
from ..service.agentService import return_agent_answer


def agent_query_response(post_agent_query: PostAgentQuery):
    return return_agent_answer(post_agent_query.query)
