import os

structure = [
    "playstore-trend-agent/agents/ingestion_agent.py",
    "playstore-trend-agent/agents/preprocessing_agent.py",
    "playstore-trend-agent/agents/topic_extraction_agent.py",
    "playstore-trend-agent/agents/canonicalization_agent.py",
    "playstore-trend-agent/agents/trend_agent.py",
    "playstore-trend-agent/storage/topic_memory.json",
    "playstore-trend-agent/output/trend_report_sample.csv",
    "playstore-trend-agent/main.py",
    "playstore-trend-agent/requirements.txt",
    "playstore-trend-agent/README.md",
    "playstore-trend-agent/INSTRUCTIONS.md",
]

for filepath in structure:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        pass # Creates empty file
print("Project structure created successfully!")