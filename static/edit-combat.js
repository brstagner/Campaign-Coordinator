const attacks_input = document.querySelector('#attacks_input');

attacks_input.addEventListener('click', function (e) {
    e.preventDefault();
    if (e.target.classList.contains('delete')){
        e.target.parentElement.remove();
    };
    if (e.target.classList.contains('add')) {
        let new_attack = document.createElement('p');
        attacks_input.append(new_attack);
        let new_weapon_input = document.createElement('input');
        new_weapon_input.setAttribute('list', 'weapons_datalist');
        new_weapon_input.classList.add('weapons_input');
        new_attack.append(new_weapon_input);

        let new_dice_input = document.createElement('input');
        new_dice_input.classList.add('dice_input');
        new_attack.append(new_dice_input)

        let new_number_input = document.createElement('input');
        new_number_input.classList.add('number_input');
        new_number_input.type = 'number';
        new_attack.append(new_number_input);

        let delete_button = document.createElement('button');
        delete_button.classList.add('delete');
        delete_button.innerText = 'Delete';
        new_attack.append(delete_button);
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