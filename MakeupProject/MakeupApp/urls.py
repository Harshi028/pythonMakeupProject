from django.urls import path
from . import views 

app_name = 'MakeupApp'
urlpatterns = [
    path('',views.index,name='index'),
    path('signin/',views.sign_in,name='sign_in'),
    path('signup/',views.sign_up,name='sign_up'),
    path('handle_signin/',views.handle_signin,name='handle_signin'),
    path('handle_signup/',views.handle_signup,name='handle_signup'),
    path('add_par/',views.add_par, name = 'add_par'),
    path('display_par/',views.display_par, name = 'display_par'),
    path('view_menu/<int:id>/',views.view_menu,name = 'view_menu'),
    path('add_menu/<int:par_id>/',views.add_menu, name = 'add_menu'),
    path('delete_menu/<int:id>/',views.delete_menu, name= 'delete_menu'),
    path('cusdisplay_par/<str:username>/',views.cusdisplay_par, name = 'cusdisplay_par'),
    path('cusmenu/<int:id>/<str:username>/',views.cusmenu, name = 'cusmenu'),
    path('show_cart/<str:username>/',views.show_cart,name = "show_cart"),
    path('add_to_cart/<int:menuid>/<str:username>/',views.add_to_cart, name = 'add_to_cart'),
    path('orders/<str:username>',views.orders, name = 'orders'),
    path('checkout/<str:username>/',views.checkout, name = 'checkout'),
]