from flask import Flask, render_template,request, redirect ,url_for,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret_Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Person(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(60))
    email=db.Column(db.String(60))
    phone=db.Column(db.String(60))

    def __init__(self, name , email, phone):
        self.name=name
        self.email=email
        self.phone=phone

    def __repr__(self):
        return '{name:'+self.name+' , email: '+str(self.email)+' , phone: '+str(self.phone)+'}'

@app.route("/")
def index():
    allPersons = Person.query.all()#formnan datani getirmek ucun yaziram
    return render_template("index.html", persons = allPersons)#person deye kececek her yerde

@app.route('/insert' , methods = ['POST'])#insert route-u yaradiram
def insert():
    #name, surname, email
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        newPerson=Person( name, email, phone)
        db.session.add(newPerson)
        db.session.commit()#db-daki butun emeliyatlari tekrarliyiram



        flash("Məlumat daxil oldu Təşəkkürlər!") #Mesaj vermek ucun istifade olunur

        return redirect(url_for('index'))

@app.route('/delete/<id>' , methods = ['GET'])#id-e gore silirem
def delete(id):
    selectedPerson = Person.query.get(id)
    db.session.delete(selectedPerson)
    db.session.commit()
    flash("Məlumat silindi. Təşəkkürlər!")
    
    return redirect(url_for('index'))

@app.route('/edit/<id>' , methods = ['POST'])
def edit(id):
    selectedPerson=Person.query.get(id)
    selectedPerson.name = request.form['name']
    selectedPerson.email = request.form['email']
    selectedPerson.phone = request.form['phone']
    db.session.commit()
    flash("Məlumat dəyişdirildi. Təşəkkürlər!")
    return redirect(url_for("index"))

