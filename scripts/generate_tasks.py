import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from datamark.generators.tasks import write_tasks
print("Generated",len(write_tasks()),"tasks")
