function like(slug, id) {
    var element = document.getElementById("like")
    $.get(`/articles/like/${slug}/${id}`).then(response => {
        if(response["response"] === "Liked"){
            element.className = "fa fa-heart"
            count.innerText = Number(count.innerText) + 1
        }else if (response["response"] === "UnLiked"){
            element.className = "fa fa-heart-o"
            count.innerText = Number(count.innerText) - 1
        }
    })
}