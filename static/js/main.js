function menuFunction() {
    document.getElementById("menuDropdown").classList.toggle("show");
}
// Close the dropdown menu if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('.menu-dropbtn')) {
        var dropdowns = document.getElementsByClassName("menu-dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
                var openDropdown = dropdowns[i];
                if (openDropdown.classList.contains('show')) {
                        openDropdown.classList.remove('show');
                }
            }
        }
    }

