
var width = window.innerWidth;
var height = window.innerHeight;
var viewBox = '0 0 ' + width + ' ' + height;

var svgContainer = d3.select("#paint")
                        .classed('svg-container', true)
                        .append("svg:svg")
//responsive SVG needs these 2 attributes and no width and height attr
                        .attr("viewBox", viewBox)
                        .attr("preserveAspectRatio", "xMidYMid meet")

d3.json("data.json", function(json) {
    var force = d3.layout.force()
                .charge(-200)
                .linkDistance(150)
                .nodes(json.nodes)
                .links(json.links)
                .size([width, height])
                .start();

    var link = svgContainer.selectAll(".link")
                .data(json.links)
                .enter()
                .append("svg:line")
                    .attr("class", "link")
                    .style("stroke-width", function(d) { return Math.sqrt(d.value); })
                    .attr("x1", function(d) { return d.source.x; })
                    .attr("y1", function(d) { return d.source.y; })
                    .attr("x2", function(d) { return d.target.x; })
                    .attr("y2", function(d) { return d.target.y; });

    var nodes = svgContainer.selectAll('.node')
                .data(json.nodes)
                .enter()
                .append('svg:path')
                    .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
                    .attr("d", d3.svg.symbol()
                    .size(function(d) { return d.size; })
                    .type(function (d) { return d.shape; }))
                    .attr("class", "node")
                    .style("fill", function(d) { return d.color;})
                .call(force.drag);

  nodes.append("svg:title").text(function(d) { return d.name; });

  svgContainer.style("opacity", 1e-6).transition()
                .duration(1000).style("opacity", 1);

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    nodes.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  });
});
