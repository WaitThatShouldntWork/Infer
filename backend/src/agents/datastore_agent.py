from src.utils import call_model
from src.utils.graph_db_utils import execute_query
from src.agents import Agent, agent_metadata
import logging
from src.prompts import PromptEngine
from datetime import datetime
from src.utils import to_json

logger = logging.getLogger(__name__)

current_user = "John Doe"
engine = PromptEngine()
narrative_options = "Bills, Groceries, Entertainment, Rent, Shopping"

graph_schema_prompt = engine.load_prompt("graph-schema", narrative_options=narrative_options)

generate_cypher_query_prompt = engine.load_prompt("generate-cypher-query",
                                                  graph_schema_prompt=graph_schema_prompt,
                                                  current_date=datetime.now())

@agent_metadata(
    name="DatastoreAgent",
    description="This agent is responsible for handling database queries.",
    prompt=generate_cypher_query_prompt,
    tools=[],
)
class DatastoreAgent(Agent):
    def invoke(self, user_prompt):
        llm_query = call_model(self.prompt, user_prompt)
        logger.info("llm query: ")
        logger.info(llm_query)
        json_query = to_json(llm_query)
        logger.info("Cypher generated by the LLM: ")
        logger.info(json_query)
        if json_query["query"] == "None":
            return "No database query"
        db_response = execute_query(json_query['query'])
        print(db_response)
        logger.info(db_response)
        return db_response
