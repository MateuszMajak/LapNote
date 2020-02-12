from datetime import date
from CircuitsTimes import db
from flask_login import UserMixin
from CircuitsTimes import login_manager

# I created web.db using db.create_all() in the terminal
db.metadata.clear()


@login_manager.user_loader
def get_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    YearOfBirth = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    CarID = db.Column(db.Integer, nullable=False, default=1)
    private = db.Column(db.Integer, default=1)
    LapTime_id = db.relationship('LapTimes', backref='driver', foreign_keys='[LapTimes.user_id]', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Cars(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    Make = db.Column(db.String(15), nullable=False)
    Model = db.Column(db.String(15), nullable=False)
    Year = db.Column(db.Integer, nullable=False)
    Power = db.Column(db.Float, nullable=False)
    Cylinders = db.Column(db.Integer, nullable=False)
    Transmission = db.Column(db.String(20), nullable=False)
    DrivenWheels = db.Column(db.String(20), nullable=False)
    DoorsNumber = db.Column(db.Integer, nullable=False)
    CarSize = db.Column(db.String(15), nullable=False)
    CarStyle = db.Column(db.String(15), nullable=False)
    LapTime_id = db.relationship('LapTimes', backref="car", lazy='dynamic')

    def __repr__(self):
        return f"Car('{self.id}', '{self.Make}', '{self.Model}')"


class LapTimes(db.Model):
    __tablename__ = 'LapTimes'
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.Date, nullable=False, default=date.today)
    comment = db.Column(db.Text, nullable=True)
    Time = db.Column(db.Float, nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Lap('{self.Time}', '{self.date_added}')"


class Tracks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(30), nullable=False)
    Length = db.Column(db.Float, nullable=False)
    LapTime_id = db.relationship('LapTimes', backref='circuit', lazy='dynamic', foreign_keys="[LapTimes.track_id]")
    #type_id = db.Column(db.Integer, db.ForeignKey('vehicletype.id'), nullable=False)

    def __repr__(self):
        return f"Track('{self.id}', '{self.Name}', '{self.Length}')"


class vehicletype(db.Model):
    __name__ = 'vehicletype'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(30), nullable=False)
    #Tracks_id = db.relationship('Tracks', backref='circuitType', lazy='dynamic', foreign_keys="[Tracks.type_id]")

    def __repr__(self):
        return f"Vehicle('{self.Name}')"

