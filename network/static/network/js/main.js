function changeLikeButton(status, button) {
    if (status) {
        button.className = "btn btn-danger like_btn"
        button.innerHTML = "Unlike!"
        button.dataset.liked = true
    }
    else {
        button.className = "btn btn-success like_btn"
        button.innerHTML = "like!"
        button.dataset.liked = false
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.getElementsByClassName("like_btn")
    for (const button of buttons) {
        fetch(`likes/${button.value}`)
            .then(res => res.json())
            .then(data => data["liked"])
            .then(status => {
                changeLikeButton(status, button)
            })
    }

    document.querySelectorAll(".like_btn").forEach(btn => btn.addEventListener("click", () => {
        const status = btn.dataset.liked === "true" ? true : false
        fetch(`/likes/${btn.value}`, {
            method: 'POST',
            body: JSON.stringify({
                liked: !status
            })
        })
            .then(response => response.json())
            .then(result => console.log(result))
            .then(() => changeLikeButton(!status, btn))
    }))
})
