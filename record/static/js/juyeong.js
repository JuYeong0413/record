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

