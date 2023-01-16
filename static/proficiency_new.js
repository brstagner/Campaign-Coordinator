// These array/set pairs categorize proficiencies which are not differentiated by the API
const all_skills = ['skill-acrobatics', 'skill-animal-handling', 'skill-arcana', 'skill-athletics', 'skill-deception', 'skill-history', 'skill-insight', 'skill-intimidation', 'skill-investigation', 'skill-medicine', 'skill-nature', 'skill-perception', 'skill-performance', 'skill-persuasion', 'skill-religion', 'skill-sleight-of-hand', 'skill-stealth', 'skill-survival'];

const skills = new Set();

const all_wp = ['battleaxes', 'blowguns', 'clubs', 'crossbows-heavy', 'crossbows-light', 'daggers', 'darts', 'flails', 'glaives', 'greataxes', 'greatclubs', 'greatswords', 'halberds', 'hand-crossbows', 'handaxes', 'javelins', 'lances', 'light-hammers', 'longbows', 'longswords', 'maces', 'martial-weapons', 'mauls', 'morningstars', 'nets', 'pikes', 'quarterstaffs', 'rapiers', 'scimitars', 'shields', 'shortbows', 'shortswords', 'sickles', 'simple-weapons', 'slings', 'spears', 'tridents', 'war-picks', 'warhammers', 'whips'];

const weapons = new Set();

const all_ap = ['all-armor', 'breastplate', 'chain-mail', 'chain-shirt', 'half-plate-armor', 'heavy-armor', 'hide-armor', 'leather-armor', 'light-armor', 'medium-armor', 'padded-armor', 'plate-armor', 'ring-mail', 'scale-mail', 'splint-armor', 'studded-leather-armor'];

const armor = new Set();

const all_tp = ['alchemists-supplies', 'bagpipes', 'brewers-supplies', 'caligraphers-supplies', 'carpenters-tools', 'cartographers-tools', 'cobblers-tools', 'cooks-utensils', 'dice-set', 'disguise-kit', 'drum', 'dulcimer', 'flute', 'forgery-kit', 'glass-blowers-tools', 'herbalism-kit', 'horn', 'jewlers-tools', 'land-vehicles', 'leather-workers-tools', 'lute', 'lyre', 'masons-tools', 'navigators-tools', 'painters-supplies', 'pan-flute', 'playing-card-set', 'poisoners-kit', 'potters-tools', 'shawm', 'smiths-tools', 'theives-tools', 'tinkers-tools', 'viol', 'water-vehicles', 'weavers-tools', 'woodcarvers-tools'];

const tools = new Set();

// Do I need this?
const all_languages = ['abyssal', 'celestial', 'common', 'deep-speech', 'draconic', 'dwarvish', 'elvish', 'giant', 'gnomish', 'goblin', 'halfling', 'infernal', 'orc', 'primordial', 'sylvan', 'undercommon'];

const languages = new Set();

// These get the player class and race from the database, via html
const class_ = document.querySelector('#class_').dataset.class_.split('/')[0].toLowerCase();
const race = document.querySelector('#race').dataset.race.toLowerCase();

// These are the static elements displaying what the player starts with, given race/class choices
const start_skills_list = document.querySelector('#start_skills_list');
const start_wp_list = document.querySelector('#start_wp_list');
const start_ap_list = document.querySelector('#start_ap_list');
const start_tp_list = document.querySelector('#start_tp_list');
const start_languages_list = document.querySelector('#start_languages_list');

// Divs containing optional proficiencies
const class_bonus = document.querySelector('#class_bonus');
class_bonus.innerText = `${document.querySelector('#class_').dataset.class_.split('/')[0]} Proficiency Options:`;
const race_bonus = document.querySelector('#race_bonus');
race_bonus.innerText = `${document.querySelector('#race').dataset.race} Proficiency Options:`;

// Hidden form fields that will hold submitted values after all choices have been made
const skills_input = document.querySelector('#skills_input');
const weapons_input = document.querySelector('#weapons_input');
const armor_input = document.querySelector('#armor_input');
const tools_input = document.querySelector('#tools_input');
const languages_input = document.querySelector('#languages_input');

// Gets class & race data from API, adds proficiencies to relevant category Set
async function getStartProficiencies () {
    let class_data = await axios.get(`https://www.dnd5eapi.co/api/classes/${class_}`);
    let race_data = await axios.get(`https://www.dnd5eapi.co/api/races/${race}`);

    let class_start_proficiencies = class_data.data.proficiencies;
    for (let proficiency of class_start_proficiencies) {
        if (all_skills.includes(proficiency.index)) {
            skills.add(proficiency.name);
        }
        if (all_wp.includes(proficiency.index)) {
            weapons.add(proficiency.name);
        }
        if (all_ap.includes(proficiency.index)) {
            armor.add(proficiency.name);
        }
        if (all_tp.includes(proficiency.index)) {
            tools.add(proficiency.name);
        }
    }
    let race_start_proficiencies = race_data.data.starting_proficiencies;
    for (let proficiency of race_start_proficiencies) {
        if (all_skills.includes(proficiency.index)) {
            skills.add(proficiency.name);
        };
        if (all_wp.includes(proficiency.index)) {
            weapons.add(proficiency.name);
        };
        if (all_ap.includes(proficiency.index)) {
            armor.add(proficiency.name);
        };
        if (all_tp.includes(proficiency.index)) {
            tools.add(proficiency.name);
        };
    };
    let start_race_languages = race_data.data.languages;
    for (let language of start_race_languages) {
        languages.add(language.name);
    };
    // Fills hidden form inputs with stringified arrays of relevant proficiencies
    skills_input.value = JSON.stringify(Array.from(skills));
    weapons_input.value = JSON.stringify(Array.from(weapons));
    armor_input.value = JSON.stringify(Array.from(armor));
    tools_input.value = JSON.stringify(Array.from(tools));
    languages_input.value = JSON.stringify(Array.from(languages));
}

