from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from app.agents.decision_node import is_weather_query
from app.services.weather import get_weather
from app.services.rag_service import get_rag_response

# Step 1: Define state schema
class GraphState(BaseModel):
    input: str
    output: str | None = None

# Step 2: Define route logic
def route(state):
    query = state.input
    if is_weather_query(query):
        return "weather_node"
    return "rag_node"

# Step 3: Build the graph with the schema
def build_graph():
    builder = StateGraph(GraphState)  

    builder.add_node("weather_node", lambda state: {"output": get_weather(state.input)})
    builder.add_node("rag_node", lambda state: {"output": get_rag_response(state.input)})


    builder.set_conditional_entry_point(route)
    builder.add_edge("weather_node", END)
    builder.add_edge("rag_node", END)

    return builder.compile()
