$(function() {
    $("#id_name").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: `https://graph.facebook.com/search?access_token=EAALmkmmgVssBAE0F3F9laFTXr8KUSPB2m9E3ttt3Xs17z1xb9t1EsvAijVoypSSqJrbkyJPlyAzQnuQgwfKX308TozyqRoaZCwtzEyA5mjKeDKGcTyrL5andZAZB9hOTefnDBBif2vtuatTjr8AgQ5eZCUdIPyAZD&q=${request.term}&type=group&callback=?`,
                dataType: "jsonp",
                data: {
                    featureClass: "P",
                    style: "full",
                    maxRows: 12//,
                    //name_startsWith: request.term
                },
                success: function (data) {
                    res = $.map(data.data, function (item) {
                        if (item.name.toLowerCase().indexOf(request.term.toLowerCase()) >= 0) {

                            return {
                                label: item.name,
                                value: item.id
                            }
                        }
                    });
                    response(res);
                }
            });
        },
        minLength: 0,
        //select: function (event, ui) {
        //    console.log('selected ' + ui.item.label);
        //    $("#autocomplete-group").attr('value', ui.item.label);
        //    console.log($("#autocomplete-group"));
        //},
        open: function () {
            $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
        },
        close: function () {
            $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
        },
    });
    //$("form").submit(function () {
    //    var data = {
    //        name: $("#autocomplete-group").val(),
    //    };
    //    $.post("http://myfbfilter.dev:8000/create/", data, function (resp) {
    //        var el = $(resp);
    //        //$("#comments").prepend(el);
    //        //form.get(0).reset();
    //    });
    //    return false;
    //});

    //$("body").on("submit", "#likeform", submit_like);
    //
    //$("#rate").on("change", submit_rating);
});
