import time
from agentreplay import step, save, report

@step()
def search_web(q):
    time.sleep(0.2); return ["result A", "result B"]

@step()
def call_llm(prompt):
    time.sleep(0.5); return "Here is the synthesized answer."

@step()
def flaky_tool(x):
    raise TimeoutError("the API is not responding")

@step("agent")
def agent(question):
    docs = search_web(question)
    try:
        flaky_tool(docs)
    except TimeoutError:
        pass
    return call_llm(f"{question} {docs}")

agent("What is the best way to debug an AI agent?")
save("demo.json"); report("demo.json", "demo.html")
print("Open demo.html")
