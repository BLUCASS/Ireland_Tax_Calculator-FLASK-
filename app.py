from flask import Flask, render_template, redirect, url_for, request, session
from controller import Payslip

app = Flask(__name__)
app.secret_key = 'ireland_tax_calculator'


@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'GET':
        return render_template('calculate.html')
    
    salary = request.form.get('salary')
    state = request.form.get('state')

    session['salary'] = float(salary)
    session['state'] = state
    return redirect(url_for('payslip'))

@app.route('/payslip')
def payslip():
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
    salary = session.get('salary', None)
    if not salary: return redirect(url_for('calculate'))
    usc = Payslip().export_usc(salary)
    return render_template('usc.html', usc=usc, salary=salary)

if __name__ == ("__main__"):
    app.run(debug=True)