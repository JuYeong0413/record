// 가사 펼치기, 접기
$('#show_lyrics').click(function() {
    $('#hide_lyrics').removeClass('hide');
    $('#show_lyrics').addClass('hide');

    $('#lyrics').removeClass('hide');
});

$('#hide_lyrics').click(function() {
    $('#show_lyrics').removeClass('hide');
    $('#hide_lyrics').addClass('hide');

    $('#lyrics').addClass('hide');
});

// 모바일 버전 메인페이지 placeholder
$(document).ready(function() {
    if($(window).width() < 800) {
        $("#main-placeholder").attr("placeholder", "플레이리스트 검색");
    }
});
