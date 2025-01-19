from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.template.context_processors import static
from django.urls import path
from.import views

urlpatterns = [
    path('store/',views.store,name="store"),
    path('',views.home,name="home"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('update_item/',views.updateItem,name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('signup/', views.signup_user, name="signup"),
    path('search',views.search,name="search"),
]
urlpatterns += staticfiles_urlpatterns()#point to remember for css