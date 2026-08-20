from utils.clickhouse_agent import clickhouse_agent


result = clickhouse_agent(
    "What are the production requirements for the Street scene?"
)

print("\n===== FINAL AGENT RESPONSE =====")
print(result)