function openModal(content_id) {
    var modal = document.getElementById("myModal");
    var modalBody = document.getElementById("modal-body");

    // Fetch content detail using AJAX
    fetch(`/recommand/content_detail/${content_id}/`)
        .then(response => response.text())
        .then(data => {
            modalBody.innerHTML = data;
            modal.style.display = "block";
        });
}

function closeModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}

window.onclick = function(event) {
    var modal = document.getElementById("myModal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
