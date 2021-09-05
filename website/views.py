from flask import Blueprint, render_template, request, flash
from sqlalchemy.sql.functions import session_user, user
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from .models import User, Make_Deposit, Make_Withdrawl, Make_Transaction, Avail_Loan, Claim_FD
from . import db

views = Blueprint('views', __name__)

#Check for SQL querries keywords to prevent SQL Injection attacks
def validate_SQL(input_string):
    for i in range(len(input_string)):
        if input_string[i:i+6] == "SELECT":
            flash("Please refrain from entering SQL querries!", category='error')
            return False
        elif input_string[i:i+5] == "WHERE" or input_string[i:i+5] == "UNION":
            flash("Please refrain from entering SQL querries!", category='error')
            return False
        elif input_string[i:i+4] == "DROP" or input_string[i:i+4] == "FROM":
            flash("Please refrain from entering SQL querries!", category='error')
            return False
        elif input_string[i:i+3] == "AND":
            flash("Please refrain from entering SQL querries!", category='error')
            return False
    return True

#Check for XSS cross site scripting by preventing entry of javascript code
def validate_JS(input_string):
    for i in range(len(input_string)):
        if input_string[i:i+9] == "<script>":
            flash("Please refrain from entering javascript code!", category='error')
            return False
    return True

@views.route('/', methods=['GET', 'POST'])
@views.route('home')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/deposit', methods = ['GET','POST'])
@login_required
def deposit():
    if request.method == 'POST':
        amount_string = request.form.get('amount')
        amount = int(amount_string)
        source = request.form.get('source')
        note = request.form.get('note')

        if validate_JS(amount_string) and validate_JS(note) and validate_JS(source) and validate_SQL(amount_string) and validate_SQL(source) and validate_SQL(note):
            if amount < 0:
                flash('Cannot deposited a negative amount!', category='error')
            else:
                new_deposit = Make_Deposit(amount=amount, source=source, note=note, user_id=current_user.id)
                user = User.query.filter_by(id = '{}'.format(current_user.id)).first()
                user.balance += amount
                db.session.add(new_deposit)
                db.session.commit()
                flash('Amount deposited: '+amount_string, category='success')
    
    return render_template("deposit.html", user=current_user)

@views.route('/withdrawl', methods=['GET', 'POST'])
@login_required
def withdraw():
    if request.method == 'POST':
        amount_string = request.form.get('amount')
        amount = int(amount_string)
        purpose = request.form.get('purpose')
        note = request.form.get('note')

        user = User.query.filter_by(id = '{}'.format(current_user.id)).first()

        if validate_JS(amount_string) and validate_JS(note) and validate_JS(purpose) and validate_SQL(amount_string) and validate_SQL(purpose) and validate_SQL(note):
            if amount > user.balance:
                flash('Cannot withdraw that amount!', category='error')
            elif amount < 0:
                flash('Cannot withdraw a negative amount!', cateogry='error')
            else:
                new_withdrawl = Make_Withdrawl(amount=amount, purpose=purpose, note=note, user_id=current_user.id)
                user.balance -= amount
                db.session.add(new_withdrawl)
                db.session.commit()
                flash('Amount withdrawn: '+amount_string, category='success')
        
    return render_template("withdrawl.html", user=current_user)

@views.route('/transaction', methods=['GET', 'POST'])
@login_required
def transaction():
    if request.method == 'POST':
        recipient_id = request.form.get('recipient_id')
        amount_string = request.form.get('amount')
        amount = int(amount_string)
        note = request.form.get('note')
        password = request.form.get('password')

        user = User.query.filter_by(id = '{}'.format(current_user.id)).first()
        recipient = User.query.filter_by(id = '{}'.format(recipient_id)).first()

        if validate_JS(amount_string) and validate_JS(note) and validate_JS(password) and validate_JS(recipient_id) and validate_SQL(amount_string) and validate_SQL(password) and validate_SQL(note) and validate_SQL(recipient_id):
            if check_password_hash(user.password, password):
                if amount > user.balance:
                    flash('Cannot transfer above amount of money, please check your balance!', category='error')
                else:
                    new_transaction = Make_Transaction(recipient_id=recipient_id, amount=amount, note=note, user_id=current_user.id)
                    user.balance -= amount
                    recipient.balance += amount
                    db.session.add(new_transaction)
                    db.session.commit()
                    flash("Amount Transferred: "+amount_string, category='success')
            else:
                flash('Incorrect password!', category='error')

    return render_template("transaction.html", user=current_user)

@views.route('/loan', methods=['GET', 'POST'])
@login_required
def loan():
    if request.method == 'POST':
        loan_index = request.form.get('loan_index')
        amount_string = request.form.get('amount')
        amount = int(amount_string)
        note = request.form.get('note')
        password = request.form.get('password')

        user = User.query.filter_by(id = '{}'.format(current_user.id)).first()

        if validate_JS(amount_string) and validate_JS(note) and validate_JS(password) and validate_JS(loan_index) and validate_SQL(amount_string) and validate_SQL(password) and validate_SQL(note) and validate_SQL(loan_index):
            if check_password_hash(user.password, password):
                if loan_index == '1':
                    if amount > 800:
                        flash('Cannot take a loan of that amount!', category='error')
                    elif user.balance < 1000:
                        flash('Your balance is less than the minimum balance required for taking the loan!', category='error')
                    else:
                        new_loan = Avail_Loan(loan_index=loan_index, repay_amount=amount*1.02, amount=amount, note=note, user_id=current_user.id)
                        user.balance += amount
                        db.session.add(new_loan)
                        db.session.commit()
                        flash("Successfully availed loan!", category='success')
                elif loan_index == '2':
                    if amount > 1000:
                        flash('Cannot take a loan of that amount!', category='error')
                    elif user.balance < 3500:
                        flash('Your balance is less than the minimum balance required for taking the loan!', category='error')
                    else:
                        new_loan = Avail_Loan(loan_index=loan_index, repay_amount=amount*1.025, amount=amount, note=note, user_id=current_user.id)
                        user.balance += amount
                        db.session.add(new_loan)
                        db.session.commit()
                        flash("Successfully availed loan!", category='success')
                elif loan_index == '3':
                    if amount > 5000:
                        flash('Cannot take a loan of that amount!', category='error')
                    elif user.balance < 8000:
                        flash('Your balance is less than the minimum balance required for taking the loan!', category='error')
                    else:
                        new_loan = Avail_Loan(loan_index=loan_index, repay_amount=amount*1.03, amount=amount, note=note, user_id=current_user.id)
                        user.balance += amount
                        db.session.add(new_loan)
                        db.session.commit()
                        flash("Successfully availed loan! Kindly repay loan before the tenure ends to avoid unnecessary fees.", category='success')
                else:
                    flash('Invalid loan index, please check again.', category='error')
            else:
                flash('Incorrect password!', category='error')
    
    return render_template("loan.html", user=current_user)

