from flask import Flask, render_template, redirect, session, flash, request
from flask_bcrypt import Bcrypt

from models.models import User, Campaign, Player, Demo, Vitals, Combat, Spells, Level, Ability, Proficiency, Items, db, connect_db

from forms.user_forms import RegisterUser, LoginUser, EditUser
from forms.player_forms import PlayerCreate, EditPlayer, EditDemo, EditVitals, EditCombat, EditSpells, EditAbility, EditProficiency, EditItems
from forms.campaign_forms import CreateCampaign, EditCampaign

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dnd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://clrjitnwxwowcq:ba4ed7fb8b6eb0a81c468a91ee53eb4459bf6cec14f5b75f840ea2b2dbc46e8f@ec2-3-211-6-217.compute-1.amazonaws.com:5432/db14nh9pf6snev'

# import os

# database_url = os.environ['DATABASE_URL']

# # fix incorrect database URIs currently returned by Heroku's pg setup
# database_url = database_url.replace('postgres://', 'postgresql://')

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = database_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'key'

bcrypt = Bcrypt()

app.app_context().push()

connect_db(app)

### User Routes ###

@app.route('/')
def home():
    """
    Redirect to user page if logged in
    Redirect to login page if not logged in
    """
    if 'username' in session:
        return redirect(f'/user/{session["username"]}')
    else:
        return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Shows form to add users
    Adds a new user to database
    """
    form = RegisterUser()

    if form.validate_on_submit():
        username = form.username.data
        if User.query.filter(User.username==username).first():
            flash('Username already in use, choose a different username')
            return redirect('/register')

        email = form.email.data
        if User.query.filter(User.email==email).first():
            flash('Email already in use')
            return redirect('/register')

        password = form.password.data

        user = User.register(username, email, password)

        db.session.add(user)
        db.session.commit()

        db.session.refresh(user)
        session['username'] = user.username
        session['user_id'] = user.user_id

        return redirect(f'/user/{user.username}')
    else:
        return render_template('user/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Renders login page (username and password form)
    Redirects to user detail page
    """

    if 'username' and 'user_id' in session:
        return redirect(f'/user/{session["username"]}')

    form = LoginUser()

    if form.validate_on_submit():
        username = form.username.data,
        password = form.password.data

        # Authenticate will return a user or False
        user = User.authenticate(username, password)

        if user:
            # Keep logged in
            session['username'] = user.username
            session['user_id'] = user.user_id
            return redirect(f'/user/{user.username}')
        else:
            form.username.errors = ['Bad username or password']
            return render_template('user/login.html', form=form)

    return render_template('user/login.html', form=form)

@app.route('/user/<username>', methods=['GET', 'POST'])
def show_user(username):
    """
    Redirects to user detail page
    """
    if 'username' in session and session['username'] == username:
        user = User.query.filter(User.username==username).first()
        players = Player.query.filter(Player.user_id==user.user_id).all()
        pc_campaign_ids = set([player.campaign_id for player in players])
        pc_campaigns = [Campaign.query.get(campaign_id) for campaign_id in pc_campaign_ids]

        campaigns = Campaign.query.filter(Campaign.user_id==user.user_id).all()
        return render_template ('/user/details.html', user=user, username=username, players=players, campaigns=campaigns, pc_campaigns=pc_campaigns)
    else:
        flash(f'Not authorized to see details page for "{username}"')
        return redirect('/')

@app.route('/user/<username>/edit', methods=['GET', 'POST'])
def edit_user(username):
    """
    Renders user edit page
    Updates user information in the database
    """
    user = User.query.filter(User.username==username).first()

    if 'username' not in session or  user.username != session['username']:
        flash(f'Not authorized to edit {username}')
        return redirect('/')

    form = EditUser()

    if form.validate_on_submit():
        current_password = form.current_password.data

        # Authenticate will return a user or False
        authorized = User.authenticate(username, current_password)

        if authorized:
            # Permit edits

            new_username = form.new_username.data
            new_email = form.new_email.data
            new_password = form.new_password.data

            hashed = bcrypt.generate_password_hash(new_password)
            # Turn bytestring into normal (unicode utf8) string
            hashed_utf8 = hashed.decode('utf8')

            user.username = new_username
            user.email = new_email
            user.password = hashed_utf8

            db.session.commit()
            
            session['username'] = new_username

            return redirect(f'/user/{user.username}')
        
        else:
            flash('Authentication failed, check password')
            return redirect(f'/user/{username}/edit')
    else:

        form.new_username.data = user.username
        form.new_email.data = user.email

        return render_template('user/edit-user.html', form=form, user=user)


