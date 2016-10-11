from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.views.decorators.cache import never_cache
from external.models import ExternalNoncriticalTransaction, ExternalCriticalTransaction
from internal.models import Administrator, RegularEmployee, SystemManager, InternalNoncriticalTransaction, InternalCriticalTransaction
from global_templates.common_functions import *
from global_templates.constants import *
import os

"""
                        Render Web Pages
"""

# Internal User Home Page
@never_cache
@login_required
@user_passes_test(is_internal_user)
def index(request):
    user = request.user
    if is_regular_employee(user):
        return render(request, 'internal/index.html', {'user_type': REGULAR_EMPLOYEE, 'first_name': user.regularemployee.first_name, 'last_name': user.regularemployee.last_name})
    elif is_system_manager(user):
        return render(request, 'internal/index.html', {'user_type': SYSTEM_MANAGER, 'first_name': user.systemmanager.first_name, 'last_name': user.systemmanager.last_name})
    elif is_administrator(user):
        return render(request, 'internal/index.html', {'user_type': ADMINISTRATOR, 'first_name': user.administrator.first_name, 'last_name': user.administrator.last_name})
    else:
        return HttpResponseRedirect(reverse('internal:error'))

# External Log Page
@never_cache
@login_required
@user_passes_test(is_administrator)
def view_external_log(request):
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        f = open(dir_path+'/../log/external_log.log', 'r')
        lines = f.readlines()
        f.close()
        return render(request, 'internal/log.html', {'content': lines})
    except Exception as m:
        print(m)
        return HttpResponseRedirect(reverse('internal:error'))

# Internal Log Page
@never_cache
@login_required
@user_passes_test(is_administrator)
def view_internal_log(request):
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        f = open(dir_path+'/../log/internal_log.log', 'r')
        lines = f.readlines()
        f.close()
        return render(request, 'internal/log.html', {'content': lines})
    except:
        return HttpResponseRedirect(reverse('internal:error'))

# Server Log Page
@never_cache
@login_required
@user_passes_test(is_administrator)
def view_server_log(request):
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        f = open(dir_path+'/../log/server_log.log', 'r')
        lines = f.readlines()
        f.close
        return render(request, 'internal/log.html', {'content': lines})
    except:
        return HttpResponseRedirect(reverse('internal:error'))

# Internal User Error Page
@never_cache
@login_required
@user_passes_test(is_internal_user)
def error(request):
    return render(request, 'internal/error.html')

# View Critical Transactions
@never_cache
@login_required
@user_passes_test(is_system_manager)
def critical_transactions(request):
    user = request.user
    if is_regular_employee(user) or is_administrator(user):
        return render(request, 'internal/index.html')
    elif is_system_manager(user):
        transactions = ExternalCriticalTransaction.objects.filter().exclude(status=TRANSACTION_STATUS_RESOLVED).order_by('time_created')
        top_critical_transaction = ExternalCriticalTransaction.objects.filter().exclude(status=TRANSACTION_STATUS_RESOLVED).order_by('time_created').first()
        top_noncritical_transaction = ExternalNoncriticalTransaction.objects.filter().exclude(status=TRANSACTION_STATUS_RESOLVED).order_by('time_created').first()
        if top_critical_transaction is None:
            return render(request, 'internal/critical_transactions.html', {'transactions': transactions})
        elif top_noncritical_transaction is None:
            can_resolve = True
        elif top_critical_transaction.time_created > top_noncritical_transaction.time_created:
            can_resolve = False
        else:
            can_resolve = True
        return render(request, 'internal/critical_transactions.html', {'transactions': transactions, 'can_resolve': can_resolve})
    else:
        return HttpResponseRedirect(reverse('internal:error'))

