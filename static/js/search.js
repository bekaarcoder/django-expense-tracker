const searchField = document.querySelector("#search");
const expenseContainer = document.querySelector(".expense-container");
const searchContainer = document.querySelector(".expense-search-container");
const noResult = document.querySelector(".no-result");
const searchBody = document.querySelector(".search-body");

searchField.addEventListener("keyup", (e) => {
  if (e.target.value.length > 0) {
    searchBody.innerHTML = "";
    fetch("/expenses/search", {
      body: JSON.stringify({ searchText: e.target.value }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        expenseContainer.classList.add("d-none");
        searchContainer.classList.remove("d-none");
        if (data.length === 0) {
          searchContainer.classList.add("d-none");
          noResult.classList.remove("d-none");
          noResult.innerHTML = "<p class='lead'>No records found.</p>";
        } else {
          searchContainer.classList.remove("d-none");
          noResult.classList.add("d-none");
          data.forEach((expense) => {
            searchBody.innerHTML += `
            <tr>
              <td>${expense.date}</td>
              <td>${expense.amount}</td>
              <td>${expense.description}</td>
              <td>${expense.category}</td>
              <th></th>
            </tr>
          `;
          });
        }
      });
  } else {
    expenseContainer.classList.remove("d-none");
    searchContainer.classList.add("d-none");
  }
});
