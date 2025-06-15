from flask import Flask,render_template,request,redirect,url_for,flash,render_template_string,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'qwertyuiopasdfghjkl'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/vitclub'

db = SQLAlchemy(app)

class Contactus(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.now)

class Login(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.now)

class Users(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    regno = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

@app.route("/")
def home():
    return render_template('vit.html')

@app.route("/contact",methods = ['GET','POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        entry = Contactus(name = name,email = email,message=message)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')

@app.route("/login",methods = ['GET','POST'])
def login_page():
    if(request.method=='POST'):
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = Users.query.filter_by(email = email,password=password).first()

        if user:
            db.session.add(user)
            db.session.commit()
            
            session['user'] = user.email.split('@')[0]
            
            return render_template_string("""
            <script>
                alert("Log In Successful!!");
                window.location.href = "{{ url_for('home') }}";
            </script>
        """)
            
        else:
            return render_template_string("""
            <script>
                alert("Invalid Credentials!!");
                window.location.href = "{{ url_for('home') }}";
            </script>
        """)
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('home'))

@app.route("/register",methods = ['GET','POST'])
def register():
    if(request.method=='POST'):
        name = request.form.get('name')
        regno = request.form.get('regno')
        email = request.form.get('email')
        password = request.form.get('password')
        
        existing_user = Login.query.filter_by(email=email).first()
        if existing_user:
            return render_template_string("""
            <script>
                alert("User already exists. Please Sign In.");
                window.location.href = "{{ url_for('login_page') }}";
            </script>
        """)

        new_user = Users(name=name,regno=regno,email=email, password=password)

        db.session.add(new_user)
        db.session.commit()
        # In this method message is not showing   <=====
        # print("Registration successful. You can now log in.")
        # return redirect(url_for('login_page'))

        #By this method alert comes  <=====
        return render_template_string("""
            <script>
                alert("Registration successful. You can now log in.");
                window.location.href = "{{ url_for('login_page') }}";
            </script>
        """)
        
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
