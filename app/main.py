import asyncio
import logging
import os
import sys
from typing import Dict

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

SERVICE_PORTS: Dict[str, int] = {
    "/auth": 9000,
    "/customers": 9001,
    "/gst": 9003,
    "/aa": 9004,
    "/fhc": 9005,
    "/credit": 9006,
    "/cam": 9007,
    "/exec": 9009,
    "/ese": 9010,
    "/ckyc": 9011,
    "/mca": 9012,
    "/epfo": 9013,
}

logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "severity": "%(levelname)s", "message": "%(message)s", "service": "aarohan-demo-platform"}',
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("aarohan-demo-platform")

app = FastAPI(
    title="AAROHAN Demo Platform Gateway",
    description="Cloud Run gateway for the hackathon backend profile",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _cors_headers() -> Dict[str, str]:
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST,PUT,PATCH,DELETE,OPTIONS,HEAD",
        "Access-Control-Allow-Headers": "*",
    }


def _resolve_upstream(path: str) -> int | None:
    for prefix, port in SERVICE_PORTS.items():
        if path == prefix or path.startswith(prefix + "/"):
            return port
    return None


@app.get("/")
async def root():
    return JSONResponse(
        content={"service": "aarohan-demo-platform", "status": "ok", "routes": list(SERVICE_PORTS.keys())},
        headers=_cors_headers(),
    )


@app.get("/health")
@app.get("/readiness")
@app.get("/livez")
async def health(request: Request):
    return JSONResponse(
        content={"service": "aarohan-demo-platform", "status": "ok", "path": request.url.path},
        headers=_cors_headers(),
    )


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
async def proxy(full_path: str, request: Request):
    path = f"/{full_path}"
    upstream_port = _resolve_upstream(path)
    if upstream_port is None:
        return JSONResponse(status_code=404, content={"message": "Route not found", "path": path}, headers=_cors_headers())

    if request.method == "OPTIONS":
        return Response(status_code=204, headers=_cors_headers())

    upstream_url = f"http://127.0.0.1:{upstream_port}{path}"
    if request.url.query:
        upstream_url = f"{upstream_url}?{request.url.query}"

    headers = {key: value for key, value in request.headers.items() if key.lower() != "host"}
    body = await request.body()

    upstream_response = None
    last_error: Exception | None = None
    async with httpx.AsyncClient(timeout=60.0) as client:
        for attempt in range(1, 31):
            try:
                upstream_response = await client.request(
                    request.method,
                    upstream_url,
                    content=body,
                    headers=headers,
                )
                break
            except (httpx.ConnectError, httpx.RemoteProtocolError, httpx.ReadTimeout) as exc:
                last_error = exc
                if attempt == 30:
                    raise
                await asyncio.sleep(1)

    if upstream_response is None:
        raise last_error if last_error is not None else RuntimeError("Upstream request failed")

    response_headers = {
        key: value
        for key, value in upstream_response.headers.items()
        if key.lower() not in {"content-length", "transfer-encoding", "connection", "content-encoding"}
    }
    response_headers.update(_cors_headers())
    return Response(
        content=upstream_response.content,
        status_code=upstream_response.status_code,
        headers=response_headers,
        media_type=upstream_response.headers.get("content-type"),
    )
