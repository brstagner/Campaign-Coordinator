from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database (dnd)"""
    db.app = app
    db.init_app(app)

### Player Models ###
class Player(db.Model):
    __tablename__ = 'players'

    player_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    party_notes = db.Column(db.Text)
    player_notes = db.Column(db.Text)
    dm_notes = db.Column(db.Text)
    demo = db.Column(db.Boolean)
    vitals = db.Column(db.Boolean)
    combat = db.Column(db.Boolean)
    spells = db.Column(db.Boolean)
    ability = db.Column(db.Boolean)
    level = db.Column(db.Boolean)
    proficiency = db.Column(db.Boolean)
    items = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='cascade'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.campaign_id', ondelete='cascade'))

class Demo(db.Model):
    __tablename__ = 'demo'

    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id', ondelete='cascade'), primary_key=True, unique=True)
    
    player_level = db.Column(db.Integer, default=1)
    player_xp = db.Column(db.Integer, default=0)
    race = db.Column(db.String(200))
    subrace = db.Column(db.String(200))
    job = db.Column(db.String(200))
    subjob = db.Column(db.String(200))
    alignment = db.Column(db.String(200))
    age = db.Column(db.Integer)
    size = db.Column(db.String(20))
    notes = db.Column(db.Text)

    # def __repr__(self):
    #     """Show class info"""
    #     user = self
    #     return f'<Name: {self.name}, Gender: {self.gender}, Race: {self.race}, Age: {self.age}, Alignment: {self.alignment}>'

class Vitals(db.Model):
    __tablename__ = 'vitals'
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id', ondelete='cascade'), primary_key=True, unique=True)

    hp = db.Column(db.Integer)
    max_hp = db.Column(db.Integer)
    # hd, pool of hit dice ex. [(3, 1d8), (2, 1d6)]
    hd = db.Column(db.VARCHAR)
    # conditions ex. ['Paralyzed', 'Blind']
    conditions = db.Column(db.VARCHAR)
    notes = db.Column(db.Text)

class Combat(db.Model):
    __tablename__ = 'combat'
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id', ondelete='cascade'), primary_key=True, unique=True)
    # attacks: name, damage, number ex. [('Short Sword', '1d6', 2), ('Dragon Breath', '2d6', 1)]
    attacks = db.Column(db.VARCHAR)
    ac = db.Column(db.Integer)
    initiative = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    inspiration = db.Column(db.Integer)
    ki = db.Column(db.Integer)
    max_ki = db.Column(db.Integer)
    notes = db.Column(db.Text)

class Spells(db.Model):
    __tablename__ = 'spells'
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id', ondelete='cascade'), primary_key=True, unique=True)
    # known ex. ['Magic Missile', 'Otto's Irresistible Dance']
    known = db.Column(db.VARCHAR)
    # all below are prepared spells & #; cantrips ex. [('Magic Missile', 2), ('Light', 1)]
    cantrips = db.Column(db.VARCHAR)
    lv1 = db.Column(db.VARCHAR)
    lv2 = db.Column(db.VARCHAR)
    lv3 = db.Column(db.VARCHAR)
    lv4 = db.Column(db.VARCHAR)
    lv5 = db.Column(db.VARCHAR)
    lv6 = db.Column(db.VARCHAR)
    lv7 = db.Column(db.VARCHAR)
    lv8 = db.Column(db.VARCHAR)
    lv9 = db.Column(db.VARCHAR)
    notes = db.Column(db.Text)

class Ability(db.Model):
    __tablename__ = 'abilities'

    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id', ondelete='cascade'), primary_key=True, unique=True)
    strength = db.Column(db.Integer, nullable=False)
    dexterity = db.Column(db.Integer, nullable=False)
    constitution = db.Column(db.Integer, nullable=False)
    intelligence = db.Column(db.Integer, nullable=False)
    wisdom = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # def __repr__(self):
    #     """Show class info"""
        # user = self
        # return f'<Strength: {self.strength}, Dexterity: {self.dexterity}, Constitution: {self.constitution}, Intelligence: {self.intelligence}, Wisdom: {self.wisdom}, Charisma: {self.charisma}>'

class Level(db.Model):
    __tablename__ = 'levels'
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id', ondelete='cascade'), primary_key=True, unique=True)

    Barbarian = db.Column(db.Integer, default=0)
    Bard = db.Column(db.Integer, default=0)
    Cleric = db.Column(db.Integer, default=0)
    Druid = db.Column(db.Integer, default=0)
    Fighter = db.Column(db.Integer, default=0)
    Monk = db.Column(db.Integer, default=0)
    Paladin = db.Column(db.Integer, default=0)
    Ranger = db.Column(db.Integer, default=0)
    Rogue = db.Column(db.Integer, default=0)
    Sorcerer = db.Column(db.Integer, default=0)
    Warlock = db.Column(db.Integer, default=0)
    Wizard = db.Column(db.Integer, default=0)

    def __repr__(self):
        """Show class info"""
        user = self
        # all_classes = ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard']
        # classes = ''
        # for class_ in all_classes:
        #     if self.class_ != 0:
        #         classes += f'{class_} level {self.class_}'
        # return classes
        

        # return f'<Barbarian: {self.barbarian}, Bard: {self.bard}, Cleric: {self.cleric}, Druid: {self.druid}, Fighter: {self.fighter}, Monk: {self.monk}, Paladin: {self.paladin}, Ranger: {self.ranger}, Rogue: {self.rogue}, Sorcerer: {self.sorcerer}, Warlock: {self.warlock}, Wizard: {self.wizard}>'
    
    # @classmethod
    # def classes(cls, player_id):
    #     for col in self:
    #         return col.__dict__

class Proficiency(db.Model):
    __tablename__ = 'proficiencies'

    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id', ondelete='cascade'), primary_key=True, unique=True)

    # ex. ['Short Sword', 'Shield]
    skills = db.Column(db.VARCHAR)
    weapons = db.Column(db.VARCHAR)
    armor = db.Column(db.VARCHAR)
    tools = db.Column(db.VARCHAR)
    languages = db.Column(db.VARCHAR)
    traits = db.Column(db.VARCHAR)
    features = db.Column(db.VARCHAR)
    notes = db.Column(db.Text)

class Items(db.Model):
    __tablename__ = 'items'

    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id', ondelete='cascade'), primary_key=True, unique=True)

    weapons = db.Column(db.VARCHAR)
    armor = db.Column(db.VARCHAR)
    tools = db.Column(db.VARCHAR)
    wallet = db.Column(db.VARCHAR)
    other = db.Column(db.VARCHAR)

    weight = db.Column(db.Integer)
    max_weight = db.Column(db.Integer)
    notes = db.Column(db.Text)

### Campaign Models ###

class Campaign(db.Model):
    __tablename__ = 'campaigns'

    campaign_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='cascade'))

    @classmethod
    def register(cls, password):
        """Register campaign with hashed password and return campaign"""
        hashed = bcrypt.generate_password_hash(password)
        # Turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode('utf8')
        # Return instance of campaign with campaign_id and hashed password
        return cls(password=hashed_utf8)

    @classmethod
    def authenticate(cls, campaign_id, password):
        """
        Validate that campaign exists and password is correct
        Return campaign if valid, else return False
        """
        campaign = Campaign.query.filter_by(campaign_id=campaign_id).first()
        if campaign and bcrypt.check_password_hash(campaign.password, password):
            # Return user instance
            return campaign
        else:
            return False

### User Model ###
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    @classmethod
    def register(cls, username, email, password):
        """Register user with hashed password and return user"""
        hashed = bcrypt.generate_password_hash(password)
        # Turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode('utf8')
        # Return instance of user with username and hashed password
        return cls(username=username, email=email, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, password):
        """
        Validate that user exists and password is correct
        Return user if valid, else return False
        """
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # Return user instance
            return user
        else:
            return False

    def __repr__(self):
        """Show info user"""
        user = self
        return f'<Username: {self.username}, Password: {self.password}, Email: {self.email}>'

