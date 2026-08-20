from utils.tools.clickhouse_tool import get_production_data


result = get_production_data("Street")

print("\n===== CLICKHOUSE RESULT =====")
print(result)