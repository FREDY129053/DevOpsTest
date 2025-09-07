import uvicorn

if __name__ == "__main__":
  uvicorn.run(
    app="src.server:app",
    host="localhost",
    port=8080,
    log_level="info"
  )