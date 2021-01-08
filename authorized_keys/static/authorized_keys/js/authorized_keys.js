
/* To enable navbar burger menu as of https://bulma.io/documentation/components/navbar/#navbar-menu (accessed 2021-01-08). */

document.addEventListener('DOMContentLoaded', () => {

  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Check if there are any navbar burgers
  if ($navbarBurgers.length > 0) {

    // Add a click event on each of them
    $navbarBurgers.forEach( el => {
      el.addEventListener('click', () => {

        // Get the target from the "data-target" attribute
        const target = el.dataset.target;
        const $target = document.getElementById(target);

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        el.classList.toggle('is-active');
        $target.classList.toggle('is-active');

      });
    });
  }

  /* End example Bulma snippet */

  const $key_text = document.getElementById('key_text');
  const $key_title = document.getElementById('key_title');

  if ($key_text && $key_title) {
    key_text.addEventListener('input', () => {
      comment_match = key_text.value.match(/^\S+ \S+ (.+)\n?$/);
      if (comment_match && comment_match.length > 1) {
          key_title.value = comment_match[1];
      }
    });
  }

});
