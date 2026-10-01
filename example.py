import time
from agentreplay import step, save, report

@step()
def search_web(q):
    time.sleep(0.2); return ["résultat A", "résultat B"]

@step()
def call_llm(prompt):
    time.sleep(0.5); return "Voici la réponse synthétisée."

@step()
def flaky_tool(x):
    raise TimeoutError("l'API ne répond pas")

@step("agent")
def agent(question):
    docs = search_web(question)
    try:
        flaky_tool(docs)
    except TimeoutError:
        pass
    return call_llm(f"{question} {docs}")

agent("Quel est le meilleur outil pour déboguer un agent ?")
save("demo.json"); report("demo.json", "demo.html")
print("Ouvre demo.html")
