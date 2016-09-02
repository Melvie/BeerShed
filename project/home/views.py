
#################
#### imports ####
#################

from project import db, app, socketio #pragma: no cover
from project.models import CarboyStates #pragma: no cover
from flask import flash, redirect, url_for, render_template, Blueprint, request #pragma: no cover
from forms import MessageForm #pragma: no cover
from functools import wraps #pragma: no cover 
from flask_login import login_required, current_user #pragma: no cover
from flask_principal import Permission, RoleNeed, Principal,identity_loaded, Identity, UserNeed
################
#### config ####
################

admin_permission = Permission(RoleNeed('admin'))

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)


################
#### routes ####
################
#print admin_permission
@home_blueprint.route('/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def home():
    error = None
    form = MessageForm(request.form)
    #if form.validate_on_submit():
       # new_message = BlogPost(
        #    form.title.data,
         #   form.description.data,
          #  current_user.id
        #)
        #db.session.add(new_message)
        #db.session.commit()
        #flash('New entry was successfully posted. Thanks.')
       # return redirect(url_for('home.home'))

    info = db.session.query(CarboyStates).all()
    

    return render_template(
            'index.html', info=info, form=form, error=error)

@home_blueprint.route('/guest')
def guest():
    error = None
    form = MessageForm(request.form)
    info = db.session.query(CarboyStates).all()
    flash("Welcome Guest!")
    return render_template('guest.html',info=info, form = form, error=error)

@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
        identity.user = current_user

        if hasattr(current_user, 'name'):
            identity.provides.add(UserNeed(current_user.name))

        if hasattr(current_user, 'role'):
            identity.provides.add(RoleNeed(current_user.role))

@socketio.on('my event')
#@admin_permission.require
def handle_params(json):
    print "recieved this mesS: {}".format(str(json))


  

