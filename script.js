const formTitle = document.getElementById("formTitle");
const formFields = document.getElementById("formFields");
const formButton = document.getElementById("formButton");
const toggleText = document.getElementById("toggleText");
const toggleLink = document.getElementById("toggleLink");

let isLogin = true;

function toggleForm(e) {
    e.preventDefault();
    isLogin = !isLogin;

    if (isLogin) {
        formTitle.textContent = "Login";
        formFields.innerHTML = `
            <div class="input-box">
                <input type="email" placeholder="Email" required>
                <i class='bx bxs-user'></i>
            </div>
            <div class="input-box">
                <input type="password" placeholder="Password" required>
                <i class='bx bxs-lock-alt'></i>
            </div>
        `;
        formButton.textContent = "Login";
        toggleText.innerHTML = `Don’t have an account? <a href="#" id="toggleLink">Register</a>`;
    } else {
        formTitle.textContent = "Register";
        formFields.innerHTML = `
            <div class="input-box">
                <input type="text" placeholder="Full Name" required>
                <i class='bx bxs-user'></i>
            </div>
            <div class="input-box">
                <input type="email" placeholder="Email" required>
                <i class='bx bxs-envelope'></i>
            </div>
            <div class="input-box">
                <input type="password" placeholder="Password" required>
                <i class='bx bxs-lock-alt'></i>
            </div>
            <div class="input-box">
                <input type="password" placeholder="Confirm Password" required>
                <i class='bx bxs-lock-alt'></i>
            </div>
        `;
        formButton.textContent = "Register";
        toggleText.innerHTML = `Already have an account? <a href="#" id="toggleLink">Login</a>`;
    }

    // Bağlantıyı yeniden etkinleştir
    document.getElementById("toggleLink").addEventListener("click", toggleForm);
}

document.getElementById("toggleLink").addEventListener("click", toggleForm);
