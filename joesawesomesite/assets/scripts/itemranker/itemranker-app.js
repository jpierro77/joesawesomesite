//Item class: Item on List
class Item
{
	constructor(item_name, votes, rank){
		this.item_name = item_name;
		this.votes = votes;
		this.rank = rank;
	}

}
class UI
{
	static addItemToTable(item, rank){
		const item_list = document.querySelector('#item-list');

		const row = document.createElement("tr");

		row.innerHTML = `
			<td>${rank}</td>
			<td>${item.item_name}</td>
			<td>${item.votes}</td>
			<td ><a href = "#" class="btn delete-btn delete">X</a></td>
			<td><a style = "display: none" href = "#" class = "btn vote-btn vote">+</a></td>
		` ;

		item_list.appendChild(row);
	}

	static deleteItem(el, item_list){
		if(el.classList.contains('delete')){
			var itemName = el.parentElement.parentElement.getElementsByTagName('td')[1].innerHTML
			for(var i = 0; i < item_list.length; i++){
				if(item_list[i].item_name === itemName){
					item_list.splice(i, 1);
					break;
				}
			}
			el.parentElement.parentElement.remove();

			if(item_list.length < 2){
				document.querySelector("#start-vote").disabled = true;
			}
			if(item_list.length < 1)
			    UI.disableSaveButton();

		}
	}

	static clearTable(){
		const item_list = document.querySelector('#item-list');
		item_list.innerHTML = "";
		document.querySelector("#start-vote").disabled = true;
	}

	static postToTwitter(list){
        $.ajax({
            url : "twitterpost/", // the endpoint
            type : "POST", // http method
            data : { item_list : list }, // data sent with the post request
            // handle a successful response
            success : function(json) {
                var win = window.open(json, '_blank');
  			    win.focus();
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                alert("Failed to make post!");
            }
        });
	}

	static saveList(save_data){
	    $.ajax({
            url: "savelist/",
            type: "POST",
            data: {save_data: JSON.stringify(save_data),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },

            success : function(data){
                //check for error saving the data
                if(!data.was_saved){
                    if(data.redirect_type === "none")
                        alert("Invalid form, failed to save!")
                    else if(data.redirect_type === "login"){
                        alert("Please sign in before creating a new list");
                        window.location.href = data.redirect_url
                    }
                }
                else{
                    var win = window.open(data.redirect_url);
                }

            },
            // handle a non-successful response
             error : function(xhr,errmsg,err) {
                    alert("Failed to make post!");
             }
        });
	}

	static enableStartButton(){
	    $("#start-vote").prop("disabled", false);
	}
	static enableSaveButton(){
	    $("#save-list").prop("disabled", false);
	}
	static disableStartButton(){
	    $("#start-vote").prop("disabled", true);
	}
	static disableSaveButton(){
	    $("#save-list").prop("disabled", true);
	}
   static setListType(){
        const item_list = document.querySelector('#item-list');
        if($("#listtype option:selected").val() === "personal" && globalItemList.length > 1){
            UI.enableStartButton();
        }else{
            if(globalItemList.length > 0)
                UI.enableSaveButton();
            UI.disableStartButton();
        }




    }

}

class Voting
{
	constructor(item_list){
		this.buttonIndex = 4;
		this.rowIndex1 = 0;
		this.rowIndex2 = 1;
		this.rowList = document.querySelector("#item-list").getElementsByTagName('tr');
		for(let element of this.rowList){
		    $(element).toggleClass("item-showing");
			element.cells[3].querySelector("a").style.display = "none";
			element.cells[4].querySelector("a").addEventListener('click', (e) =>{
				e.preventDefault();
				this.addVote(element.getElementsByTagName('td')[1].innerHTML);
			});
		}
		this.item_list = item_list;
	}

	showVoteButton(element){
		element.querySelector("a").style.display = '';
		$(element).parent().toggleClass('item-showing');
	}

	hideVoteButton(element){
		element.querySelector("a").style.display = "none";
		$(element).parent().toggleClass('item-showing');
	}

	addVote(itemName){

		//Add vote
		for(var i = 0; i < this.item_list.length; i++){
			if(this.item_list[i].item_name === itemName){
				this.item_list[i].votes += 1;
				break;
			}
		}
		if(this.rowIndex1 < this.rowList.length - 2){
			if(this.rowIndex2 < this.rowList.length - 1){
				this.hideVoteButton(this.rowList[this.rowIndex2].getElementsByTagName('td')[this.buttonIndex]);
				this.rowIndex2++;
				this.showVoteButton(this.rowList[this.rowIndex2].getElementsByTagName('td')[this.buttonIndex]);
			}else{
				this.hideVoteButton(this.rowList[this.rowIndex1].getElementsByTagName('td')[this.buttonIndex]);
				this.hideVoteButton(this.rowList[this.rowIndex2].getElementsByTagName('td')[this.buttonIndex]);
				this.rowIndex1++;
				this.rowIndex2 = this.rowIndex1 + 1;
				this.showVoteButton(this.rowList[this.rowIndex1].getElementsByTagName('td')[this.buttonIndex]);
				this.showVoteButton(this.rowList[this.rowIndex2].getElementsByTagName('td')[this.buttonIndex]);
			}
		}else{
			this.endVotes();
		}
	}

