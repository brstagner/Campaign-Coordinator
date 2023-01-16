from models.models import User, Campaign, Player, Demo, Vitals, Combat, Spells, Level, Ability, Proficiency, Items, db, connect_db

db.drop_all()
db.create_all()

user = User.register('user', 'user@user.com', 'password')
db.session.add(user)
db.session.commit()

campaign = Campaign(user_id=1, name='Cat Attack', description='My cats like to bite, this is about them doing that')
db.session.add(campaign)
db.session.commit()

player = Player(user_id=1, name='Spike Wallscratcher', campaign_id=1)
db.session.add(player)
db.session.commit()

demo = Demo(player_id=1, player_xp=0, player_level=1, race='Half-Elf', subrace='Quarter-Elf', job='Cat', subjob='Mouser', alignment='Chaotic Neutral', age=100, size='Small', notes='Demo Notes')
db.session.add(demo)

vitals = Vitals(player_id=1, hp=10, max_hp=10, hd="[(3, '1d8'), (2, '1d6')]", conditions="['Paralyzed', 'Blind']", notes='Vitals Notes')
db.session.add(vitals)

combat = Combat(player_id=1, attacks="[('Short Sword', '1d6', 2), ('Dragon Breath', '2d6', 1)]", ac=1, initiative=10, speed=50, inspiration=3, ki=1, max_ki=5, notes='Combat Notes')
db.session.add(combat)

spells = Spells(player_id=1, known="['Magic Missile', 'Light']", cantrips="[('Magic Missile', 2), ('Light', 1)]", lv2="[('Spell 3', 7), ('Spell 4', 8)]", notes='Spells Notes')
db.session.add(spells)

ability = Ability(player_id=1, strength=5, dexterity=20, constitution=10, intelligence=13, wisdom=3, charisma=50, notes='Ability Notes')
db.session.add(ability)

levels = Level(player_id=1, Barbarian=1)
db.session.add(levels)

proficiency = Proficiency(player_id=1, weapons="['Short Sword', 'Shield']", notes='Proficiency Notes')
db.session.add(proficiency)

items = Items(player_id=1, weapons="['Short Sword', 'Shield']", wallet="[('Silver', 2), ('Gold', 3)]", weight=5, max_weight=10, notes='Items Notes')
db.session.add(items)

db.session.commit()