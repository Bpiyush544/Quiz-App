
//--------------------toggle sidebar --------------------------------------------

let sidebar = document.querySelector(".sidebar");
let main = document.querySelector("main");
function togside() {
    sidebar.classList.toggle("show");
    main.classList.toggle("move")
}

let cut = document.querySelector(".cut");
cut.addEventListener("click", () => {
    sidebar.classList.remove("show");
    main.classList.remove("move")
})

