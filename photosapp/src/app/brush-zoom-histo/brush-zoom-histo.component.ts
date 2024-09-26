import { Component, OnInit, ElementRef, ViewEncapsulation, Input, SimpleChanges, OnChanges } from '@angular/core';

import * as d3 from 'd3';
import { select } from 'd3-selection';
import { scaleLinear } from 'd3-scale';
import { range, histogram, max } from 'd3-array';
import { format } from 'd3-format';
import { randomBates } from 'd3-random';
import { axisBottom } from 'd3-axis';
import * as d3TimeFormat from 'd3-time-format';

import { SP500 } from './../shareddata/sp500';


import { ImageService } from '../image.service';
import { Stock } from '../stock';

/*export interface MyData {
    date : any;
    value: any;
    length:number;
    x0:number;
    x1:number;
}*/



@Component({
  selector: 'app-brush-zoom-histo',
  encapsulation: ViewEncapsulation.None,
  templateUrl: './brush-zoom-histo.component.html',
  styleUrls: ['./brush-zoom-histo.component.css']
})
export class BrushZoomHistoComponent implements OnInit {
  private hostElement; // Native element hosting the SVG container
  private zoom: any;

  isLoading: boolean;

  @Input() data: Stock[];

  constructor(private imageService: ImageService, private elRef: ElementRef) {
    this.hostElement = this.elRef.nativeElement;
  }

  ngOnInit(): void {
    this.imageService.getImagesTimebar()
      .subscribe(data => {
        this.data = data;
        this.isLoading = false;
        console.log(data);
        this.drawhistogram2();
      });

  }

  drawhistogram2() {
    // set the dimensions and margins of the graph
    var margin = { top: 10, right: 30, bottom: 30, left: 40 }
    var width = 700 - margin.left - margin.right;
    var height = 500 - margin.top - margin.bottom;

    // parse the date / time
    var parseDate = d3.timeParse("%Y-%m-%dT%H:%M:%S.%LZ");

    this.data.forEach(function(d: any) {
      d.date = parseDate(d.date);
    });


    console.log("histo");
    // set the ranges
    var x = d3.scaleTime()
      //.domain([new Date(1970, 6, 3), new Date(2032, 0, 1)])
      .domain(d3.extent(this.data, (d: any) => d.date))
      .rangeRound([0, width]);
    var y = d3.scaleLinear()
      //.domain([1,10000])
      .range([height, 0]);

    // set the parameters for the histogram
    var my_histogram = d3.histogram()
      .value(function(d: any) { return d.date; })
      .domain(x.domain())
      .thresholds(x.ticks(d3.timeYear));

    // append the svg object to the body of the page
    // append a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svg = d3.select(this.hostElement).select("#hist")
      .attr("width", width)
      .attr("height", height)
      .attr('viewBox', '0 0 ' + 700 + ' ' + 500)
      .append('g')
      .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

    // group the data for the bars
    var bins = my_histogram(this.data);

    // Scale the range of the data in the y domain
    y.domain([0, d3.max(bins, function(d: any) { return d.length; })]);

    var div = d3.select(this.hostElement).append("div")
      .attr("class", "tooltip")
      .style("opacity", 0);

    // append the bar rectangles to the svg element
    svg.selectAll("rect")
      .data(bins)
      .enter().append("rect")
      .attr("class", "bar")
      .attr("x", 1)
      .attr("transform", function(d: any) {
        return "translate(" + x(d.x0) + "," + y(d.length) + ")";
      })
      .attr("width", function(d: any) {
        var barWidth = x(d.x1) - x(d.x0);
        if (barWidth < 0 ){barWidth = 0};
        return barWidth;
      })
      .attr("height", function(d: any) {
        var barHeight = height - y(d.length);
        if ( barHeight < 2) {
           barHeight = 2
        }
        return barHeight;
      })
      .on("mouseover", function(event,d: any) {
        d3.select(this)
          .attr("class", "barover");
        div.transition()
          .duration(200)
          .style("opacity", .9);
        div.html("number of files : " + d.length)
          .style("left", (event.pageX) + "px")
          .style("top", (event.pageY - 28) + "px");
      })
      .on("mouseout", function(d, i) {
        d3.select(this).attr("class", "bar");
        div.transition()
          .duration(500)
          .style("opacity", 0);
      });

    // add the x Axis
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    // add the y Axis
    svg.append("g")
      .call(d3.axisLeft(y));
  }


}