// Renders starting proficiency strings
function fillStart (set_, location) {
    let array = Array.from(set_);
    location.innerText += array.join(', ');
}

async function renderStart () {
    await getStartProficiencies();
    fillStart(skills, start_skills_list);
    fillStart(weapons, start_wp_list);
    fillStart(armor, start_ap_list);
    fillStart(tools, start_tp_list);
    fillStart(languages, start_languages_list);
};

renderStart();

async function getBonusClassProficiencies (endpoint) {
    let response = await axios.get(`https://www.dnd5eapi.co/api/classes/${endpoint}`);
    categories = response.data.proficiency_choices;

    // Monks have a proficiency option category that's subdivided
    if (class_ == 'monk') {
        let desc = document.createElement('div');
        desc.style = 'outline:0.01em solid black; padding:5px; margin:5px';
        desc.innerText = `${categories[0].desc}: `;
        desc.id = `${categories[0].desc}`;
        class_bonus.append(desc);

        let options = categories[0].from.options;
        for (let option of options) {
            let box = document.createElement('input');
            box.type = 'checkbox';
            box.id = `class-${option.item.index}`;
            box.value = `${option.item.name}`;
            box.setAttribute('class', `${categories[0].desc}`);
            desc.append(box);
            let label = document.createElement('label');
            label.for = `class-${option.item.index}`;
            label.innerText = `${option.item.name}`;
            desc.append(label);
        }
        
        let sub_desc = document.createElement('div');
        sub_desc.style = 'outline:0.01em solid black; padding:5px; margin:5px';
        sub_desc.innerText = `${categories[1].desc}: `;
        sub_desc.id = `${categories[1].desc}`;
        class_bonus.append(sub_desc);

        let sub_options_0 = categories[1].from.options[0].choice.from.options;
        let sub_options_1 = categories[1].from.options[1].choice.from.options;

        for (let option of sub_options_0) {
            let box = document.createElement('input');
            box.type = 'checkbox';
            box.id = `class-${option.item.index}`;
            box.value = `${option.item.name}`;
            sub_desc.append(box);
            let label = document.createElement('label');
            label.for = `class-${option.item.index}`;
            label.innerText = `${option.item.name}`;
            sub_desc.append(label);
        }
        for (let option of sub_options_1) {
            let box = document.createElement('input');
            box.type = 'checkbox';
            box.id = `class-${option.item.index}`;
            box.value = `${option.item.name}`;
            sub_desc.append(box);
            let label = document.createElement('label');
            label.for = `class-${option.item.index}`;
            label.innerText = `${option.item.name}`;
            sub_desc.append(label);
        }
        sub_desc.addEventListener('click', function (event) {
            if (event.target.checked) {
                tools.add(event.target.value);
                tools_input.value = JSON.stringify(Array.from(tools));
            }
            else {
                tools.delete(event.target.value);
                tools_input.value = JSON.stringify(Array.from(tools));
            }
        });
    }

        // For all classes except Monks
        else {
            for (let category of categories) {
        let desc = document.createElement('div');
        desc.style = 'outline:0.01em solid black; padding:5px; margin:5px';
        desc.innerText = `${category.desc}: `;
        desc.id = `${category.desc}`;
        class_bonus.append(desc);

        
        let options = category.from.options;
            for (let option of options) {
                let box = document.createElement('input');
                box.type = 'checkbox';
                box.id = `class-${option.item.index}`;
                box.value = `${option.item.name}`;
                box.setAttribute('class', `${category.desc}`);
                desc.append(box);
                let label = document.createElement('label');
                label.for = `class-${option.item.index}`;
                label.innerText = `${option.item.name}`;
                desc.append(label);
            }
        }
        
        desc.addEventListener('click', function (event) {
            let proficiency = event.target.value.toLowerCase().replaceAll(': ', '-').replaceAll(' ', '-').replaceAll("'", '');
            if (event.target.checked) {
                
                if (all_skills.includes(proficiency)) {
                    skills.add(event.target.value);
                    skills_input.value = JSON.stringify(Array.from(skills));
                };
                if (all_wp.includes(proficiency)) {
                    weapons.add(event.target.value);
                    weapons_input.value = JSON.stringify(Array.from(weapons));
                };
                if (all_ap.includes(proficiency)) {
                    armor.add(event.target.value);
                    armor_input.value = JSON.stringify(Array.from(armor));
                };
                if (all_tp.includes(proficiency)) {
                    tools.add(event.target.value);
                    tools_input.value = JSON.stringify(Array.from(tools));
                };
                
            }
            else {
                if (all_skills.includes(proficiency)) {
                    skills.delete(event.target.value);
                    skills_input.value = JSON.stringify(Array.from(skills));
                };
                if (all_wp.includes(proficiency)) {
                    weapons.delete(event.target.value);
                    weapons_input.value = JSON.stringify(Array.from(weapons));
                };
                if (all_ap.includes(proficiency)) {
                    armor.delete(event.target.value);
                    armor_input.value = JSON.stringify(Array.from(armor));
                };
                if (all_tp.includes(proficiency)) {
                    tools.delete(event.target.value);
                    tools_input.value = JSON.stringify(Array.from(tools));
                };
            }
            }
        );
    }

    
}