@app.route('/logout')
def logout():
    """
    Clear any information from the session
    Redirect to ('/')
    """
    if 'username' in session:
        session.pop('username')
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/')


### Player Creation Routes ###

@app.route('/player/create', methods=['GET', 'POST'])
def create():
    """
    Shows form to create player
    Adds new player to database
    """
    form = PlayerCreate()

    if form.validate_on_submit():
        user_id = session['user_id']
        campaign_id = form.campaign_id.data
        password = form.password.data

        # Authenticate will return a user or False
        campaign = Campaign.authenticate(campaign_id, password)

        if campaign or campaign_id == None:
            # Permit creation

            name = form.name.data
            party_notes = form.party_notes.data
            player_notes = form.player_notes.data
            dm_notes = form.dm_notes.data
            demo = form.demo.data
            vitals = form.vitals.data
            combat = form.combat.data
            spells = form.spells.data
            ability = form.ability.data
            level = form.level.data
            proficiency = form.proficiency.data
            items = form.items.data

            player = Player(user_id=user_id, name=name, campaign_id=campaign_id, party_notes=party_notes, player_notes=player_notes, dm_notes=dm_notes,demo=demo, vitals=vitals, combat=combat, spells=spells, ability=ability, level=level, proficiency=proficiency, items=items)
            db.session.add(player)
            db.session.commit()

            player_id = player.player_id

            demo = Demo(player_id=player_id, player_level=1, player_xp=0, race='', subrace='', job='', subjob='', alignment='', age=0, size='', notes='')
            db.session.add(demo)

            levels = Level(player_id=player_id, Barbarian=0, Bard=0, Cleric=0, Druid=0, Fighter=0, Monk=0, Paladin=0, Ranger=0, Rogue=0, Sorcerer=0, Warlock=0, Wizard=0)
            db.session.add(levels)

            vitals = Vitals(player_id=player_id, hp=0, max_hp=0, hd=[], conditions=[], notes='')
            db.session.add(vitals)

            combat = Combat(player_id=player_id, attacks=[], ac=0, initiative=0, speed=0, inspiration=0, ki=0, max_ki=0, notes='')
            db.session.add(combat)

            spells = Spells(player_id=player_id, known='', cantrips=[], lv1=[], lv2=[], lv3=[], lv4=[], lv5=[], lv6=[], lv7=[], lv8=[], lv9=[], notes='')
            db.session.add(spells)

            ability = Ability(player_id=player_id, strength=0, dexterity=0, constitution=0, intelligence=0, wisdom=0, charisma=0, notes='')
            db.session.add(ability)

            proficiency = Proficiency(player_id=player_id, skills=[], weapons=[], armor=[], tools=[], languages=[], traits=[], features=[], notes='')
            db.session.add(proficiency)

            items = Items(player_id=player_id, weapons=[], armor=[], tools=[], wallet=[], other=[], weight=0, max_weight=0, notes='')
            db.session.add(items)

            db.session.commit()

            db.session.refresh(player)
            player_id = player.player_id

            return redirect(f'/player/{player_id}')

        else:
            flash('Authentication failed, check password')
            return redirect(f'/player/create')
    else:
        username = session['username']
        return render_template('player/create.html', form=form, username=username)


### Player Edit Routes ###

