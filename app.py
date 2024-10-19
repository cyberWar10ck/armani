from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# مدل‌های پایگاه‌داده
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shareholders = db.relationship('Shareholder', backref='project', lazy=True)

class Shareholder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    partners = db.relationship('Partner', backref='shareholder', lazy=True)

class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    shareholder_id = db.Column(db.Integer, db.ForeignKey('shareholder.id'), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        shareholders_count = int(request.form.get('shareholders_count', 0))
        
        # ایجاد و ذخیره پروژه
        project = Project(name=project_name)
        db.session.add(project)
        db.session.commit()
        
        for i in range(shareholders_count):
            shareholder_name = request.form.get(f'shareholder_{i}_name')
            shareholder_percentage = float(request.form.get(f'shareholder_{i}_percentage', 0))
            partners_count = int(request.form.get(f'shareholder_{i}_partners_count', 0))
            
            # ایجاد و ذخیره سهام‌دار
            shareholder = Shareholder(name=shareholder_name, percentage=shareholder_percentage, project=project)
            db.session.add(shareholder)
            db.session.commit()
            
            for j in range(partners_count):
                partner_name = request.form.get(f'shareholder_{i}_partner_{j}_name')
                partner_percentage = float(request.form.get(f'shareholder_{i}_partner_{j}_percentage', 0))
    
                if partner_name:  # چک کنید که نام خالی نباشد
                    partner = Partner(name=partner_name, percentage=partner_percentage, shareholder=shareholder)
                    db.session.add(partner)


            
            db.session.commit()

            
        
        return redirect(url_for('index'))
    #this is test comment for commit author change
    projects = Project.query.all()
    return render_template('index.html', projects=projects)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
