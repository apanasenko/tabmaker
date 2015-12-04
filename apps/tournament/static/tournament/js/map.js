ymaps.ready(init);


function update_location(text, lon, lat){
    $("#id_location_lon").val(lon);
    $("#id_location_lat").val(lat);
    $("#id_location").val(text);
}


function init () {
    var lon = $("#id_location_lon").val().replace(',', '.');
    var lat = $("#id_location_lat").val().replace(',', '.');
    var can_edit = Boolean($("#id_location").size());
    var map = new ymaps.Map("map", {
        center: [lon, lat],
        zoom: 14
    });

    var placemark = new ymaps.Placemark([lon, lat], {
        iconContent: "Место проведения турнира",
        hintContent: "Перетащите метку для указания адреса"
    }, {
        balloonPanelMaxMapArea: 0,
        draggable: can_edit,
        preset: "islands#blueStretchyIcon",
        openEmptyBalloon: true
    });

    placemark.events.add('balloonopen', function (e) {
        placemark.properties.set('balloonContent', "Идет загрузка данных...");
        ymaps.geocode(placemark.geometry.getCoordinates(), {
            results: 1
        }).then(function (res) {
            var newContent = res.geoObjects.get(0) ?
                res.geoObjects.get(0).properties.get('name') :
                'Не удалось определить адрес.';
            placemark.properties.set('balloonContent', newContent);
        });
    });

    if(can_edit) {
        placemark.events.add('dragend', function (e) {

            ymaps.geocode(placemark.geometry.getCoordinates(), {
                results: 1
            }).then(function (res) {
                update_location(
                    res.geoObjects.get(0).properties.get('text'),
                    placemark.geometry.getCoordinates()[0],
                    placemark.geometry.getCoordinates()[1]
                );
            });
        });

        map.events.add('click', function (e) {
            placemark.geometry.setCoordinates(e.get('coords'));
            ymaps.geocode(e.get('coords'), {
                results: 1
            }).then(function (res) {
                update_location(
                    res.geoObjects.get(0).properties.get('text'),
                    placemark.geometry.getCoordinates()[0],
                    placemark.geometry.getCoordinates()[1]
                );
            });
        });
    }

    map.geoObjects.add(placemark);
}
