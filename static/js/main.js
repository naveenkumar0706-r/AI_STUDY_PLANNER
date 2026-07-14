/* ==========================================================
   AI Study Planner — Main JS
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
    initDarkMode();
    initSidebarToggle();
    initFormValidation();
    animateProgressBars();
});

/* ---------------- Dark Mode ---------------- */
function initDarkMode() {
    const toggle = document.getElementById("darkModeToggle");
    const html = document.documentElement;
    const saved = localStorage.getItem("studyplanner-theme");

    if (saved === "dark") {
        html.setAttribute("data-theme", "dark");
        if (toggle) toggle.textContent = "☀️";
    }

    if (toggle) {
        toggle.addEventListener("click", () => {
            const isDark = html.getAttribute("data-theme") === "dark";
            html.setAttribute("data-theme", isDark ? "light" : "dark");
            toggle.textContent = isDark ? "🌙" : "☀️";
            localStorage.setItem("studyplanner-theme", isDark ? "light" : "dark");
        });
    }
}

/* ---------------- Sidebar Toggle (mobile) ---------------- */
function initSidebarToggle() {
    const btn = document.getElementById("sidebarToggle");
    const sidebar = document.getElementById("sidebar");
    if (btn && sidebar) {
        btn.addEventListener("click", () => sidebar.classList.toggle("open"));
        document.addEventListener("click", (e) => {
            if (!sidebar.contains(e.target) && !btn.contains(e.target)) {
                sidebar.classList.remove("open");
            }
        });
    }
}

/* ---------------- Client-side Form Validation ---------------- */
function initFormValidation() {
    document.querySelectorAll("form[data-validate]").forEach((form) => {
        form.addEventListener("submit", (e) => {
            let valid = true;
            form.querySelectorAll("[required]").forEach((field) => {
                clearFieldError(field);
                if (!field.value.trim()) {
                    valid = false;
                    showFieldError(field, "This field is required.");
                }
            });

            const pw1 = form.querySelector('[name="password1"]');
            const pw2 = form.querySelector('[name="password2"]');
            if (pw1 && pw2 && pw1.value !== pw2.value) {
                valid = false;
                showFieldError(pw2, "Passwords do not match.");
            }

            if (!valid) e.preventDefault();
        });
    });
}

function showFieldError(field, message) {
    field.classList.add("is-invalid");
    let err = field.parentElement.querySelector(".form-error");
    if (!err) {
        err = document.createElement("div");
        err.className = "form-error";
        field.parentElement.appendChild(err);
    }
    err.textContent = message;
}

function clearFieldError(field) {
    field.classList.remove("is-invalid");
    const err = field.parentElement.querySelector(".form-error");
    if (err) err.remove();
}

/* ---------------- Progress Bar Animation ---------------- */
function animateProgressBars() {
    document.querySelectorAll(".progress-bar[data-value]").forEach((bar) => {
        const target = bar.getAttribute("data-value") + "%";
        bar.style.width = "0%";
        requestAnimationFrame(() => {
            setTimeout(() => { bar.style.width = target; }, 100);
        });
    });
}

/* ---------------- Lightweight toast notification helper ---------------- */
function showNotification(message, type = "info") {
    const el = document.createElement("div");
    el.className = `alert alert-${type}`;
    el.style.position = "fixed";
    el.style.bottom = "24px";
    el.style.right = "24px";
    el.style.zIndex = "9999";
    el.style.minWidth = "260px";
    el.style.boxShadow = "0 10px 30px rgba(0,0,0,0.15)";
    el.textContent = message;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 4000);
}
