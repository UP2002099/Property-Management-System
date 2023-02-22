$(document).ready(function() {
    function getRoomQty() {
        var roomQty = $("#roomQty").val()
        return roomQty;
    }

    function getCondition() {
        var condition = $("#conditionSelect").val()
        return condition;
    }

    $("#roomQty").click(function() {
        if (getRoomQty() != "none") {
            $("#rooms").prop("disabled", false)
        }
        else {
            $("#rooms").prop("disabled", true);
        }
    });

    $("#conditionSelect").click(function() {
        if (getCondition() != "none") {
            $("#condition").prop("disabled", false)
        }
        else {
            $("#condition").prop("disabled", true);
        }
    });
    
});