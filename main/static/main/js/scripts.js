$(function () {
    $('.accordion').accordion({
        active: true,
        heightStyle: 'content',
        header: '> .accordion-item > .accordion-header'
    });
});

function setPrice(price, volumeType) {
    document.getElementById('price').innerHTML = `Цена: ${price} руб.`;
    disableBtn(volumeType);
}

function disableBtn(volumeType) {
    var volumes = ['2.5ml', '5ml', '10ml'];
    var curVolume = volumes.indexOf(volumeType);    // Получаем индекс выбранного объёма

    if (curVolume !== -1) {
        volumes.splice(curVolume, 1);   // Удаление из массива элемента с выбранным объёмом
    }

    // Ставим к каждому из оставшихся в массиве элементов false к свойству 'disabled'
    volumes.forEach(function(elem) {
        document.getElementById(elem).disabled = false;
    });

    // В свойство 'disabled' выбранного объёма ставим true
    document.getElementById(volumeType).disabled = true;
}
