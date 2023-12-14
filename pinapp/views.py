from django.shortcuts import render, get_object_or_404, redirect
from pinapp.models import Image, Comments, Category, Follow
from pinapp.forms import ImageUploadForm, CommentsForm
from django.http import HttpResponse
from datetime import datetime
#from .models import Board  
from .models import SavedImage



def base(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'base.html', context)

def category(request):
    categories = Category.objects.all()
    for i in categories:
        print(i.id)
    if request.GET.get('q'):
       query = request.GET.get('q')
       categories = Category.objects.filter(title__icontains=query)

    context = {'categories': categories}
    return render(request, 'category.html', context)

def image_list(request, image_id, slug):
    images = Image.objects.filter(category=image_id)
    print(images)
    return render(request, 'image_list.html', {'images': images})


def image_detail(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    comments = image.comments.all()
    is_following = Follow.objects.filter(user=request.user, image=image, followed=True).exists()
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.image = image
            new_comment.user_name = request.user.username  # Assign logged-in user as the commenter
            new_comment.save()
            return redirect('pinapp:image_detail', image_id=image_id)
    else:
        form = CommentsForm()

    return render(request, 'image_detail.html', {'i': image, 'comments': comments, 'form': form,'is_following': is_following})

    


def success(request):
    return render(request,'success.html')


def download_image(request, pk):
    image = get_object_or_404(Image, pk=pk)
    print(image)

    response = HttpResponse(image.image, content_type='image')
    response['Content-Disposition'] = f'attachment; filename="{image.title}.png"'

    return response

def index(request):
	
 return render(request,'index.html')
 from pinapp.models import Image, Follow

def follow_image(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    user = request.user
    follow_instance, created = Follow.objects.get_or_create(user=user, image=image)

    if 'follow' in request.POST:
        follow_instance.followed = True
    elif 'unfollow' in request.POST:
        follow_instance.followed = False
    
    follow_instance.save()
    return redirect('pinapp:image_detail', image_id=image_id)

from django.shortcuts import get_object_or_404
from .models import Image  # Import your Image model
from datetime import datetime

def create(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save(commit=False)
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            category_id = request.POST.get('category')
            
            # Instead of fetching Category object, save directly to Image model
            image_instance.title = title
            image_instance.description = description
            image_instance.image = request.FILES['image']
            image_instance.upload_date = datetime.now()
            image_instance.category_id = category_id  # Assign category ID directly

            image_instance.save()
            return redirect('pinapp:success')  # Redirect to a success URL after saving
    else:
        form = ImageUploadForm()

    return render(request, 'create.html', {'form': form, 'categories': categories})



#===========================================================================================
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def save_image(request, image_id):
    # Get the image object based on the image_id
    image = get_object_or_404(Image, pk=image_id)

    # Create a SavedImage object for the logged-in user and the image
    SavedImage.objects.get_or_create(user=request.user, image=image)

    # Return a success response
    return redirect('pinapp:display_saved_images')


@login_required
def display_saved_images(request):
    # Get all the saved images for the logged-in user
    saved_images = SavedImage.objects.filter(user=request.user)

    return render(request, 'saved_images.html', {'saved_images': saved_images})
def explore(request):
    return render(request, 'explore.html')
    

    





