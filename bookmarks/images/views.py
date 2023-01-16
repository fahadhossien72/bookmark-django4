from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . forms import ImageCreationForm
# Create your views here.
@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreationForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # assign current user to the item
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Image added successfully')
            # redirect to new created item detail view
            # return redirect(new_image.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreationForm(data=request.GET)
    context = {'form':form, 'section': 'images'}
    return render(request, 'images/create.html', context)