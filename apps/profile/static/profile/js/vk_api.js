/**
 * Created by Alexander on 05.04.2015.
 */

$(document).ready(function() {
    getCountriesFromVK();
});

function getDataFromVK(url){
    var script = document.createElement('SCRIPT');
    script.src = url;
    document.getElementsByTagName("head")[0].appendChild(script);
}

function getCountriesFromVK(){
    getDataFromVK("https://api.vk.com/method/database.getCountries?callback=loadCountries");
}

function getCitiesFromVK(){
    getDataFromVK(
        "https://api.vk.com/method/database.getCities" +
        "?country_id=" + $("#id_country_id").val() +
        "&callback=loadCities"
    );
}

function getUniversitiesFromVK(){
    getDataFromVK(
        "https://api.vk.com/method/database.getUniversities?" +
        "?country_id=" + $("#id_country_id").val() +
        "&city_id=" + $("#id_city_id").val() +
        "&callback=loadUniversities"
    );
}

function loadCountries(result) {
    updateOptionsList("#id_country_id", result, 'cid');
    $("#id_city_id").empty();
    $("#id_university_id").empty();
    $("#id_country_id").change(function() {
        getCitiesFromVK();
    });
    getCitiesFromVK();
    $("#id_country_id").material_select();
}

function loadCities(result) {
    updateOptionsList("#id_city_id", result, 'cid');
    $("#id_university_id").empty();
    $("#id_city_id").change(function() {
        getUniversitiesFromVK();
    });
    getUniversitiesFromVK();
    $("#id_city_id").material_select();
}

function loadUniversities(result) {
    updateOptionsList("#id_university_id", result, 'id');
    $("#id_university_id").change(function () {
        updateHiddenInput();
    });
    $('#id_university_id').material_select();
}

function updateHiddenInput(){
    $("#id_country_name").val($("#id_country_id option:selected").text());
    $("#id_city_name").val($("#id_city_id option:selected").text());
    $("#id_university_name").val($("#id_university_id option:selected").text());
}

function updateOptionsList(select_id, data, id){
    $(select_id).empty();
    for (var key in data.response)
        $(select_id).append(new Option(data.response[key].title, data.response[key][id]));

    // ===================================================================================
    // Костыль, нужно разобратья как исправить TODO исправить
    $('#' + $(select_id).parent().children()[0].getAttribute("data-activates")).remove()
    $(select_id).parent().children()[0].remove()
    $(select_id).removeClass("initialized")
    // ===================================================================================
}

// TODO Добавить в combobox функцию ввода и автодополнеия http://jqueryui.com/autocomplete/#combobox