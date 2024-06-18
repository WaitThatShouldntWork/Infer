import json
import logging
from src.utils.scratchpad import clear_scratchpad
from src.agents import intent_agent, answer_agent
from src.prompts import PromptEngine
from src.supervisors import solve_all

logger = logging.getLogger(__name__)

engine = PromptEngine()
director_prompt = engine.load_prompt("director")


def question(question):
    intent = intent_agent.invoke(question)
    intent_json = json.loads(intent)
    logger.info(f"Intent determined: {intent}")

    final_scratchpad = solve_all(intent_json)
    final_answer = answer_agent.invoke(question, final_scratchpad)
    logger.info(f"Final answer: {final_answer}")

    clear_scratchpad()

    return final_answer
