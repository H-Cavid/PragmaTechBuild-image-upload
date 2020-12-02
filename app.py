from flask import Flask, render_template,request, redirect ,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename#faylin adinin yoxlanilmasi  ucundu
import os




app = Flask(__name__)
app.secret_key = "Secret_Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER= 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Person(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(60))
    email=db.Column(db.String(60))
    phone=db.Column(db.String(60))
    photo=db.Column(db.String())

    def __init__(self, name , email, phone, photo):
        self.name=name
        self.email=email
        self.phone=phone
        self.photo=photo

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
        file = request.files['photo']

        if file.filename == ' ':
            flash("Heç bir şəkil seçilməyib!!!")
            return redirect(url_for('index'))
        
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('static', app.config['UPLOAD_FOLDER'], filename))
            photo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            flash('Fayl fformati desteklenmir')
            return redirect(url_for('index'))


        newPerson=Person(name , email , phone, photo)
        db.session.add(newPerson)
        db.session.commit()#db-daki butun emeliyatlari tekrarliyiram


        flash("Məlumat daxil oldu Təşəkkürlər!") #Mesaj vermek ucun istifade olunur
        return redirect(url_for('index'))








@app.route('/delete/<id>' , methods = ['GET'])#id-e gore silirem
def delete(id):
    selectedPerson = Person.query.get(id)
    os.remove(os.path.join('static', selectedPerson.photo))
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

    file = request.files['file']
    if file.filename != '':#file-n var
        if allowed_file(file.filename):#desteklenen fayl tipindedir
            #true gelen versiya
             #os.remove(os.path.join('static', selectedPerson.photo))

            filename = secure_filename(file.filename)

            file.save(os.path.join('static' , app.config['UPLOAD_FOLDER'],filename))

            selectedPerson.photo = os.path.join(app.config['UPLOAD_FOLDER'], filename)







        else:#desteklenmeyen fayl tipindedir
            flash('Desteklenen fayl formati deyil')
            return redirect(url_for('index'))





    db.session.commit()
    flash("Məlumat dəyişdirildi. Təşəkkürlər!")
    return redirect(url_for("index"))

