
document.addEventListener("DOMContentLoaded", () => {
    const message = document.getElementById("message");
    if (message) {
        document.getElementById("message").innerHTML;
        setTimeout(() => {
            document.getElementById("message").innerHTML = "";
        }, 5000)
    }
})