@app.route('/player/<player_id>/edit/player', methods=['GET', 'POST'])
def edit_player(player_id):
    """
    Verify logged-in user owns player
    Render player edit form and update player
    """
    user_id = Player.query.get(player_id).user_id
    user = User.query.get(user_id).username

    if 'username' not in session or  user != session['username']:
        flash('Not authorized to view this player')
        return redirect('/')
    
    form = EditPlayer()
    player = Player.query.get(player_id)
    current_campaign_id = player.campaign_id

    if form.validate_on_submit():
        campaign_id = form.campaign_id.data
        password = form.password.data

        # Authenticate will return a user or False
        campaign = Campaign.authenticate(campaign_id, password)

        if campaign or campaign_id == None or campaign_id == current_campaign_id:
            # Permit edit

            player.name = form.name.data
            player.party_notes = form.party_notes.data
            player.player_notes = form.player_notes.data
            player.dm_notes = form.dm_notes.data
            player.demo = form.demo.data
            player.vitals = form.vitals.data
            player.combat = form.combat.data
            player.spells = form.spells.data
            player.ability = form.ability.data
            player.level = form.level.data
            player.proficiency = form.proficiency.data
            player.items = form.items.data

            if campaign_id != None:
                player.campaign_id = campaign_id
            else:
                player.campaign_id = None

            db.session.commit()

            return redirect(f'/player/{player_id}')
        
        else:
            flash('Campaign authentication failed, check password')
            return redirect(f'/player/{player_id}/edit/player')

    else:
        form.campaign_id.data = player.campaign_id
        form.name.data = player.name
        form.party_notes.data = player.party_notes
        form.player_notes.data = player.player_notes
        form.dm_notes.data = player.dm_notes
        form.demo.data = player.demo
        form.vitals.data = player.vitals
        form.combat.data = player.combat
        form.spells.data = player.spells
        form.ability.data = player.ability
        form.level.data = player.level
        form.proficiency.data = player.proficiency
        form.items.data = player.items

        return render_template('/player/edit-player.html', form=form, player_id=player_id, player=player)

@app.route('/player/<player_id>/edit/demo', methods=['GET', 'POST'])
def edit_demo(player_id):
    """
    Verify logged-in user owns player
    Render demo edit form and update player demo
    """
    user_id = Player.query.get(player_id).user_id
    user = User.query.get(user_id).username

    if 'username' not in session or  user != session['username']:
        flash('Not authorized to view this player')
        return redirect('/')

    form = EditDemo()
    player = Player.query.get(player_id)
    demo = Demo.query.get(player_id)
    level = Level.query.get(player_id)
    player_id = player.player_id

    if form.validate_on_submit():
        
        player.name = form.name.data

        demo.player_level = form.player_level.data
        demo.player_xp = form.player_xp.data
        demo.race = form.race.data
        demo.subrace = form.subrace.data
        demo.job = form.job.data
        demo.subjob = form.subjob.data
        demo.age = form.age.data
        demo.alignment = form.alignment.data
        demo.notes = form.notes.data

        level.Barbarian = form.barbarian.data
        level.Bard = form.bard.data
        level.Cleric = form.cleric.data
        level.Druid = form.druid.data
        level.Fighter = form.fighter.data
        level.Monk = form.monk.data
        level.Paladin = form.paladin.data
        level.Ranger = form.ranger.data
        level.Rogue = form.rogue.data
        level.Sorcerer = form.sorcerer.data
        level.Warlock = form.warlock.data
        level.Wizard = form.wizard.data

        db.session.commit()

        return redirect(f'/player/{player_id}')

    else:
        form.name.data = player.name

        form.player_level.data = demo.player_level
        form.player_xp.data = demo.player_xp
        form.race.data = demo.race
        form.subrace.data = demo.subrace
        form.job.data = demo.job
        form.subjob.data = demo.subjob
        form.age.data = demo.age
        form.alignment.data = demo.alignment
        form.notes.data = demo.notes

        form.barbarian.data = level.Barbarian
        form.bard.data = level.Bard
        form.cleric.data = level.Cleric
        form.druid.data = level.Druid
        form.fighter.data = level.Fighter
        form.monk.data = level.Monk
        form.paladin.data = level.Paladin
        form.ranger.data = level.Ranger
        form.rogue.data = level.Rogue
        form.sorcerer.data = level.Sorcerer
        form.warlock.data = level.Warlock
        form.wizard.data = level.Wizard
        return render_template('/player/edit-demo.html', form=form, player_id=player_id)

