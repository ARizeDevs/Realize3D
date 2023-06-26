import torch

from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
# from shap_e.util.notebooks import create_pan_cameras, decode_latent_images, gif_widget
from shap_e.util.notebooks import decode_latent_mesh
from shap_e.util.image_util import load_image

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
xm = load_model('transmitter', device=device) 
model = load_model('image300M', device=device)
diffusion = diffusion_from_config(load_config('diffusion')) 

batch_size = 1 # this is the size of the models, higher values take longer to generate.
guidance_scale = 3.0 # this is the scale of the guidance, higher values make the model look more like the prompt.
# prompt = "mid century sofa" # this is the prompt, you can change this to anything you want.

image = load_image("img.png")
image1 = load_image("img2.png")

print("i got the image kos kesh")

latents = sample_latents(
    batch_size=batch_size,
    model=model,
    diffusion=diffusion,
    guidance_scale=guidance_scale,
    model_kwargs=dict(images=[image, image1] * batch_size),
    progress=True,
    clip_denoised=True,
    use_fp16=True,
    use_karras=True,
    karras_steps=64,
    sigma_min=1e-3,
    sigma_max=160,
    s_churn=0,
)


# render_mode = 'nerf' # you can change this to 'stf'
# size = 64 # this is the size of the renders, higher values take longer to render.

# cameras = create_pan_cameras(size, device)
# for i, latent in enumerate(latents):
#     images = decode_latent_images(xm, latent, cameras, rendering_mode=render_mode)
#     display(gif_widget(images))


    # Example of saving the latents as meshes.

for i, latent in enumerate(latents):
    t = decode_latent_mesh(xm, latent).tri_mesh()
    with open(f'example_mesh_{i}.ply', 'wb') as f: # this is three-dimensional geometric data of model.
        t.write_ply(f)
    with open(f'example_mesh_{i}.obj', 'w') as f: # we will use this file to customize in Blender Studio later.
        t.write_obj(f)