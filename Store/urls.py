from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.template.context_processors import static
from django.urls import path
from.import views

urlpatterns = [
    path('',views.store,name="store"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('update_item/',views.updateItem,name="update_item"),
]
urlpatterns += staticfiles_urlpatterns()#point to remember for css