# VideoGen

FastAPI starter for submitting video jobs to the RunPod Serverless endpoint `ejj95trq8vd2iu`.

## Current status

The existing endpoint is a ComfyUI base worker without the Wan 2.2 model files. The included Dockerfile builds a compatible worker image and the API workflow is ready to submit after deployment.

## Run locally

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export RUNPOD_API_KEY='your-key'
export RUNPOD_ENDPOINT_ID='ejj95trq8vd2iu'
uvicorn app.main:app --reload
```

`POST /videos` submits an asynchronous RunPod job, `GET /videos/{job_id}` checks status, and `POST /videos/sync` submits a synchronous job.

## Deploy the Wan worker

Use the repository's `Dockerfile` through RunPod's GitHub deployment flow. It downloads the diffusion model, text encoder, and VAE required by `workflows/wan2_2_5b_t2v_api.json`. See [RUNPOD_DEPLOY.md](RUNPOD_DEPLOY.md).

Never commit API keys or a populated `.env` file.
