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
      
      $count.text(data.likes_count + ' Likes');
  }).fail(function(xhr, status, error) {
      if (xhr.status == 403) {
          window.location.href = "/login/";  // replace with your login URL if different
      } else {
          console.error("Error liking the post:", status, error);
      }
  });
});
