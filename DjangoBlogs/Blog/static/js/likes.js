// Helper function to get the CSRF token from cookies
function getCookie(name) {
  let value = "; " + document.cookie;
  let parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

// Setup jQuery AJAX to include the CSRF token in the request headers
$.ajaxSetup({
  headers: {
      'X-CSRFToken': getCookie('csrftoken')
  }
});

// Event listener for the like button click
$(document).on('click', '.like-btn', function(e) {
  e.preventDefault();

  const $this = $(this);
  const postId = $this.attr('data-post-id');
  const url = `/like_post/${postId}/`; 
  const $icon = $this.find('i');
  const $count = $this.find('.icon-count');

  $.post(url, function(data) {
      if (data.liked) {
          $icon.removeClass('far fa-heart text-secondary').addClass('fas fa-heart text-danger');
      } else {
          $icon.removeClass('fas fa-heart text-danger').addClass('far fa-heart text-secondary');
      }

      // Update the likes count based on the server's response
      $count.text(data.likes_count);
  }).fail(function(xhr, status, error) {
      if (xhr.status == 403) {
          window.location.href = "/user/login/"; 
      } else {
          console.error("Error liking the post:", status, error);
      }
  });
});
