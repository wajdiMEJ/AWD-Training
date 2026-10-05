"""Notification microservice - entry point.

Run:  uvicorn app.main:app --reload --port 8084
  or: python -m app.main
"""
import os

from fastapi import FastAPI
from py_eureka_client import eureka_client

from app.routers import notification

PORT = int(os.getenv("PORT", "8084"))

app = FastAPI(
    title="Notification Microservice API",
    version="1.0.0",
    description=(
        "Notification microservice (Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; the notification logic is to be developed by students."
    ),
    contact={"name": "Badia Abouhdid"},
    servers=[{"url": f"http://localhost:{PORT}", "description": "Local"}],
    # Same URLs as the other microservices of the project
    docs_url="/swagger-ui",       # Swagger UI
    openapi_url="/v3/api-docs",   # OpenAPI JSON
    redoc_url="/redoc",           # alternative documentation
)

app.include_router(notification.router)

@app.on_event("startup")
async def register_with_eureka() -> None:
    await eureka_client.init_async(
        eureka_server="http://localhost:8761/eureka/",
        app_name="NOTIFICATION",
        instance_port=PORT,
        instance_host="127.0.0.1",
        health_check_url=f"http://localhost:{PORT}/api/notifications/hello",
        status_page_url=f"http://localhost:{PORT}/api/notifications/hello",
    )


@app.on_event("shutdown")
async def unregister_from_eureka() -> None:
    await eureka_client.stop_async()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)
