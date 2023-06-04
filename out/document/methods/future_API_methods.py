import base64
from PIL import Image
from io import BytesIO



with open("", "rb") as image_file:
    data = base64.b64encode(image_file.read())
    final = data.decode('utf-8')
print(final)



from gradio_client import Client

client = Client("https://cle4rview-ganhancer.hf.space/")
result = client.predict(
				"https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png",	# str representing input in 'Source Image' Image component
				fn_index=0
)
print(result)

 