# Edit External User Profile Page
@never_cache
@login_required
@user_passes_test(is_internal_user)
def edit_external_user_profile(request, external_user_id):
    user = request.user
    page_to_view = PAGE_TO_VIEW_EDIT_PROFILE
    success_page = "internal/edit_external_user_profile.html"
    error_redirect = "internal:index"
    if can_edit_external_user_page(user=user, external_user_id=external_user_id, page_to_view=page_to_view):
        try:
            external_user = User.objects.get(id=int(external_user_id))
            if not is_external_user(external_user):
                raise Exception
        except:
            return HttpResponseRedirect(reverse(error_redirect))
        profile = get_any_user_profile(username=external_user.username)
        return render(request, success_page, {"external_user": external_user, "profile": profile, 'STATES': STATES})
    else:
        return HttpResponseRedirect(reverse(error_redirect))

# Edit Internal User Profile Page
@never_cache
@login_required
@user_passes_test(is_administrator)
def edit_internal_user_profile(request, internal_user_id):
    user = request.user
    page_to_view = PAGE_TO_VIEW_EDIT_PROFILE
    success_page = "internal/edit_internal_user_profile.html"
    error_redirect = "internal:index"
    try:
        internal_user = User.objects.get(id=int(internal_user_id))
        if not is_internal_user(internal_user):
            raise Exception
    except:
        return HttpResponseRedirect(reverse(error_redirect))
    profile = get_any_user_profile(username=internal_user.username)
    return render(request, success_page, {"internal_user": internal_user, "profile": profile, 'STATES': STATES})


# External User Account Request Page
@never_cache
@login_required
@user_passes_test(is_internal_user)
def external_user_access_request(request):
    user = request.user
    list = get_user_det(user)
    return render(request, 'internal/external_user_access_request.html',{'user_type': list[2], 'first_name': list[0],'last_name':list[1] })

# Internal Noncritical Transactions Page
@never_cache
@login_required
@user_passes_test(can_resolve_internal_transaction)
def internal_noncritical_transactions(request):
    user = request.user
    success_page = 'internal/internal_noncritical_transactions.html'
    transactions = InternalNoncriticalTransaction.objects.filter().exclude(status=TRANSACTION_STATUS_RESOLVED).order_by('time_created')
    return render(request, success_page, {'transactions': transactions})

# Internal Critical Transactions Page
@never_cache
@login_required
@user_passes_test(can_resolve_internal_transaction)
def internal_critical_transactions(request):
    user = request.user
    success_page = 'internal/internal_critical_transactions.html'
    transactions = InternalCriticalTransaction.objects.filter().exclude(status=TRANSACTION_STATUS_RESOLVED).order_by('time_created')
    return render(request, success_page, {'transactions': transactions})

# Internal Noncritical Transactions Page
@never_cache
@login_required
@user_passes_test(can_resolve_internal_transaction)
def internal_noncritical_transactions(request):
    user = request.user
    list = get_user_det(user)
    success_page = 'internal/internal_noncritical_transactions.html'
    transactions = InternalNoncriticalTransaction.objects.filter().exclude(status=TRANSACTION_STATUS_RESOLVED).order_by('time_created')
    return render(request, success_page, {'user_type': list[2], 'first_name': list[0],'last_name':list[1],'transactions': transactions})

# Request Access to Internal User Personal Account Page
@never_cache
@login_required
@user_passes_test(is_administrator)
def internal_user_access_request(request):
    user = request.user
    list = get_user_det(user)
    return render(request, 'internal/internal_user_access_request.html',{'user_type': list[2], 'first_name': list[0],'last_name':list[1] })

