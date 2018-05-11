var submitting = false;
window.addEventListener('load', function () {
    var form = document.querySelector('.form');
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        if (submitting) {
            return;
        }
        submitting = true;

        var request = new XMLHttpRequest();
        request.onload = function () {
            document.querySelector('.token').value = this.responseText;
            document.querySelector('.form').submit();
        };
        request.open("GET", location.href + '?token', true);
        request.send();
    });
});