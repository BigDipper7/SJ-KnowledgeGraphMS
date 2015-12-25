/**
 * Created by MP on 15-5-11.
 */

var g;

$('input[type=file]').bootstrapFileInput();

$(document).ready(function() {
    var relationsHTML = document.getElementById("relations").innerHTML;
    if (relationsHTML.trim() != "") {
        var relationsJson = $.parseJSON(relationsHTML).relations;
        createRelationGraph(relationsJson);
    }
});

function createRelationGraph(relations) {
    var nodeMap = {};
    g = {nodes: [], edges: []};

    var result, source, target, edge_color, node_color;

    var flag0_color = "#9932cc";
    var flag1_color = "#335da8";

    node_color = "#F09300";

    for (var i = 0; i < relations.length; i++) {
        result = relations[i];
        if (containAttributes(result.relation)) {
            continue;
        }

        source = result.source;
        target = result.target;

        if (result.flag == 0) {
            edge_color = flag0_color;
        } else {
            edge_color = flag1_color;
        }

        if (nodeMap[source] !== true) {
            var data = {
                id: source,
                x: Math.random(),
                y: Math.random(),
                size: 10,
                color: node_color
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
                color: node_color
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
            color: edge_color,
            hover_color: '#000',
            type: 'curvedArrow'
        })
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