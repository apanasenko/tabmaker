/**
 * Created by Alexander on 21.05.2015.
 */

var swap_speakers = function(block){
    var s1 = $(block).parents('.team').find('.speaker_1');
    var s2 = $(block).parents('.team').find('.speaker_2');
    var temp = s1.html();
    s1.html(s2.html());
    s2.html(temp);
};


$(document).ready(function(){
    var blocks = $('.reverse_speakers')
    for (var i = 0; i < blocks.length; i++) if ($(blocks[i]).is(':checked')) {
        swap_speakers(blocks[i]);
    }
    $('.reverse_speakers').change(function(){
        swap_speakers(this);
    });
});
