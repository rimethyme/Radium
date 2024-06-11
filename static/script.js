document.addEventListener("DOMContentLoaded", () => {
    const output = document.getElementById('output');
    const inputForm = document.getElementById('inputForm');
    const userInput = document.getElementById('userInput');
    const fullscreenBtn = document.getElementById('fullscreen-btn');

    inputForm.addEventListener('submit', handleInput);
    fullscreenBtn.addEventListener('click', toggleFullscreen);

    // Load the initial story content
    function loadInitialStory() {
        fetch('/static/story/base_of_the_tower.txt')
            .then(response => response.text())
            .then(data => {
                output.innerHTML = data;
            })
            .catch(error => console.error('Error loading base_of_the_tower.txt:', error));
    }

    function handleInput(event) {
        event.preventDefault();
        const input = userInput.value.trim().toLowerCase();
        userInput.value = '';

        if (input) {
            sendCommand(input);
        }
    }

    function sendCommand(command) {
        fetch('/command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input: command }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.response) {
                    output.innerHTML += `<p>${data.response}</p>`;
                }
            })
            .catch(error => console.error('Error sending command:', error));
    }

    // Full-screen toggle function
    function toggleFullscreen() {
        const consoleElement = document.querySelector('.console');
        if (!document.fullscreenElement) {
            if (consoleElement.requestFullscreen) {
                consoleElement.requestFullscreen();
            } else if (consoleElement.mozRequestFullScreen) { // Firefox
                consoleElement.mozRequestFullScreen();
            } else if (consoleElement.webkitRequestFullscreen) { // Chrome, Safari and Opera
                consoleElement.webkitRequestFullscreen();
            } else if (consoleElement.msRequestFullscreen) { // IE/Edge
                consoleElement.msRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }
    }

    // Load the initial story when the page loads
    window.onload = function() {
        loadInitialStory();
    };
});

document.getElementById('command-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const input = document.getElementById('command-input').value;
    fetch('/command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: input })
    })
    .then(response => response.json())
    .then(data => {
        const outputElement = document.getElementById('output');
        outputElement.innerHTML = data.response;
    });
});
