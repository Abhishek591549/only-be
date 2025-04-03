document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("register-form");
    const errorMessage = document.getElementById("error-message");
    const successMessage = document.getElementById("success-message");

    registerForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // ✅ Prevent default form submission

        // ✅ Get input values
        const full_name = document.getElementById("full_name").value.trim();
        const email = document.getElementById("email").value.trim();
        const address = document.getElementById("address").value.trim();
        const mobile_number = document.getElementById("mobile_number").value.trim();
        const password = document.getElementById("password").value;
        const confirm_password = document.getElementById("confirm_password").value;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        // ✅ Validation: Check empty fields
        if (!full_name || !email || !address || !mobile_number || !password || !confirm_password) {
            errorMessage.textContent = "❌ All fields are required!";
            return;
        }

        // ✅ Validation: Check if passwords match
        if (password !== confirm_password) {
            errorMessage.textContent = "❌ Passwords do not match!";
            return;
        }

        try {
            const response = await fetch("/register/api/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ full_name, email, address, mobile_number, password, confirm_password })
            });

            const data = await response.json();

            if (response.ok) {
                successMessage.textContent = "✅ " + data.message;
                errorMessage.textContent = "";

                // ✅ Redirect to OTP page after 1.5 seconds
                setTimeout(() => {
                    window.location.href = data.redirect_url;
                }, 1500);
            } else {
                errorMessage.textContent = "❌ " + data.error;
            }
        } catch (error) {
            console.error("Error:", error);
            errorMessage.textContent = "❌ An error occurred. Please try again.";
        }
    });
});