# View Noncritical Transactions
@never_cache
@login_required
@user_passes_test(is_internal_user)
def noncritical_transactions(request):
    user = request.user
    list = get_user_det(user)
    if is_administrator(user):
        return render(request, 'internal/index.html')
    elif is_regular_employee(user) or is_system_manager(user):
        can_request = False
        transactions = ExternalNoncriticalTransaction.objects.filter().exclude(status=TRANSACTION_STATUS_RESOLVED).order_by('time_created')
        top_critical_transaction = ExternalCriticalTransaction.objects.filter().exclude(status=TRANSACTION_STATUS_RESOLVED).order_by('time_created').first()
        top_noncritical_transaction = ExternalNoncriticalTransaction.objects.filter().exclude(status=TRANSACTION_STATUS_RESOLVED).order_by('time_created').first()
        already_exists = InternalNoncriticalTransaction.objects.filter(initiator_id=user.id, status=TRANSACTION_STATUS_UNRESOLVED)
        if not already_exists.exists():
            can_request = True
        if top_noncritical_transaction is None:
            return render(request, 'internal/noncritical_transactions.html', {'user_type': list[2], 'first_name': list[0],'last_name':list[1],'transactions': transactions})
        elif top_critical_transaction is None:
            can_resolve = True
        elif top_critical_transaction.time_created < top_noncritical_transaction.time_created:
            can_resolve = False
        else:
            can_resolve = True
        if is_system_manager(user):
            access_to_resolve = True
        else:
            access_to_resolve = False
            permission_codename = 'internal.can_resolve_external_noncritical_transaction_' + str(top_noncritical_transaction.id)
            if user.has_perm(permission_codename):
                access_to_resolve = True
        return render(request, 'internal/noncritical_transactions.html', {'user_type': list[2],'first_name':list[0],'last_name':list[1],'transactions': transactions, 'can_resolve': can_resolve, 'access_to_resolve': access_to_resolve, 'can_request': can_request})
    else:
        return HttpResponseRedirect(reverse('internal:error'))

# View External User Checking Account Page
@never_cache
@login_required
@user_passes_test(is_internal_user)
def view_external_user_checking_account(request, external_user_id):
    user = request.user
    page_to_view = PAGE_TO_VIEW_CHECKING_ACCOUNT
    success_page = "internal/view_external_user_" + page_to_view + ".html"
    error_redirect = "internal:index"
    if can_view_external_user_page(user=user, external_user_id=external_user_id, page_to_view=page_to_view):
        try:
            external_user = User.objects.get(id=int(external_user_id))
            if not is_external_user(external_user):
                raise Exception
        except:
            return HttpResponseRedirect(reverse(error_redirect))
        checking_account = get_external_user_account(user=external_user, account_type=ACCOUNT_TYPE_CHECKING)
        return render(request, success_page, {"user": external_user, "checking_account": checking_account})
    else:
        return HttpResponseRedirect(reverse(error_redirect))

# View External User Profile Page
@never_cache
@login_required
@user_passes_test(is_internal_user)
def view_external_user_profile(request, external_user_id):
    user = request.user
    page_to_view = PAGE_TO_VIEW_PROFILE
    success_page = "internal/view_external_user_" + page_to_view + ".html"
    error_redirect = "internal:index"
    admin_privilege = False
    if can_view_external_user_page(user=user, external_user_id=external_user_id, page_to_view=page_to_view):
        try:
            external_user = User.objects.get(id=int(external_user_id))
            if not is_external_user(external_user):
                raise Exception
        except:
            return HttpResponseRedirect(reverse(error_redirect))
        profile = get_any_user_profile(username=external_user.username)
        if is_administrator(user):
            admin_privilege = True
        return render(request, success_page, {"user": external_user, "profile": profile, 'admin_privilege': admin_privilege})
    else:
        return HttpResponseRedirect(reverse(error_redirect))

# View External User Savings Account Page
@never_cache
@login_required
@user_passes_test(is_internal_user)
def view_external_user_savings_account(request, external_user_id):
    user = request.user
    page_to_view = PAGE_TO_VIEW_SAVINGS_ACCOUNT
    success_page = "internal/view_external_user_" + page_to_view + ".html"
    error_redirect = "internal:index"
    if can_view_external_user_page(user=user, external_user_id=external_user_id, page_to_view=page_to_view):
        try:
            external_user = User.objects.get(id=int(external_user_id))
            if not is_external_user(external_user):
                raise Exception
        except:
            return HttpResponseRedirect(reverse(error_redirect))
        savings_account = get_external_user_account(user=external_user, account_type=ACCOUNT_TYPE_SAVINGS)
        return render(request, success_page, {"user": external_user, "savings_account": savings_account})
    else:
        return HttpResponseRedirect(reverse(error_redirect))

