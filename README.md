# AgentReplay

**Vois exactement ce que ton agent IA a fait, étape par étape.**
Zéro dépendance, 1 fichier Python, 1 décorateur.

```python
from agentreplay import step, save, report

@step()
def call_llm(prompt): ...
```

Lance ton agent, puis `report("run.json", "run.html")` : tu obtiens une page avec
chaque appel, ses entrées, ses sorties, ses erreurs et sa durée.

## Installer
Copie `agentreplay.py` dans ton projet (Python 3.8+). Essaie `python example.py`.

## Pourquoi
Déboguer un agent à coups de `print`, c'est pénible. AgentReplay te montre
la chaîne complète et où ça casse.

## Roadmap
- [ ] Coût et tokens par étape
- [ ] Comparer deux runs
- [ ] Intégrations OpenAI / Anthropic / LangChain
- [ ] Version hébergée (équipes)

MIT License
