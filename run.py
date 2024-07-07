import sys
import os

# Add the app directory to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
