import gradio as gr
import cv2
import numpy
import os
import random
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url
import gc
import torch.cuda

from realesrgan import RealESRGANer
 

last_file = None
img_mode = "RGBA"

 

def realesrgan(img, model_name, denoise_strength, outscale):
    """Real-ESRGAN function to restore (and upscale) images.
    """
    if not img:
        return

    # Define model parameters
    if model_name == 'ESERGANx4':   
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        netscale = 4
        file_path = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth']
    elif model_name == 'ESRNetx4':  
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        netscale = 4
        file_path = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/RealESRNet_x4plus.pth']
   
    elif model_name == 'ESERGANx2':   
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
        netscale = 2
        file_path = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth']

    # Determine model paths  (local loading in other project, try and merge ?)
    model_path = os.path.join('weights', model_name + '.pth')
    if not os.path.isfile(model_path):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        for url in file_path:
            # model_path will be updated
            model_path = load_file_from_url(
                url=url, model_dir=os.path.join(ROOT_DIR, 'weights'), progress=True, file_name=None)

    # denoiser control
    dni_weight = None
    if model_name == 'realesr-general-x4v3' and denoise_strength != 1:
        wdn_model_path = model_path.replace('realesr-general-x4v3', 'realesr-general-wdn-x4v3')
        model_path = [model_path, wdn_model_path]
        dni_weight = [denoise_strength, 1 - denoise_strength]

    # Restorer Class
    upsampler = RealESRGANer(
        scale=netscale,
        model_path=model_path,
        dni_weight=dni_weight,
        model=model,
        tile=0,
        tile_pad=10,
        pre_pad=10,
        half=False,
        gpu_id=None
    )
 
    cv_img = numpy.array(img)
    img = cv2.cvtColor(cv_img, cv2.COLOR_RGBA2BGRA)
 
    try:
            output, _ = upsampler.enhance(img, outscale=outscale)
    except RuntimeError as error:
        print('Error', error)
        print('If you encounter CUDA out of memory, try to set --tile with a smaller number.')
    else:
        # Save restored image and return it to the output Image component
        if img_mode == 'RGBA':  # RGBA images should be saved in png format
            extension = 'png'
        else:
            extension = 'jpg'

        out_filename = f"output_{rnd_string(8)}.{extension}"
        cv2.imwrite(out_filename, output)
        global last_file
        last_file = out_filename
        torch.cuda.empty_cache()
        gc.collect()
        return out_filename


def rnd_string(x):

    characters = "abcdefghijklmnopqrstuvwxyz_0123456789"
    result = "".join((random.choice(characters)) for i in range(x))
    return result


def reset():

    global last_file
    if last_file:
        print(f"Deleting {last_file} ...")
        os.remove(last_file)
        last_file = None
        torch.cuda.empty_cache()
        gc.collect()

    return gr.update(value=None), gr.update(value=None)


def has_transparency(img):
    """Alpha channel checking
    """
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True
    return False


def image_properties(img):
    """
        Dimensions, (A)RGB
    """
    global img_mode
    if img:
        if has_transparency(img):
            img_mode = "RGBA"
        else:
            img_mode = "RGB"
        properties = f"Width: {img.size[0]}, Height: {img.size[1]}  |  Color Mode: {img_mode}"
        return properties
    
 


def main():
 
    with gr.Blocks(title="ESERGAN Portable") as demo:

        

        with gr.Accordion("Options/Parameters"):
            with gr.Row():
                model_name = gr.Dropdown(label="ESRGAN inference model to be used",
                                         choices=["ESERGANx4", "ESRNetx4",
                                                  "ESERGANx2",],
                                         value="ESERGANx2", show_label=True)
                denoise_strength = gr.Slider(label="Denoise Strength",
                                             minimum=0, maximum=1, step=0.1, value=0.62)
                outscale = gr.Slider(label="Upscaling Factor",
                                     minimum=1, maximum=10, step=1, value=3, show_label=True)
 

        with gr.Row():
            with gr.Group():
                input_image = gr.Image(label="Source Image", type="pil", image_mode="RGBA" )
                input_image_properties = gr.Textbox(label="Image Properties", max_lines=1 )
            output_image = gr.Image(label="Restored Image", image_mode="RGBA")
        with gr.Row():
            restore_btn = gr.Button("Restore Image")
            reset_btn = gr.Button("Reset")

        # Event listeners:
        input_image.change(fn=image_properties, inputs=input_image, outputs=input_image_properties)
        restore_btn.click(fn=realesrgan,
                          inputs=[input_image, model_name, denoise_strength,  outscale],
                          outputs=output_image)
        reset_btn.click(fn=reset, inputs=[], outputs=[output_image, input_image])

 
    demo.launch(share=False)


if __name__ == "__main__":
    main()