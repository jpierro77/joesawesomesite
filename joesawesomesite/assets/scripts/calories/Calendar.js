class CalendarUI{
    static pop_up_form(days, date_str){
        var date = CalendarUI.find_date(days, date_str);
        if(date){
            CalendarUI.fill_day(date);
            $('input[name=daily_limit]').val(date.limit);
        }else{
            $('input[name=daily_limit]').val($("#daily-limit")[0].innerText);
        }
    }

    static find_date(days, date_str){
        var day = false;
        days.forEach(function(element){
            if(element.date == date_str){
                day = element;
            }
        });

        return day;
    }

    static fill_day(date){
        date.foods.forEach(function(element){
            UI.save_food(element.foodname, element.calories);
        });
    }

    static convert_datestr(date_str){
        var dates = date_str.split("-");
        return (dates[1] + "/"+dates[2]+"/"+dates[0]);
    }
}
class Calendar{
    constructor(cal_id){
        this.cal_id = cal_id;
        this.prev_selected_day = '';
    }
    render_calendar(){
        var calendarEl = document.getElementById(this.cal_id);
        if(this.cal_id == "calendar"){
            try{
                var events_array = [];
                content = document.getElementById('days-data').textContent.replace(/\\/g, '');
                var days_json = JSON.parse(content).content.days;
                days_json.forEach(function(element){
                    var day = new DayForm(element.date, element.limit);
                    day.foods = element.foods;
                    events_array.push({
                        "title": day.total_calories() + "/"+element.limit+" cal",
                        "start": element.date
                    });
                });
                var calendar = new FullCalendar.Calendar(calendarEl, {
                    plugins: [ 'dayGrid', 'list', 'interaction'],
                    events: events_array,
                    dateClick: function(info) {
                        try{
                            $(this.prev_selected_day).css("background-color", "#f4e1d2");
                        }catch(except){}
                        UI.clear_form();
                        this.prev_selected_day = info.dayEl;
                        $("input[name=date]").val(info.dateStr)
                        $("#date_label").html("Your " + CalendarUI.convert_datestr(info.dateStr));
                        //$(info.dayEl).css("background-color", "green");
                        $("#addDateForm").css("display", "block");
                        UI.clear_form();
                        CalendarUI.pop_up_form(days_json, info.dateStr);
                  }
                });
            }catch(exception){
                 var calendar = new FullCalendar.Calendar(calendarEl, {
                    plugins: [ 'dayGrid', 'list', 'interaction'],
                    dateClick: function(info) {
                        try{
                            $(this.prev_selected_day).css("background-color", "#f4e1d2");
                        }catch(exception){}
                        UI.clear_form();
                        this.prev_selected_day = info.dayEl;
                        $("input[name=date]").val(info.dateStr);
                        $("#date_label").html("Your " + CalendarUI.convert_datestr(info.dateStr));
                        //$(info.dayEl).css("background-color", "green");
                        $("#addDateForm").css("display", "block");
                  }
                });
            }

            calendar.render();
        }

    }
}

document.addEventListener('DOMContentLoaded', function() {
    var logged_in = document.getElementById('user-authenticated').innerText;
    if(logged_in === "True")
        calendar = new Calendar('calendar');
    else
        calendar = new Calendar('calendar-unselectable');

    calendar.render_calendar();

});
