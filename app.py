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
    return render_template('login.html', title='Sign In', form=form)

@app.route('/widget')
def Widget():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJUZXN0VGVsZWNvbnN1bHRhIiwibmFtZSI6IlRlc3RUZWxlY29uc3VsdGEiLCJpc3MiOiJZMmx6WTI5emNHRnlhem92TDNWekwwOVNSMEZPU1ZwQlZFbFBUaTlrWWpKalptSTBOeTAyTURKaUxUUm1OR0V0T0ROaE1TMDRNREV4WkRNNE1qZGpNek0iLCJleHAiOiIxNTkyNjM3MDgwIn0.bbcFiX7bywA8ExWmuSHIys36TDVzlIOswE3llnPtqYM"
    return render_template('widget.html', title='widget', token=token)

@app.route('/demo')
def demo():
    return render_template('demo.html')

# ////////////////////  Demos ///////////////
@app.route('/democonstula')
def teleconsulta():
    return render_template('democonstula.html')

@app.route('/demovisita')
def demovisita():
    return render_template('demovisita.html')

# //////////////////// Respuestas ///////////// 
@app.route('/repuestateleconsulta')
def respuestateleconsulta():
    numero = request.args.get('numero')
    sendWebexMsg("por favor ingresa a la videoconsulta en este link:")
    directorio =[("Uriel","+5215580663521")]
    #sendSMS(directorio)
    return render_template('repuestateleconsulta.html')

@app.route('/respuestatelevisita')
def respuestatelevisita():
    numero = request.args.get('numero')
    sendWebexMsg("por favor ingresa a la televisita en este link:")
    directorio =[("Uriel","+5215580663521")]
    #sendSMS(directorio)
    return render_template('respuestatelevisita.html', title='respuestatelevisita')
     

@app.route('/')
def index():
    return redirect(url_for("demo"))

if __name__ == "__main__":
    app.run(host="0.0.0.0")   