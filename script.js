document.getElementById("inquiryForm").addEventListener("submit", function (e) {
  e.preventDefault();
  
  // Simple fake "submit"
  const status = document.getElementById("formStatus");
  status.textContent = "Thank you! We'll get back to you soon.";
  this.reset();
});
