from flask import Flask, render_template, redirect, url_for, request, session
from controller import Payslip

app = Flask(__name__)
app.secret_key = 'ireland_tax_calculator'


@app.route('/')
def index():
    '''Home page, cleaning the session when loaded'''
    session.clear()
    return render_template('index.html')

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    '''Taking the information from the user and saving in the session.'''
    if request.method == 'GET':
        return render_template('calculate.html')
    
    salary = request.form.get('salary')
    state = request.form.get('state')

    session['salary'] = float(salary)
    session['state'] = state
    return redirect(url_for('payslip'))

@app.route('/payslip')
def payslip():
    '''This route shows the payslip after getting a salary, if there is no salary
    in the session, it will redirect to the salary's page'''
    from datetime import datetime
    date = datetime.now().date().strftime('%B %d, %Y')
    hour = datetime.now().strftime('%H:%M')
    
    salary = session.get('salary', None)
    if not salary: return redirect(url_for('calculate'))
    
    state = session.get('state', None)
    payslip = Payslip().get_payslip(salary, state)
    return render_template('payslip.html', payslip=payslip, date=date, hour=hour)

@app.route('/usc')
def usc():
    '''This route show the detailed USC, if there is no salary in the session,
    it will redirect to the salary's page'''
    salary = session.get('salary', None)
    if not salary: return redirect(url_for('calculate'))
    
    usc = Payslip().export_usc(salary)
    return render_template('usc.html', usc=usc, salary=salary)

@app.route('/links')
def links():
    return render_template('links.html')

if __name__ == ("__main__"):
    app.run(debug=True)