@app.route('/player/<player_id>/edit/vitals', methods=['GET', 'POST'])
def edit_vitals(player_id):
    """
    Verify logged-in user owns player
    Render vitals edit form and update player vitals
    """
    user_id = Player.query.get(player_id).user_id
    user = User.query.get(user_id).username

    if 'username' not in session or  user != session['username']:
        flash('Not authorized to view this player')
        return redirect('/')

    form = EditVitals()
    vitals = Vitals.query.get(player_id)

    if form.validate_on_submit():
        vitals.hp = form.hp.data
        vitals.max_hp = form.max_hp.data
        vitals.hd = form.hd.data
        vitals.conditions = form.conditions.data
        vitals.notes = form.notes.data

        db.session.commit()

        return redirect(f'/player/{player_id}')
    
    else:
        form.hp.data = vitals.hp
        form.max_hp.data = vitals.max_hp
        form.hd.data = vitals.hd
        form.conditions.data = vitals.conditions
        form.notes.data = vitals.notes

        conditions = eval(vitals.conditions)
        hd = eval(vitals.hd)
        return render_template('/player/edit-vitals.html', form=form, player_id=player_id, vitals=vitals, conditions=conditions, hd=hd)

@app.route('/player/<player_id>/edit/combat', methods=['GET', 'POST'])
def edit_combat(player_id):
    """
    Verify logged-in user owns player
    Render combat edit form and update player combat
    """
    user_id = Player.query.get(player_id).user_id
    user = User.query.get(user_id).username

    if 'username' not in session or  user != session['username']:
        flash('Not authorized to view this player')
        return redirect('/')

    form = EditCombat()
    combat = Combat.query.get(player_id)
    attacks = eval(combat.attacks)
    weapons = eval(Items.query.get(player_id).weapons)

    if form.validate_on_submit():
        combat.attacks = form.attacks.data
        combat.ac = form.ac.data
        combat.inititative = form.initiative.data
        combat.speed = form.speed.data
        combat.inspiration = form.inspiration.data
        combat.ki = form.ki.data
        combat.max_ki = form.max_ki.data
        combat.notes = form.notes.data

        db.session.commit()

        return redirect(f'/player/{player_id}')
    
    else:
        form.attacks.data = combat.attacks
        form.ac.data = combat.ac
        form.initiative.data = combat.initiative
        form.speed.data = combat.speed
        form.inspiration.data = combat.inspiration
        form.ki.data = combat.ki
        form.max_ki.data = combat.max_ki
        form.notes.data = combat.notes

        return render_template('/player/edit-combat.html', form=form, player_id=player_id, attacks=attacks, weapons=weapons)

@app.route('/player/<player_id>/edit/spells', methods=['GET', 'POST'])
def edit_spells(player_id):
    """
    Verify logged-in user owns player
    Render spells edit form and update player spells
    """
    user_id = Player.query.get(player_id).user_id
    user = User.query.get(user_id).username

    if 'username' not in session or  user != session['username']:
        flash('Not authorized to view this player')
        return redirect('/')

    form = EditSpells()
    spells = Spells.query.get(player_id)
    known_spells = []
    if spells.known:
        known_spells = eval(spells.known)
    available = [spells.cantrips, spells.lv1, spells.lv2, spells.lv3, spells.lv4, spells.lv5, spells.lv6, spells.lv7, spells.lv8, spells.lv9]

    available_spells = []
    for spell in available:
        if spell:
            available_spells.append(eval(spell))
        else:
            available_spells.append(())

    if form.validate_on_submit():
        spells.known = form.known.data
        spells.cantrips = form.lv0.data
        spells.lv1 = form.lv1.data
        spells.lv2 = form.lv2.data
        spells.lv3 = form.lv3.data
        spells.lv4 = form.lv4.data
        spells.lv5 = form.lv5.data
        spells.lv6 = form.lv6.data
        spells.lv7 = form.lv7.data
        spells.lv8 = form.lv8.data
        spells.lv9 = form.lv9.data
        spells.notes = form.notes.data
    
        db.session.commit()

        return redirect(f'/player/{player_id}')

    else:
        form.known.data = spells.known
        form.lv0.data = spells.cantrips
        form.lv1.data = spells.lv1
        form.lv2.data = spells.lv2
        form.lv3.data = spells.lv3
        form.lv4.data = spells.lv4
        form.lv5.data = spells.lv5
        form.lv6.data = spells.lv6
        form.lv7.data = spells.lv7
        form.lv8.data = spells.lv8
        form.lv9.data = spells.lv9
        form.notes.data = spells.notes

        return render_template('/player/edit-spells.html', form=form, player_id=player_id, known_spells=known_spells, available_spells=available_spells)

