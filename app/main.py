import uvicorn
import os

if __name__ == "__main__":
  uvicorn.run(
    app="src.server:app",
    host=os.getenv("SERVER_HOST", "localhost"),
    port=int(os.getenv("SERVER_PORT", 8080)),
    log_level="info"
  )