@views.route('/repay_loan', methods=['GET', 'POST'])
@login_required
def repay_loan():
    if request.method == 'POST':
        loan_id = request.form.get('loan_id')
        amount_string = request.form.get('amount')
        amount = int(amount_string)
        password = request.form.get('password')

        user = User.query.filter_by(id = '{}'.format(current_user.id)).first()
        loan = Avail_Loan.query.filter_by(id = '{}'.format(loan_id)).first()

        if validate_JS(amount_string) and validate_JS(password) and validate_JS(loan_id) and validate_SQL(amount_string) and validate_SQL(password) and validate_SQL(loan_id):
            if check_password_hash(user.password, password):
                if amount <= int(loan.repay_amount):
                    loan.repay_amount -= amount
                    user.balance -= amount
                    db.session.commit()
                    flash('Replayed Amount: '+amount_string, category='success')
                else:
                    flash('Cannot repay that amount!', category='error')
                if loan.repay_amount == 0:
                    loan.status = "Loan Repayed, No Debt!"
                    db.session.commit()
                    flash('Loan has been fully repayed!', category='success')

    return render_template("repay_loan.html", user=current_user)

@views.route('/fixed_deposit', methods=['GET', 'POST'])
@login_required
def invest_fd():
    if request.method == 'POST':
        fd_index = request.form.get('fd_index')
        amount_string = request.form.get('amount')
        amount = int(amount_string)
        note = request.form.get('note')
        password = request.form.get('password')

        user = User.query.filter_by(id = '{}'.format(current_user.id)).first()

        if validate_JS(amount_string) and validate_JS(note) and validate_JS(password) and validate_JS(fd_index) and validate_SQL(amount_string) and validate_SQL(password) and validate_SQL(note) and validate_SQL(fd_index):
            if check_password_hash(user.password, password):
                if fd_index == '1':
                    if amount < 100:
                        flash('Amount below minimum investment amount!', category='error')
                    elif amount > 500:
                        flash('Amount exceeds maximum investment amount!', category='error')
                    else:
                        new_fd = Claim_FD(fd_index=fd_index, amount=amount, claim_amount = amount*1.01, note = note, user_id = current_user.id)
                        user.balance -= amount
                        db.session.commit()
                        flash("Successfully invested in fixed deposit!", category='success')
                elif fd_index == '2':
                    if amount < 1000:
                        flash('Amount below minimum investment amount!', category='error')
                    elif amount > 2000:
                        flash('Amount exceeds maximum investment amount!', category='error')
                    else:
                        new_fd = Claim_FD(fd_index=fd_index, amount=amount, claim_amount = amount*1.02, note = note, user_id = current_user.id)
                        user.balance -= amount
                        db.session.add(new_fd)
                        db.session.commit()
                        flash("Successfully invested in fixed deposit!", category='success')
                elif fd_index == '3':
                    if amount < 2000:
                        flash('Amount below minimum investment amount!', category='error')
                    elif amount > 5000:
                        flash('Amount exceeds maximum investment amount!', category='error')
                    else:
                        new_fd = Claim_FD(fd_index=fd_index, amount=amount, claim_amount = amount*1.03, note = note, user_id = current_user.id)
                        user.balance -= amount
                        db.session.add(new_fd)
                        db.session.commit()
                        flash("Successfully invested in fixed deposit!", category='success')
            else:
                flash('Incorrect password!', category='error')  
                 
    return render_template("fixed_deposit.html", user=current_user)

@views.route('/claim_fixed_deposit', methods=['GET', 'POST'])
@login_required
def claim_fd():
    if request.method == 'POST':
        fd_id = request.form.get('fd_id')
        amount_string = request.form.get('amount')
        amount = int(amount_string)
        password = request.form.get('password')

        user = User.query.filter_by(id = '{}'.format(current_user.id)).first()
        fd = Claim_FD.query.filter_by(id = '{}'.format(fd_id)).first()

        if validate_JS(amount_string) and validate_JS(fd_id) and validate_JS(password) and validate_SQL(amount_string) and validate_SQL(password) and validate_SQL(fd_id):
            if check_password_hash(user.password, password):
                if amount <= fd.claim_amount:
                    user.balance += amount
                    fd.claim_amount -= amount
                    db.session.commit()
                    flash("Claimed Amount: "+amount_string, category='success')
                else:
                    flash("Cannot claim that amount of money!", category='error')

                if fd.claim_amount == 0:
                    fd.status = "Fully claimed!"
                    db.session.commit()
                    flash("Your entire fixed deposit amount has been claimed!", category='success')

    return render_template("claim_fixed_deposit.html", user=current_user)
