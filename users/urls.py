from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns=[

path('',views.home,name='home'),

path('farmerlogin/',views.farmerlogin,name='farmerlogin'),

path('officerlogin/',views.officerlogin,name='officerlogin'),

path('farmerregister/',views.farmerregister,name='farmerregister'),

path('officerregister/',views.officerregister,name='officerregister'),

path('farmerdashboard/',views.farmerdashboard,name='farmerdashboard'),

path('officerdashboard/',views.officerdashboard,name='officerdashboard'),

path('logout/', views.logout_view, name='logout'),

path('farmerprofile/',views.farmerprofile,name="farmerprofile"),

path("askquestion/", views.askquestion, name="askquestion"),

path("myquestions/", views.myquestions, name="myquestions"),

path("postannouncement/",views.postannouncement,name="postannouncement"),

path("announcements/",views.viewannouncements,name="viewannouncements"),

path("marketprices/", views.marketprices, name="marketprices"),

path("officermarketprices/", views.officermarketprices, name="officermarketprices"),

path("marketprice/add/", views.add_marketprice,name="add_marketprice"),

path("marketprice/edit/<int:id>/", views.edit_marketprice, name="edit_marketprice"),

path("marketprice/delete/<int:id>/", views.delete_marketprice, name="delete_marketprice"),

path("ask-officer/",views.ask_officer,name="ask_officer"),

path("officer-questions/",views.officer_questions,name="officer_questions"),

path("answer-question/<int:id>/",views.answer_question,name="answer_question"),

path("farm-records/",views.farm_records,name="farm_records"),

path("add-activity/",views.add_activity,name="add_activity"),

path("my-crop-advice/", views.my_crop_advice, name="my_crop_advice"),

path("add-crop-advice/", views.add_crop_advice, name="add_crop_advice"),

path("tips/", views.farming_tips, name="farming_tips"),

path("add-tip/", views.add_farming_tip, name="add_farming_tip"),

path("manage-farming-tips/",views.manage_farming_tips,name="manage_farming_tips"),

path("edit-farming-tip/<int:id>/",views.edit_farming_tip,name="edit_farming_tip"),

path("delete-farming-tip/<int:id>/",views.delete_farming_tip,name="delete_farming_tip"),

path("manage-crop-advice/",views.manage_crop_advice,name="manage_crop_advice"),

path("edit-crop-advice/<int:id>/",views.edit_crop_advice,name="edit_crop_advice"),

path("delete-crop-advice/<int:id>/",views.delete_crop_advice,name="delete_crop_advice"),

path("registered-farmers/", views.registered_farmers, name="registered_farmers"),

path("officer-profile/", views.officer_profile, name="officer_profile"),

path("weather/",views.weather_dashboard,name="weather_dashboard"),

path("load-subcounties/", views.load_subcounties, name="load_subcounties"),

path("load-wards/", views.load_wards, name="load_wards"),

path("save-location/", views.save_location, name="save_location"),

path("edit-profile/",views.edit_profile,name="edit_profile"),

path("edit-officer-profile/",views.edit_officer_profile,name="edit_officer_profile"),

path("edit-farm-activity/<int:id>/",views.edit_farm_activity,name="edit_farm_activity"),

path("delete-farm-activity/<int:id>/",views.delete_farm_activity,name="delete_farm_activity"),

path("website-feedback/",views.website_feedback,name="website_feedback"),

path("officer-tasks/",views.officer_tasks,name="officer_tasks"),

path("add-officer-task/",views.add_officer_task,name="add_officer_task"),

path("edit-officer-task/<int:id>/",views.edit_officer_task,name="edit_officer_task"),

path("delete-officer-task/<int:id>/",views.delete_officer_task,name="delete_officer_task"),

path("complete-officer-task/<int:id>/",views.complete_officer_task,name="complete_officer_task"),
     
]