# View Internal User Profile Page
@never_cache
@login_required
@user_passes_test(is_administrator)
def view_internal_user_profile(request, internal_user_id):
    user = request.user
    page_to_view = PAGE_TO_VIEW_PROFILE
    success_page = "internal/view_internal_user_" + page_to_view + ".html"
    error_redirect = "internal:index"
    try:
        internal_user = User.objects.get(id=internal_user_id)
        if not is_internal_user(internal_user):
            raise Exception
    except:
        return HttpResponseRedirect(reverse(error_redirect))
    profile = get_any_user_profile(username=internal_user.username)
    return render(request, success_page, {"user": internal_user, "profile": profile})

"""
                        Validate Webpages
"""

# Approve Criticial Transactions
@never_cache
@login_required
@user_passes_test(is_system_manager)
def validate_critical_transaction_approval(request, transaction_id):
    user = request.user
    list = get_user_det(user)
    success_page = 'internal/critical_transactions.html'
    success_page_reverse = 'internal:critical_transactions'
    try:
        top_critical_transaction = ExternalCriticalTransaction.objects.get(id=transaction_id)
    except:
        return render(request, success_page, {'user_type': list[2], 'first_name': list[0],'last_name':list[1],'transactions': transactions, 'error_message': "Transaction does not exist"})
    transactions = ExternalCriticalTransaction.objects.filter().exclude(status=TRANSACTION_STATUS_RESOLVED).order_by('time_created')
    if commit_transaction(transaction=top_critical_transaction, user=user):
        return HttpResponseRedirect(reverse(success_page_reverse))
    else:
        return render(request, success_page, {'user_type': list[2], 'first_name': list[0],'last_name':list[1],'transactions': transactions, 'error_message': "Approved transaction not commmited"})

# Deny Criticial Transactions
@never_cache
@login_required
@user_passes_test(is_system_manager)
def validate_critical_transaction_denial(request, transaction_id):
    user = request.user
    list = get_user_det(user)
    success_page = 'internal/critical_transactions.html'
    success_page_reverse = 'internal:critical_transactions'
    try:
        top_critical_transaction = ExternalCriticalTransaction.objects.get(id=transaction_id)
    except:
        return render(request, success_page, {'user_type': list[2], 'first_name': list[0],'last_name':list[1],'transactions': transactions, 'error_message': "Transaction does not exist"})
    transactions = ExternalCriticalTransaction.objects.filter().exclude(status=TRANSACTION_STATUS_RESOLVED).order_by('time_created')
    if deny_transaction(transaction=top_critical_transaction, user=user):
        return HttpResponseRedirect(reverse(success_page_reverse))
    else:
        return render(request, success_page, {'user_type': list[2], 'first_name': list[0],'last_name':list[1],'transactions': transactions, 'error_message': "Denied transaction not commmited"})

# Request External User Transaction Access
@never_cache
@login_required
@user_passes_test(can_resolve_internal_transaction)
def validate_external_noncritical_transaction_access_request_approval(request, transaction_id):
    user = request.user
    list = get_user_det(user)
    try:
        internal_transaction = InternalNoncriticalTransaction.objects.get(id=int(transaction_id))
        external_transaction = get_external_noncritical_transaction(internal_transaction)
        initiator = internal_transaction.initiator
    except:
        return HttpResponseRedirect(reverse('internal:error'))
    if is_regular_employee(initiator):
        content_type = ContentType.objects.get_for_model(RegularEmployee)
    else:
        return HttpResponseRedirect(reverse('internal:error'))
    permission_codename = 'can_resolve_external_noncritical_transaction_' + str(external_transaction.id)
    permission_name = "Can resolve external noncritical transaction " + str(external_transaction.id)
    try:
        permission = Permission.objects.get(codename=permission_codename, name=permission_name, content_type=content_type)
    except:
        permission = Permission.objects.create(codename=permission_codename,name=permission_name, content_type=content_type)
    if commit_transaction(transaction=internal_transaction, user=user):
        initiator.user_permissions.add(permission)
        initiator.save()
        return HttpResponseRedirect(reverse('internal:internal_noncritical_transactions'))
    else:
        return HttpResponseRedirect(reverse('internal:error'))

