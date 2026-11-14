# Deploy the Wan 2.2 worker

The existing RunPod endpoint runs a ComfyUI base worker. It contains no Wan model files, which is why generation fails before execution.

## Deployment route

Use RunPod's GitHub deployment flow so RunPod builds the image in the cloud.

1. In RunPod, create a Serverless endpoint from this GitHub repository.
2. Use `/` as the context path and `Dockerfile` as the Dockerfile path.
3. Configure one GPU per worker and select a GPU with enough VRAM for Wan 2.2 TI2V 5B.
4. Start with zero active workers and one maximum worker to control cost.
5. Set a container disk of at least 30 GB because the image embeds the model weights.
6. Wait for the endpoint to report Ready, then submit `workflows/wan2_2_5b_t2v_api.json`.

## Required model paths

- `models/diffusion_models/wan2.2_ti2v_5B_fp16.safetensors`
- `models/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors`
- `models/vae/wan2.2_vae.safetensors`

After deployment, the workflow must no longer report empty lists for `UNETLoader` or `CLIPLoader`, or restrict `VAELoader` to `pixel_space`.
