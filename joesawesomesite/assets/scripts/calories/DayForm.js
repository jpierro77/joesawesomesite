class DayForm
{
    constructor(date, limit){
        this.date = date;
        this.limit = limit;
        this.foods = [];
    }

    total_calories(){
        var total_calories = 0;
        for (var i = 0; i < this.foods.length; i++){
            total_calories += parseInt(this.foods[i].calories);
        }

        return total_calories;
    }
}

class Food
{
    constructor(food_name, calories){
        this.foodname = food_name; //inconsistent naming convention but I really don't wanna break the page
        this.calories = calories;
    }
}

class UI
{
    static open_edit(){
       $('#day_form_inputs').show();
       $('#day_form_buttons').hide();
    }

    static save_food(food_name, calories){
        if(UI.validate_food(food_name, calories)){
            $("#food_list").append(
                `
                    <div class = 'food_item food_item_display'>
                        <div class= 'food_item_props'>
                            <p class = "food_name_display">${food_name}</p>
                            <p class = "calories_display">${calories}</p>
                        </div>
                        <div class = 'food_item_buttons'>
                            <button class = 'edit_food_btn' onClick ="event.preventDefault(); UI.edit_food($(this).parent().parent())">Edit</button>
                            <button class = 'remove_food_btn' onClick ="event.preventDefault(); UI.remove_food($(this).parent().parent())">Remove</button>
                        </div>
                    </div>
                `
             );

            UI.close_edit();
        }

   }
    static edit_food(element){
        UI.open_edit();
        var food_properties = element.children()[0];
        var food_buttons = element.children()[1];
        var food_name = $(food_properties.children[0])[0].innerText;
        var calories = $(food_properties.children[1])[0].innerText;
        $($(food_properties).children()[0]).attr('id', 'editing_name');
        $($(food_properties).children()[1]).attr('id', 'editing_calories');
        $(food_buttons).attr('id', 'editing_buttons');
        $(food_buttons).hide();
        $("input[name='foodname']").val(food_name);
        $("input[name='calories']").val(calories);
        $('#remove_food_btn').attr("disabled", true);
        $("#save_food_btn").attr(
        "onClick",
        "event.preventDefault(); UI.save_edit($('#food_name_input').val(), $('#calorie_input').val())");
    }
    static save_edit(food_name, calories){
        if(UI.validate_food(food_name, calories)){
            $('#editing_name').html(food_name);
            $('#editing_calories').html(calories);
            $('#editing_buttons').show();
            $('#edting_buttons').attr('id', '');
            $('#editing_name').attr('id', '');
            $('#editing_calories').attr('id', '');
            $('#day_form_inputs').hide();
            $("#save_food_btn").attr(
            "onClick",
            "event.preventDefault(); UI.save_food($('#food_name_input').val(), $('#calorie_input').val())");
            $('#remove_food_btn').attr("disabled", false);
            UI.close_edit();
        }
    }

    static close_edit(){
        $('input[name="foodname"]').val('');
        $('input[name="calories"]').val('');
        $('#day_form_inputs').hide();
        $('#day_form_buttons').show();
        $('#editing_buttons').show();
        $('#edting_buttons').attr('id', '');
    }

    static save_day(){
        var food_list = $(".food_item_display");
        var day_form = new DayForm($('input[name="date"]').val(), $('input[name="daily_limit"]').val());

        for(var i = 0; i < food_list.length; i++){
            var food_name = food_list[i].children[0].children[0].innerText;
            var calories = food_list[i].children[0].children[1].innerText;
            var food = new Food(food_name, calories);
            day_form.foods.push(food);
        }

        $.ajax({
            url: "newday/",
            type: "POST",
            data:{
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                day_data: JSON.stringify(day_form)
            },
            success: function(json){
                if(!json.error)
                    location.reload(true);
            }
        });
    }

    static clear_form(){
        $("#food_list").html("");
    }
    static remove_food(element){
        element.remove();
    }

    static close_form(){
        $('#addDateForm').hide();
    }

    //This function goes at the bottom because it messes up the text editor

    static validate_food(food_name, calories){
        if(/[~`!#$%\^&*+=\-\[\]\\';,/{}|\\":<>\?]/g.test(food_name) || food_name.length < 1){
            alert("Please Don't Use Symbols for Food Name");
            return false;
        }
        if(!$.isNumeric(calories)){
            alert("Please enter a numeric calorie value");
            return false;
        }
        return true;
    }

}

//Adding fix for enter keypress
$("#food_name_input").on("keydown", function(event){
    if(event.keyCode === 13){
        event.preventDefault();
    }

});

$("#calorie_input").on("keydown", function(event){
    if(event.keyCode === 13){
        event.preventDefault();
    }

});