# Request External User Transaction Access
@never_cache
@login_required
@user_passes_test(can_resolve_internal_transaction)
def validate_external_noncritical_transaction_access_request_denial(request, transaction_id):
    user = request.user
    list = get_user_det(user)
    try:
        transaction = InternalNoncriticalTransaction.objects.get(id=transaction_id)
        if deny_transaction(transaction=transaction, user=user):
            return HttpResponseRedirect(reverse('internal:internal_noncritical_transactions'))
        else:
            return render(request, 'internal/internal_noncritical_transactions.html', {'user_type': list[2], 'first_name': list[0],'last_name':list[1],'error_message': 'Denied transaction not committed'})
    except:
        return HttpResponseRedirect(reverse('internal:error'))

# Request External User Account Access
@never_cache
@login_required
@user_passes_test(is_internal_user)
def validate_external_user_access_request(request):
    user = request.user
    error_redirect = "internal:error"
    external_user_id = request.POST['external_user_id']
    page_to_view = request.POST['page_to_view']
    if page_to_view == PAGE_TO_VIEW_EDIT_PROFILE and not is_administrator(user):
        success_redirect = "internal:edit_external_user_profile"
    elif page_to_view == PAGE_TO_VIEW_EDIT_PROFILE and is_administrator(user):
        return HttpResponseRedirect(reverse(error_redirect))
    else:
        success_redirect = "internal:view_external_user_" + page_to_view
    pending_approval_redirect = "internal:index"
    try:
        external_user = User.objects.get(id=int(external_user_id))
        if not is_external_user(external_user):
            raise Exception
    except:
        return HttpResponseRedirect(reverse(error_redirect))
    access_granted = does_user_have_external_user_permission(user=user, external_user=external_user, page_to_view=page_to_view)
    if access_granted:
        return HttpResponseRedirect(reverse(success_redirect, kwargs={'external_user_id': external_user.id}))
    elif is_regular_employee(user) and not access_granted:
        return HttpResponseRedirect(reverse(pending_approval_redirect))
    else:
        return HttpResponseRedirect(reverse(error_redirect))

# Validate Internal Critical Transactions Reqeust
@never_cache
@login_required
@user_passes_test(is_administrator)
def validate_internal_critical_transaction_access_request_approval(request, transaction_id):
    user = request.user
    success_redirect = "internal:internal_critical_transactions"
    error_redirect = "internal:error"
    try:
        internal_transaction = InternalCriticalTransaction.objects.get(id=int(transaction_id))
        initiator = internal_transaction.initiator
    except:
        return HttpResponseRedirect(reverse(error_redirect))
    if is_regular_employee(initiator):
        content_type = ContentType.objects.get_for_model(RegularEmployee)
    else:
        return HttpResponseRedirect(reverse(error_redirect))
    if commit_transaction(transaction=internal_transaction, user=user):
        return HttpResponseRedirect(reverse(success_redirect))
    else:
        return HttpResponseRedirect(reverse(error_redirect))

