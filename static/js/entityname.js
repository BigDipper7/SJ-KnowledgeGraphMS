var g;
var relations;
var temp_data;
var description;
var attPics;
var attVids;
var attTxts;

$(document).ready(function() {

    var entity = document.getElementById("entity_name").innerHTML;

    var selectedQueryLanguage = "gremlin";
    var postData = "g.V(\"" + entity + "\").Tag(\"source\").Out(null, \"relation\").Tag(\"target\").All()";
    $.ajax({
        type: 'POST',
        url: "/sjkg/ajax/entity/" + entity,
        crossDomain: true,
        success: function(data) {
            temp_data = data;
            document.getElementById("graph-container").innerHTML = "";
            createGraphVisualization(data, null);
            addEntities();
            addRelations();
            addAttributes();
        },
        dataType: "json"
    });

})

function addEntities() {
    var entitiyDiv = document.getElementById("entities");
    var nodes = g.nodes;

    if (nodes.length > 0) {
        entitiyDiv.style.visibility = "visible";
        entitiyDiv.innerHTML = "<h5>按实体浏览</h5>";
    }
    for (var i = 0; i < nodes.length; i++) {
        entitiyDiv.innerHTML += "<button type=\"button\" class=\"btn btn-info\" onclick=\"visual_entity(this.innerHTML)\">" + nodes[i].label + "</button>&nbsp;&nbsp;";
    }
}

function addRelations() {
    var relationDiv = document.getElementById("relations");

    if (relations.length > 0) {
        relationDiv.style.visibility = "visible";
        relationDiv.innerHTML = "<h5>按关系浏览</h5>";
    }

    for (var i = 0; i < relations.length; i++) {
        relationDiv.innerHTML += "<button type=\"button\" class=\"btn btn-info\" onclick=\"visual_relation(this.innerHTML)\">" + relations[i] + "</button>&nbsp;&nbsp;";
    }
}

function addAttributes() {

    var attributesDiv = document.getElementById("attributes");
    attributesDiv.style.visibility = "hidden";

    if (attTxts.length != 0 || attPics.length != 0 || attVids.length != 0) {
        attributesDiv.style.visibility = "visible";
        attributesDiv.innerHTML = "<h5>按属性浏览</h5>";
    }

    if (attTxts.length != 0) {
        attributesDiv.innerHTML += "<hr><h6>文字属性</h6>";

        for (var i = 0; i < attTxts.length; i++) {
            var txt = attTxts[i];

            var new_button = "<button type=\"button\" class=\"btn btn-default btn-info\" data-container=\"body\" data-toggle=\"popover\" data-placement=\"bottom\" data-content=\"";
            new_button += txt.value + "\">" + txt.name + "</button>&nbsp;&nbsp;";

            attributesDiv.innerHTML += new_button;
        }
    }

    if (attPics.length != 0) {
        attributesDiv.innerHTML += "<hr><h6>图片属性:</h6>";
        for (var i = 0; i < attPics.length; i++) {
            var pic = attPics[i];

            var pic_button = "<a href=\"" + pic.target + "\" target=\"_blank\"><button type=\"button\" class=\"btn btn-pic btn-info\">" + pic.source + (i+1) +  "</button></a>&nbsp;&nbsp;";
            attributesDiv.innerHTML += pic_button;
        }
    }

    if (attVids.length != 0) {
        attributesDiv.innerHTML += "<hr><h6>视频属性:</h6>";
        for (var i = 0; i < attVids.length; i++) {
            var vid = attVids[i];

            var video_button = "<a href=\"" + vid.target + "\" target=\"_blank\"><button type=\"button\" class=\"btn btn-pic btn-info\">" + pic.source + (i+1) + "</button></a>&nbsp;&nbsp;";
            attributesDiv.innerHTML += video_button;
        }
    }

    $('[data-toggle="popover"]').popover();
    console.log(attributesDiv.innerHTML);
}


function visual_relation(name) {
    document.getElementById("graph-container").innerHTML = "";
    createGraphVisualization(temp_data, name)
}

function visual_entity(name) {
    var selectedQueryLanguage = "gremlin";
    var postData = "g.V(\"" + name + "\").Tag(\"source\").Out(null, \"relation\").Tag(\"target\").All()";
    //console.log(postData);
    $.ajax({
        type: 'POST',
        url: "/sjkg/ajax/entity/" + name,
        crossDomain: true,
        success: function(data) {
            //console.log(data);
            temp_data = data;
            document.getElementById("graph-container").innerHTML = "";
            createGraphVisualization(data, null);
            addEntities();
            addRelations();
            addAttributes();
        },
        dataType: "json"
    });
}

function relation_exist(relation_name) {
    for (var i = 0; i < relations.length; i++) {
        if (relations[i] == relation_name) {
            return true;
        }
    }
    return false;
}

function createGraphVisualization(data, relation_name) {
    
    //if (window.sigmaGraph) {
    //    sigmaGraph.kill();
    //}

    var results = data.result;

    var nodeMap = {};
    g = {nodes:[], edges: []};

    var result, source, target, source_color, target_color;

    relations = new Array();
    attPics = new Array();
    attVids = new Array();
    attTxts = new Array();
    description = undefined;
    for (var i = 0; i < results.length; i++) {
        result = results[i];

        if (containAttributes(result.relation)) {

            if (result.relation[10] == '图') {
                console.log("图片");
                attPics.push(result);
            } else if (result.relation[10] == '视') {
                console.log("视频");
                attVids.push(result);
            } else {
                console.log(result.relation);
                hehe = result.relation.substring(10);
                console.log(result.relation.substring(10));
                attTxts.push({'name': hehe, 'value': result.target});
            }

            continue;
        }

        if (!relation_exist(result.relation)) {
            relations.push(result.relation);
        }

        if (relation_name == null || (relation_name != null && result.relation == relation_name)) {
            source = result.source;
            target = result.target;

            source_color = "#001B8A";
            target_color = "#F09300";

            if (nodeMap[source] !== true) {
                var data = {
                    id: source,
                    x: Math.random(),
                    y: Math.random(),
                    size: 10,
                    color: source_color
                };
                data.label = source;
                g.nodes.push(data);
                nodeMap[source] = true;
            }

            if (nodeMap[target] !== true) {
                var data = {
                    id: target,
                    x: Math.random(),
                    y: Math.random(),
                    size: 10,
                    color: target_color
                };
                data.label = target;
                g.nodes.push(data);
                nodeMap[target] = true;
            }

            g.edges.push({
                id: "e" + i,
                label: result.relation,
                source: source,
                target: target,
                size: 5,
                color: '#ccc',
                hover_color: '#000',
                type: 'curvedArrow'
            })
        }

    }
    sigma.renderers.def = sigma.renderers.canvas;
    sigmaGraph = new sigma({
        graph: g,
        container: 'graph-container',
        settings: {
            doubleClickEnabled: false,
            minEdgeSize: 0.5,
            maxEdgeSize: 4,
            enableEdgeHovering: true,
            edgeHoverColor: 'edge',
            defaultNodeColor: '#ec5148',
            edgeLabelSize: 'proportional',
            defaultEdgeHoverColor: '#000',
            defaultEdgeLabelSize: 15,
            defaultLabelSize: 15,
            edgeHoverSizeRatio: 1,
            edgeHoverExtremities: true
        }
    });

    var dragListener = sigma.plugins.dragNodes(sigmaGraph, sigmaGraph.renderers[0]);
}

function containAttributes(a) {
    if (a.length > 9) {
        if (a[0] == "a" && a[1] == "t" && a[2] == "t") {
            return true;
        }
    }
    return false;
}
