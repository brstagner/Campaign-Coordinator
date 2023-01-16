const conditions_input = document.querySelector('#conditions_input');
let body = document.querySelector('body');

let condition_inputs = document.getElementsByClassName('conditions_input');
for (let input of condition_inputs) {
    input.setAttribute('list', 'conditions_datalist');
};

async function getConditions () {
    let response = await axios.get(`https://www.dnd5eapi.co/api/conditions`);
    let conditions = response.data.results;
    let datalist = document.createElement('datalist');
    datalist.id = 'conditions_datalist';
    for (let condition of conditions) {
        let option = document.createElement('option');
        option.setAttribute('value', `${condition.name}`);
        option.innerText = `${condition.name}`;
        datalist.append(option);
    };
    body.append(datalist);
};

getConditions();

conditions_input.addEventListener('click', function (e) {
    e.preventDefault();
    if (e.target.classList.contains('delete')){
        // console.log(e.target.previousElementSibling);
        e.target.previousElementSibling.remove();
        e.target.remove();
    };
    if (e.target.classList.contains('add')) {
        let new_condition = document.createElement('p');
        conditions_input.append(new_condition);
        let new_conditions_input = document.createElement('input');
        new_conditions_input.setAttribute('list', 'conditions_datalist');
        new_conditions_input.classList.add('conditions_input');
        new_condition.append(new_conditions_input);
        let delete_button = document.createElement('button');
        delete_button.classList.add('delete');
        delete_button.innerText = 'Delete';
        new_condition.append(delete_button);
    };
});

hd_input.addEventListener('click', function (e) {
    e.preventDefault();
    if (e.target.classList.contains('delete')){
        e.target.parentElement.remove();
    };
    if (e.target.classList.contains('add')) {
        let new_hd = document.createElement('p');
        hd_input.append(new_hd);
        let new_hd_number_input = document.createElement('input');
        new_hd_number_input.classList.add('hd_number_input');
        new_hd_number_input.type = 'number';
        new_hd.append(new_hd_number_input);
        let new_hd_die_input = document.createElement('input');
        new_hd_die_input.classList.add('hd_die_input');
        new_hd.append(new_hd_die_input);
        let delete_button = document.createElement('button');
        delete_button.classList.add('delete');
        delete_button.innerText = 'Delete';
        new_hd.append(delete_button);
    };
});

const submit = document.querySelector('#submit');

submit.addEventListener('click', function (e) {
    // e.preventDefault();
    let conditions_list = [];
    let condition_inputs = document.getElementsByClassName('conditions_input');
    for (let condition of condition_inputs) {
        conditions_list.push(condition.value)
    };
    document.querySelector('#conditions').value = JSON.stringify(conditions_list);
    
    let dice_numbers = [];
    let hd_numbers = document.getElementsByClassName('hd_number_input');
    let dice_rolls = [];
    let hd_dice = document.getElementsByClassName('hd_die_input');
    let dice_zip = '';

    for (let number of hd_numbers) {
        dice_numbers.push(number.value)
    };

    for (let die of hd_dice) {
        dice_rolls.push(die.value)
    };

    for (let i = 0; i < dice_numbers.length; i++){
        dice_zip += (`(${dice_numbers[i]}, "${dice_rolls[i]}"),`);
    };

    document.querySelector('#hd').value = `[${dice_zip}]`; 
});