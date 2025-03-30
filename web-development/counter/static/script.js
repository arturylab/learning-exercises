function changeMessage() {
    document.getElementById("message").innerHTML = "Hello, Flask & JavaScript!";
}

document.addEventListener("DOMContentLoaded", function() {
    fetch("/get_count")  
        .then(response => response.json())
        .then(data => {
            document.getElementById("counter").innerText = data.count;
        });
});

function updateCounter(action) {
    fetch(`/click/${action}`, {method: 'POST'})
    .then(response => response.json())
    .then(data => {
        document.getElementById("counter").innerHTML = data.count;
    })
    .catch(error => console.error('Error:', error));
}