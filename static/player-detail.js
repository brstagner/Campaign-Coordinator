const buttons = document.getElementsByTagName('button');

for (let button of buttons) {
    button.addEventListener('click', function (e) {
        e.preventDefault();
        if (e.target.nextElementSibling.hidden == true) {
            e.target.nextElementSibling.hidden = false;
        }
        else {
            e.target.nextElementSibling.hidden = true;
        }
    });
}