# Validate Internal Critical Transactions Reqeust
@never_cache
@login_required
@user_passes_test(is_administrator)
def validate_internal_critical_transaction_access_request_denial(request, transaction_id):
    user = request.user
    success_redirect = "internal:internal_critical_transactions"
    error_redirect = "internal:error"
    try:
        internal_transaction = InternalCriticalTransaction.objects.get(id=int(transaction_id))
        initiator = internal_transaction.initiator
    except:
        return HttpResponseRedirect(reverse(error_redirect))
    if is_regular_employee(initiator):
        content_type = ContentType.objects.get_for_model(RegularEmployee)
    else:
        return HttpResponseRedirect(reverse(error_redirect))
    if deny_transaction(transaction=internal_transaction, user=user):
        return HttpResponseRedirect(reverse(success_redirect))
    else:
        return HttpResponseRedirect(reverse(error_redirect))

# Validate Internal Noncritical Transactions Reqeust
@never_cache
@login_required
@user_passes_test(is_regular_employee)
def validate_internal_noncritical_transaction_request(request, transaction_id):
    user = request.user
    try:
        external_transaction = ExternalNoncriticalTransaction.objects.get(id=int(transaction_id))
        already_exists = InternalNoncriticalTransaction.objects.filter(initiator_id=user.id, status=TRANSACTION_STATUS_UNRESOLVED)
        if already_exists.exists():
            raise Exception
    except:
        return HttpResponseRedirect(reverse('internal:index'))
    if create_internal_noncritical_transaction(user=user, external_transaction=external_transaction):
        return HttpResponseRedirect(reverse('internal:noncritical_transactions'))
    else:
        return HttpResponseRedirect(reverse('internal:error'))

# Request Internal User Account Access
@never_cache
@login_required
@user_passes_test(is_administrator)
def validate_internal_user_access_request(request):
    user = request.user
    error_redirect = "internal:error"
    internal_user_id = request.POST['internal_user_id']
    page_to_view = request.POST['page_to_view']
    if page_to_view == PAGE_TO_VIEW_EDIT_PROFILE:
        success_redirect = "internal:edit_internal_user_profile"
    else:
        success_redirect = "internal:view_internal_user_" + page_to_view
    try:
        internal_user = User.objects.get(id=int(internal_user_id))
        if not is_internal_user(internal_user):
            raise Exception
    except:
        return HttpResponseRedirect(reverse(error_redirect))
    return HttpResponseRedirect(reverse(success_redirect, kwargs={'internal_user_id': internal_user.id}))

# Approve Non-criticial Transactions
@never_cache
@login_required
@user_passes_test(can_view_noncritical_transaction)
def validate_noncritical_transaction_approval(request, transaction_id):
    user = request.user
    list = get_user_det(user)
    success_page = 'internal/noncritical_transactions.html'
    success_page_reverse = 'internal:noncritical_transactions'
    try:
        top_noncritical_transaction = ExternalNoncriticalTransaction.objects.get(id=transaction_id)
    except:
        return render(request, success_page, {'user_type': list[2], 'first_name': list[0],'last_name':list[1],'transactions': transactions, 'error_message': "Transaction does not exist"})
    transactions = ExternalNoncriticalTransaction.objects.filter().exclude(status=TRANSACTION_STATUS_RESOLVED).order_by('time_created')
    if not can_resolve_noncritical_transaction(user, transaction_id):
        return render(request, success_page, {'user_type': list[2], 'first_name': list[0],'last_name':list[1],'transactions': transactions, 'error_message': "Do not have permission to resolve transaction"})
    if commit_transaction(transaction=top_noncritical_transaction, user=user):
        return HttpResponseRedirect(reverse(success_page_reverse))
    else:
        return render(request, success_page, {'user_type': list[2], 'first_name': list[0],'last_name':list[1],'transactions': transactions, 'error_message': "Approved transaction not commmited"})

