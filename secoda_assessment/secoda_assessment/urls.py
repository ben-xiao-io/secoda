"""
URL configuration for secoda_assessment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from metadata_extractor.views import get_table_metadata, get_table_metadata_from_str

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get-table-metadata/', get_table_metadata, name='get_table_metadata'),
    path('api/get-table-metadata-from-str/', get_table_metadata_from_str, name='get_table_metadata_from_str'),
]
