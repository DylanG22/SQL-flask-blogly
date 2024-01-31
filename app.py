from flask import Flask, request, render_template, flash, session, redirect
from models import db, connect_db, User
from seed import seed_db


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SECRET_KEY'] = 'gu3rhgufbu4q8v'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True 

connect_db(app)

# with app.app_context():    Only needed when initializing db
#     seed_db()


@app.route('/')
def show_all_users():
    users = User.query.all()
    return render_template('allUsers.html',users=users)

@app.route('/user/<user_id>')
def user_page(user_id):
    user = User.query.get(user_id)

    return render_template('userPage.html',user=user)


@app.route('/adduser')
def add_user():
    return render_template('adduser.html')

@app.route('/adduser', methods=['POST'])
def db_add_user():
    first = request.form['first_name']
    last = request.form['last_name']
    prof_pic = request.form['profile_pic']
    if prof_pic == '':
        prof_pic = None
    new_user = User(first_name=first,last_name=last,profile_pic=prof_pic)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/user/{new_user.id}')


@app.route('/edit/<user_id>')
def edit_user(user_id):
    user = User.query.get(user_id)

    return render_template('edit.html',user=user)

@app.route('/edit/<user_id>', methods=['POST'])
def db_edit_user(user_id):
    edit = User.query.get(user_id)
    edit.first_name = request.form['first_name']
    edit.last_name = request.form['last_name']
    edit.profile_pic = request.form['profile_pic']
    db.session.add(edit)
    db.session.commit()
    return redirect(f'/user/{user_id}')

@app.route('/delete/<user_id>',methods=['POST'])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/')