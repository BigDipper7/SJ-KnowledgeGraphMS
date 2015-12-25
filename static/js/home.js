
$("#btnSearch").click(function() {
    var entity1 = document.getElementById("entity1").value;
    var entity2 = document.getElementById("entity2").value;
    var level = document.getElementById("level").value;

    console.log(entity1 + " " + entity2 + " " + level)
    document.getElementById("data").submit();
});
