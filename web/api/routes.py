from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .config import ALLOWED_PATH_CHARS
from .db import get_all_stats, record_attempt, reset_stats
from .exercises import discover_exercises, get_exercise_code
from .runner import run_code

router = APIRouter()


class RunRequest(BaseModel):
    code: str


def validate_path(value: str, name: str = "path") -> str:
    """Validate path component to prevent directory traversal."""
    if not value:
        raise HTTPException(status_code=400, detail=f"Invalid {name}: empty")
    if ".." in value or "/" in value or "\\" in value:
        raise HTTPException(status_code=400, detail=f"Invalid {name}: {value}")
    if not all(c in ALLOWED_PATH_CHARS for c in value.lower()):
        raise HTTPException(status_code=400, detail=f"Invalid {name}: {value}")
    return value


@router.get("/exercises")
def list_exercises() -> dict:
    """List all exercises grouped by topic, with stats."""
    stats = get_all_stats()
    exercises = discover_exercises()

    result = {}
    for topic, names in exercises.items():
        result[topic] = [
            {
                "name": name,
                "attempts": stats.get((topic, name), {}).get("attempts", 0),
                "passes": stats.get((topic, name), {}).get("passes", 0),
            }
            for name in names
        ]

    return result


@router.get("/exercises/{topic}/{name}")
def get_exercise(topic: str, name: str) -> dict:
    """Get skeleton code for an exercise."""
    topic = validate_path(topic, "topic")
    name = validate_path(name, "name")

    code = get_exercise_code(topic, name)
    if code is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return {"code": code}


@router.post("/exercises/{topic}/{name}/run")
def run_exercise(topic: str, name: str, request: RunRequest) -> dict:
    """Run user code and return test results."""
    topic = validate_path(topic, "topic")
    name = validate_path(name, "name")

    result = run_code(topic, name, request.code)
    record_attempt(topic, name, result.passed)
    return result.to_dict()


@router.get("/stats")
def get_stats() -> dict:
    """Get all exercise stats."""
    stats = get_all_stats()
    return {f"{topic}/{name}": data for (topic, name), data in stats.items()}


@router.delete("/exercises/{topic}/{name}/stats")
def reset_exercise_stats(topic: str, name: str) -> dict:
    """Reset stats for an exercise."""
    topic = validate_path(topic, "topic")
    name = validate_path(name, "name")
    reset_stats(topic, name)
    return {"status": "ok"}
