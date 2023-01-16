// Name input fields, add relevent list attributes
const race_input = document.querySelector('#race');
race_input.setAttribute('list', 'race_datalist');

const subrace_input = document.querySelector('#subrace');
subrace_input.setAttribute('list', 'subrace_datalist');

const job_input = document.querySelector('#job');
job_input.setAttribute('list', 'job_datalist');

const alignment_input = document.querySelector('#alignment');
alignment_input.setAttribute('list', 'alignment_datalist');

// Create datalists, add relevant ids
const race_datalist = document.createElement('datalist');
race_datalist.id = 'race_datalist';

const subrace_datalist = document.createElement('datalist');
subrace_datalist.id = 'subrace_datalist'

const job_datalist = document.createElement('datalist');
job_datalist.id = 'job_datalist';

const alignment_datalist = document.createElement('datalist');
alignment_datalist.id = 'alignment_datalist';

// Get list of races from api, create option elements, append these
// to race datalist, append datalist to race input field
async function getRaceOptions () {
    let response = await axios.get(`https://www.dnd5eapi.co/api/races`);
    let choices = response.data.results;
    for (let choice of choices) {
        let option = document.createElement('option');
        option.setAttribute('value', `${choice.name}`);
        option.innerText = `${choice.name}`;
        race_datalist.append(option)
    };
    race_input.append(race_datalist);
};

getRaceOptions();

// Get list of subraces from api, create option elements, append these
// to subrace datalist, append datalist to subrace input field
async function getSubraceOptions () {
    let response = await axios.get(`https://www.dnd5eapi.co/api/subraces`);
    let choices = response.data.results;
    for (let choice of choices) {
        let option = document.createElement('option');
        option.setAttribute('value', `${choice.name}`);
        option.innerText = `${choice.name}`;
        subrace_datalist.append(option)
    };
    subrace_input.append(subrace_datalist);
};

getSubraceOptions();

// Get list of classes from api, create option elements, append these
// to job datalist, append datalist to job input field
async function getJobOptions () {
    let response = await axios.get(`https://www.dnd5eapi.co/api/classes`);
    let choices = response.data.results;
    for (let choice of choices) {
        let option = document.createElement('option');
        option.setAttribute('value', `${choice.name}`);
        option.innerText = `${choice.name}`;
        job_datalist.append(option)
    };
    job_input.append(job_datalist);
    
};

getJobOptions();

// Get list of alignments from api, create option elements, append these
// to alignment datalist, append datalist to alignment input field
async function getAlignmentOptions () {
    let response = await axios.get(`https://www.dnd5eapi.co/api/alignments`);
    let choices = response.data.results;
    for (let choice of choices) {
        let option = document.createElement('option');
        option.setAttribute('value', `${choice.name}`);
        option.innerText = `${choice.name}`;
        alignment_datalist.append(option)
    };
    alignment_input.append(alignment_datalist);
    
};

getAlignmentOptions();

// async function autofill () {
    
// }
    
