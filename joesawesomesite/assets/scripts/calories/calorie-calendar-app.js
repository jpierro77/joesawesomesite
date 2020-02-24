var prev_selected_day;
document.addEventListener('DOMContentLoaded', function() {
    var logged_in = document.getElementById('user-authenticated').innerText;
    if(logged_in === "True")
        calendarEl = document.getElementById('calendar');
    else
        calendarEl = document.getElementById('calendar-unselectable');
    if(logged_in === "True"){
        try{
            var events_array = [];
            content = document.getElementById('days-data').textContent.replace(/\\/g, '');
            var daysJson = JSON.parse(content).content.days;
            daysJson.forEach(function(element){
                events_array.push({
                    "title": addCalories(element) + "/"+element.limit+" cal",
                    "start": element.date
                });
            });
            var calendar = new FullCalendar.Calendar(calendarEl, {
                plugins: [ 'dayGrid', 'list', 'interaction'],
                events: events_array,
                dateClick: function(info) {
                    try{
                        $(prev_selected_day).css("background-color", "white");
                    }catch(exception){}
                    prev_selected_day = info.dayEl;
                    $("input[name=date]").val(info.dateStr)
                    $(info.dayEl).css("background-color", "green");
                    $("#addDateForm").css("display", "block");
                    clearForm();
                    popUpForm(daysJson, info.dateStr);
              }
            });
        }catch(exception){
             var calendar = new FullCalendar.Calendar(calendarEl, {
                plugins: [ 'dayGrid', 'list', 'interaction'],
                dateClick: function(info) {
                    try{
                        $(prev_selected_day).css("background-color", "white");
                    }catch(exception){}
                    prev_selected_day = info.dayEl;
                    $("input[name=date]").val(info.dateStr);
                    $(info.dayEl).css("z-index", "10000");
                    $(info.dayEl).css("background-color", "green");
                    $("#addDateForm").css("display", "block");
                    $("#calendar-cover").css("display", "block");
              }
            });
        }
     }
     else{
        var calendar = new FullCalendar.Calendar(calendarEl, {
            plugins: ['dayGrid']
        });
     }
    calendar.render();
});


function hideForm(){
    $("#addDateForm").css("display", "none");
    $(prev_selected_day).css("background-color", "white");
}
