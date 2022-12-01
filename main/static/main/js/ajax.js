// Получение переменной cookie по имени
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Настройка AJAX
$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

function to_favorites()
{
    var current = $(this);
    var type = current.data('type');
    var pk = current.data('id');

    $.ajax({
        url : "/" + type + "/" + pk + "/favorite/",
        type : 'POST',
        data : { 'obj' : pk },

        success: (data) => {
            var el = jQuery('#fav_' + pk)
            if (el.hasClass(added_to_favorites_class))
                el.removeClass(added_to_favorites_class)
            else
                el.addClass(added_to_favorites_class)
        }
    });

    return false;
}

function to_cart()
{
    var current = $(this);
    var type = current.data('type');
    var pk = current.data('id');

    console.log('Тип: ' + type + '\npk: ' + pk);

    $.ajax({
        url : "/" + type + "/" + pk + "/cart/",
        type : 'POST',
        data : { 'obj' : pk },

//        success: (data) => {
//            var el = jQuery('#fav_' + pk)
//            if (el.hasClass(added_to_favorites_class))
//                el.removeClass(added_to_favorites_class)
//            else
//                el.addClass(added_to_favorites_class)
//        }
    });

    return false;
}
