
var width = 800,
    height = 600,
    fill = d3.scale.category20();

var svgContainer = d3.select("#paint")
  			.append("svg:svg")
    		.attr("width", width)
    		.attr("height", height);

d3.json("data.json", function(json) {
  var force = d3.layout.force()
      			.charge(-120)
      			.linkDistance(30)
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
	// Node types
	var functions = json.nodes.filter(function(node) {return node.type=='function';});
	//var classes = json.nodes.filter(function(node) {return node.type=='class';});
	var imports = json.nodes.filter(function(node) {return node.type=='import';});
	//var modules = json.nodes.filter(function(node) {return node.type=='module';});
	var others = json.nodes.filter(function(node) {return node.type!='function';});

	var func_symbol = svgContainer.selectAll("circle.node")
      			.data(functions)
    			.enter()
  				.append("svg:circle")
      				.attr("class", "node")
      				.attr("cx", function(d) { return d.x; })
      				.attr("cy", function(d) { return d.y; })
					.attr("r", 5)
      				.style("fill", 'green')
      			.call(force.drag);

	var other_symbol = svgContainer.selectAll("rect.node")
      			.data(others)
    			.enter()
  				.append("svg:rect")
      				.attr("class", "node")
      				.attr("x", function(d) { return d.x; })
      				.attr("y", function(d) { return d.y; })
      				.attr("width", 10)
					.attr("height", 10)
      				.style("fill", 'red')
      			.call(force.drag);

  func_symbol.append("svg:title")
      		 .text(function(d) { return d.name; });
  other_symbol.append("svg:title")
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

	func_symbol.attr("cx", function(d) { return d.x; })
        	   .attr("cy", function(d) { return d.y; });
    other_symbol.attr("x", function(d) { return d.x; })
        		 .attr("y", function(d) { return d.y; });
  });
});
