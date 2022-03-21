from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'financeAwareness'

urlpatterns = [
    #Main
    path('',views.index,name='index'),   

    #registration
    path('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('register/',views.register,name='register'),
    path('password_change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),

    #transaction
    path('dashboard',views.TransactionListView.as_view(),name='transactions'),
    path('transaction/<int:transaction_id>',views.TransactionDetailView.as_view(),name='transaction_details'),
    
    path('transaction/expense/new',views.CreateExpense.as_view(),name='new_expense'),
    path('transaction/income/new',views.CreateIncome.as_view(),name='new_income'),
    path('transaction/<int:transaction_id>/update/',views.TransactionUpdate.as_view(),name='transaction_form_update'),
    path('transaction/<int:id>/delete/',views.TransactionDelete.as_view(),name='transaction_form_delete'),
    path('transaction/ajax/subcategories',views.get_subcategories,name='ajaxSubcategories'),
    path('transaction/ajax/categories',views.get_categories,name='ajaxCategories'),
    path('transaction/search',views.search_transactions,name='search_transactions'),

    #planned
    path('transaction/planned',views.PlannedListView.as_view(),name='planned'),
    path('transaction/planned/new',views.CreatePlannedExpense.as_view(),name='new_planned'),
    path('transaction/planned/<int:transaction_id>',views.PlannedDetailView.as_view(),name='planned_details'),
    path('transaction/<int:transaction_id>/pdf',views.planned_to_pdf,name='planned_details_pdf'),
    path('transaction/planned/<int:transaction_id>/add',views.PlannedAdd.as_view(),name='planned_form_add'),
    path('transaction/planned/<int:transaction_id>/update',views.PlannedUpdate.as_view(),name='planned_form_update'),
    path('transaction/planned/<int:id>/delete',views.PlannedDelete.as_view(),name='planned_form_delete'),

    #recurring
    path('transaction/recurring',views.RecurringListView.as_view(),name='recurrings'),
    path('transaction/recurring/expense/new',views.CreateRecurringExpense.as_view(),name='new_reccuring_expense'),
    path('transaction/recurring/income/new',views.CreateRecurringIncome.as_view(),name='new_reccuring_income'),
    path('transaction/recurring/<int:transaction_id>',views.RecurringDetailView.as_view(),name='recurring_details'),
    path('transaction/recurring/<int:transaction_id>/add',views.RecurringAdd.as_view(),name='recurring_form_add'),
    path('transaction/recurring/<int:transaction_id>/update',views.RecurringUpdate.as_view(),name='recurring_form_update'),
    path('transaction/recurring/<int:id>/delete',views.RecurringDelete.as_view(),name='recurring_form_delete'),

    #category
    path('categories',views.category_list,name='categories'),
    path('categories/new/',views.category_form,name='new_category'),
    path('categories/new/<str:income>',views.category_form,name='new_category'),
    path('categories/<int:category_id>',views.category_details,name='category_details'),
    path('categories/update/<int:category_id>',views.category_form_update,name='category_form_update'),
    path('categories/delete/<int:id>',views.CategoryDelete.as_view(),name='category_form_delete'),

    #subcategory
    path('subcategories/new/<int:master_category>',views.subcategory_form,name='subcategory_form'),
    path('subcategories/update/<int:subcategory_id>',views.subcategory_form_update,name='subcategory_form_update'),
    path('subcategories/delete/<int:id>',views.SubcategoryDelete.as_view(),name='subcategory_form_delete'),

    #tag
    path('tags/',views.tag_list,name='tags'),
    path('tags/new',views.tag_form,name='new_tag'),
    path('tags/update/<int:tag_id>',views.tag_form_update,name='tag_form_update'),
    path('tags/delete/<int:id>',views.TagDelete.as_view(),name='tag_form_delete'),

    #account
    path('accounts/',views.account_list,name='accounts'),
    path('accounts/new',views.account_form,name='new_account'),
    path('accounts/update/<int:account_id>',views.account_form_update,name='account_form_update'),
    path('accounts/delete/<int:id>',views.AccountDelete.as_view(),name='account_form_delete'),

    #transfer
    path('accounts/transfer/new',views.transfer_form,name='transfer_form'),
    path('accounts/transfer/update/<int:transfer_id>',views.transfer_form_update,name='transfer_form_update'),
    path('accounts/transfer/delete/<int:id>',views.TransferDelete.as_view(),name='transfer_form_delete'),

    #saving goal
    path('savings/new',views.saving_goal_form,name='saving_goal_form'),
    path('savings/completed/<int:account_id>',views.saving_goal_accomplished,name='saving_goal_accomplished'),
    path('savings/update/<int:account_id>',views.saving_goal_form_update,name='saving_goal_form_update'),
    path('savings/delete/<int:id>',views.GoalDelete.as_view(),name='saving_goal_form_delete'),

    #reports
    path('reports/',views.reports_list,name='reports_list'),
    path('reports/category',views.category_details_report,name='report_category_details'),
    path('reports/tags',views.tags_details_report,name='report_tags_details'),
    path('reports/planned',views.planned_details_report,name='report_planned_details'),
    path('reports/recurring',views.recurring_details_report,name='report_recurring_details'),
    path('reports/details',views.expense_income_details_report,name='report_expense_income_details'),
]
