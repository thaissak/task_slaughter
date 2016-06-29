from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.load_model('Schedule')
        self.db = self._app.db

   
    def index(self):
        return self.load_view('index.html')

    def registration(self):
        return self.load_view('registration.html')

    def logout(self):
        session.pop('user_id')
        return redirect('/task_slaughter')

    def insert_user(self):
        print request.form
        new_user = {'first_name':request.form['first_name'],'last_name':request.form['last_name'],
        'email':request.form['email'],'password':request.form['password'],'pwd_conf':request.form['pwd_conf'], 'phone':request.form['phone']}
        validation = self.models['User'].user_validation(new_user)
        print new_user
        if validation['status']:
            print "1"
            user_id = self.models['User'].insert_user(new_user)
            session['user_id'] = user_id
            return redirect('/task_slaughter/dashboard')
        else:
            print "2"
            for error in validation['errors']:
                flash(error, 'validation')
            return redirect('/task_slaughter/registration')

    def login_process(self):
        user_info = {'email': request.form['email'],'password': request.form['password']}
        
        user = self.models['User'].get_user_by_email(user_info['email'])
        if not user:
            flash("E-mail and/or Password invalid!", 'login')
            return redirect('/task_slaughter')
        
        if not self.models['User'].pwd_validation(user['password'], user_info['password']):
            flash("E-mail and/or Password invalid!", 'login')
            return redirect('/task_slaughter')
            
        session['user_id'] = user['id']
        return redirect('/task_slaughter/dashboard')




