from tinydb import TinyDB, Query
import os

# Construct the path to the root-level file
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
file_path = os.path.join(root_path, "urldb.json")

# Check if the file exists
if os.path.exists(file_path):
    print("urldb exists")
else:
    print("urldb does not exist creating")

Instance = TinyDB(file_path)