@app.route('/player/<player_id>/edit/ability', methods=['GET', 'POST'])
def edit_ability(player_id):
    """
    Verify logged-in user owns player
    Render ability edit form and update player ability
    """
    user_id = Player.query.get(player_id).user_id
    user = User.query.get(user_id).username

    if 'username' not in session or  user != session['username']:
        flash('Not authorized to view this player')
        return redirect('/')


    form = EditAbility()
    ability = Ability.query.get(player_id)

    if form.validate_on_submit():
        ability.strength = form.strength.data
        ability.dexterity = form.dexterity.data
        ability.constitution = form.constitution.data
        ability.intelligence = form.intelligence.data
        ability.wisdom = form.wisdom.data
        ability.charisma = form.charisma.data
        ability.notes = form.notes.data

        db.session.commit()

        return redirect(f'/player/{player_id}')
    
    else:
        form.strength.data = ability.strength
        form.dexterity.data = ability.dexterity
        form.constitution.data = ability.constitution
        form.intelligence.data = ability.intelligence
        form.wisdom.data = ability.wisdom
        form.charisma.data = ability.charisma
        form.notes.data = ability.notes

        return render_template('/player/edit-ability.html', form=form, player_id=player_id)

@app.route('/player/<player_id>/edit/proficiency', methods=['GET', 'POST'])
def edit_proficiency(player_id):
    """
    Verify logged-in user owns player
    Render proficiency edit form and update player proficiency
    """
    user_id = Player.query.get(player_id).user_id
    user = User.query.get(user_id).username

    if 'username' not in session or  user != session['username']:
        flash('Not authorized to view this player')
        return redirect('/')

    form = EditProficiency()
    proficiency = Proficiency.query.get(player_id)

    proficiency_list = [proficiency.skills, proficiency.weapons, proficiency.armor, proficiency.tools, proficiency.languages, proficiency.traits, proficiency.features]
    proficiencies = []

    for prof in proficiency_list:
        if prof:
            proficiencies.append(eval(prof))
        else:
            proficiencies.append(())

    if form.validate_on_submit():
        proficiency.skills = form.skills.data
        proficiency.weapons = form.weapons.data
        proficiency.armor = form.armor.data
        proficiency.tools = form.tools.data
        proficiency.languages = form.languages.data
        proficiency.traits = form.traits.data
        proficiency.features = form.features.data
        proficiency.notes = form.notes.data

        db.session.commit()

        return redirect(f'/player/{player_id}')
    
    else:
        form.skills.data = proficiency.skills
        form.weapons.data = proficiency.weapons
        form.armor.data = proficiency.armor
        form.tools.data = proficiency.tools
        form.languages.data = proficiency.languages
        form.traits.data = proficiency.traits
        form.features.data = proficiency.features
        form.notes.data = proficiency.notes

        return render_template('/player/edit-proficiency.html', form=form, player_id=player_id, proficiencies=proficiencies)

@app.route('/player/<player_id>/edit/items', methods=['GET', 'POST'])
def edit_items(player_id):
    """
    Verify logged-in user owns player
    Render items edit form and update player items
    """
    user_id = Player.query.get(player_id).user_id
    user = User.query.get(user_id).username

    if 'username' not in session or  user != session['username']:
        flash('Not authorized to view this player')
        return redirect('/')

    form = EditItems()
    items = Items.query.get(player_id)
    weapons = []
    if items.weapons:
        weapons = eval(items.weapons)
    armor = []
    if items.armor:
        armor = eval(items.armor)
    tools = []
    if items.tools:
        tools = eval(items.tools)
    if items.wallet:
        wallet = eval(items.wallet)
    other = []
    if items.other:
        other = eval(items.other)

    if form.validate_on_submit():
        items.weapons = form.weapons.data
        items.armor = form.armor.data
        items.tools = form.tools.data
        items.wallet = form.wallet.data
        items.other = form.other.data
        items.weight = form.weight.data
        items.max_weight = form.max_weight.data
        items.notes = form.notes.data

        db.session.commit()

        return redirect(f'/player/{player_id}')
    
    else:
        form.weapons.data = items.weapons
        form.armor.data = items.armor
        form.tools.data = items.tools
        form.wallet.data = items.wallet
        form.other.data = items.other
        form.weight.data = items.weight
        form.max_weight.data = items.max_weight
        form.notes.data = items.notes

        return render_template('/player/edit-items.html', form=form, player_id=player_id, weapons=weapons, armor=armor, tools=tools, wallet=wallet, other=other)

