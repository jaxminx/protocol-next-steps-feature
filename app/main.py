"""The API. Routes use /me rather than a member ID, so a caller can only ever reach their own data."""
import json
import logging
import time
import uuid
from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.cleaning import clean
from app.config import DEMO_TOKENS, DemoUser
from app.next_steps import build_next_steps
from app.records import load_member_file

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("next_steps")

# Loaded once at startup, so a broken file stops the server instead of failing mid-request.
MEMBER_FILES = {
    user.member_id: load_member_file(DATA_DIR / f"{user.member_id}.json")
    for user in DEMO_TOKENS.values()
}

app = FastAPI(title="Next Steps API", description="Flags, retest status and suggested tests for a member.")


class Unauthorized(Exception):
    pass


def authenticate(
    credentials: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False)),
) -> DemoUser:
    if credentials is None or credentials.credentials not in DEMO_TOKENS:
        raise Unauthorized
    return DEMO_TOKENS[credentials.credentials]


@app.exception_handler(Unauthorized)
async def handle_unauthorized(request: Request, exc: Unauthorized) -> JSONResponse:
    return JSONResponse({"error": "unauthorized"}, status_code=401, headers={"WWW-Authenticate": "Bearer"})


@app.middleware("http")
async def protect_and_log(request: Request, call_next):
    """Stops health data being cached, hides error details, and logs without values or names."""
    request_id = uuid.uuid4().hex
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as exc:
        # Only the exception type: its message could contain a health value.
        log.error(json.dumps({"request_id": request_id, "error": type(exc).__name__}))
        response = JSONResponse({"error": "internal_error", "request_id": request_id}, status_code=500)

    if request.url.path.startswith("/v1/"):
        response.headers["Cache-Control"] = "no-store"
    log.info(json.dumps({
        "request_id": request_id,
        "path": request.url.path,
        "status": response.status_code,
        "ms": round((time.perf_counter() - started) * 1000, 1),
    }))
    return response


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/v1/me/next-steps")
def next_steps(user: DemoUser = Depends(authenticate)) -> JSONResponse:
    record = clean(MEMBER_FILES[user.member_id])
    return JSONResponse(jsonable_encoder(build_next_steps(record, user.preferred_name)))
