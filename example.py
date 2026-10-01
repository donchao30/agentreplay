import time
from agentreplay import step, save, report, set_price

# Example prices (USD per 1M tokens). Use your own model's real prices.
set_price("demo-model", 3.0, 15.0)

@step()
def search_web(q):
    time.sleep(0.2); return ["result A", "result B"]

@step()
def call_llm(prompt):
    time.sleep(0.5)
    # Any response with a `usage` field (OpenAI / Anthropic style) is detected automatically.
    return {"model": "demo-model", "text": "Here is the synthesized answer.",
            "usage": {"input_tokens": 120, "output_tokens": 45}}

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
    return call_llm(f"{question} {docs}")["text"]

agent("What is the best way to debug an AI agent?")
save("demo.json"); report("demo.json", "demo.html")
print("Open demo.html")
