from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm

from sqlalchemy import desc

from datetime import datetime

from wtforms import SelectField, StringField, DateField


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://username:password@localhost/equipment'

db=SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['SECRET_KEY'] = 'secret'

class Item(db.Model):
  __tablename__ = 'equipment'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200))
  number = db.Column(db.String(200))
  identifier = db.Column(db.String(200))
  item_type = db.Column(db.Integer, db.ForeignKey('itemtype.id'))
  main_option = db.Column(db.Integer, db.ForeignKey('option.id'))
  use_type = db.Column(db.Integer, db.ForeignKey('usetype.id'))
  office = db.Column(db.Integer, db.ForeignKey('office.id'))
  document = db.Column(db.String(200))
  purchase_date = db.Column(db.DateTime)
  comment = db.Column(db.String(500))
  created_date = db.Column(db.DateTime, default=datetime.utcnow)

  def __init__(self, name, number, identifier, item_type, main_option, use_type, office, document, purchase_date, comment):
    self.name = name
    self.number = number
    self.identifier = identifier
    self.item_type = item_type
    self.main_option = main_option
    self.use_type = use_type
    self.office = office
    self.document = document
    self.purchase_date = purchase_date
    self.comment = comment


class ItemType(db.Model):
  __tablename__ = 'itemtype'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(300))

  def __init__(self, name):
    self.name = name

class Option(db.Model):
  __tablename__ = 'option'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(300))

  def __init__(self, name):
    self.name = name


class UseType(db.Model):
  __tablename__ = 'usetype'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(300))

  def __init__(self, name):
    self.name = name


class Office(db.Model):
  __tablename__ = 'office'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(300))

  def __init__(self, name):
    self.name = name



""" Формы """

class Form(FlaskForm):
  name = StringField("Наименование: ")
  number = StringField("Номер: ")
  identifier = StringField("Идентификатор: ")
  item_type = SelectField('item_type', choices=[])
  main_option = SelectField('main_option', choices=[])
  use_type = SelectField('use_type', choices=[])
  office = SelectField('office', choices=[])
  document = StringField("Документ: ")
  purchase_date = DateField("Дата покупки: ", format='%Y-%m')
  comment = StringField("Комментарий: ")



""" CRUD на оборудование """

@app.route('/new_equipment', methods=['GET','POST'])
def new_equipment():
  form = Form()
  form.item_type.choices = [(item_type.id, item_type.name) for item_type in ItemType.query.all()]
  form.main_option.choices = [(main_option.id, main_option.name) for main_option in Option.query.all()]
  form.use_type.choices = [(use_type.id, use_type.name) for use_type in UseType.query.all()]
  form.office.choices = [(office.id, office.name) for office in Office.query.all()]
  if request.method == 'POST':
    item = Item(name=form.name.data, number=form.number.data, identifier=form.identifier.data, item_type=form.item_type.data, main_option=form.main_option.data, use_type=form.use_type.data, office=form.office.data, document=form.document.data, purchase_date=form.purchase_date.data, comment=form.comment.data)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for("index"))
  return render_template('new_equipment.html', form=form)

@app.route('/', methods=['GET','POST'])
def index():
  old_first = Item.query.order_by(Item.created_date)
  new_first = Item.query.order_by(desc(Item.created_date))
  name_sorted = Item.query.order_by(Item.name)
  itemtypes = ItemType.query.all()
  return render_template('index.html', old_first=old_first, new_first=new_first, name_sorted=name_sorted, itemtypes=itemtypes)

@app.route('/filter/<int:id>', methods=['GET','POST'])
def filter(id):
  old_first = Item.query.order_by(Item.created_date)
  new_first = Item.query.order_by(desc(Item.created_date))
  name_sorted = Item.query.order_by(Item.name)
  itemtypes = ItemType.query.all()
  return render_template('filter.html', old_first=old_first, new_first=new_first, name_sorted=name_sorted, itemtypes=itemtypes, id=id)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
  item = Item.query.get(id)
  form = Form(obj=item)
  form.item_type.choices = [(item_type.id, item_type.name) for item_type in ItemType.query.all()]
  form.main_option.choices = [(main_option.id, main_option.name) for main_option in Option.query.all()]
  form.use_type.choices = [(use_type.id, use_type.name) for use_type in UseType.query.all()]
  form.office.choices = [(office.id, office.name) for office in Office.query.all()]
  if request.method == "POST":
    item.name = form.name.data
    item.number = form.number.data
    item.identifier = form.identifier.data
    item.item_type = form.item_type.data
    item.main_option = form.main_option.data
    item.use_type = form.use_type.data
    item.office = form.office.data
    item.document = form.document.data
    item.purchase_date = form.purchase_date.data
    item.comment = form.comment.data
    db.session.commit()
    return redirect(url_for("index"))
  return render_template("edit.html", form=form)

