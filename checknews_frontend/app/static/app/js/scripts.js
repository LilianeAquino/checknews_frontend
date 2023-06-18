var btn = document.getElementById('show-chat');
var container = document.querySelector('.container');
var successMessage = document.getElementById('success-message');

btn.addEventListener('click', function() {       
        if(container.style.display === 'block') {
            container.style.display = 'none';
        }
        else {
            container.style.display = 'block';
        }
});

