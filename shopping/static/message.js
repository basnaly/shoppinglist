
document.addEventListener("DOMContentLoaded", () => {
    const message = document.getElementById("message");
    if (message) {
        document.getElementById("message").innerHTML;
        setTimeout(() => {
            document.getElementById("message").innerHTML = "";
            // window.location.replace(window.location.href);
        }, 10000)
    }
})