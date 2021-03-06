"""testplatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from testenvconfig import views as testenvconfigviews
from tester import views as testerviews
from dataconfigurator import views as dataconfiguratorviews

route=DefaultRouter()
route.register('user/info', testenvconfigviews.UserInfoViewset,basename='userinfo')
route.register('user/project',testenvconfigviews.UserProjectViewset,basename='userproject')
route.register('project',testenvconfigviews.ProjectViewset,)
route.register('route',testerviews.RouteViewset)
route.register('datasource',dataconfiguratorviews.DataSourceViewset,)
route.register('case',testerviews.CaseViewset,)
route.register('task',testerviews.TaskViewset,)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(route.urls)),
    # path('user/info/', views.UserProjectViewset),
    # 此处配置jwt认证接口
    path('login/', obtain_jwt_token),
]
