document.addEventListener("DOMContentLoaded", function() {
    const button = document.getElementById("auraButton");

    // Create the aura element
    const aura = document.createElement("div");
    aura.classList.add("aura");
    button.appendChild(aura);

    // Remove the aura when mouse leaves
    button.addEventListener("mouseleave", function() {
        aura.style.transform = "translate(-50%, -50%) scale(0)";
    });

    // Add event listener for mouse enter to show aura
    button.addEventListener("mouseenter", function() {
        aura.style.transform = "translate(-50%, -50%) scale(1)";
    });
});