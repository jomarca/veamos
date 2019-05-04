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
from django.forms import ModelForm
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import numpy as np



# from .models import Comment


# class CommentForm(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('name', 'email', 'body')
  
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

# def detail(request,product_id):
#   product = get_object_or_404(Product, pk=product_id)

#     # List of active comments for this post
#   comments = product.comments.filter(active=True)

#   if request.method == 'POST':
#         # A comment was posted
#     comment_form = CommentForm(data=request.POST)
#     if comment_form.is_valid():
#             # Create Comment object but don't save to database yet
#       new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#       new_comment.product = product
#       new_comment.user = request.user
#             # Save the comment to the database
#       new_comment.save()
#   else:
#     comment_form = CommentForm()   

#   return render(request,
#                   'detail.html',
#                   {'product': product,
#                    'comments': comments,
                  #  'comment_form': comment_form})

# def testpandas(request):
#   t = np.arange(0.0, 2.0, 0.01)
#   s = 1 + np.sin(2 * np.pi * t)

#   fig, ax = plt.subplots()
#   ax.plot(t, s)

#   ax.set(xlabel='time (s)', ylabel='voltage (mV)', title='About as simple as it gets, folks')
#   ax.grid()
#   response = HttpResponse(content_type = 'image/png')
#   canvas = FigureCanvasAgg(fig)
  
#   return render(request,
#                   'test.html',
#                   {'graph': canvas,
#                   })


# def detail(request,product_id):
#   product = get_object_or_404(Product, pk=product_id)
#   return render(request,'detail.html',{'product':product})

# class DeleteComment(LoginRequiredMixin, generic.DeleteView):
#   model = Comment
#   template_name = 'detail.html'
#   # slug_url_kwarg = 'id'
#   #to ensure users can only delete own videos
#   def get_object(self):
#     product = super(DeleteComment,self).get_object()
#     if not product.user == self.request.user:
#       raise Http404
#     return product


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
#test

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

#TOD LO DE ORDENAR:

def ordenardate(request):
  # products = Product.objects.all()
  products = Product.objects.order_by('pub_date')
  paginator = Paginator(products, 10)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'products':paged_listings
  }
  return render(request,'home1.html', context)

def ordenarname(request):
  # products = Product.objects.all()
  products = Product.objects.order_by('title')
  paginator = Paginator(products, 10)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'products':paged_listings
  }
  return render(request,'home1.html', context)

def votes_total(request):
  # products = Product.objects.all()
  products = Product.objects.order_by('-votes_total')
  paginator = Paginator(products, 10)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'products':paged_listings
  }
  return render(request,'home1.html', context)