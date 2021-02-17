console.log("Application Loading...");

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
        } else {
          feedbackField.classList.add("d-none");
          usernameField.classList.remove("is-invalid");
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
        } else {
          emailFeedbackField.classList.add("d-none");
          emailField.classList.remove("is-invalid");
        }
      })
      .catch((error) => console.log(error));
  }
});
