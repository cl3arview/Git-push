from django.db import models



class Document(models.Model):

    ai_models =(
        ('bsrganx4', 'BSRGANx4'),
        ('bsrganx2', 'BSRGANx2')    )
    ai_model = models.CharField(max_length=8,choices=ai_models,default='BSRGANx4',blank=False)
    Denoiser_strength = models.CharField(max_length=100,blank=False,default=0.5)
    Upscaling_factor = models.CharField(max_length=100,blank=False,default=2)
    document = models.ImageField(upload_to='uploads')
