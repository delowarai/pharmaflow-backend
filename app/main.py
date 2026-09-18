"""Application entry point."""

from fastapi import FastAPI

app = FastAPI(title="PharmaFlow Backend")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
