const attacks_input = document.querySelector('#attacks_input');

attacks_input.addEventListener('click', function (e) {
    e.preventDefault();
    if (e.target.classList.contains('delete')){
        e.target.parentElement.parentElement.remove();
    };
    if (e.target.classList.contains('add')) {
        let new_attack = document.createElement('div');
        new_attack.classList.add('column');
        attacks_div.append(new_attack);

        let weapon_name = document.createElement('div');
        weapon_name.append('Weapon name: ');
        let new_weapon_input = document.createElement('input');
        new_weapon_input.setAttribute('list', 'weapons_datalist');
        new_weapon_input.classList.add('weapons_input');
        weapon_name.append(new_weapon_input);
        new_attack.append(weapon_name);

        let attack_dice = document.createElement('div');
        attack_dice.append('Attack dice: ');
        let new_dice_input = document.createElement('input');
        new_dice_input.classList.add('dice_input');
        new_dice_input.setAttribute('list', 'dice_datalist');
        attack_dice.append(new_dice_input);
        new_attack.append(attack_dice);

        let attack_number = document.createElement('div');
        attack_number.append('Number of attacks: ');
        let new_number_input = document.createElement('input');
        new_number_input.classList.add('number_input');
        new_number_input.type = 'number';
        attack_number.append(new_number_input);
        new_attack.append(attack_number);

        let button_div = document.createElement('div');
        let delete_button = document.createElement('button');
        delete_button.classList.add('delete');
        delete_button.innerText = 'Delete';
        button_div.append(delete_button);
        new_attack.append(button_div);
    };
});

const submit = document.querySelector('#submit');

submit.addEventListener('click', function (e) {
    // e.preventDefault();

    let weapons_list = [];
    let weapons = document.getElementsByClassName('weapons_input');
    let dice_list = [];
    let dice = document.getElementsByClassName('dice_input');
    let number_list = [];
    let numbers = document.getElementsByClassName('number_input');

    let attack_zip = '';

    for (let weapon of weapons) {
        weapons_list.push(weapon.value)
    };

    for (let die of dice) {
        dice_list.push(die.value)
    };

    for (let number of numbers) {
        number_list.push(number.value)
    };

    for (let i = 0; i < weapons_list.length; i++){
        attack_zip += (`("${weapons_list[i]}", "${dice_list[i]}", ${number_list[i]}),`);
    };

    document.querySelector('#attacks').value = `[${attack_zip}]`; 
});