import { Component, OnInit, ElementRef, ViewEncapsulation, Input, SimpleChanges, OnChanges } from '@angular/core';

import * as d3 from 'd3';
import { select } from 'd3-selection';
import { scaleLinear } from 'd3-scale';
import { range, histogram, max } from 'd3-array';
import { format } from 'd3-format';
import { randomBates } from 'd3-random';
import { axisBottom } from 'd3-axis';
import * as d3TimeFormat from 'd3-time-format';
import {Image} from '../image';


@Component({
  selector: 'app-d3-image-viewer',
  templateUrl: './d3-image-viewer.component.html',
  styleUrls: ['./d3-image-viewer.component.css']
})
export class D3ImageViewerComponent implements OnInit {
  private hostElement; // Native element hosting the SVG container
  @Input() my_image: Image;


  constructor( private elRef: ElementRef) {
    this.hostElement = this.elRef.nativeElement;
  }

  ngOnInit() {
    console.log("hello")
  }

  ngOnChanges(changes: SimpleChanges) {
    if(changes) {
      console.log(changes)
      this.updateImage(changes.my_image.currentValue);
    }
  }

  updateImage(image){
    var svg =  d3.select(this.hostElement).select("#imageZone")

    var view_w = 1000
    var view_h = 700
    var g = svg
      .attr("width", view_w)
      .attr("height", view_h)
      .append('g')

    g.append('image')
      .attr('xlink:href', image.image_base64)
  
    //debug info to show image id
    g.append('text')
      .attr("x",100)
      .attr("y",100)
      .text(image.image_id)

      var zoomFn = d3.zoom()
          .scaleExtent([0.01, 40])
          .on('zoom', function() {
              console.log("zooming")
              g.attr("transform", d3.event.transform)
          })
    svg.call(zoomFn);

    //set initial zoom to fit
    console.log("image size is : (w/h)" +image.width + " " + image.height )
    var ratio_w = 1/(image.width/view_w);
    var ratio_h = 1/(image.height/view_h);
    var ratio = 1;
    if (ratio_h<ratio_w) {
     ratio = ratio_h;
    }
    else{
     ratio = ratio_w;
    }
    svg.call(zoomFn.transform, d3.zoomIdentity.scale(ratio))


  }
}
