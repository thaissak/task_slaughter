from system.core.model import Model
from time import strftime
from datetime import datetime

class Schedule(Model):
    def __init__(self):
        super(Schedule, self).__init__()

    def curr_date(self):
        # datetime.date.today() + datetime.timedelta(days=1)
        curr_date = datetime.now()
        curr_date = curr_date.strftime("%b %d, %Y")
        return curr_date

    def get_locations(self, user_id):
        query = "SELECT * from locations where user_id = :id"
        data = {'id': user_id}
        return self.db.query_db(query, data)

    def get_tasks(self, user_id):
        query = "SELECT * from tasks where user_id = :id"
        data = {'id': user_id}
        return self.db.query_db(query, data)

    def get_task_by_id(self, task_id):
        query = "SELECT * from tasks join locations on tasks.location_id = locations.id where tasks.id = :id limit 1"
        data = {'id': task_id}
        return self.db.get_one(query, data)

    def get_curr_pending(self, user_id):
    	query = "select tasks.id, tasks.date, date_format(tasks.time,'%k:%i') as time, tasks.task_name, tasks.status, locations.location_name, locations.street_name, locations.zip_code, locations.city from tasks join locations on tasks.location_id = locations.id where tasks.user_id = :id and tasks.date= CURDATE() and tasks.status = 'Pending' order by STR_TO_DATE(time,'%k:%i') ASC"
    	data = {'id': user_id}
    	return self.db.query_db(query, data)

    def get_curr_done(self, user_id):
        query = "select tasks.id, tasks.date, date_format(tasks.time,'%k:%i') as time, tasks.task_name, tasks.status, locations.location_name, locations.street_name, locations.zip_code, locations.city from tasks join locations on tasks.location_id = locations.id where tasks.user_id = :id and tasks.date= CURDATE() and tasks.status = 'Done' order by STR_TO_DATE(time,'%k:%i') ASC"
        data = {'id': user_id}
        return self.db.query_db(query, data)

    def get_curr_cancelled(self, user_id):
        query = "select tasks.id, tasks.date, date_format(tasks.time,'%k:%i') as time, tasks.task_name, tasks.status, locations.location_name, locations.street_name, locations.zip_code, locations.city from tasks join locations on tasks.location_id = locations.id where tasks.user_id = :id and tasks.date= CURDATE() and tasks.status = 'Cancelled' order by STR_TO_DATE(time,'%k:%i') ASC"
        data = {'id': user_id}
        return self.db.query_db(query, data)

    def update_task_done(self, task_id):
    	query = "update tasks set status='Done' where id=:id"
    	data = {'id': task_id}
    	return self.db.query_db(query, data)

    def update_task_cancel(self, task_id):
   		query = "update tasks set status='Cancelled' where id =:id"
   		data = {'id': task_id}
   		return self.db.query_db(query, data)

    def insert_location(self, new_location):
        query = "insert into locations (location_name, street_name, city, state, zip_code, user_id) values (:location_name, :street_name, :city, :state, :zip_code, :user_id)"
        data = {'location_name':new_location['location_name'], 'street_name':new_location['street_name'], 'city':new_location['city'], 'state':new_location['state'], 'zip_code':new_location['zip_code'], 'user_id':new_location['user_id']}
        return self.db.query_db(query, data)

    def insert_task(self, new_task):
        query = "insert into tasks (task_name, description, priority, date, time, user_id, location_id, notification, status) values (:task_name, :description, :priority, :date, :time, :user_id, :location_id, :notification, :status)"
        data = {'task_name':new_task['task_name'], 'description':new_task['description'], 'priority':new_task['priority'], 'date':new_task['date'],'time':new_task['time'], 'user_id':new_task['user_id'], 'location_id':new_task['location_id'], 'notification':new_task['notification'], 'status':new_task['status']}
        return self.db.query_db(query, data)

    def update_task(self, info_task):
        query = "update tasks set task_name=:task_name, description=:description, priority=:priority, date=:date, time=:time, user_id=:user_id, location_id=:location_id, status=:status where id=:id"
        data = {'id':info_task['task_id'], 'task_name':info_task['task_name'], 'description':info_task['description'], 'priority':info_task['priority'], 'date':info_task['date'],'time':info_task['time'], 'user_id':info_task['user_id'], 'location_id':info_task['location_id'], 'status':info_task['status']}
        return self.db.query_db(query, data)   

    def get_future_tasks(self, user_id):
        query = "SELECT tasks.id, tasks.status, tasks.task_name, tasks.description, date_format(tasks.date, '%b %d, %Y') as date, date_format(tasks.time,'%k:%i') as time, locations.location_name, locations.street_name, locations.city, locations.state, locations.zip_code FROM tasks JOIN locations ON tasks.location_id = locations.id JOIN users on tasks.user_id = users.id WHERE users.id=:id and tasks.date > CURDATE() ORDER BY tasks.date ASC, tasks.time ASC"
        data = {'id' : user_id}
        return self.db.query_db(query, data) 

    def location_validation(self, new_location):
        errors = []

        if not new_location['location_name'] or not new_location['street_name'] or not new_location['city'] or not new_location['state'] or not new_location['zip_code']:
            errors.append('All location fields are mandatory!')
        if len (new_location['state']) > 2:
            errors.append('State must have only 2 letters!')
        if self.get_locations(new_location['location_name']):
            errors.append('You already have a location with this name!')

        if errors:
            return {"status": False, "errors": errors}
        else:
            return { "status": True}

    def task_validation(self, new_task):
	    errors = []

	    if not new_task['task_name'] or not new_task['priority'] or not new_task['date'] or not new_task['time'] or not new_task['status']:
	        errors.append('All tasks fields are mandatory!')
	    if self.get_tasks(new_task['task_name']):
	        errors.append('You already have a task with this name!')

	    if errors:
	        return {"status": False, "errors": errors}
	    else:
	        return { "status": True}

    def twilio(self, user_id):
      query="SELECT phone from users where id = :id"
      data={'id': user_id}
      return self.db.query_db(query, data)

    def twilio_body(self, task_id):
      query="SELECT tasks.task_name, tasks.description, date_format(tasks.date, '%b %d, %Y') as date, date_format(tasks.time,'%h:%i %p') as time, locations.location_name, locations.street_name, locations.city, locations.state, locations.zip_code from tasks JOIN locations on tasks.location_id = locations.id where tasks.id = :id"
      data = {'id': task_id}
      return self.db.query_db(query, data)


   