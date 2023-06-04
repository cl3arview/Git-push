from django import forms

from .models import Document

class UploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields =('document','ai_model','Denoiser_strength','Upscaling_factor') 



 
 