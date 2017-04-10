try:
    from urllib import quote_plus #python 2
except:
    pass
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
# Create your views here.
from django.core.paginator import Paginator ,EmptyPage,PageNotAnInteger
from django.http import HttpResponse ,HttpResponseRedirect,Http404 
from .models import Note
from .forms import PostForm
from django.db.models import Q 

'''
 Views for notes: create,update,details,delete
'''

def note_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form=PostForm(request.POST or None)
	if form.is_valid():
		instance=form.save(commit=False)
		#print form.cleaned_data.get("title")
		instance.save()
		instance.user=request.user
		messages.success(request,"Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
#	else:
#		messages.error(request,"Not Seccesfully Created")
	context={
	"form":form,
	}
	return render(request,"note_form.html",context)
def note_detail(request,slug=None):
	instance=get_object_or_404(Note,slug=slug)
	context={
		"title":instance.title,
		"instance":instance,

	}

	return render(request,"note_detail.html",context)

def note_list(request):
	queryset_list=Note.objects.all()
	query=request.GET.get("q")
	if query:
		queryset_list=queryset_list.filter(Q(title__icontains=query)|Q(content__icontains=query)|Q(user__first_name__icontains=query)
			|Q(user__last_name__icontains=query)
			).distinct()
	paginator=Paginator(queryset_list,3)
	page_request_var="page"
	page=request.GET.get(page_request_var)
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)
	context={
	"object_list": queryset,
	"title":"Notes",
	"page_request_var":page_request_var
	}	
	return render(request,"note_list.html",context)

def note_update(request,slug=None):
	instance=get_object_or_404(Note,slug=slug)
	form=PostForm(request.POST or None,instance=instance)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		messages.success(request,"<a href='#'> Item </a> Saved",extra_tages='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context={
		"title":instance.title,
		"instance": instance,
		"form": form,
	}
	return render(request,"note_form.html",context)
	
def note_delete(request,slug=None):
	instance=get_object_or_404(Note,slug=slug)
	instance.delete()
	messages.success(request,"Successfully deleted")
	return redirect("notes:list")
