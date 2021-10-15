from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q

from .models import Order, OrderMatching

# Create your views here.

def home(request):
    """View function for home page of site."""
    num_sell_orders = Order.objects.filter(type__exact='s').count()
    num_buy_orders = Order.objects.filter(type__exact='b').count()
    num_users = User.objects.count() - 1

    context = {
        'num_sell_orders': num_sell_orders,
        'num_buy_orders': num_buy_orders,
        'num_users': num_users,
    }
    context['LocationDetail'] = {}
    for (c, name) in settings.LOCATION_CHOICE:
        obj = Order.objects.filter(location__exact=c)
        context['LocationDetail'][name] = {
            'num_sell_orders': obj.filter(type__exact='s').count(),
            'num_buy_orders': obj.filter(type__exact='b').count(),
        }
    return render(request, 'home.html', context=context)

def index(request):
    """View function for market page of site."""
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')

def get_orders(request):
    '''
    Get all Orders which have match TYPE and LOCATION
    '''
    # Get type and location from resquest
    type = request.GET.get('type', None)  
    location = request.GET.get('location', None)  

    if (type and location):
        # Find all object in data
        result = list(
            Order.objects.filter(
                type=type, location=location
            ).order_by('price').values()
        )
        if result:
            return JsonResponse({
                "status": "success",
                "result": result,
            })

    return JsonResponse({
        "status": "No items"
    })

# User Profile
class OderListofUser(LoginRequiredMixin, generic.ListView):
    """
    User profile view, list of orders create by User
    """
    model = Order
    # paginate_by = 5
    template_name ='market/user_profile.html'

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """
        Return list of Order objects created by User
        """
        target_user = get_object_or_404(User, username=self.request.user)
        return Order.objects.filter(username=target_user)
        
    def get_context_data(self, **kwargs):
        """
        Add User to context so they can be displayed in the template
        """
        # Call the base implementation first to get a context
        context = super(OderListofUser, self).get_context_data(**kwargs)
        # Get the user object from the "username" URL parameter and add it to the context
        user = get_object_or_404(User, username=self.request.user)
        if user:
            context['username'] = user.username
        return context

class MatchbyUser(LoginRequiredMixin, generic.ListView):
    """
    User profile view, list of orders create by User
    """
    model = OrderMatching
    template_name ='market/order_matching.html'
    ordering = ['username']

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """
        Return list of OrderMatching objects created by User
        """
        # type = 's' if (self.kwargs["type"]=='buy') else 'b'
        target_user = get_object_or_404(User, username=self.request.user)
        return OrderMatching.objects.filter(
                Q(username=target_user) |
                Q(order__username=target_user)
            ).filter(order__type__isnull=False)#.filter(order__type=type)

    def get_context_data(self, **kwargs):
        """
        Add User to context so they can be displayed in the template
        """
        # Call the base implementation first to get a context
        context = super(MatchbyUser, self).get_context_data(**kwargs)
        # Get the user object from the "username" URL parameter and add it to the context
        user = get_object_or_404(User, username=self.request.user)
        if user:
            context['username'] = user.username
        context['trader_type'] = 'bán' if (self.kwargs["type"][0]=='b') else 'mua'
        return context


# Order create, delete
class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['type', 'location', 'item_id', 'quality', 'price', 'amount']

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super(OrderCreate, self).form_valid(form)

    def get_success_url(self):
        """
        Back to the market home page
        """
        return reverse('user-profile')

class OrderDelete(LoginRequiredMixin, DeleteView):
    model = Order

    def get_queryset(self):
        """
        Return list of order objects created by current User
        """
        username = get_object_or_404(User, username=self.request.user)
        return Order.objects.filter(username=username)

    def get_success_url(self):
        """
        Back to the market home page
        """
        return reverse('user-profile')


# Order_Matching create, delete
class OrderMatchingCreate(LoginRequiredMixin, CreateView):
    model = OrderMatching
    fields = ['order', 'amount']

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super(OrderMatchingCreate, self).form_valid(form)

    def get_success_url(self):
        """
        Back to the market home page
        """
        # Minus the amount in Order by the amount match
        order_obj = Order.objects.get(id=self.object.order.id)
        order_obj.amount = order_obj.amount - self.object.amount
        order_obj.save()
        return reverse('market-index')

class OrderMatchingDelete(LoginRequiredMixin, DeleteView):
    model = OrderMatching

    def get_queryset(self):
        """
        Return list of order objects created by current User
        or the objects has order.username is current User
        """
        target_user = get_object_or_404(User, username=self.request.user)
        return OrderMatching.objects.filter(
                Q(username=target_user) |
                Q(order__username=target_user)
            ).filter(order__type__isnull=False)

    def get_success_url(self):
        """
        Back to the user page
        """
        # If cancel, return the amount minus when create
        order_obj = Order.objects.get(id=self.object.order.id)
        if (self.kwargs['st'] == 'cancel'):
            order_obj.amount = order_obj.amount + self.object.amount
            order_obj.save()
        # Delete order when amount become 0
        else:
            if (order_obj.amount==0):
                order_obj.delete()

        return reverse('matching-list-view', kwargs={'type': self.kwargs['type']})