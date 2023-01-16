from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, URLField, TextAreaField, IntegerField, SelectField, RadioField, SelectMultipleField, widgets, BooleanField
from wtforms.validators import InputRequired, Optional, AnyOf, URL, NumberRange

class PlayerCreate(FlaskForm):
    """
    Model for form object with all fields for adding new users to database
    """
    campaign_id = IntegerField('Campaign ID #', validators=[Optional()])
    password = PasswordField('Campaign Password (required if selecting a campaign)')
    name = StringField('Player Name (required)', validators=[InputRequired(message='Name cannot be blank')])
    story = TextAreaField('Player Backstory (visible to DM)')
    public = TextAreaField('PC Public Information (visible to party members)')

class EditPlayer(FlaskForm):
    name = StringField('Name', validators=[InputRequired(message='Name cannot be blank')])
    story = TextAreaField('Player Backstory (visible to DM)')
    public = TextAreaField('PC Public Information (visible to party members)')
    campaign_id = IntegerField('Campaign ID #', validators=[Optional()])
    password = PasswordField('Campaign Password (required if selecting a new campaign)')

class EditDemo(FlaskForm):
    name = StringField('Name')
    player_level = IntegerField('Player Level')
    player_xp = IntegerField('Player XP')
    race = StringField('Race')
    subrace = StringField('Subrace')
    job = StringField('Job')
    subjob = StringField('Subjob')
    age = IntegerField('Age')
    alignment = StringField('Alignment')

    barbarian = IntegerField('Barbarian')
    bard = IntegerField('Bard')
    cleric = IntegerField('Cleric')
    druid = IntegerField('Druid')
    fighter = IntegerField('Fighter')
    monk = IntegerField('Monk')
    paladin = IntegerField('Paladin')
    ranger = IntegerField('Ranger')
    rogue = IntegerField('Rogue')
    sorcerer = IntegerField('Sorcerer')
    warlock = IntegerField('Warlock')
    wizard = IntegerField('Wizard')

    notes = TextAreaField('Notes')

class EditVitals(FlaskForm):
    hp = IntegerField('HP')
    max_hp = IntegerField('Max HP')
    hd = StringField('HD')
    conditions = StringField('Conditions')
    notes = TextAreaField('Vitals Notes')

class EditCombat(FlaskForm):
    attacks = StringField('Attacks')
    ac = IntegerField('AC')
    initiative = IntegerField('Initiative')
    speed = IntegerField('Speed')
    inspiration = IntegerField('Inspiration')
    ki = IntegerField('Ki')
    max_ki = IntegerField('Max Ki')
    notes = TextAreaField('Combat Notes')

class EditSpells(FlaskForm):
    known = StringField('Known Spells')
    lv0 = StringField('Level 0')
    lv1 = StringField('Level 1')
    lv2 = StringField('Level 2')
    lv3 = StringField('Level 3')
    lv4 = StringField('Level 4')
    lv5 = StringField('Level 5')
    lv6 = StringField('Level 6')
    lv7 = StringField('Level 7')
    lv8 = StringField('Level 8')
    lv9 = StringField('Level 9')
    notes = TextAreaField('Spell Notes')

class EditAbility(FlaskForm):
    strength = IntegerField('Strength')
    dexterity = IntegerField('Dexterity')
    constitution = IntegerField('Constitution')
    intelligence = IntegerField('Intelligence')
    wisdom = IntegerField('Wisdom')
    charisma = IntegerField('Charisma')
    notes = TextAreaField('Ability Notes')

class EditProficiency(FlaskForm):
    skills = StringField('Skills')
    weapons = StringField('Weapons')
    armor = StringField('Armor')
    tools = StringField('Tools')
    languages = StringField('Lanuages')
    traits = StringField('Traits')
    features = StringField('Features')
    notes = TextAreaField('Proficiency Notes')

class EditItems(FlaskForm):
    weapons = StringField('Weapons')
    armor = StringField('Armor')
    tools = StringField('Tools')
    wallet = StringField('Wallet')
    other = StringField('Other')
    weight = IntegerField('Weight', default=0)
    max_weight = IntegerField('Max Weight', default=0)
    notes = TextAreaField('Items Notes')

