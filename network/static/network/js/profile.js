// Get CSRF Token for post requests
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener("DOMContentLoaded",()=>{
    let button = document.getElementById("follow_btn")

    button.addEventListener("click",()=>{
        if (button.dataset.follows === "0") {
            button.dataset.follows = "1";
            button.className = "btn btn-danger";
            button.innerHTML = "Unfollow!"
            const data = {
                user : button.value,
                follows : true
            };
            updateFollows(data)
        }
        else if (button.dataset.follows === "1") {
            button.dataset.follows = "0";
            button.className = "btn btn-success";
            button.innerHTML = "follow!"
            const data = {
                user : button.value,
                follows : false
            };
            updateFollows(data)
        }
    })

    function updateFollows(info) {
        fetch('/update_follows',{
            method : "POST",
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'},
            body: JSON.stringify(info)
        })
        // .then(response => JSON.parse(response))
        .then(response => console.log(response))
    }
})