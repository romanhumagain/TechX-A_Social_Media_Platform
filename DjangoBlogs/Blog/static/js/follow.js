$(document).ready(function() {
  
  $('.follow-btn').on('click', function(e) {
      e.preventDefault();

      const $this = $(this);  
      const action = $this.data('action');
      const slug = $this.data('slug');
      let url;

     
      if (action === 'follow') {
          url = `/user/follow/${slug}/`;
      } else if (action === 'unfollow') {
          url = `/user/unfollow/${slug}/`;
      } else {
          console.error('Invalid action');
          return;
      }

      // AJAX request
      $.ajax({
          type: 'POST',
          url: url,
          data: {
              'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
          },
          success: function(response) {
              if (response.success) {
                  if (action === 'follow') {
                      $this.html('<i class="fas fa-user-minus"></i> Unfollow')
                          .data('action', 'unfollow')
                          .toggleClass('btn-outline-secondary btn-secondary');
                  } else {
                      $this.html('<i class="fas fa-user-plus"></i> Follow')
                          .data('action', 'follow')
                          .toggleClass('btn-outline-secondary btn-secondary');
                  }
      
                  // Update the follower count in the DOM
                  $('.follower-count').text(response.follower_count + ' Followers');
              } else {
                  console.error('Failed to follow/unfollow');
              }
          }  
      });  
  });  
});  
