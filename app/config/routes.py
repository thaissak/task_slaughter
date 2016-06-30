from system.core.router import routes


routes ['/task_slaughter'] = 'Users#index'

routes ['/task_slaughter/registration'] = 'Users#registration'

routes ['/task_slaughter/dashboard'] = 'Schedules#dashboard'

routes ['/task_slaughter/new_schedule'] = 'Schedules#new_schedule'

routes ['/task_slaughter/<id>/edit_schedule'] = 'Schedules#edit_schedule'

routes['/task_slaughter/future_tasks'] = 'Schedules#display_all'

routes ['/task_slaughter/logout'] = 'Users#logout'

routes ['POST'] ['/task_slaughter/login_process'] = 'Users#login_process'

routes ['POST'] ['/task_slaughter/registration_process'] = 'Users#insert_user'

routes ['POST'] ['/task_slaughter/schedule_process'] = 'Schedules#insert_schedule'

routes ['POST'] ['/task_slaughter/update_process'] = 'Schedules#update_schedule'

routes ['POST'] ['/task_slaughter/dashboard/status_update'] = 'Schedules#task_st_update'

# routes ['POST'] ['/task_slaughter/dashboard/task_sms'] = 'Schedules#twilio_text'




