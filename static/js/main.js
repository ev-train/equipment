document.getElementById('sort-form').addEventListener("submit", sortList);

function sortList(event) {
    event.preventDefault();
    var el = document.getElementById('sort-form');
    var sort = el.sort.value;
    var new_first = document.getElementById('new-first');
    var old_first = document.getElementById('old-first');
    var name_sorted = document.getElementById('name-sorted');

    if(sort == "newfirst") {
        new_first.style.display = "block";
        old_first.style.display = "None";
        name_sorted.style.display = "None";
    }

    if(sort == "oldfirst") {
        new_first.style.display = "None";
        old_first.style.display = "block";
        name_sorted.style.display = "None";
    }

    if(sort == "namesorted") {
        new_first.style.display = "None";
        old_first.style.display = "None";
        name_sorted.style.display = "block";
    }
}

