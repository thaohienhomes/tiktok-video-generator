#!/usr/bin/env python3
"""
FastAPI server với minimal config để debug
"""

print("🔧 Starting FastAPI Fixed Server...")

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
    print("✅ FastAPI imported successfully")
except ImportError as e:
    print(f"❌ FastAPI import failed: {e}")
    exit(1)

# Tạo app với minimal config
app = FastAPI(
    title="FastAPI Fixed Server",
    version="1.0.0",
    description="Debugging FastAPI server"
)

# Add error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    print(f"❌ Global exception: {type(exc).__name__}: {str(exc)}")
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"error": f"{type(exc).__name__}: {str(exc)}"}
    )

@app.get("/")
async def root():
    try:
        print("📝 GET / called")
        return {
            "message": "FastAPI Fixed Server works!", 
            "status": "success",
            "server": "fastapi"
        }
    except Exception as e:
        print(f"❌ Error in root endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    try:
        print("📝 GET /health called")
        return {
            "health": "OK",
            "server": "fastapi_fixed",
            "endpoints": ["/", "/health"]
        }
    except Exception as e:
        print(f"❌ Error in health endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
        print("🚀 Starting FastAPI server on http://127.0.0.1:8004")
        
        # Chạy với minimal config
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=8004, 
            log_level="info",
            access_log=True
        )
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        import traceback
        traceback.print_exc() 