var swap_speakers = function(block){
    var s1 = $(block).parents('.team').find('.speaker_1');
    var s2 = $(block).parents('.team').find('.speaker_2');
    var temp = s1.html();
    s1.html(s2.html());
    s2.html(temp);
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
