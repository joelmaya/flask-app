from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql  import func


app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI']='postgres://postgres:maya2008a@localhost/acaye'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://wbcivkccfnoifr:687e3116b8b73c5f911ad07345d6c58b1482558551e784a97268fc41812a6bcd@ec2-3-232-240-231.compute-1.amazonaws.com:5432/d69lt47v2kel52?sslmode=require'


db = SQLAlchemy(app)

class data(db.Model):
	__tablename__='data'

	id = db.Column(db.Integer,primary_key = True)
	email = db.Column(db.String(200),unique = True)
	height = db.Column(db.Integer)

	def __init__(self,email,height):

		self.email= email
		self.height = height



@app.route('/')
def index():
	return render_template('index.html')




@app.route('/success' ,methods=["POST"])
def success():

	if request.method == "POST":
		email = request.form['email_name']
		height = request.form['height_name']


		if db.session.query(data).filter(data.email == email).count() == 0:
			Data = data(email,height) 
			db.session.add(Data)
			db.session.commit()

			Average_height = db.session.query(func.avg(data.height)).scalar()
			average_height = round(Average_height,1)
			count = db.session.query(data.height).count()
			send_email(email,height,average_height,count)

			return render_template('success.html')
	return render_template('index.html',text = 'email already exist')




if __name__ == '__main__':
	app.debug=True
	app.run()


