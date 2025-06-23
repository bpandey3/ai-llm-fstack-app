from langgraph.graph import StateGraph, END
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from connect_sql import get_schema  # fetches tables from Snowflake

# Step 1: Define the state
class AgentState(dict):
    pass

# Step 2: Define nodes

def classify_query(state: AgentState) -> str:
    user_input = state['user_input'].lower()
    vague_keywords = ["select query", "some query", "write query", "give me query"]
    if any(k in user_input for k in vague_keywords):
        return "clarify_table"
    return "generate_sql"

def clarify_table(state: AgentState) -> AgentState:
    tables = get_schema()  # returns a list of table names
    state['tables'] = tables
    state['response'] = f"Which table do you want to query? Available tables: {', '.join(tables)}"
    return state

def generate_sql(state: AgentState) -> AgentState:
    llm = ChatOpenAI(temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that writes SQL queries based on database schema."),
        ("human", "{user_input}")
    ])
    user_input = state['user_input']
    table_info = state.get("tables_info", get_schema(include_columns=True))  # you can modify this
    formatted_prompt = prompt.format(user_input=user_input + "\n\nSchema:\n" + str(table_info))
    response = llm.invoke([HumanMessage(content=formatted_prompt)])
    state['response'] = response.content
    return state

# Step 3: Build the graph
graph = StateGraph(AgentState)

graph.add_node("clarify_table", clarify_table)
graph.add_node("generate_sql", generate_sql)

graph.set_entry_point(classify_query)
graph.add_conditional_edges(
    classify_query,
    {
        "clarify_table": "clarify_table",
        "generate_sql": "generate_sql"
    }
)
graph.add_edge("clarify_table", END)
graph.add_edge("generate_sql", END)

app = graph.compile()

# Step 4: Run the agent
if __name__ == "__main__":
    import sys
    user_input = input("Enter your query: ")
    final_state = app.invoke({"user_input": user_input})
    print(final_state['response'])
