// Populate skills datalist
const skills_datalist = document.querySelector('#skills_datalist');

async function getSkills () {
    let response = await axios.get(`https://www.dnd5eapi.co/api/skills`);
    let skills = response.data.results;
    for (let skill of skills) {
        let option = document.createElement('option');
        option.setAttribute('value', `${skill.name}`);
        // option.innerText = `${skill.name}`;
        skills_datalist.append(option);
    };
};

getSkills();

// Populate weapon proficiency datalist
const all_weapons = ["Battleaxes", "Blowguns", "Clubs",
    "Crossbows, Heavy", "Crossbows, Light", "Daggers", "Darts",
    "Flails", "Glaives", "Greataxes", "Greatclubs", "Greatswords",
    "Halberds", "Hand Crossbows", "Handaxes", "Javelins", "Lances",
    "Light Hammers", "Longbows", "Longswords", "Maces", "Martial-weapons",
    "Mauls", "Morningstars", "Nets", "Pikes", "Quarterstaffs", "Rapiers",
    "Scimitars", "Shortbows", "Shortswords", "Sickles",
    "Simple Weapons", "Slings", "Spears", "Tridents", "War Picks",
    "Warhammers", "Whips"];

const weapons_datalist = document.querySelector('#weapons_datalist');

for (let skill of all_weapons) {
    let option = document.createElement('option');
    option.value = skill;
    weapons_datalist.append(option);
};

// Populate armor proficiency datalist
const all_armor = ["All Armor", "Breastplate", "Chain Mail", "Chain Shirt",
    "Half Plate Armor", "Heavy Armor", "Hide Armor", "Leather Armor",
    "Light Armor", "Medium Armor", "Padded Armor", "Plate Armor",
    "Ring Mail", "Scale Mail", "Shields", "Splint Armor", "Studded Leather Armor"];

const armor_datalist = document.querySelector('#armor_datalist');

for (let skill of all_armor) {
    let option = document.createElement('option');
    option.value = skill;
    armor_datalist.append(option);
};

// Populate tool proficiency datalist
const all_tools = ["Alchemist's Supplies", "Bagpipes", "Brewer's Supplies",
    "Caligrapher's Supplies", "Carpenter's Tools", "Cartographer's Tools",
    "Cobbler's Tools", "Cook's Utensils", "Dice Set", "Disguise Kit",
    "Drum", "Dulcimer", "Flute", "Forgery Kit", "Glassblower's Tools",
    "Herbalism Kit", "Horn", "Jewler's Tools", "Land Vehicles",
    "Leatherworker's Tools", "Lute", "Lyre", "Mason's Tools",
    "Navigator's Tools", "Painter's Supplies", "Pan Flute",
    "Playing Card Set", "Poisoner's-kit", "Potter's Tools", "Shawm",
    "Smith's Tools", "Theive's Tools", "Tinker's Tools", "Viol",
    "Water Vehicles", "Weaver's Tools", "Woodcarver's Tools"];

const tools_datalist = document.querySelector('#tools_datalist');

for (let skill of all_tools) {
    let option = document.createElement('option');
    option.value = skill;
    tools_datalist.append(option);
};

// Populate languages datalist
const languages_datalist = document.querySelector('#languages_datalist');

async function getLanguages () {
    let response = await axios.get(`https://www.dnd5eapi.co/api/languages`);
    let languages = response.data.results;
    for (let language of languages) {
        let option = document.createElement('option');
        option.setAttribute('value', `${language.name}`);
        // option.innerText = `${skill.name}`;
        languages_datalist.append(option);
    };
};

getLanguages();

// Populate traits datalist
const traits_datalist = document.querySelector('#traits_datalist');

async function getTraits () {
    let response = await axios.get(`https://www.dnd5eapi.co/api/traits`);
    let traits = response.data.results;
    for (let trait of traits) {
        let option = document.createElement('option');
        option.setAttribute('value', `${trait.name}`);
        // option.innerText = `${skill.name}`;
        traits_datalist.append(option);
    };
};

getTraits();

// Populate features datalist
const features_datalist = document.querySelector('#features_datalist');

async function getFeatures () {
    let response = await axios.get(`https://www.dnd5eapi.co/api/features`);
    let features = response.data.results;
    for (let feature of features) {
        let option = document.createElement('option');
        option.setAttribute('value', `${feature.name}`);
        // option.innerText = `${skill.name}`;
        features_datalist.append(option);
    };
};

getFeatures();

const inputs = document.querySelector('#inputs');

inputs.addEventListener('click', function (e) {
    e.preventDefault();
    if (e.target.classList.contains('delete')) {
        e.target.parentElement.remove();
    };
    if (e.target.classList.contains('add')) {
        let new_proficiency = document.createElement('div');
        e.target.parentElement.append(new_proficiency);

        let new_proficiency_name = document.createElement('input');
        new_proficiency_name.classList.add(`${e.target.parentElement.dataset.class}`);
        new_proficiency_name.setAttribute('list', `${e.target.parentElement.dataset.list}`);
        new_proficiency.append(new_proficiency_name);

        let delete_button = document.createElement('button');
        delete_button.classList.add('delete');
        delete_button.innerText = 'Delete';
        new_proficiency.append(delete_button);
    };
});

function fillInputs (type, input) {
    let proficiency_list = [];
    let proficiencies = document.getElementsByClassName(`${type}`);
    for (let proficiency of proficiencies) {
        proficiency_list.push(proficiency.value)
    };
    document.querySelector(`#${input}`).value = JSON.stringify(proficiency_list);
};

const submit = document.querySelector('#submit');
submit.addEventListener('click', function (e) {
    // e.preventDefault();

    fillInputs('skill', 'skills');
    fillInputs('weapon', 'weapons');
    fillInputs('armor', 'armor');
    fillInputs('tool', 'tools');
    fillInputs('language', 'languages');
    fillInputs('trait', 'traits');
    fillInputs('feature', 'features');
});