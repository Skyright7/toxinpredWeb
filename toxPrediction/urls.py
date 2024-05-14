
from django.urls import path

from .views import doToxPredict,taskResult

urlpatterns = [
    path('api/toxPredict/', doToxPredict, name='doToxPredict'),
    path('task_result/',taskResult, name='taskResult')
]