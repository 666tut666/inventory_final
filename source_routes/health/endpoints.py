from fastapi import APIRouter, Response, status

router = APIRouter(tags=["health"])


class HealthEndpoints:
    @staticmethod
    @router.get("/health/ping")
    def ping():
        return Response(status_code=status.HTTP_200_OK, content="Pong")