getBonusClassProficiencies(`${class_}`);



async function getBonusRaceProficiencies (endpoint) {
    let response = await axios.get(`https://www.dnd5eapi.co/api/races/${endpoint}`);
    let proficiencies = response.data.starting_proficiency_options;
    let prof_desc = document.createElement('div');

    prof_desc.style = 'outline:0.01em solid black; padding:5px; margin:5px';

    if (proficiencies?.desc) {
        prof_desc.innerText = `${proficiencies.desc}:`;
        prof_desc.id = `${proficiencies.desc}`;
    }
    else if (proficiencies) {
        prof_desc.innerText = `Choose ${proficiencies.choose}:`;
        prof_desc.id = 'race-skills';
    }
    else { return; };
    
    race_bonus.append(prof_desc);

    let options = proficiencies.from.options;

    for (let option of options) {
        let box = document.createElement('input');
        box.type = 'checkbox';
        box.id = `class-${option.item.index}`;
        box.value = `${option.item.name}`;
        box.setAttribute('class', `${options.desc}`);
        prof_desc.append(box);
        let label = document.createElement('label');
        label.for = `class-${option.item.index}`;
        label.innerText = `${option.item.name}`;
        prof_desc.append(label);
    }

    prof_desc.addEventListener('click', function (event) {
            let proficiency = event.target.value.toLowerCase().replaceAll(': ', '-').replaceAll(' ', '-').replaceAll("'", '');
            if (event.target.checked) {
                
                if (all_skills.includes(proficiency)) {
                    skills.add(event.target.value);
                    skills_input.value = JSON.stringify(Array.from(skills));
                };
                if (all_wp.includes(proficiency)) {
                    weapons.add(event.target.value);
                    weapons_input.value = JSON.stringify(Array.from(weapons));
                };
                if (all_ap.includes(proficiency)) {
                    armor.add(event.target.value);
                    armor_input.value = JSON.stringify(Array.from(armor));
                };
                if (all_tp.includes(proficiency)) {
                    tools.add(event.target.value);
                    tools_input.value = JSON.stringify(Array.from(tools));
                };
                
            }
            else {
                if (all_skills.includes(proficiency)) {
                    skills.delete(event.target.value);
                    skills_input.value = JSON.stringify(Array.from(skills));
                };
                if (all_wp.includes(proficiency)) {
                    weapons.delete(event.target.value);
                    weapons_input.value = JSON.stringify(Array.from(weapons));
                };
                if (all_ap.includes(proficiency)) {
                    armor.delete(event.target.value);
                    armor_input.value = JSON.stringify(Array.from(armor));
                };
                if (all_tp.includes(proficiency)) {
                    tools.delete(event.target.value);
                    tools_input.value = JSON.stringify(Array.from(tools));
                };
            }
    })
    
    let language_options = response.data.language_options;
    let lang_desc = document.createElement('div');

    lang_desc.style = 'outline:0.01em solid black; padding:5px; margin:5px';

    if (language_options.desc) {
        lang_desc.innerText = `${language_options.desc}:`;
        lang_desc.id = `${language_options.desc}`;
    }
    else {
        lang_desc.innerText = `Choose ${language_options.choose}:`;
        lang_desc.id = 'race-languages';
    }
    
    race_bonus.append(lang_desc);

    let lang_options = language_options.from.options;

    for (let option of lang_options) {
        let box = document.createElement('input');
        box.type = 'checkbox';
        box.id = `class-${option.item.index}`;
        box.value = `${option.item.name}`;
        box.setAttribute('class', `${options.desc}`);
        lang_desc.append(box);
        let label = document.createElement('label');
        label.for = `class-${option.item.index}`;
        label.innerText = `${option.item.name}`;
        lang_desc.append(label);
    }

    lang_desc.addEventListener('click', function (event) {
            let language = event.target.value;
            if (event.target.checked) {
                languages.add(language);
                languages_input.value = JSON.stringify(Array.from(languages));
                }
            else {
                languages.delete(language);
                languages_input.value = JSON.stringify(Array.from(languages));
            }
            })
}


getBonusRaceProficiencies(`${race}`);