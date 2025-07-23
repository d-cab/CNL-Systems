  const heroButton = document.getElementById('hero-button');
  const heroSection = document.querySelector('.hero');

  window.addEventListener('scroll', () => {
    const heroBottom = heroSection.offsetTop + heroSection.offsetHeight;
    if (window.scrollY > heroBottom - 80) {
      heroButton.classList.add('sticky');
    } else {
      heroButton.classList.remove('sticky');
    }
  });
