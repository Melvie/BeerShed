#################
#### imports ####
#################

from flask import flash, redirect, render_template, request, \
    url_for, Blueprint, current_app, session #pragma: no cover
from forms import LoginForm #pragma: no cover
from project import db, app#pragma: no cover
from project.models import User, bcrypt#pragma: no cover
from flask_login import login_user, login_required, logout_user, current_user #pragma: no cover
from flask_principal import Principal, Permission, RoleNeed, identity_loaded, Identity, identity_changed, UserNeed, AnonymousIdentity

################
#### config ####
################

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)

################
#### routes ####
################

# route for handling the login page logic
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['username']).first()
            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
                #session['logged_in'] = True
                login_user(user)
                flash('You were logged in.')
                identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
                if user.role == "admin":
                    print user.role
                    flash('Welcome Admin!')
                    return redirect(url_for('home.home'))

                else:
                    #render_template('guest.html',form=form, error=error)
                    return redirect(url_for('home.guest'))

            else:
                error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    identity_changed.send(current_app._get_current_object(),identity=AnonymousIdentity())
    flash('You were logged out.')
    return redirect(url_for('users.login'))
