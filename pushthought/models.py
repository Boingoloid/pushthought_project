from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


# Create your models here.



class Program(models.Model):
    '''CATEGORY_CHOICES = (
        ('Documentary', 'Documentary'),
        ('Show/Series', 'Show/Series (including web only)'),
        ('Articles/Blog (written)','Articles/Blog (written)'),
        ('Podcast', 'Podcast'),
        ('Other', 'Other'),
    )
    category = models.CharField(max_length=255,
                                      choices=CATEGORY_CHOICES,)
    category_other = models.CharField(max_length=255,null=True,blank=True)
    '''

    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255,)
    image = models.ImageField(null=True,blank=True)
    description = models.TextField()
    userField = models.CharField(max_length=255,default=1,blank=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class Segment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    date_released = models.DateField(editable=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True,blank=True)
    link = models.URLField()
    description = models.TextField()
    episode = models.CharField(max_length=255,null=True,blank=True)
    program = models.ForeignKey(Program,editable=False)

    def __unicode__(self):
        return '%s | %s' % (self.date_released,self.title)

    def __str__(self):
        return '%s | %s' % (self.date_released,self.title)

    class Meta:
        ordering = ['-date_released']


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class MenuItem(models.Model):

    CATEGORY_CHOICES = (
        ('Local Representative', 'Local Representative'),
        ('Regulator', 'Regulator'),
        ('Executive', 'Executive'),
        ('Corporation', 'Corporation'),
        ('Petition', 'Petition'),
        ('Donation', 'Donation'),
        ('Other', 'Other'),
    )

    category = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    isMessage = models.NullBooleanField(null=True,blank=True)
    messageText = models.TextField(null=True,blank=True)
    messageType = models.CharField(max_length=255,null=True,blank=True)
    targetName = models.CharField(max_length=255,null=True,blank=True)
    phone = PhoneNumberField(null=True,blank=True)
    twitterID = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    website = models.URLField(null=True,blank=True)
    facebook_page = models.URLField(null=True,blank=True)
    segment = models.ForeignKey(Segment)
    image = models.ImageField(null=True,blank=True)

    class Meta:
        ordering = ['category','-isMessage','order',]

    def __unicode__(self):
        return '%s | %s | isMessage:%s' % (self.segment,self.category,self.isMessage)

    def __str__(self):
        return '%s | %s | isMessage:%s' % (self.segment,self.category,self.isMessage)


class LocalRepresentative(models.Model):
    category = models.CharField(max_length=255)