### Player Routes ###

@app.route('/player/<player_id>')
def player_detail(player_id):
    """
    Verify logged-in user owns player
    Render player details page
    """

    player = Player.query.get(player_id)

    if player == None:
        flash('Not authorized to view this player')
        return redirect('/')
    
    user_id = Player.query.get(player_id).user_id
    user = User.query.get(user_id)
    username = user.username

    if 'username' not in session or username != session['username']:
            flash('Not authorized to view this player')
            return redirect('/')
    
    demo = Demo.query.get(player_id)

    levels = Level.query.get(player_id)
    classes = {'Barbarian': levels.Barbarian, 'Bard':levels.Bard, 'Cleric':levels.Cleric, 'Druid':levels.Druid, 'Fighter':levels.Fighter, 'Monk':levels.Monk, 'Paladin':levels.Paladin, 'Ranger':levels.Ranger, 'Rogue':levels.Rogue, 'Sorcerer':levels.Sorcerer, 'Warlock':levels.Warlock, 'Wizard':levels.Wizard}

    vitals = Vitals.query.get(player_id)
    hd = eval(vitals.hd)
    conditions = eval(vitals.conditions)

    combat = Combat.query.get(player_id)
    attacks = eval(combat.attacks)

    spells = Spells.query.get(player_id)
    spells_notes = spells.notes

    known_spells = []
    if spells.known:
        known_spells = eval(spells.known)
    
    available = [spells.cantrips, spells.lv1, spells.lv2, spells.lv3, spells.lv4, spells.lv5, spells.lv6, spells.lv7, spells.lv8, spells.lv9]

    available_spells = []
    for spells in available:
        if spells:
            available_spells.append(eval(spells))
        else:
            available_spells.append(())

    ability = Ability.query.get(player_id)

    level = Level.query.get(player_id)

    proficiency = Proficiency.query.get(player_id)
    proficiency_list = [proficiency.skills, proficiency.weapons, proficiency.armor, proficiency.tools, proficiency.languages, proficiency.traits, proficiency.features]
    proficiencies = []
    for prof in proficiency_list:
        if prof:
            proficiencies.append(eval(prof))
        else:
            proficiencies.append(())

    items_object = Items.query.get(player_id)
    items_list = [items_object.weapons, items_object.armor, items_object.tools, items_object.wallet, items_object.other]
    items = []
    for item in items_list:
        if item:
            items.append(eval(item))
        else:
            items.append(())

    return render_template('player/details.html', player=player, username=username, user=user, demo=demo, vitals=vitals, hd=hd, conditions=conditions, combat=combat, attacks=attacks, known_spells=known_spells, available_spells=available_spells, ability=ability, level=level, proficiencies=proficiencies,    items_object=items_object, items=items, spells=spells, proficiency=proficiency, classes=classes, spells_notes=spells_notes)


### Campaign Routes ###

@app.route('/<username>/campaign/create', methods=['GET', 'POST'])
def create_campaign(username):
    """
    Shows form to create campaign
    Adds a new campaign to database
    """
    form = CreateCampaign()
    user_id = User.query.filter(User.username==username).first().user_id

    if 'username' not in session or  username != session['username']:
        flash(f'Not authorized to create a campaign for {username}')
        return redirect('/')
    
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        password = form.password.data
        
        campaign = Campaign.register(password)
        campaign.user_id = user_id
        campaign.name = name
        campaign.description = description


        db.session.add(campaign)
        db.session.commit()

        db.session.refresh(campaign)

        return redirect(f'/campaign/{campaign.campaign_id}')
    else:
        return render_template('campaign/create.html', form=form, username=username)

