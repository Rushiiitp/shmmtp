from django.db import models
import numpy as np
from django.core.files import File
from PIL.Image import open
import tensorflow as tf
from keras.models import load_model
import os
# Create your models here.


class Image(models.Model):
    # picture = models.ImageField()
    classified = models.CharField(max_length=200, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    picture = models.FileField()

    def __str__(self):
        return "Image classified at {}".format(self.uploaded.strftime("%Y-%m-%d %H:%M"))

    def save(self, *args, **kwargs):
        try:
            img = open(self.picture)
            imgRsz = img.resize((120, 120))
            pix = np.array(imgRsz)
            imgScaled = pix/255.0
            inputImg = np.expand_dims(imgScaled, axis=0)
            # model
            print(inputImg.shape)
            path = os.getcwd()
            print(os.path.join(path, r"imagesApp\classificationModel\\temp.h5"))

            model = load_model(
                os.path.join(path, r"imagesApp\classificationModel\\temp.h5"))

            # print("im hereeeeeeeeeeeeeeeeeeeeeeeeee")
            if model.predict(inputImg) > 0.5:
                self.classified = "There is no crack on wall"
                print(1, "There is no crack on wall")
            else:
                self.classified = "There is crack on wall"
                print(0, "there is crack on a wall")
            print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")

            print("suceessfully image is classified !!!!!")
            return self.classified
        except:
            print("classification failed")
        super().save(*args, **kwargs)
