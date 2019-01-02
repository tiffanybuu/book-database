from flask import Flask

app = Flask(__name__)


# where the database will be stored locally
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/tiffanybuu/Flask/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False