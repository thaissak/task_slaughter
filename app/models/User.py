from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()
    
    def get_users(self):
        return self.db.query_db("SELECT * FROM users")

    def get_user_by_email(self, email):
        query = "SELECT * from users where email = :email LIMIT 1"
        data = {'email': email}
        return self.db.get_one(query, data)

    def get_user_by_id(self, user_id):
        query = "SELECT * from users where id = :id LIMIT 1"
        data = {'id': user_id}
        return self.db.get_one(query, data)

    def insert_user(self, new_user):
        user_pwd = self.bcrypt.generate_password_hash(new_user['password'])
        query = "INSERT into users (first_name, last_name, email, password, phone) values(:first_name, :last_name, :email, :password, :phone)"
        data = {'first_name': new_user['first_name'], 'last_name': new_user['last_name'], 'email': new_user['email'], 'password': user_pwd, 'phone': new_user['phone'], }
        return self.db.query_db(query, data)

    def user_validation(self, new_user):
        email_regex = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        phone_regex = re.compile(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')
        errors = []

        if not new_user['first_name'] or not new_user['last_name'] or not new_user['email'] or not new_user['password'] or not new_user['pwd_conf'] or not new_user['phone']:
            errors.append('All fields are mandatory!')
        if not phone_regex.match (new_user['phone']):
            errors.append('Phone is invalid!')
        if not email_regex.match (new_user['email']):
            errors.append('Invalid e-mail!')
        if len (new_user['password']) < 8:
            errors.append('Password must have at least 8 characters!')
        if new_user['password'] != new_user['pwd_conf']:
            errors.append('Passwords are not a match!')
        if self.get_user_by_email(new_user['email']):
            errors.append('E-mail already exists!')

        if errors:
            return {"status": False, "errors": errors}
        else:
            return { "status": True}

    def pwd_validation(self, password, pwd_validate):
        return self.bcrypt.check_password_hash(password, pwd_validate)