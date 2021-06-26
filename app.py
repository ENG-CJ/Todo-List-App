
from flask import  Flask,request,redirect,render_template
from flask_sqlalchemy import  SQLAlchemy
from datetime import  datetime
from  wtforms import StringField,PasswordField
from  flask_wtf import FlaskForm

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SECRET_KEY']='secret'

db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(100), nullable=False)
    date_created=db.Column(db.DateTime, nullable=False,default=datetime.utcnow())


@app.route('/',methods=['GET','POST'])
def index():

    if request.method=='POST':
        task_content=request.form['content']
        new_task=Todo(content=task_content)
        db.session.add(new_task)
        db.session.commit()
        return  redirect('/')
    else:
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template('todo.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    delete_task=Todo.query.get_or_404(id)
    db.session.delete(delete_task)
    db.session.commit()
    return  redirect('/')

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    staff = Todo.query.get_or_404(id)
    if request.method=='POST':
        staff.content=request.form['content']
        db.session.commit()
        return redirect('/')
    else:
        return render_template('update.html',staff=staff)



if __name__=="__main__":
    app.run(debug=True)