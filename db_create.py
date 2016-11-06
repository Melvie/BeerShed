from project import db  #pragma: no cover
from project.models import CarboyStates #pragma: no cover

##create the database adn the db tables



db.create_all()

#should be pulling this info from arduino/rpi


## instert
db.session.add(CarboyStates(1, "Clean",20))
db.session.add(CarboyStates(2,"Clean",20))
db.session.add(CarboyStates(3, "Clean",20))

## commit the changes
db.session.commit()
