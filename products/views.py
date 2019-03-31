from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Product,Vote
from django.utils import timezone
from django.db import IntegrityError
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.urls import reverse_lazy
from django.views import generic

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
    if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.POST['circulating_supply'] and request.FILES['image'] and request.POST['max_supply'] :
      product = Product()
      product.title = request.POST['title']
      product.body = request.POST['body']
      if request.POST['url'].startswith('https://'):
        product.url = request.POST['url']
      else:
        product.url = 'https://' + request.POST['url']
      #product.icon = request.FILES['icon']
      
      product.circulating_supply = request.POST['circulating_supply']
      product.max_supply = request.POST['max_supply']
      product.image = request.FILES['image']
      product.pub_date = timezone.datetime.now()
      product.votes_total = 1
      product.hunter = request.user
      #check that length of the file is between 20 and 250 characters
      if len(request.POST['body']) < 50 or len(request.POST['body']) > 270:
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


class UpdateProduct(LoginRequiredMixin,generic.UpdateView):
  model = Product
  template_name = 'edit.html'
  fields = ['title','body','url','max_supply','circulating_supply']
  success_url = reverse_lazy('home')
  def get_object(self):
    product = super(UpdateProduct, self).get_object()
    if not product.hunter == self.request.user:
      raise Http404
    return product

class DeleteProduct(LoginRequiredMixin, generic.DeleteView):
  model = Product
  template_name = 'delete.html'
  success_url = reverse_lazy('home')
  #to ensure users can only delete own videos
  def get_object(self):
    product = super(DeleteProduct, self).get_object()
    if not product.hunter == self.request.user:
      raise Http404
    return product


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
