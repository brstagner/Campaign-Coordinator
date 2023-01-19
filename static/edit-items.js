// Populate equipment datalists

const weapons_datalist = document.querySelector('#weapons_datalist');
const armor_datalist = document.querySelector('#armor_datalist');
const tools_datalist = document.querySelector('#tools_datalist');
const walletDatalist = document.querySelector('#wallet_datalist');

async function getEquipment (type, datalist) {
    let response = await axios.get(`https://www.dnd5eapi.co/api/equipment-categories/${type}`);
    let equipment = response.data.equipment;
    for (let item of equipment) {
        let option = document.createElement('option');
        option.setAttribute('value', `${item.name}`);
        datalist.append(option);
    };
};

getEquipment('weapon', weapons_datalist);
getEquipment('armor', armor_datalist);
getEquipment('tools', tools_datalist);

// Add new inputs
const inputs = document.querySelector('#inputs');

inputs.addEventListener('click', function (e) {
    e.preventDefault();
    if (e.target.classList.contains('delete')) {
        e.target.parentElement.remove();
    };
    if (e.target.classList.contains('add')) {
        let new_item = document.createElement('div');
        e.target.parentElement.parentElement.append(new_item);

        let new_item_name = document.createElement('input');
        new_item_name.classList.add(`${e.target.parentElement.parentElement.dataset.class}`);
        new_item_name.setAttribute('list', `${e.target.parentElement.parentElement.dataset.list}`);
        new_item.append(new_item_name);

        let delete_button = document.createElement('button');
        delete_button.classList.add('delete');
        delete_button.innerText = 'Delete';
        new_item.append(delete_button);
    };
});

const multi_inputs = document.querySelector('#multi-inputs');

multi_inputs.addEventListener('click', function (e) {
    e.preventDefault();
    if (e.target.classList.contains('delete')) {
        e.target.parentElement.remove();
    };
    if (e.target.classList.contains('add')) {
        let new_item = document.createElement('div');
        e.target.parentElement.parentElement.append(new_item);

        new_item.append(`${e.target.parentElement.parentElement.dataset.name_label}`);

        let new_item_name = document.createElement('input');
        new_item_name.classList.add(`${e.target.parentElement.parentElement.dataset.name_class}`);
        new_item_name.setAttribute('list', `${e.target.parentElement.parentElement.dataset.list}`);
        new_item.append(new_item_name);

        new_item.append('Number:')

        let new_item_number = document.createElement('input');
        new_item_number.classList.add(`${e.target.parentElement.parentElement.dataset.number_class}`);
        new_item_number.type = 'number';
        new_item.append(new_item_number);

        let delete_button = document.createElement('button');
        delete_button.classList.add('delete');
        delete_button.innerText = 'Delete';
        new_item.append(delete_button);
    };
});


// Fill form inputs
function fillInputs (type, input) {
    let item_list = [];
    let items = document.getElementsByClassName(`${type}`);
    for (let item of items) {
        item_list.push(item.value)
    };
    document.querySelector(`#${input}`).value = JSON.stringify(item_list);
};

function fillMultiInputs (type) {
    let item_names = [];
    let item_names_inputs = document.getElementsByClassName(`${type}_name`)
    let item_numbers = [];
    let item_numbers_inputs = document.getElementsByClassName(`${type}_number`)
    let item_zip = '';

    for (let name of item_names_inputs) {
        item_names.push(name.value)
    }
    for (let number of item_numbers_inputs) {
        item_numbers.push(number.value)
    }
    for (let i = 0; i < item_names.length; i++){
        item_zip += `("${item_names[i]}", ${item_numbers[i]}),`;
    }
    document.querySelector(`#${type}`).value = `[${item_zip}]`;
};

const submit = document.querySelector('#submit');
submit.addEventListener('click', function (e) {
    // e.preventDefault();

    fillInputs('weapon', 'weapons');
    fillInputs('armor', 'armor');
    fillInputs('tool', 'tools');

    fillMultiInputs('wallet');
    fillMultiInputs('other');

});


