function getCookie(name) {
  let value = "; " + document.cookie;
  let parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

$.ajaxSetup({
  headers: {
      'X-CSRFToken': getCookie('csrftoken')
  }
});

$(document).on('click', '.like-btn', function(e) {
  e.preventDefault();
  let postId = $(this).attr('data-post-id');
  let url = `/like_post/${postId}/`; 

  $.post(url, function(data) {
      location.reload();
  });
});
