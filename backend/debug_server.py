print("Starting debug server...")

try:
    from fastapi import FastAPI
    print("✅ FastAPI imported successfully")
except ImportError as e:
    print(f"❌ FastAPI import failed: {e}")
    exit(1)

app = FastAPI(title="Debug Server")

@app.get("/")
async def read_root():
    print("GET / called")
    return {"message": "Debug server works!", "status": "success"}

@app.get("/health")
async def health():
    print("GET /health called") 
    return {"health": "OK", "server": "debug"}

if __name__ == "__main__":
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
        print("🚀 Starting server on http://127.0.0.1:8002")
        uvicorn.run(app, host="127.0.0.1", port=8002, log_level="info")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        import traceback
        traceback.print_exc() 