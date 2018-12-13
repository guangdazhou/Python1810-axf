from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^home/$', views.home, name='home'),

    url(r'^marketbase/$', views.marketbase, name='marketbase'),
    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name='market'),

    url(r'^cart/$', views.cart, name='cart'),
    url(r'^mine/$', views.mine, name='mine'),

    url(r'^register/$', views.register, name='register'),
    url(r'^checkemail/$', views.checkemail, name=
        'checkemail'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^addcart/$', views.addcart, name='addcart'),
    url(r'^subcart/$',views.subcart,name='subcart'),

    url(r'^changecartstatus/$',views.changecartstatus,name='changecartstatus'),
    url(r'^changecartisall/$',views.changecartisall,name='changecartisall'),

    url(r'^generateorder/$',views.generateorder,name='generateorder'),
    url(r'^orderdetail/(\d+)/$',views.orderdetail,name='orderdetail'),
    url(r'^orderlist/(\d+)/$', views.orderlist, name='orderlist'),
]