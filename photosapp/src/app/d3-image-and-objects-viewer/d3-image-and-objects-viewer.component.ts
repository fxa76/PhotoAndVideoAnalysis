import { Component, OnInit, ElementRef, ViewEncapsulation, Input, SimpleChanges, OnChanges } from '@angular/core';

import * as d3 from 'd3';
import { select } from 'd3-selection';
import { scaleLinear } from 'd3-scale';
import { range, histogram, max } from 'd3-array';
import { format } from 'd3-format';
import { randomBates } from 'd3-random';
import { axisBottom } from 'd3-axis';
import * as d3TimeFormat from 'd3-time-format';
import { Image } from '../image';
import { Object_in_image } from '../object_in_image';

@Component({
  selector: 'app-d3-image-and-objects-viewer',
  templateUrl: './d3-image-and-objects-viewer.component.html',
  styleUrls: ['./d3-image-and-objects-viewer.component.css']
})
export class D3ImageAndObjectsViewerComponent implements OnInit {
  private hostElement; // Native element hosting the SVG container
  @Input() my_image: Image;
  private svg;
  private g;
  private view_w = 1200;
  private view_h = 800;
 private objects_layer;

  constructor(private elRef: ElementRef) {
    this.hostElement = this.elRef.nativeElement;

  }

  ngOnInit() {
    console.log("hello")
    this.svg = d3.select(this.hostElement).select("#imageZone")

    this.g = this.svg
      .attr("width", this.view_w)
      .attr("height", this.view_h)
      .append('g')
    this.createImage();//changes.my_image.currentValue);
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes) {
      console.log(changes)
      if (this.g != undefined) {
        this.objects_layer.remove();
        this.objects_layer = this.g.selectAll('.rectangle')
          .data(this.my_image.objs)
          .enter().append('a')
          .attr("x", (d) => { return d.x })
          .attr("y", (d) => { return d.y })
          .attr("xlink:href", function (d) { return "./faces/" + d.objects_id })

          .append('rect')
          .attr("x", (d) => { return d.x })
          .attr("y", (d) => { return d.y })
          .attr("width", (d) => { return d.w })
          .attr("height", (d) => { return d.h })
          .attr("style", (d) => {
            if (d.over) {
              return "stroke:red; fill:red; opacity:0.9"//d3.select(this).attr("opacity", .9).style("fill", "red");
            }
            else {
              return "stroke:red; fill:white; opacity:0.1"
            }

          })
          .on("mouseover", function (d) {
            d3.select(this).attr("opacity", .9).style("fill", "red");
            d.over = true;
          })
          .on("mouseout", function (d) {
            d3.select(this).attr("style", "stroke:red; fill:white; opacity:0.1");
            d.over = false;
          })
      }
    }
  }

  createImage() {


    var photo_layer = this.g.append('image')
      .attr('xlink:href', this.my_image.image_base64_overlay);


    this.objects_layer = this.g.selectAll('.rectangle')
      .data(this.my_image.objs)
      .enter().append('a')
      .attr("x", (d) => { return d.x })
      .attr("y", (d) => { return d.y })
      .attr("xlink:href", function (d) { return "./faces/" + d.objects_id })

      .append('rect')
      .attr("x", (d) => { return d.x })
      .attr("y", (d) => { return d.y })
      .attr("width", (d) => { return d.w })
      .attr("height", (d) => { return d.h })
      .attr("style", (d) => {
        if (d.over) {
          return "stroke:red; fill:red; opacity:0.9"//d3.select(this).attr("opacity", .9).style("fill", "red");
        }
        else {
          return "stroke:red; fill:white; opacity:0.1"
        }

      })
      .on("mouseover", function (d) {
        d3.select(this).attr("opacity", .9).style("fill", "red");
        d.over = true;
      })
      .on("mouseout", function (d) {
        d3.select(this).attr("style", "stroke:red; fill:white; opacity:0.1");
        d.over = false;
      })

    var myg = this.g;
    //define zoom settings
    var zoomFn = d3.zoom()
      .scaleExtent([0.01, 40])
      .on('zoom', function () {
        console.log("zooming")
        myg.attr("transform", d3.event.transform)
      })

    this.svg.call(zoomFn);

    //set initial zoom to fit
    console.log("image size is : (w/h)" + this.my_image.width + " " + this.my_image.height)
    var ratio_w = 1 / (this.my_image.width / this.view_w);
    var ratio_h = 1 / (this.my_image.height / this.view_h);
    var ratio = 1;
    if (ratio_h < ratio_w) {
      ratio = ratio_h;
    }
    else {
      ratio = ratio_w;
    }
    this.svg.call(zoomFn.transform, d3.zoomIdentity.scale(ratio))

  }



}
