// https://medium.com/better-programming/reactive-charts-in-angular-8-using-d3-4550bb0b4255
import { Component, OnInit, OnDestroy, AfterContentInit, ElementRef } from '@angular/core';
import { Router } from '@angular/router';
import { ViewChild } from '@angular/core';

import * as d3 from 'd3';

import { BrushZoomHistoComponent } from './../brush-zoom-histo/brush-zoom-histo.component';
import { ChartControlsService } from '../chart-controls.service';



export class DeliveryMetric {
  state: string;
  stateDisplayValue: string;
  mean: number;
  stdDev: number;

  constructor(stateIn, stateDisplayValueIn, meanIn, stdDevIn) {
    this.state = stateIn;
    this.stateDisplayValue = stateDisplayValueIn;
    this.mean = meanIn;
    this.stdDev = stdDevIn;
  }
}


@Component({
  selector: 'app-timeline',
  templateUrl: './timelinebar.component.html',
  styleUrls: ['./timelinebar.component.scss']  
})
export class TimelinebarComponent implements OnInit, OnDestroy, AfterContentInit {

  @ViewChild('brushZoom', { static: true }) chart: BrushZoomHistoComponent;

  chartData = [];

  refreshInterval;

  deliveryMetrics: DeliveryMetric[];

  displayedColumns = ['legend', 'stateDisplayValue', 'mean', 'stdDev'];

  constructor(private router: Router, public chartControlsService: ChartControlsService) {
    this.chartControlsService.fullScreen = false;
   }

  ngOnInit() {
  }

  initialize() {
  }

  ngOnDestroy() {

  }

  ngAfterContentInit() {
    //this.initialize();
  }

  toggleData(event) {
    this.chartControlsService.showData = event.checked;
  }
}
