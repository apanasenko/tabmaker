var swap_speakers = function(block){
    var s1 = $(block).parents('.team').find('.speaker_1');
    var s2 = $(block).parents('.team').find('.speaker_2');
    if ($(block).is(':checked')){
        s2.insertBefore(s1);
    } else {
        s1.insertBefore(s2);
    }
};

$(document).ready(function(){
    $('.reverse_speakers').each(function () {
        $(this).change(function(){
            swap_speakers(this);
        });
        if ($(this).is(':checked'))
            swap_speakers(this);
    });
});
