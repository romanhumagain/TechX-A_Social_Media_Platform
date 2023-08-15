$(document).ready(function() {
  // Attach a click event to the follow/unfollow button
  $('.follow-btn').on('click', function(e) {
      e.preventDefault();

      const $this = $(this);  // Cache the button reference
      const action = $this.data('action');
      const slug = $this.data('slug');
      let url;

      // Determine the URL based on the action
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
                  // Toggle the button's state and action
                  if (action === 'follow') {
                      $this.text('Unfollow').data('action', 'unfollow').toggleClass('btn-outline-secondary btn-secondary');
                  } else {
                      $this.text('Follow').data('action', 'follow').toggleClass('btn-outline-secondary btn-secondary');
                  }

                  // Update the follower count in the DOM
                  $('.follower-count').text(response.follower_count + ' Followers');
              } else {
                  console.error('Failed to follow/unfollow');
              }
          },
          error: function(xhr, status, error) {
              console.error('AJAX error:', status, error);
          }
      });
  });
});
