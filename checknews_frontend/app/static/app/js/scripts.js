var btn = document.getElementById('show-chat');
var btn_baloon = document.getElementById('show-chat-baloon');
var container = document.querySelector('.container');

btn.addEventListener('click', function() {       
        if(container.style.display === 'block') {
            container.style.display = 'none';
        }
        else {
            container.style.display = 'block';
        }
});

btn_baloon.addEventListener('click', function() {       
    if(container.style.display === 'block') {
        container.style.display = 'none';
    }
    else {
        container.style.display = 'block';
    }
});


