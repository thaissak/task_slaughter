from system.core.controller import *

class Schedules(Controller):
    def __init__(self, action):
        super(Schedules, self).__init__(action)
        self.load_model('User')
        self.load_model('Schedule')
        self.db = self._app.db
   
   
    def dashboard(self):
        return self.load_view('dashboard.html')

    def new_schedule(self):
        return self.load_view('new_schedule.html')

    def insert_schedule(self):
        return self.redirect('/task_slaughter/dashboard')
