const yearElement = document.getElementById("year");
if (yearElement) {
  yearElement.textContent = String(new Date().getFullYear());
}

const form = document.querySelector(".contact-form");
const status = document.getElementById("form-status");

if (form && status) {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    status.textContent =
      "Thanks! Your request is ready. Connect this form to your email or CRM to receive submissions.";
    form.reset();
  });
}
