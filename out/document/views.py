from django.shortcuts import render,redirect
from .forms import UploadForm
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
 

 
def index(request):
    return render(request, 'document/index.html')
 
def beta(request):
    if request.method == 'POST':
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'document/beta.html')
    else:
        form = UploadForm()
        return render(request, 'document/beta.html',{'form' : form})

def stripped(request):
    return render(request, 'document/stripped.html')



import base64
from PIL import Image
from io import BytesIO

 

# Grabbing the Form from the POST request and serializing it into a dict so it can exposed to the FAST_API endpoint 
def stripped(request):
    if request.method == 'POST':
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            form_post = UploadForm.POST.copy() # to make it mutable
            to_encode = form_post['document'] 
            to_encode = base64.b64encode(to_encode.read()).decode('utf-8')
            UploadForm.POST = form_post
            form.save()
            return render(request, 'document/stripped.html')
    else:
        form = UploadForm()
    
        return render(request, 'document/stripped.html',{'form' : form})
    



 