# Deny Non-criticial Transactions
@never_cache
@login_required
@user_passes_test(can_view_noncritical_transaction)
def validate_noncritical_transaction_denial(request, transaction_id):
    user = request.user
    list = get_user_det(user)
    success_page = 'internal/noncritical_transactions.html'
    success_page_reverse = 'internal:noncritical_transactions'
    try:
        top_noncritical_transaction = ExternalNoncriticalTransaction.objects.get(id=transaction_id)
    except:
        return render(request, success_page, {'user_type': list[2], 'first_name': list[0],'last_name':list[1],'transactions': transactions, 'error_message': "Transaction does not exist"})
    transactions = ExternalNoncriticalTransaction.objects.filter().exclude(status=TRANSACTION_STATUS_RESOLVED).order_by('time_created')
    if not can_resolve_noncritical_transaction(user, transaction_id):
        return render(request, success_page, {'user_type': list[2], 'first_name': list[0],'last_name':list[1],'transactions': transactions, 'error_message': "Do not have permission to resolve transaction"})
    if deny_transaction(transaction=top_noncritical_transaction, user=user):
        return HttpResponseRedirect(reverse(success_page_reverse))
    else:
        return render(request, success_page, {'user_type': list[2], 'first_name': list[0],'last_name':list[1],'transactions': transactions, 'error_message': "Denied transaction not commmited"})

# Validate Internal User Profile Edit Page
@never_cache
@login_required
@user_passes_test(is_administrator)
def validate_internal_profile_edit(request, internal_user_id):
    user = request.user
    success_redirect = 'internal:index'
    error_redirect = 'internal:error'
    username = request.POST['username']
    profile = get_any_user_profile(username=username)
    if int(profile.user.id) != int(internal_user_id):
        return HttpResponseRedirect(reverse(error_redirect))
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    street_address = request.POST['street_address']
    city = request.POST['city']
    state = request.POST['state']
    zipcode = request.POST['zipcode']
    if validate_profile_change(profile=profile, first_name=first_name, last_name=last_name, street_address=street_address, city=city, state=state, zipcode=zipcode):
        return HttpResponseRedirect(reverse(success_redirect))
    else:
        return HttpResponseRedirect(reverse(error_redirect))


# Validate Profile Edit Page
@never_cache
@login_required
@user_passes_test(is_internal_user)
def validate_profile_edit(request, external_user_id):
    user = request.user
    success_redirect = 'internal:index'
    error_redirect = 'internal:error'
    username = request.POST['username']
    profile = get_any_user_profile(username=username)
    if int(profile.user.id) != int(external_user_id):
        return HttpResponseRedirect(reverse(error_redirect))
    first_name = request.POST['first_name']
    """ This preserves PII privilege of editing profile
    last_name = request.POST['last_name']
    street_address = request.POST['street_address']
    city = request.POST['city']
    state = request.POST['state']
    zipcode = request.POST['zipcode']
    """
    if is_system_manager(user):
        """ This preserves PII privilege of editing profile
        if validate_profile_change(profile=profile, first_name=first_name, last_name=last_name, street_address=street_address, city=city, state=state, zipcode=zipcode):
        """
        if validate_first_name_save(profile=profile, first_name=first_name):
            return HttpResponseRedirect(reverse(success_redirect))
        else:
            return HttpResponseRedirect(reverse(error_redirect))
    elif is_regular_employee(user):
        try:
            permission_codename = 'can_internal_user_edit_external_user_profile_' + str(external_user_id)
            permission = Permission.objects.get(codename=permission_codename)
            permission_codename = 'internal.' + permission_codename
        except:
            return HttpResponseRedirect(reverse(error_redirect))
        if user.has_perm(permission_codename):
            """ This preserves PII privilege of editing profile
            if validate_profile_change(profile=profile, first_name=first_name, last_name=last_name, street_address=street_address, city=city, state=state, zipcode=zipcode):
            """
            if validate_first_name_save(profile=profile, first_name=first_name):
                user.user_permissions.remove(permission)
                user.save()
                return HttpResponseRedirect(reverse(success_redirect))
            else:
                return HttpResponseRedirect(reverse(error_redirect))
        else:
            return HttpResponseRedirect(reverse(error_redirect))
    else:
        return HttpResponseRedirect(reverse(error_redirect))
