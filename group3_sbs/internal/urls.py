from django.conf.urls import url
from . import views

app_name = 'internal'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^error/$', views.error, name='error'),
    url(r'^external_user/checking_account/(?P<external_user_id>[1-9][0-9]*)/view/$', views.view_external_user_checking_account, name='view_external_user_checking_account'),
    url(r'^external_user/profile/(?P<external_user_id>[1-9][0-9]*)/edit/$', views.edit_external_user_profile, name='edit_external_user_profile'),
    url(r'^external_user/profile/(?P<external_user_id>[1-9][0-9]*)/edit/validate/$', views.validate_profile_edit, name='validate_profile_edit'),
    url(r'^external_user/profile/(?P<external_user_id>[1-9][0-9]*)/view/$', views.view_external_user_profile, name='view_external_user_profile'),
    url(r'^external_user/request_access/$', views.external_user_access_request, name='external_user_access_request'),
    url(r'^external_user/request_access/validate/$', views.validate_external_user_access_request, name='validate_external_user_access_request'),
    url(r'^external_user/savings_account/(?P<external_user_id>[1-9][0-9]*)/view/$', views.view_external_user_savings_account, name='view_external_user_savings_account'),
    url(r'^internal_user/profile/(?P<internal_user_id>[1-9][0-9]*)/edit/$', views.edit_internal_user_profile, name='edit_internal_user_profile'),
    url(r'^internal_user/profile/(?P<internal_user_id>[1-9][0-9]*)/edit/validate/$', views.validate_internal_profile_edit, name='validate_internal_profile_edit'),
    url(r'^internal_user/request_access/$', views.internal_user_access_request, name='internal_user_access_request'),
    url(r'^internal_user/request_access/validate/$', views.validate_internal_user_access_request, name='validate_internal_user_access_request'),
    url(r'^internal_user/profile/(?P<internal_user_id>[1-9][0-9]*)/view/$', views.view_internal_user_profile, name='view_internal_user_profile'),
    url(r'^transaction/external_noncritical/$', views.noncritical_transactions, name='noncritical_transactions'),
    url(r'^transaction/external_critical/$', views.critical_transactions, name='critical_transactions'),
    url(r'^transaction/external_critical/(?P<transaction_id>[1-9][0-9]*)/approve/$', views.validate_critical_transaction_approval, name='validate_critical_transaction_approval'),
    url(r'^transaction/external_critical/(?P<transaction_id>[1-9][0-9]*)/deny/$', views.validate_critical_transaction_denial, name='validate_critical_transaction_denial'),
    url(r'^transaction/external_noncritical/(?P<transaction_id>[1-9][0-9]*)/approve/$', views.validate_noncritical_transaction_approval, name='validate_noncritical_transaction_approval'),
    url(r'^transaction/external_noncritical/(?P<transaction_id>[1-9][0-9]*)/deny/$', views.validate_noncritical_transaction_denial, name='validate_noncritical_transaction_denial'),
    url(r'^transaction/external_noncritical/(?P<transaction_id>[1-9][0-9]*)/request/$', views.validate_internal_noncritical_transaction_request, name='validate_internal_noncritical_transaction_request'),
    url(r'^transaction/external_noncritical/(?P<transaction_id>[1-9][0-9]*)/request/approve/$', views.validate_external_noncritical_transaction_access_request_approval, name='validate_external_noncritical_transaction_access_request_approval'),
    url(r'^transaction/external_noncritical/(?P<transaction_id>[1-9][0-9]*)/request/deny/$', views.validate_external_noncritical_transaction_access_request_denial, name='validate_external_noncritical_transaction_access_request_denial'),
    url(r'^transaction/internal_critical/$', views.internal_critical_transactions, name='internal_critical_transactions'),
    url(r'^transaction/internal_critical/(?P<transaction_id>[1-9][0-9]*)/approve/$', views.validate_internal_critical_transaction_access_request_approval, name='validate_internal_critical_transaction_access_request_approval'),
    url(r'^transaction/internal_critical/(?P<transaction_id>[1-9][0-9]*)/deny/$', views.validate_internal_critical_transaction_access_request_denial, name='validate_internal_critical_transaction_access_request_denial'),
    url(r'^transaction/internal_noncritical/$', views.internal_noncritical_transactions, name='internal_noncritical_transactions'),
]
