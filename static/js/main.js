let usernameErr = false;
let emailErr = false;

const handleRegisterButtonDisable = () => {
  if (!usernameErr && !emailErr) {
    registerBtn.removeAttribute("disabled");
  } else {
    registerBtn.disabled = true;
  }
};

const registerBtn = document.querySelector("#registerBtn");
const usernameField = document.querySelector("#usernameField");
const feedbackField = document.querySelector("#username-feedback");

usernameField.addEventListener("keyup", (e) => {
  if (e.target.value.length > 0) {
    fetch("/auth/validate-username", {
      body: JSON.stringify({ username: e.target.value }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.username_error) {
          usernameField.classList.add("is-invalid");
          feedbackField.classList.remove("d-none");
          feedbackField.innerHTML = `<p>${data.username_error}</p>`;
          usernameErr = true;
          handleRegisterButtonDisable();
        } else {
          feedbackField.classList.add("d-none");
          usernameField.classList.remove("is-invalid");
          usernameErr = false;
          handleRegisterButtonDisable();
        }
      })
      .catch((error) => console.log(error));
  }
});

const emailField = document.querySelector("#emailField");
const emailFeedbackField = document.querySelector("#email-feedback");

emailField.addEventListener("keyup", (e) => {
  if (e.target.value.length > 0) {
    fetch("/auth/validate-email", {
      body: JSON.stringify({ email: e.target.value }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.email_error) {
          emailField.classList.add("is-invalid");
          emailFeedbackField.classList.remove("d-none");
          emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`;
          emailErr = true;
          handleRegisterButtonDisable();
        } else {
          emailFeedbackField.classList.add("d-none");
          emailField.classList.remove("is-invalid");
          emailErr = false;
          handleRegisterButtonDisable();
        }
      })
      .catch((error) => console.log(error));
  }
});

const showPasswordToggle = document.querySelector("#showPasswordToggle");
const passwordField = document.querySelector("#passwordField");

showPasswordToggle.addEventListener("click", (e) => {
  if (passwordField.getAttribute("type") === "password") {
    passwordField.setAttribute("type", "text");
    showPasswordToggle.textContent = "HIDE";
  } else {
    passwordField.setAttribute("type", "password");
    showPasswordToggle.textContent = "SHOW";
  }
});
