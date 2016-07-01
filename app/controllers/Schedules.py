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
        p_tasks = self.models['Schedule'].get_curr_pending(session['user_id'])
        d_tasks = self.models['Schedule'].get_curr_done(session['user_id'])
        c_tasks = self.models['Schedule'].get_curr_cancelled(session['user_id'])
        return self.load_view('dashboard.html', curr_date=curr_date, user=user, p_tasks=p_tasks, d_tasks=d_tasks, c_tasks=c_tasks)

    def new_schedule(self):
        locations = self.models['Schedule'].get_locations(session['user_id'])
        return self.load_view('new_schedule.html', locations=locations)

    def edit_schedule(self, id):
        task = self.models['Schedule'].get_task_by_id(id)
        locations = self.models['Schedule'].get_locations(session['user_id'])
        return self.load_view('edit_schedule.html', task=task, locations=locations)

    def display_all(self):
        all_tasks = self.models['Schedule'].get_future_tasks(session['user_id'])
        return self.load_view('all_tasks.html', all_tasks = all_tasks)

    def task_st_update(self):
        if request.form['button'] == 'done':
            print "got in"
            self.models['Schedule'].update_task_done(request.form['task_id'])
            print "ok"
            return redirect('/task_slaughter/dashboard')

        if request.form['button'] == 'cancel':
            self.models['Schedule'].update_task_cancel(request.form['task_id'])
            return redirect('/task_slaughter/dashboard')

    def insert_schedule(self):
        print request.form
        if request.form['location_id']:
            print "location id"
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
                if new_task['task_name']:
                    task_validation = self.models['Schedule'].task_validation(new_task)
                    if task_validation['status']:
                        self.models['Schedule'].insert_task(new_task)
                        return redirect('/task_slaughter/dashboard')
                    else:
                        for error in task_validation['errors']:
                            flash(error)
                        return redirect('/task_slaughter/new_schedule')
                else:
                    return redirect('/task_slaughter/dashboard')
            else:
                for error in location_validation['errors']:
                    flash(error)
                return redirect('/task_slaughter/new_schedule')

    # def update_schedule(self):
    #     print "im in"
    #     print request.form
    #     edit_task = {'task_id': request.form['task_id'], 'task_name':request.form['task_name'], 'description':request.form['description'], 'priority':request.form['priority'], 'date':request.form['date'], 'time':request.form['time'], 'user_id':request.form['user_id'], 'location_id':request.form['location_id'], 'status':'Pending'}
    #     print edit_task
    #     if request.form['location_id']:
    #         print "ok"
    #         print "ok"
    #         print "ok"
    #         print "ok"
    #         worked = self.models['Schedule'].update_task(edit_task)
    #         print "this is worked"
    #         print "this is worked"
    #         print "this is worked"
    #         print "this is worked"
    #         print "this is worked"
    #         print "this is worked"
    #         print worked
    #         return redirect('/task_slaughter/dashboard')
            
    #     else:
    #         new_location = {'location_name':request.form['location_name'], 'street_name':request.form['street_name'], 'city':request.form['city'], 'state':request.form['state'], 'zip_code':request.form['zip_code'], 'user_id':request.form['user_id']}
    #         location_validation = self.models['Schedule'].location_validation(new_location)
    #         if location_validation['status']:
    #             location_id = self.models['Schedule'].insert_location(new_location)
    #             edit_task = {'task_name':request.form['task_name'], 'description':request.form['description'], 'priority':request.form['priority'], 'date':request.form['date'], 'time':request.form['time'], 'user_id':request.form['user_id'], 'location_id':location_id, 'notification':'off', 'status':'Pending'}
    #             self.models['Schedule'].update_task(edit_task)
    #             return redirect('/task_slaughter/dashboard')
            

    def twilio_text(self):
        phone=self.models['Schedule'].twilio(session['user_id'])
        phone_num=phone[0]['phone']
        text_body = self.models['Schedule'].twilio_body(request.form['task_id'])
        message_body = "Reminder from Task Slaughter! " + str(text_body[0]['task_name']) + ": " + str(text_body[0]['street_name']) + ", " + str(text_body[0]['city']) +", " + str(text_body[0]['zip_code']) + " on " + str(text_body[0]['date']) + " at " + str(text_body[0]['time'])
        ACCOUNT_SID = "AC3490836a9e230b983987438e82c9ba7d" 
        AUTH_TOKEN = "dcd9dd3a87976054f2f50d9e3477b3f0" 
        client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
        client.messages.create(
           body = message_body, 
           to = phone_num, 
           from_ = "+16506677014"
        )
        return redirect ('/task_slaughter/dashboard')
    
    

