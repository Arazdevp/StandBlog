function like(slug, id) {
    var element = document.getElementById("like")
    $.get(`/articles/like/${slug}/${id}`).then(response => {
        if (response["response"] === "Liked") {
            element.className = "fa fa-heart"
            count.innerText = Number(count.innerText) + 1
        } else if (response["response"] === "UnLiked") {
            element.className = "fa fa-heart-o"
            count.innerText = Number(count.innerText) - 1
        }
    })
}

$(document).ready(function () {
    $('#commentForm').submit(function (e) {
        e.preventDefault(); // جلوگیری از رفرش صفحه
        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-Requested-With': 'XMLHttpRequest'},
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    console.log(data);
                    let html = '<li' + (data.comment.is_reply ? ' class="replied"' : '') + '>' +
                        '<div class="author-thumb">' +
                        '<img src="' + data.comment.profile_image_url + '" alt="profile">' +
                        '</div>' +
                        '<div class="right-content">' +
                        '<h4>' + data.comment.username + '<span>' + data.comment.created_at + '</span></h4>' +
                        '<p>' + data.comment.body + '</p>';
                    if (!data.comment.is_reply) {
                        html += '<button onclick="set_value(' + data.comment.id + ', this)" class="btn btn-warning">Reply</button>';
                    }
                    html += '</div></li><br>';

                    if (data.comment.is_reply) {
                        let parentId = $("#parent_id").val();
                        let parentElement = $("#comment-" + parentId);
                        let repliesContainer = parentElement.find("ul.replies");
                        if (repliesContainer.length === 0) {
                            repliesContainer = $('<ul class="replies"></ul>');
                            parentElement.append(repliesContainer);
                        }
                        repliesContainer.append(html);
                    } else {
                        $("#commentsList").append(html);
                    }
                    $('#commentForm')[0].reset();
                    $("#parent_id").val("");
                    if (last_comment_for_replay) {
                        last_comment_for_replay.innerHTML = "Reply";
                        last_comment_for_replay = null;
                    }
                }
            },
            error: function (xhr, errmsg, err) {
                console.log("Error: " + errmsg);
            }
        });
    });
});
