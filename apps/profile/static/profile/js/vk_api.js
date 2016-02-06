var FULL_COUNTRY_OPTION_ID = -1;
var FULL_COUNTRY_OPTION_LABEL = 'Полный список';
var DEFAULT_COUNTRY_ID = 1;
var DEFAULT_LANG = 'ru';
var Item = function(selector_id, selector_name, selector_list) {
    return {
        get: function() {
            return {
                id: $(selector_id).val(),
                name: $(selector_name).val()
            };
        },
        set: function(id, name) {
            $(selector_id).val(id);
            $(selector_name).val(name);
            return this;
        },
        unset: function() {
            $(selector_id).val('');
            $(selector_name).val('');
            $(selector_list).val('');
            return this;
        },
        list: function() {
            return $(selector_list);
        },
        disable: function() {
            $(selector_list).prop('disabled', true);
        },
        enable: function() {
            $(selector_list).prop('disabled', false);
        }
    }
};
var country = new Item('#id_country_id', '#id_country_name', '#countries');
var city = new Item('#id_city_id', '#id_city_name', '#city_list');
var university = new Item('#id_university_id', '#id_university_name', '#university_list');
var callback = null;


$(document).ready(function() {
    //VK.init({
    //    apiId: <apiId>
    //});
    loadCountries(false);
});


function getDataFromVK(url){
    var script = document.createElement('SCRIPT');
    script.src = url;
    document.getElementsByTagName('head')[0].appendChild(script);
}


function loadCountries(need_all) {
    need_all = need_all || country.get().id ? 1 : 0;
    var count = 1000; // all (max 255)

    callback = function (data) {
        country.list().empty();
        data.response.forEach(function(x) {
            country.list().append(new Option(x.title, x.cid));
        });
        if ( ! need_all) {
            country.list().append(new Option(FULL_COUNTRY_OPTION_LABEL, FULL_COUNTRY_OPTION_ID));
        }
        if (country.get().id) {
            country.list().val(country.get().id);
        } else {
            country.list().val(DEFAULT_COUNTRY_ID);
            country.set(country.list().val(), country.list().find('option:selected').text());
        }
        country.list().change(function() {
            country.set(this.value, this.options[this.selectedIndex].text);
            city.unset();
            university.unset();
            university.disable();
            loadCities();
        });
        loadCities();
    };

    getDataFromVK(
        'https://api.vk.com/method/database.getCountries' +
        '?need_all=' + need_all +
        '&count=' + count +
        '&lang=' + DEFAULT_LANG +
        '&callback=callback'
    );
    //VK.Api.call(
    //    'database.getCountries',
    //    {
    //        need_all: need_all,
    //        count: count
    //    },
    //    update_country_list
    //);
}


function loadCities(){
    if (country.get().id == FULL_COUNTRY_OPTION_ID) {
        loadCountries(true);
    }
    city.list().val(city.get().name);
    city.list().autocomplete({
        minLength: 0,
        source: function(request, response) {
            //VK.Api.call(
            //    'database.getCities',
            //    {
            //        need_all: 0,
            //        country_id: country.get().id,
            //        q: request.term
            //    },
            //    updateCityList
            //);
            callback = function (data) {
                if (typeof(data.response) !== 'object'){
                    return;
                }
                response(data.response
                        .filter(function(x) {
                            return typeof(x) === 'object';
                        })
                        .map(function(x) {
                            var desc = [];
                            if (x.area) {
                                desc.push(x.area);
                            }
                            if (x.region) {
                                desc.push(x.region);
                            }
                            return {
                                id: x.cid,
                                value: x.title,
                                label: x.title,
                                desc: desc.join(', ')
                            }
                        })
                );
            };

            getDataFromVK(
                'https://api.vk.com/method/database.getCities' +
                '?need_all=' + '0' +
                '&country_id=' + country.get().id +
                '&q=' + request.term +
                '&lang=' + DEFAULT_LANG +
                '&callback=callback'
            );
        },
        select: function(event, ui) {
            city.set(ui.item.id, ui.item.value);
        },
        change: function(event, ui) {
            if (ui.item){
                city.set(ui.item.id, ui.item.value);
                university.unset();
                university.enable();
                loadUniversities();
            } else {
                city.list().val(city.get().name);
            }
        }
    }).autocomplete('instance')._renderItem = function(ul, item) {
        return $('<li>').append('<a>' + item.label + '<br>' + '<span class="region">' + item.desc + '</span>' + '</a>').appendTo(ul);
    };
    if (city.get().id) {
        loadUniversities();
    } else {
        university.disable();
    }
}


function loadUniversities() {
    university.list().val(university.get().name);
    university.list().autocomplete({
        minLength: 0,
        source: function(request, response) {
            callback = function (data) {
                if (typeof(data.response) !== 'object'){
                    return;
                }
                response(data.response
                        .filter(function(x) {
                            return typeof(x) === 'object';
                        })
                        .map(function(x) {
                            return {
                                id: x.id,
                                value: x.title,
                                label: x.title
                            }
                        })
                );
            };
            getDataFromVK(
                'https://api.vk.com/method/database.getUniversities' +
                '?need_all=' + '0' +
                '&country_id=' + country.get().id +
                '&city_id=' + city.get().id +
                '&q=' + request.term +
                '&lang=' + DEFAULT_LANG +
                '&callback=callback'
            );
            //VK.Api.call(
            //    'database.getUniversities',
            //    {
            //        need_all: 0,
            //        country_id: country.get().id,
            //        city_id: city.get().id,
            //        q: request.term
            //    },
            //    updateCityList
            //);
        },
        select: function(event, ui) {
            university.set(ui.item.id, ui.item.value);
        },
        change: function(event, ui) {
            if (ui.item){
                university.set(ui.item.id, ui.item.value);
            } else {
                university.list().val(university.get().name);
            }
        }
    });
}