@app.route('/campaign/<campaign_id>')
def dm_campaign_view(campaign_id):
    """
    Verify logged-in user owns campaign
    Render campaign page (DM view)
    """
    campaign = Campaign.query.get(campaign_id)
    dm = User.query.get(campaign.user_id).username
    players = Player.query.filter(Player.campaign_id==campaign_id).all()

    if 'username' not in session or dm != session['username']:
        flash('Not authorized to view this campaign as dungeon master')
        return redirect('/')

    return render_template('/campaign/detail.html', dm=dm, players=players, campaign=campaign)

@app.route('/campaign/<campaign_id>/edit', methods=['GET', 'POST'])
def edit_campaign(campaign_id):
    """
    Shows form to edit campaign
    Updates campaign in database
    """
    form = EditCampaign()
    campaign = Campaign.query.get(campaign_id)
    username = User.query.get(campaign.user_id).username

    if 'username' not in session or  username != session['username']:
        flash(f'Not authorized to edit this campaign as DM')
        return redirect('/')
    
    if form.validate_on_submit():
        campaign.name = form.name.data
        campaign.description = form.description.data

        db.session.commit()

        return redirect(f'/campaign/{campaign.campaign_id}')
    else:
        form.name.data = campaign.name
        form.description.data = campaign.description
        return render_template('campaign/edit-campaign.html', form=form, username=username, campaign=campaign)

@app.route('/campaign/<campaign_id>/party')
def party_campaign_view(campaign_id):
    """
    Verify logged-in user owns campaign
    Render campaign page (PC view)
    """

    campaign = Campaign.query.get(campaign_id)
    dm = User.query.get(campaign.user_id).username
    user_id = User.query.filter(User.username==session['username']).first().user_id
    players = Player.query.filter(Player.campaign_id==campaign_id).all()
    user_ids = [player.user_id for player in players]

    if 'username' not in session or user_id not in user_ids: 
        flash('Not authorized to view this campaign as party member')
        return redirect('/')

    return render_template('/campaign/party_detail.html', players=players, campaign=campaign, username=session['username'], dm=dm)


@app.route('/campaign/<campaign_id>/player/<player_id>')
def dm_player_view(campaign_id, player_id):
    """
    Verify logged-in user owns campaign
    Render player detail page (DM view)
    """
    campaign = Campaign.query.get(campaign_id)
    dm = User.query.get(campaign.user_id)
    player = Player.query.get(player_id)

    if 'username' not in session or dm.username != session['username']:
        flash('Not authorized to view this player as dungeon master')
        return redirect('/')

    if int(campaign_id) != player.campaign_id:
        flash("Player is not in this campaign's party")
        return redirect('/')

    demo = Demo.query.get(player_id)

    levels = Level.query.get(player_id)
    classes = {'Barbarian': levels.Barbarian, 'Bard':levels.Bard, 'Cleric':levels.Cleric, 'Druid':levels.Druid, 'Fighter':levels.Fighter, 'Monk':levels.Monk, 'Paladin':levels.Paladin, 'Ranger':levels.Ranger, 'Rogue':levels.Rogue, 'Sorcerer':levels.Sorcerer, 'Warlock':levels.Warlock, 'Wizard':levels.Wizard}

    vitals = Vitals.query.get(player_id)
    hd = eval(vitals.hd)
    conditions = eval(vitals.conditions)

    combat = Combat.query.get(player_id)
    attacks = eval(combat.attacks)

    spells = Spells.query.get(player_id)
    spells_notes = spells.notes

    known_spells = []
    if spells.known:
        known_spells = eval(spells.known)
    
    available = [spells.cantrips, spells.lv1, spells.lv2, spells.lv3, spells.lv4, spells.lv5, spells.lv6, spells.lv7, spells.lv8, spells.lv9]

    available_spells = []
    for spells in available:
        if spells:
            available_spells.append(eval(spells))
        else:
            available_spells.append(())

    ability = Ability.query.get(player_id)

    level = Level.query.get(player_id)

    proficiency = Proficiency.query.get(player_id)
    proficiency_list = [proficiency.skills, proficiency.weapons, proficiency.armor, proficiency.tools, proficiency.languages, proficiency.traits, proficiency.features]
    proficiencies = []
    for prof in proficiency_list:
        if prof:
            proficiencies.append(eval(prof))
        else:
            proficiencies.append(())

    items_object = Items.query.get(player_id)
    items_list = [items_object.weapons, items_object.armor, items_object.tools, items_object.wallet, items_object.other]
    items = []
    for item in items_list:
        if item:
            items.append(eval(item))
        else:
            items.append(())

    return render_template('/campaign/dm_player_view.html', campaign=campaign, player=player, demo=demo, vitals=vitals, hd=hd, conditions=conditions, combat=combat, attacks=attacks, known_spells=known_spells, available_spells=available_spells, ability=ability, level=level, proficiencies=proficiencies, items_object=items_object, items=items, spells=spells, proficiency=proficiency, classes=classes, spells_notes=spells_notes)

