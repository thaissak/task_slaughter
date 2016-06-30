from system.core.controller import *
from time import strftime
from twilio.rest import TwilioRestClient

class Schedules(Controller):
    def __init__(self, action):
        super(Schedules, self).__init__(action)
        self.load_model('User')
        self.load_model('Schedule')
        self.db = self._app.db
   
   
    def dashboard(self):
        # display the current date
        curr_date = self.models['Schedule'].curr_date()
        #display user name
        user = self.models['User'].get_user_by_id(session['user_id'])    
        #display tasks for the logged user for the current date
        tasks = self.models['Schedule'].get_curr_tasks(session['user_id'])
        return self.load_view('dashboard.html', curr_date=curr_date, user=user, tasks=tasks)

    def new_schedule(self):
        locations = self.models['Schedule'].get_locations(session['user_id'])
        return self.load_view('new_schedule.html', locations=locations)

    def task_update(self):
        if request.form['button'] == 'done':
            print "got in"
            self.models['Schedule'].update_task_done(request.form['task_id'])
            print "ok"
            return redirect('/task_slaughter/dashboard')

        if request.form['button'] == 'cancel':
            self.models['Schedule'].update_task_cancel(request.form['task_id'])
            return redirect('/task_slaughter/dashboard')

    def insert_schedule(self):
        if request.form['location_id']:
            new_task = {'task_name':request.form['task_name'], 'description':request.form['description'], 'priority':request.form['priority'], 'date':request.form['date'], 'time':request.form['time'], 'user_id':request.form['user_id'], 'location_id':request.form['location_id'], 'notification':'off', 'status':'Pending'}
            task_validation = self.models['Schedule'].task_validation(new_task)
            if task_validation['status']:                
                self.models['Schedule'].insert_task(new_task)
                return redirect('/task_slaughter/dashboard')
            else:
                for error in task_validation['errors']:
                    flash(error)
                return redirect('/task_slaughter/new_schedule')
        else:
            new_location = {'location_name':request.form['location_name'], 'street_name':request.form['street_name'], 'city':request.form['city'], 'state':request.form['state'], 'zip_code':request.form['zip_code'], 'user_id':request.form['user_id']}
            location_validation = self.models['Schedule'].location_validation(new_location)
            if location_validation['status']:
                location_id = self.models['Schedule'].insert_location(new_location)
                new_task = {'task_name':request.form['task_name'], 'description':request.form['description'], 'priority':request.form['priority'], 'date':request.form['date'], 'time':request.form['time'], 'user_id':request.form['user_id'], 'location_id':location_id, 'notification':'off', 'status':'Pending'}
                task_validation = self.models['Schedule'].task_validation(new_task)
                if task_validation['status']:
                    self.models['Schedule'].insert_task(new_task)
                    return redirect('/task_slaughter/dashboard')
                else:
                    for error in task_validation['errors']:
                        flash(error)
                    return redirect('/task_slaughter/new_schedule')
            else:
                for error in location_validation['errors']:
                    flash(error)
                return redirect('/task_slaughter/new_schedule')
    
    # def twilio_text(self):
    #     print request.form
    #     print 'haha'
    #     print 'haha'
    #     print 'haha'
    #     print 'haha'
    #     print 'haha'
    #     print 'haha'
    #     phone = self.models['Schedule'].twilio(session['user_id'])
    #     text_body = self.models['Schedule'].twilio_body(request.form['task_id'])
    #     ACCOUNT_SID = "AC3490836a9e230b983987438e82c9ba7d" 
    #     AUTH_TOKEN = "dcd9dd3a87976054f2f50d9e3477b3f0" 
    #     client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
    #     client.messages.create(
    #         to= phone,
    #         from_="+16506677014",
    #         body=text_body
    #     )
    #     print "INSIDE TWILIO TEXT METHOD"
    #     print phone
    #     print text_body
    #     return redirect ('/task_slaughter/dashboard')

