from utils.production_agent import production_agent


script_analysis = {
    "title": "THE LAST SIGNAL",
    "characters": ["Sarah", "John"],
    "locations": ["Laboratory", "Street"],
    "summary": "Sarah discovers a mysterious machine in a laboratory and runs outside to meet John."
}


result = production_agent(script_analysis)


print("\n===== PRODUCTION AGENT =====")
print(result)