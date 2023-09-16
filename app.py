from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)



app.config['MONGO_URI'] = 'mongodb://localhost:27017/flaskusers'
mongo = PyMongo(app)

db=mongo.db



@app.route('/',methods=['GET','POST'])
def add_user():
    if 'register' in request.form and request.method == 'POST': 
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        data = {
            'name': name,
            'email': email,
            'password': password
        }
        id = mongo.db.register.insert_one(data)

        return redirect(url_for('users'))

    return render_template('index.html')

@app.route('/users')
def users():
    users = mongo.db.register.find()
    return render_template("view_users.html",data=users)

@app.route('/user/<id>', methods=['GET','POST','PUT'])
def update_user(id):
    user = mongo.db.register.find_one({'_id': ObjectId(id)})
    
    if request.method == 'POST': 
        name = request.form['new_name']
        email = request.form['new_email']
        password = request.form['new_password']
        
        data = {
            'name': name,
            'email': email,
            'password': password
        }
        mongo.db.register.update_one({'_id': ObjectId(id)}, {'$set': data})
        return redirect(url_for('users'))

    return render_template("view_user.html", data=user)


@app.route('/delete/<string:user_id>')
def delete_user(user_id):
    try:
        collection = mongo.db.register
        result = collection.delete_one({'_id': ObjectId(user_id)})
        return redirect(url_for('add_user'))
    except pymongo.errors.PyMongoError as e:
        return jsonify({'error': f'Error deleting user: {str(e)}'})


       
            
if __name__ == "__main__":
    app.run(debug=True)