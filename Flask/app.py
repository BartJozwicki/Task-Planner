from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = '42424242'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


#Prepare skeleton of the DATABASE
class Todo(db.Model):
    #The id reference of each entry 
    id = db.Column(db.Integer, primary_key = True)
    #Task column
    content = db.Column(db.String(200), nullable = False)
    #Date created column
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/about')
def about():
   return render_template('about.html')

@app.route('/contact')
def contact():
   return render_template('contact.html')

#GET is accepted by default if you want to use any other methods add them as methods = [...]
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        #Create new task from the input
        new_task = Todo(content=task_content)
        #Try to commit it to the database
        try:
            #Push changes
            db.session.add(new_task)
            #Commit changed
            db.session.commit()
            #Refresh
            return redirect('/')
        except:
            return('Commit to the server failed')
    else:
        #Sort tasks by the date 
        db.create_all()
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Problem'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task = task)

if __name__ == "__main__":
    app.run()
