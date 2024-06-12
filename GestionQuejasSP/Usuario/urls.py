from django.urls import path
from .views import user_list, create_user, edit_user, group_create, group_edit, group_list, \
    password_change_done, ClasificacionListView, ClasificacionDeleteView, ClasificacionUpdateView, \
    ClasificacionCreateView, \
    conclusion_new, conclusion_delete, conclusion_edit, enti_new, enti_delete, enti_edit, satis_delete, satis_edit, \
    satis_new, caso_delete, caso_edit, caso_new, moda_new, moda_delete, moda_edit, via_new, via_edit, via_delete, \
    procedencia_edit, procedencia_delete, procedencia_new, confirmiar_eliminacion, confirmiar_eliminacion_group, \
    crear_usuario

from django.contrib.auth.views import PasswordChangeView
from .views import MyPasswordChangeView

urlpatterns = [

    # User Crud
    path('', user_list, name='user_list'),
    path('create/', create_user, name='user_create'),
    path('registro_user/', crear_usuario, name='registro_user'),
    path('update/<int:pk>/', edit_user, name='user_update'),
    path('confirmiar_eliminacion/<int:pk>/', confirmiar_eliminacion, name='confirmiar_eliminacion'),

    # Grupo crud
    path('grupoE/<int:pk>/', group_edit, name='grupoE'),
    path('confirmiar_eliminacion_grupo/<int:pk>/', confirmiar_eliminacion_group, name='confirmiar_eliminacion_grupo'),
    path('grupoC/', group_create, name='grupoC'),
    path('grupoL/', group_list, name='grupoL'),


    # Cambiar Contraseña
    path('cambiar-contrasena/', MyPasswordChangeView.as_view(),
         name='change_password'),
    path('pasword_change/', password_change_done, name='password_change_done'),


    # Clasificacion crud
    path('delete_clas/<int:pk>/', ClasificacionDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>/', ClasificacionUpdateView.as_view(), name='edit'),
    path('clasificacion/', ClasificacionCreateView.as_view(), name='clasificacion'),
    path('listas/',  ClasificacionListView.as_view(), name='list_desp'),

    # Conclusion crud
    path('conclusion_new/', conclusion_new, name='conclusion_new'),
    path('conclusion_delete/<int:pk>/', conclusion_delete, name='conclusion_delete'),
    path('conclusion_edit/<int:pk>/', conclusion_edit, name='conclusion_edit'),

    # Entidad crud
    path('create_enti/', enti_new, name='create_enti'),
    path('enti_delete/<int:pk>/', enti_delete, name='enti_delete'),
    path('enti_edit/<int:pk>/', enti_edit, name='enti_edit'),

    # satisfaccion crud
    path('create_satis/', satis_new, name='create_satis'),
    path('satis_delete/<int:pk>/', satis_delete, name='satis_delete'),
    path('satis_edit/<int:pk>/', satis_edit, name='satis_edit'),

    # CasoscPrensas crud
    path('create_caso/', caso_new, name='create_caso'),
    path('caso_delete/<int:pk>/', caso_delete, name='caso_delete'),
    path('caso_edit/<int:pk>/', caso_edit, name='caso_edit'),

    # moda crud
    path('create_moda/', moda_new, name='create_moda'),
    path('moda_delete/<int:pk>/', moda_delete, name='moda_delete'),
    path('moda_edit/<int:pk>/', moda_edit, name='moda_edit'),

# via crud
    path('create_via/', via_new, name='create_via'),
    path('via_delete/<int:pk>/', via_delete, name='via_delete'),
    path('via_edit/<int:pk>/', via_edit, name='via_edit'),

# procedencia crud
    path('create_procedencia/', procedencia_new, name='create_procedencia'),
    path('procedencia_delete/<int:pk>/', procedencia_delete, name='procedencia_delete'),
    path('procedencia_edit/<int:pk>/', procedencia_edit, name='procedencia_edit'),





]