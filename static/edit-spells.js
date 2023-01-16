const known_input = document.querySelector('#known_input');
const submit = document.querySelector('#submit');

submit.addEventListener('click', function (e) {
    // e.preventDefault();

    let known_list = [];
    let known_inputs = document.getElementsByClassName('known_input');
    console.log(known_inputs);
    for (let spell of known_inputs) {
        known_list.push(spell.value)
    };
    document.querySelector('#known').value = JSON.stringify(known_list);

    for (let i = 0; i < 10; i++){
        let spell_names = [];
        let spell_names_inputs = document.getElementsByClassName(`lv${i}_name`)
        let spell_numbers = [];
        let spell_numbers_inputs = document.getElementsByClassName(`lv${i}_number`)
        let spell_zip = '';

        for (let name of spell_names_inputs) {
            spell_names.push(name.value)
        }
        for (let number of spell_numbers_inputs) {
            spell_numbers.push(number.value)
        }
        for (let i = 0; i < spell_names.length; i++){
            spell_zip += `("${spell_names[i]}", ${spell_numbers[i]}),`;
        }

        document.querySelector(`#lv${i}`).value = `[${spell_zip}]`;
    }
});

known_input.addEventListener('click', function (e) {
    e.preventDefault();
    if (e.target.classList.contains('delete')){
        e.target.parentElement.remove();
    };
    if (e.target.classList.contains('add')) {
        let new_known = document.createElement('div');
        known_input.append(new_known);

        let new_known_input = document.createElement('input');
        new_known_input.classList.add('known_input');
        new_known.append(new_known_input)

        let delete_button = document.createElement('button');
        delete_button.classList.add('delete');
        delete_button.innerText = 'Delete';
        new_known.append(delete_button);
    };
});

const prepared = document.querySelector('#prepared');

for (let i = 0; i < 10; i++){
    document.querySelector(`#lv${i}_input`).addEventListener('click', function (e) {
        e.preventDefault();
        if (e.target.classList.contains('delete')){
            e.target.parentElement.remove();
        };
        if (e.target.classList.contains('add')) {
            let new_spell = document.createElement('div');
            document.querySelector(`#lv${i}_input`).append(new_spell);

            let new_spell_name = document.createElement('input');
            new_spell_name.classList.add(`lv${i}_name`);
            new_spell.append(new_spell_name);

            let new_spell_number = document.createElement('input');
            new_spell_number.classList.add(`lv${i}_number`);
            new_spell_number.type = 'number';
            new_spell.append(new_spell_number);

            let delete_button = document.createElement('button');
            delete_button.classList.add('delete');
            delete_button.innerText = 'Delete';
            new_spell.append(delete_button);
    };
    })
};





