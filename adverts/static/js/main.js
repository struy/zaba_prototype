$(document).ready(function () {
    $('.navbar-toggler[data-target="#navbarSupportedContent"]').off('click').click(function (event) {
        $('#navbarSupportedSubContent').removeClass('show');
    });

    $('.nav-item[data-target="#navbarSupportedSubContent"]').off('click').click(function (event) {
        $('#navbarSupportedContent').removeClass('show');
    });
});

// jQuery counterUp
$('[data-toggle="counter-up"]').counterUp({
    delay: 10,
    time: 1000
});

