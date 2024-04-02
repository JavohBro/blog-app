from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import FileExtensionValidator
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to='post_pics/', blank=True, null=True)
    post_video = models.FileField(upload_to='post_videos/', blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    likes = models.PositiveIntegerField(default=0)    

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.post_image:  # Check if there's an image to resize
            with Image.open(self.post_image.path) as img:
                if img.height > 750 or img.width > 500:
                    output_size = (750, 500)
                    img.thumbnail(output_size)
                    img.save(self.post_image.path)
                    
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

         # When image height is greater than its width
        if img.height > img.width:
            # make square by cutting off equal amounts top and bottom
            left = 0
            right = img.width
            top = (img.height - img.width)/2
            bottom = (img.height + img.width)/2
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 300 or img.width >300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

        # When image width is greater than its height
        elif img.width > img.height:
            # make square by cutting off equal amounts left and right
            left = (img.width - img.height)/2
            right = (img.width + img.height)/2
            top = 0
            bottom = img.height
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 300 or img.width >300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "post")


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.content