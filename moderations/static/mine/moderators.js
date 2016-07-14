"use strict";
var remove_line = function() {
    // remove the parent div and recalc sum
    //selected_mods.delete .add("{{ moderator.user.username|lower }}");
    selected_mods.delete($(this).parent().find("input").val().toLowerCase());
    //console.log($(this).parent().text(), $(this).parent().val());
    $(this).parent().remove();
    return false;
};

var add_line = function() {
    // create a new div with text input field and - button
    var $new_li = $('<li class="list-group-item"></li>');
    var $new_button = $("<button class='pull-right btn remove'><i class='glyphicon glyphicon-minus-sign'/></button>");
    $(this).parent().append($new_li);
    $new_li.append($new_button);
    var $new_input = $('<input type="text"/>');
    //var $new_input = $('<select/>');
    $new_li.append($new_input);
    //for (let m of all_mods) {
    //    // todo: get rid of existing moderators
    //    $new_input.append($(`<option value="${m.value}">${m.label}</option>`));
    //}
    $new_input.autocomplete({
        source: function (request, response) {
            let res = $.map(all_mods, function (item) {
                if (item.label.toLowerCase().indexOf(request.term.toLowerCase()) >= 0 &&
                    !selected_mods.has(item.label.toLowerCase())) {
                    return item;
                }
            });
            console.log(res);
            response(res);
        },
        minLength: 0,
        change: function(event, ui) {
            if (!ui.item) {
                $(this).val('');
            }
        },
        select: function (event, ui) {
            //console.log('selected ' + ui.item.label);
            event.preventDefault();
            $(this).val(ui.item.label);
            selected_mods.add(ui.item.label.toLowerCase());
            //$("#group_id").val(ui.item.value);
            //console.log($("#autocomplete-group"));
        },
        open: function () {
            $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
        },
        close: function () {
            $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
        }
    });
    return false;
};

var bind_callbacks = function() {
    $(document).on("click", ".add", add_line);
    $(document).on("click", ".remove", remove_line);
};

$(function() {

    bind_callbacks();

});

