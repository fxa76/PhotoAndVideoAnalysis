import { Component, OnInit } from '@angular/core';

import { SearchParamService } from '../search-param.service';
import {SearchParam} from '../searchParam';

import { MapService } from '../map.service';
import { Poi } from '../poi';

import OlMap from 'ol/Map';
import OlXYZ from 'ol/source/XYZ';
import OlTileLayer from 'ol/layer/Tile';
import OlView from 'ol/View';

import {fromLonLat,transformExtent} from 'ol/proj.js';
import { getBottomLeft, getTopRight} from 'ol/extent.js';
import TileLayer from 'ol/layer/Tile.js';
import { toLonLat} from 'ol/proj.js';
import OSM from 'ol/source/OSM.js';

import Overlay from 'ol/Overlay.js';
import Feature from 'ol/Feature.js';
import VectorSource from 'ol/source/Vector.js';
import {  Vector as VectorLayer} from 'ol/layer.js';
import {  Icon, Style, Circle as CircleStyle, RegularShape as RegularShape, Fill, Stroke} from 'ol/style.js';
import Point from 'ol/geom/Point.js';
import Projection from 'ol/proj/Projection.js';
import GeoJSON from 'ol/format/GeoJSON.js';
import Select from 'ol/interaction/Select.js';
import Extent from 'ol/extent'


import * as d3 from 'd3';
import { ImageService } from '../image.service';


@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})

export class MapComponent implements OnInit {

  map: OlMap;
  view: OlView;
  iconStyleCoordFromExif:Style;
  iconStyleCoordUserDefined:Style;
  vectorSource = VectorSource;
  vectorLayer: VectorLayer;
  rasterLayer :TileLayer;
  extent : Extent;
  poi:Poi[];
  topRight:number[];
  bottomLeft:number[];
  myColor:any;
  
 styles: {[year:number]:{style:any}}={};

  constructor(private mapService: MapService ,  private searchParamService: SearchParamService, private imageService:ImageService ) {
  }

  ngOnInit() {
      this.topRight = [180,90];
      this.bottomLeft = [-180,-90];

      //Create colors by years
      this.myColor = d3.scaleLinear().domain([2016,2024]).range(["orange", "blue"])
      console.log("Color test : "+this.myColor(5))
      /*var years = [
        2018,
        2001,
        2004,
        2005,
        2008,
        2009,
        2010,
        2011,
        2012,
        2013,
        2014,
        2015,
        2016,
        2017,
       
        2019,
        2020,
        2021,
        2022,
        2023,
        2024,
        1970];*/

      this.imageService.getImagesYears()
      .subscribe(years => {
        for (var year of years){
          this.styles[year.years] = {'style':new Style({
            image: new CircleStyle({
              radius: 5,
              fill: new Fill({
                color: this.myColor(year.years)//'orange'
              })
            })
          })
          }
        }
      });
      //Create styles for each year
      this.iconStyleCoordFromExif= new Style({
        image: new CircleStyle({
          radius: 5,
          fill: new Fill({
            color: this.myColor(5)//'orange'
          })
        })
      });

      this.iconStyleCoordUserDefined = new Style({
        image: new RegularShape({
          radius: 5,
          points:4,
          fill: new Fill({
            color: this.myColor(9)//'red'
          })
        })
      });

      this.vectorSource = new VectorSource({
        features: []
      });

      this.vectorLayer = new VectorLayer({
        source: this.vectorSource
      });

      this.rasterLayer = new TileLayer({
        source: new OSM()
      });

      this.map = new OlMap({
        layers: [this.rasterLayer, this.vectorLayer],
        target: 'map',
        view: new OlView({
          //center: fromLonLat([2.3026, 48.7593]),
          //zoom: 10
        })

      });
      var b = fromLonLat(this.searchParamService.searchParam.bottomLeft);
      var t = fromLonLat(this.searchParamService.searchParam.topRight);

      var myExtent = [b[0],b[1],t[0],t[1]];
      this.map.getView().fit(myExtent , this.map.getSize());

      //add the selection interaction to enable clicking on a feature
      var select = new Select();
      this.map.addInteraction(select);
      select.on('select', function(e) {
            var featuresClicked = e.target.getFeatures();
            featuresClicked.forEach(function(feature) {
                this.openInNewTab("detail/" + feature.get('image_id'))
            }.bind(this));
      }.bind(this));

      this.map.on('moveend', this.onMoveEnd.bind(this));
  }

  onMoveEnd(evt):void {
    this.extent = evt.map.getView().calculateExtent(evt.map.getSize());
    this.updateSearchParam();
    this.mapService.getPoi(this.searchParamService.searchParam)
      .subscribe(poi => {
        this.poi = poi
        console.log("number of POI received : " + this.poi.length)
        this.vectorSource.clear();
        var features = [];
        var feats = [];
        this.poi.forEach(function(d) {
          //console.log(d.image_id + " " + typeof(d.lon) + " " + d.lat +  " " + d.coord_from_exif + " d "+d.coord_from_exif + " timestamp year" + new Date(d.timestamp).getFullYear())

          if (d.lon == 'None'){d.lon = 0.0}
          if (d.lat == 'None'){d.lat = 0.0}
          var point = new Point(fromLonLat([parseFloat(d.lon), parseFloat(d.lat)]));
          //console.log(point)
          var iconFeature = new Feature({
            geometry: point
          });
          iconFeature.set('image_id', d.image_id)

          //console.log("exif:"+d.coord_from_exif)
          if(d.coord_from_exif=='True' || d.coord_from_exif){
            //iconFeature.setStyle(this.iconStyleCoordFromExif);
            iconFeature.setStyle(this.styles[new Date(d.timestamp).getFullYear()].style );
          }else{
            iconFeature.setStyle(this.iconStyleCoordUserDefined);
            console.log("this is a userdefined Coord")
          }
          feats.push(iconFeature);
        }.bind(this))
        this.vectorSource.addFeatures(feats);
        this.map.updateSize();
        this.map.render();
      });
  }

  openInNewTab(url):void {
    window.open(url, '_blank');
  }

  wrapLon(value):number {
    var worlds = Math.floor((value + 180) / 360);
    return value - (worlds * 360);
  }

  updateSearchParam():void{
    this.bottomLeft = toLonLat(getBottomLeft(this.extent));
    this.topRight = toLonLat(getTopRight(this.extent));
    var zoomLevel = this.map.getView().getZoom();
    console.log(this.bottomLeft + " " + this.topRight + " zoom level : "+ zoomLevel)
    if (zoomLevel<2){
      this.bottomLeft=[-180,-90];
      this.topRight = [180,90];
    }


    if (this.bottomLeft[0]>this.topRight[0]){
      this.topRight[0]=180;
      this.bottomLeft[0]=-180;
    }

    console.log(this.topRight + " " + this.bottomLeft);
    this.searchParamService.searchParam.bottomLeft=this.bottomLeft;
    this.searchParamService.searchParam.topRight=this.topRight;
  }
}
