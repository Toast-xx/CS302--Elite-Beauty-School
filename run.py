from app import create_app
import os
import sys

# Point Python to local WeasyPrint DLLs
base_dir = os.path.dirname(os.path.abspath(__file__))
weasy_bin = os.path.join(base_dir, "weasy-deps", "bin")
os.environ["PATH"] = weasy_bin + os.pathsep + os.environ["PATH"]

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
