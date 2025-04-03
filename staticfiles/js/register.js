document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");
    const errorMessage = document.getElementById("error-message");

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();  // ✅ Prevent normal form submission

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const csrfTokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
        const csrfToken = csrfTokenElement ? csrfTokenElement.value : "";  // ✅ Get CSRF token safely

        try {
            const response = await fetch("/register/api/", {  // ✅ Match the Django URL pattern


                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken  // ✅ Include CSRF token
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                // ✅ Store access token in localStorage
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("refresh_token", data.refresh_token);

                // ✅ Redirect to dashboard
                window.location.href = data.redirect_url;
            } else {
                errorMessage.textContent = data.error || "Login failed. Please try again.";
            }
        } catch (error) {
            console.error("Error:", error);
            errorMessage.textContent = "An error occurred. Please try again.";
        }
    });
});
