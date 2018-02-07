$(document).ready(function(){
    var getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

        for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
        }
    };

    var keyword = getUrlParameter('keywords');

    // console.log($('.article-entry-sum').html());

    $('.article-entry-title').each(function () {
        console.log($(this));
        $(this).html($(this).html().replace(keyword,"<b class='search-keyword'>"+keyword+"</b>"));
    });
    $('.article-entry-sum').each(function () {
        console.log($(this));
        $(this).html($(this).html().replace(keyword,"<b class='search-keyword'>"+keyword+"</b>"));
    });
    // var val_summary = $('.article-entry-sum').html();
    //
    // val_title = val_title.replace(keyword,"<b class='search-keyword'>"+keyword+"</b>");
    // val_summary = val_summary.replace(keyword,"<b class='search-keyword'>"+keyword+"</b>");
    //
    // $('.article-entry-title').html(val_title);
    // $('.article-entry-sum').html(val_summary);

});

