from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product,Vote
from django.utils import timezone
from django.db import IntegrityError
from django.http import HttpResponse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.

def home(request):
  # products = Product.objects.all()
  products = Product.objects.order_by('-votes_total')
  paginator = Paginator(products, 10)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'products':paged_listings
  }
  return render(request,'home1.html', context)
  # return render(request,'home1.html', {'products':products})

def search(request):
  queryset_list = Product.objects.order_by('pub_date')
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(title__icontains=keywords)

      context ={
        'products':queryset_list
      }
      return render(request,'home1.html',context)
@login_required
def create(request):
  if request.method=='POST':
    if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
      product = Product()
      product.title = request.POST['title']
      product.body = request.POST['body']
      if request.POST['url'].startswith('http://'):
        product.url = request.POST['url']
      else:
        product.url = 'http://' + request.POST['url']
      product.icon = request.FILES['icon']
      product.image = request.FILES['image']
      product.pub_date = timezone.datetime.now()
      product.votes_total = 1
      product.hunter = request.user
      #check that length of the file is between 20 and 250 characters
      if len(request.POST['body']) < 50 or len(request.POST['body']) > 250:
        return render(request,'create.html',{'lenerror':'The body needs to contain from 20 to 250 characters'})
      else:
        product.save()
        return redirect('home')
      #return redirect('/products/' + str(product.id))
    else:
      return render(request,'create.html',{'error':'all fields are required'})
  else:
    return render(request, 'create.html')

  return render(request,'create.html')

def detail(request,product_id):
  product = get_object_or_404(Product, pk=product_id)
  return render(request,'detail.html',{'product':product})

# @login_required
# def upvote(request,product_id,user_id):
#   if request.method=='POST':
#     try:
#       vote = Vote.objects.get(productID=product_id,userID=user_id)
#     except Vote.DoesNotExist:
#       vote = None
#     if vote is not None:
#       product = get_object_or_404(Product, pk=product_id)
#       product.votes_total += 1
#       product.save()
#       return redirect('/products/'+str(product.id))

@login_required
def upvote(request,product_id):
  if request.method=='POST':
    product = get_object_or_404(Product, pk=product_id)
    product.votes_total += 1
    try:
      Vote.objects.create(product=product, user=request.user)
      product.save()
    except IntegrityError:  # if "unique_together" fails, it will rais an  "IntegrityError" exception
      morethanonevote = "only one vote please"
      return render(request,'detail.html',{'morethanonevote':morethanonevote})

    return redirect('/products/'+str(product.id))

# @login_required
# def upvote(request,product_id):
#   if request.method=='POST':
#     product = get_object_or_404(Product, pk=product_id)
#     product.votes_total += 1
#     product.save()
#     return redirect('/products/'+str(product.id))
