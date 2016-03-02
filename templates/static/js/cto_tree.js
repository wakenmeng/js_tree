//var trees = {{trees|safe}};
//console.log(trees);
//for (var i=0; i<trees.length; i++) {
//    var tree = trees[i];
//    var root = tree[tree[-1]];
//    var children_ids = root['children'];
//    document.write(root['name'] + '<br />');
//    while (children_ids.length > 0){
//        chid = children_ids.shift();
//        child = tree[chid];
//        document.write(child['id'] + '<br />');
//        children_ids = children_ids.concat(child['children']);
//    }
//    document.write('<hr />');
//     
//}
//var redraw;

/* only do all this when document has finished loading (needed for RaphaelJS) */
window.onload = function() {

  var width = 600;
  var height = 400;

  var g = new Graph();



  /* add a node with a customized shape
     (the Raphael graph drawing implementation can draw this shape, please
     consult the RaphaelJS reference for details http://raphaeljs.com/) */
  var render = function(r, n) {
    var label = r.text(0, 30, n.label).attr({opacity:0});
    //the Raphael set is obligatory, containing all you want to display
    var set = r.set()
      .push(r.rect(-30, -13, 62, 86)
        .attr({ fill: '#fa8', 'stroke-width': 2, r: 9 })
      )
      .push(label);

    // make the label show only on hover
    set.hover(
      function mouseIn() {
        label.animate({ opacity: 1, 'fill-opacity': 1 }, 500);
      },
      function mouseOut() {
        label.animate({opacity:0},300);
      }
    );

    var tooltip = r.set()
      .push(
        r.rect(0, 0, 90, 30).attr({ fill: '#fec', 'stroke-width': 1, r: 9 })
      ).push(
        r.text(25, 15, 'overlay').attr({ fill: '#000000' })
      );
    for(var i in set.items) {
      set.items[i].tooltip(tooltip);
    }
    //            set.tooltip(r.set().push(r.rect(0, 0, 30, 30).attr({"fill": "#fec", "stroke-width": 1, r : "9px"})).hide());
    return set;
  };

  var st = {
    directed: true,
    label: 'Label',
    'label-style' : {
      'font-size': 20
    }
  };

  /* add a simple node */
  g.addNode("strawberry");
  g.addNode("cherry");

  /* add a node with a customized label */
  g.addNode("1", { label : "Tomato" });

  g.addNode('id35', {
    label: "meat\nand\ngreed",
    /* filling the shape with a color makes it easier to be dragged */
    /* arguments: r = Raphael object, n : node object */
    render: render
  });
  //    g.addNode("Wheat", {
  /* filling the shape with a color makes it easier to be dragged */
  /* arguments: r = Raphael object, n : node object */
  //        shapes : [ {
  //                type: "rect",
  //                x: 10,
  //                y: 10,
  //                width: 25,
  //                height: 25,
  //                stroke: "#f00"
  //            }, {
  //                type: "text",
  //                x: 30,
  //                y: 40,
  //                text: "Dump"
  //            }],
  //        overlay : "<b>Hello <a href=\"http://wikipedia.org/\">World!</a></b>"
  //    });
  var trees = {{trees|safe}};
  console.log(trees);
  for (var i=0; i<trees.length; i++) {
      var tree = trees[i];
      var root = tree[tree[-1]];
      var children_ids = root['children'];
      document.write(root['name'] + '<br />');
      while (children_ids.length > 0){
          chid = children_ids.shift();
          child = tree[chid];
          document.write(child['id'] + '<br />');
          children_ids = children_ids.concat(child['children']);
      }
      document.write('<hr />');
       
  }


  //g.removeNode("1");

  /* layout the graph using the Spring layout implementation */
  var layouter = new Graph.Layout.Spring(g);

  /* draw the graph using the RaphaelJS draw implementation */
  var renderer = new Graph.Renderer.Raphael('canvas', g, width, height);

  //redraw = function() {
  //  layouter.layout();
  //  renderer.draw();
  //};
  //hide = function(id) {
  //  g.nodes[id].hide();
  //};
  //show = function(id) {
  //  g.nodes[id].show();
  //};
  //    console.log(g.nodes["kiwi"]);
  //redraw();
};
