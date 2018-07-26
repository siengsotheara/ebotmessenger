$(document).ready(function () {
    // Get the modal
    var modal = $('#myModal');

    // When the user clicks on the button, open the modal
    $("#searchBtn").click(function () {
        modal.show();
    });

    // When the user clicks on <span> (x), close the modal
    $('.modal-body .close').click(function (e) {
        e.preventDefault();
        modal.hide();
    });

    $('form').submit(function () {
        modal.hide();
    });

    // When the user clicks anywhere outside of the modal, close it
    $(window).click(function (event) {
        if (event.target == modal[0]) {
            modal.hide();
        }
    });
});