document.addEventListener("DOMContentLoaded", function () {
    const otpForm = document.getElementById("otp-form");
    const errorMessage = document.getElementById("error-message");

    // ✅ Get email from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const email = urlParams.get("email");

    otpForm.addEventListener("submit", async function (event) {
        event.preventDefault();  // ✅ Prevent default form submission

        const otpCode = document.getElementById("otp_code").value;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;  // ✅ Get CSRF token

        try {
            const response = await fetch("/verify-otp/api/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken  // ✅ Include CSRF token in headers
                },
                body: JSON.stringify({
                    user_email: email,
                    otp_code: otpCode
                })
            });

            const data = await response.json();

            if (response.ok) {
                // ✅ Redirect to login page after successful OTP verification
                window.location.href = data.redirect_url;
            } else {
                errorMessage.textContent = data.error || "OTP verification failed. Please try again.";
            }
        } catch (error) {
            console.error("Error:", error);
            errorMessage.textContent = "An error occurred. Please try again.";
        }
    });
});
