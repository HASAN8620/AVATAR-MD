import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Response
from mangum import Mangum

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

ORIGINAL_API = "https://frux-info-api.vercel.app/api/banner"

@app.get("/banner")
async def proxy_banner(uid: str = Query(...)):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(ORIGINAL_API, params={"uid": uid, "key": "frux07"}, timeout=30)
            return Response(content=resp.content, media_type=resp.headers.get("content-type", "image/png"))
        except Exception as e:
            raise HTTPException(502, f"Proxy error: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Banner Proxy Active", "endpoint": "/banner?uid=UID"}

handler = Mangum(app)
vercel.json

{ "rewrites": [{ "source": "/(.*)", "destination": "/api/index.py" }] }
package.json

{
  "name": "banner-proxy",
  "version": "1.0.0",
  "scripts": { "vercel-build": "echo build" }
}
requirements.txt

fastapi==0.115.0
mangum==0.17.0
httpx==0.27.0
