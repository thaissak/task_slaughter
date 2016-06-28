from system.core.router import routes


routes ['/task_slaughter'] = 'Users#index'

routes ['/task_slaughter/registration'] = 'Users#registration'

routes ['/task_slaughter/dashboard'] = 'Schedules#dashboard'

routes ['/task_slaughter/new_schedule'] = 'Schedules#new_schedule'

routes ['/task_slaughter/logout'] = 'Users#logout'

routes ['POST'] ['/task_slaughter/login_process'] = 'Users#login_process'

routes ['POST'] ['/task_slaughter/registration_process'] = 'Users#insert_user'

routes ['POST'] ['/task_slaughter/schedule_process'] = 'Users#insert_schedule'


