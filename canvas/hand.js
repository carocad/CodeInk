
var width = 1200,
    height = 800,
    fill = d3.scale.category20();

var svgContainer = d3.select("#paint")
  			.append("svg:svg")
    		.attr("width", width)
    		.attr("height", height);

d3.json("data.json", function(json) {
  var force = d3.layout.force()
      			.charge(-200)
      			.linkDistance(150)
      			.nodes(json.nodes)
      			.links(json.links)
      			.size([width, height])
      			.start();

  var link = svgContainer.selectAll("line.link")
      			.data(json.links)
    			.enter()
  				.append("svg:line")
      				.attr("class", "link")
      				.style("stroke-width", function(d) { return Math.sqrt(d.value); })
      				.attr("x1", function(d) { return d.source.x; })
      				.attr("y1", function(d) { return d.source.y; })
      				.attr("x2", function(d) { return d.target.x; })
      				.attr("y2", function(d) { return d.target.y; });

	var node = svgContainer.selectAll("circle.node")
      			.data(json.nodes)
    			.enter()
  				.append("svg:circle")
      				.attr("class", "node")
      				.attr("cx", function(d) { return d.x; })
      				.attr("cy", function(d) { return d.y; })
					.attr("r", function(d) { return d.size; })
					.style("fill", function(d) {return d.color; })
      			.call(force.drag);

  node.append("svg:title")
      		 .text(function(d) { return d.name; });

  svgContainer.style("opacity", 1e-6)
     		  .transition()
     		  .duration(1000)
     		  .style("opacity", 1);

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

	node.attr("cx", function(d) { return d.x; })
        	   .attr("cy", function(d) { return d.y; });
  });
});
