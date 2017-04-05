from __future__ import unicode_literals
from django.db import models

from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils.safestring import mark_safe
from markdown_deux import markdown
# Create your models here.

class Note(models.Model):
	title=models.CharField(max_length=100)
	content=models.TextField()
	user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	slug=models.SlugField(unique=True)
	updated=models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)
	publish=models.DateField(auto_now=False,auto_now_add=False)
	def __unicode__(self):
		return self.title
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("notes:detail",kwargs={"slug": self.slug})
	def get_absolute_url_edit(self):
		return reverse("notes:update",kwargs={"slug": self.slug})


	class Meta:
		ordering=["timestamp"]

	def get_markdown(self):
		content=self.content
		markdown_text= markdown(content)
		return mark_safe(markdown_text)


def create_slug(instance,new_slug=None):
	slug=slugify(instance.title)
	if new_slug is not None:
		slug=new_slug
	qs= Note.objects.filter(slug=slug).order_by("-id")		
	exists=qs.exists()
	if exists:
		new_slug="%s-%s" %(slug,qs.first().id)
		return create_slug(instance,new_slug=new_slug)
	return slug

def pre_save_post_reciever(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug=create_slug(instance)

pre_save.connect(pre_save_post_reciever,sender=Note)

