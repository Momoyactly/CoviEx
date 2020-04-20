import flask, requests, json
from flask import request, redirect, url_for, render_template, flash
from funciones import sendWebexMsg, sendSMS
from forms import LoginForm



app = flask.Flask(__name__)
app.config["SECRET_KEY"]= "87f4236d17bbabd54836d1f65e4e0c63"
app.config["DEBUG"] = True


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "joarriag"  and form.password.data == "cisco123":
      
            return redirect(url_for('demo'))
        else:
            flash('Login requested for user login Unsuccesful. Plese check username and password')
    return render_template('loginTut.html', title='Sign In', form=form)


@app.route('/widget')
def Widget():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJUZXN0VGVsZWNvbnN1bHRhIiwibmFtZSI6IlRlc3RUZWxlY29uc3VsdGEiLCJpc3MiOiJZMmx6WTI5emNHRnlhem92TDNWekwwOVNSMEZPU1ZwQlZFbFBUaTlrWWpKalptSTBOeTAyTURKaUxUUm1OR0V0T0ROaE1TMDRNREV4WkRNNE1qZGpNek0iLCJleHAiOiIxNTkyNjM3MDgwIn0.bbcFiX7bywA8ExWmuSHIys36TDVzlIOswE3llnPtqYM"
    return render_template('widget.html', title='widget', token=token)

@app.route('/democonstula')
def democonsulta():
    with open("templates/democonstula.html") as file: 
        data = file.read()
    return data


# Uli code from here -----------------------------------

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/teleconsulta')
def teleconsulta():
    return render_template('democonstula.html')

# Agregado (Apr 20) demo televisita
# Se agrego a la carpeta de static dos archivos (.js / .css) (Apr 20 )

@app.route('/televisita')
def televisita():
    return render_template('demovisita.html')



# to here................



# Uli mde changes on this method April 19 

@app.route('/repuestateleconsulta')
def respuestateleconsulta():
    numero = request.args.get('numero')
    sendWebexMsg("por favor ingresa a la videoconsulta en este link:")
    directorio =[("Uriel","+5215580663521")]
    #sendSMS(directorio)
    return render_template('repuestateleconsulta.html')

# Codigo modificado Apr 20 para incluir la demp de televisita
@app.route('/respuestatelevisita')
def respuestatelevisita():
    numero = request.args.get('numero')
    sendWebexMsg("por favor ingresa a la videoconsulta en este link:")
    directorio =[("Uriel","+5215580663521")]
    #sendSMS(directorio)
    return render_template('repuestatelevisita.html', title='respuestatelevisita')
     


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

if __name__ == "__main__":
    app.run(host="0.0.0.0")   