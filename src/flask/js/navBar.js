/* Set the width of the sidebar to 30% and the left margin of the page content to 30% */
function openNav() {
    if (window.innerWidth > 500) {
        document.getElementById("sidenav").style.width = "30%";
        document.getElementById("main").style.marginLeft = "30%";
    }
    else {
        document.getElementById("sidenav").style.width = "80%";
        document.getElementById("main").style.marginLeft = "80%";
    }
  document.getElementById("openbtn").style.display = "none";
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("sidenav").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
  document.getElementById("openbtn").style.display = "block";
}