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
        "?country_id=" + $("#id_country_vk_id").val() +
        "&callback=loadCities"
    );
}

function getUniversitiesFromVK(){
    getDataFromVK(
        "https://api.vk.com/method/database.getUniversities?" +
        "?country_id=" + $("#id_country_vk_id").val() +
        "&city_id=" + $("#id_city_vk_id").val() +
        "&callback=loadUniversities"
    );
}

function loadCountries(result) {
    updateOptionsList("#id_country_vk_id", result);
    $("#id_city_vk_id").empty();
    $("#id_university_vk_id").empty();
    $("#id_country_vk_id").change(function() {getCitiesFromVK();});
    getCitiesFromVK();
}

function loadCities(result) {
    updateOptionsList("#id_city_vk_id", result);
    $("#id_university_vk_id").empty();
    $("#id_city_vk_id").change(function() {getUniversitiesFromVK();});
    getUniversitiesFromVK();
}

function loadUniversities(result) {
    updateOptionsList("#id_university_vk_id", result);
}

function updateOptionsList(id, data){
    $(id).empty();
    for (var key in data.response)
        $(id).append(new Option(data.response[key].title, data.response[key].cid));
}
