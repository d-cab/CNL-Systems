  const heroButton = document.getElementById('hero-button');
  const navbarSlot = document.getElementById('navbar-button-slot');
  const heroContent = document.querySelector('.hero-content');
  let isSticky = false;

  // Get the initial top offset of the button relative to the document
  const buttonOffsetTop = heroButton.getBoundingClientRect().top + window.pageYOffset;

  window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset;

    if (scrollY > buttonOffsetTop && !isSticky) {
      // Scroll past original button location, stick it to navbar
      navbarSlot.appendChild(heroButton);
      heroButton.classList.remove('btn-large');
      heroButton.classList.add('btn-small');
      isSticky = true;
    } else if (scrollY <= buttonOffsetTop && isSticky) {
      // Scroll back up above original location, return button to hero
      heroContent.appendChild(heroButton);
      heroButton.classList.remove('btn-small');
      heroButton.classList.add('btn-large');
      isSticky = false;
    }
  });
