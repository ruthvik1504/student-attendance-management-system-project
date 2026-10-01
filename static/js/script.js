document.addEventListener("DOMContentLoaded", function () {

    const deleteLinks = document.querySelectorAll(".delete-link");

    deleteLinks.forEach(function (link) {

        link.addEventListener("click", function (event) {

            const confirmed = confirm(
                "Are you sure you want to delete this student?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });

    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {

        form.addEventListener("submit", function () {

            const submitButton = form.querySelector(
                'button[type="submit"]'
            );

            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = "Processing...";
            }

        });

    });

});