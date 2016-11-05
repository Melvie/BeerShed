
#################
#### imports ####
#################
import sys
from project import db, app
#socketio #pragma: no cover
from project.models import CarboyStates, User #pragma: no cover
from flask import flash, redirect, url_for, render_template, Blueprint, request #pragma: no cover
from forms import ButtonForm #pragma: no cover
from functools import wraps #pragma: no cover
from flask_login import login_required, current_user #pragma: no cover
from flask_principal import Permission, RoleNeed, Principal,identity_loaded, Identity, UserNeed

################
#### config ####
################
#ser=serial.Serial('/dev/ttyACM0' , 9600)

admin_permission = Permission(RoleNeed('admin'))

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)
guest_blueprint = Blueprint(
    'guest',__name__,
    template_folder='templates'
)

BREW, BOTTLE, CLEAN, TRANSFER, STOP, = "brew", "bottle", "clean", "transfer", "stop"

commands = {'Brew':BREW, 'Bottle':BOTTLE, 'Clean':CLEAN, 'Transfer':TRANSFER,'Stop':STOP}

carboys = [1,2,3]

actions = {"clean":0,"bottle":0,"brew":1}

################
#### routes ####
################
#print admin_permission
@home_blueprint.route('/index/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def home():

    users = db.session.query(User).all()

    for user in users:
        print user

    error = None
    info = db.session.query(CarboyStates).order_by(CarboyStates.carboy).all()
    return render_template(
            'index.html', info=info,error=error, commands = commands, carboys=carboys)


@app.route('/<cmd>')
def command(cmd = None):

    try:
        cmd = str(cmd).split(",")
        action = cmd[0]
        carboy_id=cmd[1]

        if action == "STOP":
            response = "Turning off power to pump and hot plate"

        else:
            info = CarboyStates.query.filter(CarboyStates.carboy==int(cmd[1])).first()

            if action == "transfer":
                to_carb = cmd[2]
                info2 = CarboyStates.query.filter(CarboyStates.carboy==int(cmd[2])).first()

                response = info.transfer(info2)

            else :
                r = getattr(info,action)
                response = r()


        info = db.session.query(CarboyStates).order_by(CarboyStates.carboy).all()
        db.session.commit()
        return response

    except:
        e = sys.exc_info()[0]
        print e
        return "Error: {}".format(e)



@home_blueprint.route('/guest', methods=['GET', 'POST'])
@login_required
def guest():
    error = None
    info = db.session.query(CarboyStates).order_by(CarboyStates.carboy).all()
    return render_template(
            'guest.html', info=info,error=error, commands = commands, carboys=carboys)

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
        identity.user = current_user

        if hasattr(current_user, 'name'):
            identity.provides.add(UserNeed(current_user.name))

        if hasattr(current_user, 'role'):
            identity.provides.add(RoleNeed(current_user.role))

# @socketio.on('event')
# #@admin_permission.require
# def handle_params(data):
#     print "recieved this mess: {}".format(str(data))
#     r = data['action'][:-1]+" {}".format(data['action'][-1])
#     print r
#     ser.write(str(r))
#     ser.write('\n')