@app.route('/item/<int:id>', methods=['GET'])
def item(id):
  item = Item.query.get(id)
  item_type = ItemType.query.get(item.item_type)
  main_option = Option.query.get(item.main_option)
  use_type = UseType.query.get(item.use_type)
  office = Office.query.get(item.office)
  return render_template("item.html", item=item, item_type=item_type, main_option=main_option, use_type=use_type, office=office)



""" CRUD на справочник типов """

@app.route('/new_itemtype', methods=['GET','POST'])
def new_itemtype():
  if request.method == "POST":
    name = request.form['name']
    itemtype = ItemType(name)
    db.session.add(itemtype)
    db.session.commit()
    return redirect(url_for("itemtypes"))
  return render_template('new_itemtype.html')

@app.route('/itemtypes')
def itemtypes():
  itemtypes_list = ItemType.query.all()
  return render_template('itemtypes.html', itemtypes_list=itemtypes_list)

@app.route("/delete_type/<int:id>", methods=['POST'])
def delete_type(id):
    itemtype = ItemType.query.get(id)
    db.session.delete(itemtype)
    db.session.commit()
    return redirect(url_for("itemtypes"))

@app.route('/edit_type/<int:id>', methods=['GET', 'POST'])
def edit_type(id):
  itemtype = ItemType.query.get(id)
  if request.method == "POST":
    name = request.form["name"]
    itemtype.name = name
    db.session.commit()
    return redirect(url_for("itemtypes"))
  return render_template("edit_type.html", itemtype=itemtype)



""" CRUD на справочник основных средств """

@app.route('/new_option', methods=['GET','POST'])
def new_option():
  if request.method == "POST":
    name = request.form['name']
    option = Option(name)
    db.session.add(option)
    db.session.commit()
    return redirect(url_for("options"))
  return render_template('new_option.html')

@app.route('/options')
def options():
  options_list = Option.query.all()
  return render_template('options.html', options_list=options_list)

@app.route("/delete_option/<int:id>", methods=['POST'])
def delete_option(id):
    option = Option.query.get(id)
    db.session.delete(option)
    db.session.commit()
    return redirect(url_for("options"))

@app.route('/edit_option/<int:id>', methods=['GET', 'POST'])
def edit_option(id):
  option = Option.query.get(id)
  if request.method == "POST":
    name = request.form["name"]
    option.name = name
    db.session.commit()
    return redirect(url_for("options"))
  return render_template("edit_option.html", option=option)



""" CRUD на справочник типов использования """

@app.route('/new_usetype', methods=['GET','POST'])
def new_usetype():
  if request.method == "POST":
    name = request.form['name']
    usetype = UseType(name)
    db.session.add(usetype)
    db.session.commit()
    return redirect(url_for("usetypes"))
  return render_template('new_usetype.html')

@app.route('/usetypes')
def usetypes():
  usetypes_list = UseType.query.all()
  return render_template('usetypes.html', usetypes_list=usetypes_list)

@app.route("/delete_usetype/<int:id>", methods=['POST'])
def delete_usetype(id):
    usetype = UseType.query.get(id)
    db.session.delete(usetype)
    db.session.commit()
    return redirect(url_for("usetypes"))

@app.route('/edit_usetype/<int:id>', methods=['GET', 'POST'])
def edit_usetype(id):
  usetype = UseType.query.get(id)
  if request.method == "POST":
    name = request.form["name"]
    usetype.name = name
    db.session.commit()
    return redirect(url_for("usetypes"))
  return render_template("edit_usetype.html", usetype=usetype)



""" CRUD на справочник офисов """

@app.route('/new_office', methods=['GET','POST'])
def new_office():
  if request.method == "POST":
    name = request.form['name']
    office = Office(name)
    db.session.add(office)
    db.session.commit()
    return redirect(url_for("offices"))
  return render_template('new_office.html')

@app.route('/offices')
def offices():
  offices_list = Office.query.all()
  return render_template('offices.html', offices_list=offices_list)

@app.route("/delete_office/<int:id>", methods=['POST'])
def delete_office(id):
    office = Office.query.get(id)
    db.session.delete(office)
    db.session.commit()
    return redirect(url_for("offices"))

@app.route('/edit_office/<int:id>', methods=['GET', 'POST'])
def edit_office(id):
  office = Office.query.get(id)
  if request.method == "POST":
    name = request.form["name"]
    office.name = name
    db.session.commit()
    return redirect(url_for("offices"))
  return render_template("edit_office.html", office=office)



if __name__ == '__main__':
  app.run(debug=True)