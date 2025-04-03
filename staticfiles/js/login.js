document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("#login-form");  // ✅ Ensure the form exists
    if (!loginForm) {
        console.error("❌ Login form not found!");
        return;
    }

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission

        const emailInput = document.querySelector("#email");
        const passwordInput = document.querySelector("#password");
        const errorMessage = document.querySelector("#error-message");

        // ✅ Ensure fields exist before proceeding
        if (!emailInput || !passwordInput) {
            console.error("❌ Email or Password input not found!");
            return;
        }

        const email = emailInput.value;
        const password = passwordInput.value;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        // ✅ Clear previous error messages
        errorMessage.textContent = "";

        try {
            const response = await fetch("/api/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                // ✅ Show success message
                alert("✅ Login Successful! Redirecting to Dashboard...");

                // ✅ Redirect to dashboard after 1.5 seconds
                setTimeout(() => {
                    window.location.href = data.redirect_url;
                }, 1500);
            } else {
                errorMessage.textContent = "❌ " + data.error;
            }
        } catch (error) {
            console.error("❌ Login Error:", error);
            errorMessage.textContent = "Something went wrong. Please try again.";
        }
    });
});
