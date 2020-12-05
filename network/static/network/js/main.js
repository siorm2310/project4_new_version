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

function sendEditedPost(data) {
    
}

document.addEventListener("DOMContentLoaded", () => {
    // Load like buttons with data
    const buttons = document.getElementsByClassName("like_btn")
    for (const button of buttons) {
        fetch(`../likes/${button.value}`)
            .then(res => res.json())
            .then(data => data["liked"])
            .then(status => {
                changeLikeButton(status, button)
            })
    }
    // Interact with likes API when a like button is pressed
    document.querySelectorAll(".like_btn").forEach(btn => btn.addEventListener("click", () => {
        const status = btn.dataset.liked === "true" ? true : false
        fetch(`../likes/${btn.value}`, {
            method: 'POST',
            body: JSON.stringify({
                liked: !status
            })
        })
            .then(response => response.json())
            .then((data) => {
                changeLikeButton(!status, btn)
                likeId = btn.value;
                document.getElementById(`${likeId}-num-likes`).innerHTML = data['current_num_likes']
            }
            )
    }))

    // Edit post - send update to API
    document.querySelectorAll(".edit_btn").forEach(btn => btn.addEventListener("click",()=>{
        const postId = btn.value;
        const data = {
            title : document.querySelector(`.post-title-${postId}`).innerHTML,
            content : document.querySelector(`.post-content-${postId}`).innerHTML
        }

        const editForm = `
        <form method="POST" action="../edit/${postId}">
        <div class="form-group">
        <input type="text" name="edit_title" value="${data.title}">
      </div>
        <div class="form-group">
        <textarea class="form-control" name="edit_content" rows="3">${data.content}</textarea>
      </div>
        <div class="form-group">
        <button class="btn btn-primary" type="submit" class="sumbit_edit" name="editPost">Update this post!</button>
        </div>
        </form>
        `

        document.querySelector(`.post-card-${postId}`).innerHTML = editForm;
    }))
})
