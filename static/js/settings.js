// Select all sidebar buttons
const tabButtons = document.querySelectorAll(".tab-btn");

// Select all content sections
const tabContents = document.querySelectorAll(".tab-content");

// Function to open a tab
function openTab(tabName) {

    // Remove active class
    tabButtons.forEach(btn => btn.classList.remove("active"));
    tabContents.forEach(content => content.classList.remove("active"));

    // Activate selected button
    document
        .querySelector(`[data-tab="${tabName}"]`)
        .classList.add("active");

    // Activate selected content
    document
        .getElementById(tabName)
        .classList.add("active");

    // Save active tab
    localStorage.setItem("activeTab", tabName);
}

// Sidebar click
tabButtons.forEach(button => {

    button.addEventListener("click", () => {

        openTab(button.dataset.tab);

    });

});

// Restore last opened tab
const savedTab = localStorage.getItem("activeTab");

if (savedTab) {

    openTab(savedTab);

} else {

    openTab("profile");

}

const slider = document.getElementById("voice_volume");
const value = document.getElementById("volume-value");

if (slider && value) {

    value.textContent = slider.value;

    slider.oninput = function () {
        value.textContent = this.value;
    };

}