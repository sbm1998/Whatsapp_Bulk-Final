from django.urls import path
from .views import send_view,add_one_view,add_csv_view,send_attachment_view,welcome_view,list_phone_number_view,number_delete_view

urlpatterns = [
    path("",welcome_view,name="welcome"),
    path("message",send_view,name="send"),
    path("add_one",add_one_view,name="one"),
    path("add_csv",add_csv_view,name="csv"),
    path("attachment",send_attachment_view,name="attachment"),
    path("phone_numbers",list_phone_number_view,name="phone_number"),
    path("<int:id>/number_delete",number_delete_view,name="number_delete"),
]