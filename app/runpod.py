import httpx

from app.config import settings


class RunPodError(Exception):
    pass


class RunPodClient:
    def __init__(self) -> None:
        self.base = f"{settings.runpod_api_base.rstrip('/')}/{settings.runpod_endpoint_id}"
        self.headers = {
            "Authorization": f"Bearer {settings.runpod_api_key}",
            "Content-Type": "application/json",
        }

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        try:
            async with httpx.AsyncClient(timeout=settings.runpod_timeout_seconds) as client:
                response = await client.request(
                    method, f"{self.base}/{path.lstrip('/')}", headers=self.headers, **kwargs
                )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise RunPodError(
                f"RunPod returned HTTP {exc.response.status_code}: {exc.response.text[:1000]}"
            ) from exc
        except (httpx.HTTPError, ValueError) as exc:
            raise RunPodError(f"Could not complete RunPod request: {exc}") from exc

    async def submit(self, payload: dict) -> dict:
        return await self._request("POST", "run", json={"input": payload})

    async def submit_sync(self, payload: dict) -> dict:
        return await self._request("POST", "runsync", json={"input": payload})

    async def status(self, job_id: str) -> dict:
        return await self._request("GET", f"status/{job_id}")
