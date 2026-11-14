from fastapi import FastAPI, HTTPException

from app.runpod import RunPodClient, RunPodError
from app.schemas import VideoJob, VideoRequest

app = FastAPI(title="VideoGen API", version="0.1.0")
runpod = RunPodClient()


def worker_input(request: VideoRequest) -> dict:
    if request.mode == "image_to_video" and request.image_url is None:
        raise HTTPException(status_code=422, detail="image_url is required for image_to_video")
    return {
        "prompt": request.prompt,
        "mode": request.mode,
        "image_url": str(request.image_url) if request.image_url else None,
        "workflow": request.workflow,
        "width": request.width,
        "height": request.height,
        "frames": request.frames,
        "fps": request.fps,
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/videos", response_model=VideoJob, status_code=202)
async def create_video(request: VideoRequest) -> dict:
    try:
        return await runpod.submit(worker_input(request))
    except RunPodError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/videos/sync")
async def create_video_sync(request: VideoRequest) -> dict:
    try:
        return await runpod.submit_sync(worker_input(request))
    except RunPodError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/videos/{job_id}", response_model=VideoJob)
async def get_video(job_id: str) -> dict:
    try:
        return await runpod.status(job_id)
    except RunPodError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
