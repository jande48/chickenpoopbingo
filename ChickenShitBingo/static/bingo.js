// 75 possible numbers
var usedNumbers = new Array(76);
var calledNumbers = new Array();
var goal = "line";
// https://github.com/noahpen/bingo-js

function init() {
    generateNewCard();
}

function generateNewCard() {
    // set all elements in usedNumbers array as false
    resetUsedNumbers();
    // loops 24 times because there are 24 squares (not including free square)
    for (var i = 0; i < 25; i++) {
        if (i == 12) // skip free square
            continue;
        // generates a number for each square
        generateSquare(i);
    }
}

function generateSquare(squareNum) {
    var currentSquare = "sq" + squareNum;
    var number;
    // array of column numbers
    var baseNumbers = new Array(0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4);
    // generates random number for each square (depends on column)
    newNumber = (baseNumbers[squareNum] * 15) + generateNewNum();
    // loop makes sure there are no duplicates
    while (usedNumbers[newNumber] == true) {
        newNumber = (baseNumbers[squareNum] * 15) + generateNewNum();
    }
    // sets the used number in the array as true so no duplicates
    usedNumbers[newNumber] = true;
    // sets the current square to the new number
    
    document.getElementById(currentSquare).value = (squareNum+1);
    //document.getElementById(currentSquare).setAttribute('checked', '0');

}

function generateNewNum() {
    // generates a random numbers between 1 and 15
    return Math.floor((Math.random() * 15) + 1); //15
}

function resetUsedNumbers() {
    // sets all elements of the usedNumbers array to false (resets the array)
    for (var i = 0; i < usedNumbers.length; i++) {
        usedNumbers[i] = false;
    }
}

// when clicked, generates a new random card
function generateAnotherCard() {
    resetUsedNumbers();
    generateNewCard();
    resetSquareColours();
}

// resets all squares except FREE to white
function resetSquareColours() {
    var resetSquareCredits = 0

    for (var i=0; i < 25; i++) {
        if (i ==12)
            continue;
        var currentSquare = document.getElementById("sq" + i);
        if (currentSquare.style.backgroundColor != "#ffffff")
            resetSquareCredits += 1;
            currentSquare.style.backgroundColor == "#ffffff";
    }

    console.log(resetSquareCredits)
    return resetSquareCredits;
}

function markSquare(square) {
    var currentSquare = document.getElementById(square);
    if (currentSquare.style.backgroundColor == "lightblue") 
        currentSquare.style.backgroundColor = "#ffffff";
        // console.log(jQuery("#credits").val());
        // var newCredits = parseInt(jQuery("#credits").text())-1;
        // jQuery("#credits").empty();
        // jQuery("#credits").append(toString(newCredits));
    else
        currentSquare.style.backgroundColor = "lightblue";
        // var newCredits = parseInt(jQuery("#credits").text())+1;
        // jQuery("#credits").empty();
        // jQuery("#credits").append(toString(newCredits));
    return;
};

function loadTheSavedCard(card) {
    var cardToLoad = JSON.parse(card)
    for (var i = 0; i < 25; i++) {
        var currentSquare = document.getElementById("sq" + i);
        if (cardToLoad[i] == 0) 
            currentSquare.style.backgroundColor = "#ffffff";
        else
            currentSquare.style.backgroundColor = "lightblue";
    };
    return;
};

function makeCard() {
    var text = '{'; 
    for (var i = 0; i < 25; i++) {
        var num = i.toString();
        var currentSquare = document.getElementById("sq" + i);
        if (currentSquare.style.backgroundColor == "lightblue")
            text += '"'+num+'":1,';
        else
            text +='"'+num+'":0,';
    };
    var cardJSON = text.slice(0, -1)+'}'
    return cardJSON;
};