	displayVotes(){
		this.showVoteButton(this.rowList[this.rowIndex1].getElementsByTagName('td')[this.buttonIndex]);
		this.showVoteButton(this.rowList[this.rowIndex2].getElementsByTagName('td')[this.buttonIndex]);
	}
	endVotes(){
		this.hideVoteButton(this.rowList[this.rowIndex1].getElementsByTagName('td')[this.buttonIndex]);
		this.hideVoteButton(this.rowList[this.rowIndex2].getElementsByTagName('td')[this.buttonIndex]);
		
		//Bubble sort elements
		for(var i = 0; i < this.item_list.length; i++){
			for(var j = 0; j < this.item_list.length - i - 1; j++){
				if (this.item_list[j].votes < this.item_list[j+1].votes){
					let temp = this.item_list[j];
					this.item_list[j] = this.item_list[j+1];
					this.item_list[j+1] = temp;
				}
			}
		}

		UI.clearTable();
		var rank = 0;
		var prevVotes = -1;
		this.item_list.forEach(function(element){
		    if(prevVotes !== element.votes){
		        rank++;
		    }
		    element.rank = rank;
			UI.addItemToTable(element, rank);
			prevVotes = element.votes;
	    });

		document.querySelector("#start-vote").style.display = "";
		document.querySelector("#new-list").style.display = "";

		//document.querySelector("#share-twitter").disabled = false;
		document.querySelector("#save-list").disabled = false;
	}
}





var globalItemList = [];

document.addEventListener("DOMContentLoaded", function(){
    UI.disableStartButton(); UI.disableSaveButton();
});



document.getElementById('item-add').addEventListener('submit', (e) =>{

	e.preventDefault();
	const item_name = document.querySelector("#item").value;
	const votes = 0;
	const rank = document.querySelector("#item-list").getElementsByTagName('tr').length + 1;

	if(/[~`!#$%\^&*+=\-\[\]\\';,/{}|\\":<>\?]/g.test(item_name) || item_name.length < 1){
        alert("Please use valid characters")
    }else{
        const item = new Item(item_name, votes, rank);

	    UI.addItemToTable(item, rank);
	    globalItemList.push(item);

	    //clear item value
	    document.querySelector('#item').value = '';

        //see if you can enable button
        if(globalItemList.length > 1 && $("#listtype option:selected").val() === "personal"){
            UI.enableStartButton();
        }
        if(globalItemList.length > 0 && $("#listtype option:selected").val() === "master"){
            UI.enableSaveButton();
        }
    }
});

//Delete item
document.querySelector('#item-list').addEventListener('click', (e) =>{
	UI.deleteItem(e.target, globalItemList);
});

//DisplayVotes
document.querySelector("#start-vote").addEventListener('click', (e) =>{
	e.preventDefault();
	document.querySelector("#start-vote").style.display = "none";
	document.querySelector("#new-list").style.display = "none";
	var voting = new Voting(globalItemList);
	voting.displayVotes();
});

document.querySelector("#new-list").addEventListener('click', (e)=>{
	UI.clearTable();
	globalItemList = [];
});

/*document.querySelector("#share-twitter").addEventListener('click', (e)=>{
    e.preventDefault()
    var count = 0;
    var listString ="My Top "+globalItemList.length+ " " +document.querySelector("#typedisplay").innerHTML + ": \n";
    //list.title=document.querySelector("#typedisplay").innerHTML
    globalItemList.forEach(function(element){
        listString += (globalItemList.indexOf(element)+1) +". " + element.item_name +"\n "
    });
    UI.postToTwitter(listString);
    document.querySelector("#share-twitter").disabled = true;
}); */
document.querySelector("#save-list").addEventListener('click', (e)=>{
    e.preventDefault();
    //Prompt the user for a list title
    var failed = false;
    title = $("#listtitle").val();
    list_type = $("#listtype").val();
    if(/[~`!#$%\^&*+=\-\[\]\\';,/{}|\\":<>\?]/g.test(title) || title.length < 1){
        failed = true;
    }
    if(list_type !== "master" && list_type !== "personal"){
        failed = true;
    }

    var list = [];
    var save_data = {};

    globalItemList.forEach(function(element){
        if(/[~`!#$%\^&*+=\-\[\]\\';,/{}|\\":<>\?]/g.test(element.rank + element.item_name + element.votes)){
            failed = true;
        }
        list.push({
            "rank": element.rank,
            "item_name": element.item_name,
            "votes": element.votes
        });
    });
    save_data = {
        list_title: title,
        list_type: list_type,
        list: list
    };
   if (!failed){
        UI.saveList(save_data);
   }else{
        alert("Save failed, please check your form and don't use symbols.");
        failed = false;
   }
});
document.querySelector("#type-chooser").addEventListener('submit', (e) =>{
    e.preventDefault();
});