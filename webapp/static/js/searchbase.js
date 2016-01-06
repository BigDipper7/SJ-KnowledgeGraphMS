var x = Math.random();
var y = Math.random();

var bg;

$(document).ready(function() {
    var hiddenDiv = document.getElementById("hidden_relations");
    var relations = $.parseJSON(hiddenDiv.innerHTML)["relations"];
    var panelBodyDivs = document.getElementsByClassName("panel-body");
    for (var i = 0; i < relations.length; i++) {
        var temp_relation = relations[i];
        var panelBody = panelBodyDivs[i];
        panelBody.id = "panel" + i;
        createGraph(temp_relation, panelBody.id);
    }
    createTotalGraph(relations, "graph-container")
});

function createTotalGraph(relationss, divID) {
    var nodeMap = {};
    bg = {nodes: [], edges: []}
    var relations, relation, source, target, source_color, target_color;

    source_color = "#9932cc";
    target_color = "#335da8";

    for (var j = 0; j < relationss.length; j++) {
        relations = relationss[j];
        for (var i = 0; i < relations.length; i++) {
            relation = relations[i];
            source = relation.source;
            target = relation.target;

            var color = "#F09300";


            if (i !== 0 && nodeMap[source] !== true) {
                var data = {
                    id: source,
                    x: Math.random(),
                    y: Math.random(),
                    size: 20,
                    color: color
                };
                data.label = source;
                bg.nodes.push(data);
                nodeMap[source] = true;
            } else if (nodeMap[source] !== true) {
                var data = {
                    id: source,
                    x: Math.random(),
                    y: Math.random(),
                    size: 20,
                    color: source_color
                };
                data.label = source;
                bg.nodes.push(data);
                nodeMap[source] = true;
            }

            if (i !== relations.length - 1 && nodeMap[target] !== true) {
                var data = {
                    id: target,
                    x: Math.random(),
                    y: Math.random(),
                    size: 20,
                    color: color
                };
                data.label = target;
                bg.nodes.push(data);
                nodeMap[target] = true;
            } else if (nodeMap[target] !== true) {
                var data = {
                    id: target,
                    x: Math.random(),
                    y: Math.random(),
                    size: 20,
                    color: target_color
                };
                data.label = target;
                bg.nodes.push(data);
                nodeMap[target] = true;
            }

            bg.edges.push({
                    id: "be" + j + i,
                    label: relation.relation,
                    source: source,
                    target: target,
                    size: 8,
                    color: '#ccc',
                    hover_color: '#000',
                    type: 'curvedArrow'
            })
        }
    }

    sigma.renderers.def = sigma.renderers.canvas;
    sigmaGraph = new sigma({
        graph: bg,
        container: divID,
        settings: {
            doubleClickEnabled: false,
            minEdgeSize: 0.5,
            maxEdgeSize: 5,
            enableEdgeHovering: true,
            edgeHoverColor: 'edge',
            defaultNodeColor: '#ec5148',
            edgeLabelSize: 'proportional',
            defaultEdgeLabelSize: 15,
            defaultLabelSize: 15,
            defaultEdgeHoverColor: '#000',
            edgeHoverSizeRatio: 1,
            edgeHoverExtremities: true
        }
    });
    var dragListener = sigma.plugins.dragNodes(sigmaGraph, sigmaGraph.renderers[0])
}

function createGraph(relations, panelID) {
    var nodeMap = {};
    var g = {nodes:[], edges:[]};
    var relation, source, target, source_color, target_color;

    for (var i = 0; i < relations.length; i++) {
        relation = relations[i];
        source = relation.source;
        target = relation.target;

        var color = "#F09300";

        if (nodeMap[source] !== true) {
            var data = {
                id: source,
                x: x,
                y: y,
                size: 20,
                color: color
            };
            data.label = source;
            g.nodes.push(data);
            nodeMap[source] = true;
        }

        x = x + 1.0;

        if (nodeMap[target] !== true) {
            var data = {
                id: target,
                x: x,
                y: y,
                size: 20,
                color: color
            };
            data.label = target;
            g.nodes.push(data);
            nodeMap[target] = true;
        }

        g.edges.push({
                id: "e" + i,
                label: relation.relation,
                source: source,
                target: target,
                size: 8,
                color: '#ccc',
                hover_color: '#000',
                type: 'arrow'
        })
    }
    sigma.renderers.def = sigma.renderers.canvas;
    sigmaGraph = new sigma({
        graph: g,
        container: panelID,
        settings: {
            doubleClickEnabled: false,
            minEdgeSize: 0.5,
            maxEdgeSize: 6,
            enableEdgeHovering: true,
            edgeHoverColor: 'edge',
            defaultNodeColor: '#ec5148',
            edgeLabelSize: 'proportional',
            defaultEdgeLabelSize: 15,
            defaultEdgeHoverColor: '#000',
            edgeHoverSizeRatio: 1,
            edgeHoverExtremities: true
        }
    });

}