@app.route('/campaign/<campaign_id>/party/<player_id>')
def party_player_view(campaign_id, player_id):
    """
    Verify logged-in user is a party member in campaign
    Render campaign page (PC view)
    """

    if 'username' not in session:
        flash('Not authorized to view this player as party member')
        return redirect('/')

    user = User.query.filter(User.username==session['username']).first()

    campaign = Campaign.query.get(campaign_id)

    player = Player.query.get(player_id)
    demo = Demo.query.get(player_id)

    players = Player.query.filter(Player.campaign_id==campaign_id).all()
    users = [pc.user_id for pc in players]

    if user.user_id not in users:
        flash('Not authorized to view this player as party member')
        return redirect('/')

    if int(campaign_id) != player.campaign_id:
        flash("Player is not in this campaign's party")
        return redirect('/')
    
    # levels = Level.query.get(player_id)
    # classes = {'Barbarian': levels.Barbarian, 'Bard':levels.Bard, 'Cleric':levels.Cleric, 'Druid':levels.Druid, 'Fighter':levels.Fighter, 'Monk':levels.Monk, 'Paladin':levels.Paladin, 'Ranger':levels.Ranger, 'Rogue':levels.Rogue, 'Sorcerer':levels.Sorcerer, 'Warlock':levels.Warlock, 'Wizard':levels.Wizard}

    demo = Demo.query.get(player_id)

    levels = Level.query.get(player_id)
    classes = {'Barbarian': levels.Barbarian, 'Bard':levels.Bard, 'Cleric':levels.Cleric, 'Druid':levels.Druid, 'Fighter':levels.Fighter, 'Monk':levels.Monk, 'Paladin':levels.Paladin, 'Ranger':levels.Ranger, 'Rogue':levels.Rogue, 'Sorcerer':levels.Sorcerer, 'Warlock':levels.Warlock, 'Wizard':levels.Wizard}

    vitals = Vitals.query.get(player_id)
    hd = eval(vitals.hd)
    conditions = eval(vitals.conditions)

    combat = Combat.query.get(player_id)
    attacks = eval(combat.attacks)

    spells = Spells.query.get(player_id)
    spells_notes = spells.notes

    known_spells = []
    if spells.known:
        known_spells = eval(spells.known)
    
    available = [spells.cantrips, spells.lv1, spells.lv2, spells.lv3, spells.lv4, spells.lv5, spells.lv6, spells.lv7, spells.lv8, spells.lv9]

    available_spells = []
    for spells in available:
        if spells:
            available_spells.append(eval(spells))
        else:
            available_spells.append(())

    ability = Ability.query.get(player_id)

    level = Level.query.get(player_id)

    proficiency = Proficiency.query.get(player_id)
    proficiency_list = [proficiency.skills, proficiency.weapons, proficiency.armor, proficiency.tools, proficiency.languages, proficiency.traits, proficiency.features]
    proficiencies = []
    for prof in proficiency_list:
        if prof:
            proficiencies.append(eval(prof))
        else:
            proficiencies.append(())

    items_object = Items.query.get(player_id)
    items_list = [items_object.weapons, items_object.armor, items_object.tools, items_object.wallet, items_object.other]
    items = []
    for item in items_list:
        if item:
            items.append(eval(item))
        else:
            items.append(())

    return render_template('/campaign/party_player_view.html', campaign=campaign, player=player, demo=demo, vitals=vitals, hd=hd, conditions=conditions, combat=combat, attacks=attacks, known_spells=known_spells, available_spells=available_spells, ability=ability, level=level, proficiencies=proficiencies, items_object=items_object, items=items, spells=spells, proficiency=proficiency, classes=classes, spells_notes=spells_notes)