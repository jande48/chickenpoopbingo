
$(document).ready(function(){
    // {% if current_user.is_authenticated %}
    //     loadTheCardDifferent({{ current_user.card|tojson }})
    // {% endif %}
    $("#sq12").css('background-color', 'lightblue');
    $(".square").click(function(){
        if ($(this).attr('id') != "sq12" && $(this).css('backgroundColor') == "rgb(173, 216, 230)") var newCredits = parseInt($("#credits").text())+1;
          //console.log(newCredits)
        
        if ($(this).attr('id') != "sq12" && $(this).css('backgroundColor') == "rgb(255, 255, 255)" && parseInt($("#credits").text()) > 0) var newCredits = parseInt($("#credits").text())-1;
          //console.log(newCredits)
        
        $("#credits").text(newCredits);
        if ($(this).attr('id') != "sq12" && parseInt($("#credits").text()) > 0) markSquare($(this).attr('id'));
    })
    $("#saveCard").click(function(){
        var cardData = makeCard()
        
        $.post("/saveCard",{"myData": cardData})
        $("#message-div").empty()
        $("#message-div2").remove()
        $("#message-div").append("<div class='alert alert-success'>Your Card Has Been Saved! Check Upcoming Events!</div>")
        
    })
    $("#resetCard").click(function(){
        var addedCredits = resetSquareColours()
        newCredits = parseInt($("#credits").text())+addedCredits
        console.log(newCredits)
        $("#credits").text(newCredits);
    })
    $("#pleaseLogin").click(function(){
        $("#message-div").empty()
        $("#message-div2").remove()
        $("#message-div").append("<div class='alert alert-info'>Please Login to Play!</div>")
    })
  
});  

