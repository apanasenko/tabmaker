const FULL_COUNTRY_OPTION_ID = -1;
const FULL_COUNTRY_OPTION_LABEL = 'Полный список';
const DEFAULT_COUNTRY_ID = 1;
const DEFAULT_LANG = 'ru';
const VK_API_VERSION = 5.93;
const VK_ACCESS_TOKEN = '0932ef530932ef5309e7d4df8b0974d6de009320932ef5351c01737d8ea58da939c9124';

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

$(document).ready(function() {
    loadCountries(false);
});


function getDataFromVK(url){
    var script = document.createElement('SCRIPT');
    script.src = url;
    document.getElementsByTagName('head')[0].appendChild(script);
}


function loadCountries(need_all) {
    need_all = need_all || country.get().id ? 1 : 0;

    $.get(
        'https://api.vk.com/method/database.getCountries',
        {
            need_all: need_all,
            count: 1000, // all (max 255)
            lang: DEFAULT_LANG,
            access_token: VK_ACCESS_TOKEN,
            v: VK_API_VERSION
        },
        function (data) {
            country.list().empty();
            data.response.items.forEach(function(x) {
                country.list().append(new Option(x.title, x.id));
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
        },
        'jsonp'
    );
}


function loadCities(){
    if (parseInt(country.get().id) === FULL_COUNTRY_OPTION_ID) {
        loadCountries(true);
        return;
    }
    city.list().val(city.get().name);
    city.list().autocomplete({
        minLength: 0,
        source: function(request, response) {
            $.get(
                'https://api.vk.com/method/database.getCities',
                {
                    country_id: country.get().id,
                    q: request.term,
                    need_all: 0,
                    lang: DEFAULT_LANG,
                    access_token: VK_ACCESS_TOKEN,
                    v: VK_API_VERSION
                },
                function (data) {
                    if (typeof(data.response) !== 'object') {
                        return;
                    }
                    response(data.response.items.map(function (x) {
                        var desc = [];
                        if (x.area) {
                            desc.push(x.area);
                        }
                        if (x.region) {
                            desc.push(x.region);
                        }
                        return {
                            id: x.id,
                            value: x.title,
                            label: x.title,
                            desc: desc.join(', ')
                        }
                    }));
                },
                'jsonp'
            );
        },
        focus: function() {
            university.enable();
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
            if (city.get().id) {
                university.enable();
            } else {
                university.disable();
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
            $.get(
                'https://api.vk.com/method/database.getUniversities',
                {
                    country_id: country.get().id,
                    city_id: city.get().id,
                    q: request.term,
                    need_all: 0,
                    lang: DEFAULT_LANG,
                    access_token: VK_ACCESS_TOKEN,
                    v: VK_API_VERSION
                },
                function (data) {
                    if (typeof(data.response) !== 'object'){
                        return;
                    }
                    response(data.response.items.map(function(x) {
                        return {
                            id: x.id,
                            value: x.title,
                            label: x.title
                        }
                    }));
                },
                'jsonp'
            );
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
