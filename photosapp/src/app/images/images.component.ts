import { Component, OnInit,AfterViewInit, ElementRef, ViewChild, Input } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {FormControl} from '@angular/forms';

import { faFastForward,faFastBackward,faGlobe,faCheckDouble } from '@fortawesome/free-solid-svg-icons';
import {CdkDragDrop, moveItemInArray, transferArrayItem} from '@angular/cdk/drag-drop';

import { Image } from '../image';

import { SearchParamService } from '../search-param.service';
import { ImageService } from '../image.service';




@Component({
  selector: 'app-images',
  templateUrl: './images.component.html',
  styleUrls: ['./images.component.css']
})

export class ImagesComponent implements OnInit,AfterViewInit  {
  faFastForward=faFastForward;
  faFastBackward=faFastBackward;
  faGlobe=faGlobe;
  faCheckDouble=faCheckDouble;

  images : Image[];
  selectedImage :Image;
  isLoading:boolean = true;

  //multiple selection
  multipleSelectionEnabled : boolean = false;
  multiSelectedImages : string[] =[];
  setDate = new FormControl(new Date());
  //side nav
   opened: boolean;

  @Input() useGPS = false;


  constructor( private imageService: ImageService, private searchParamService: SearchParamService ) { }

  ngOnInit() {
    console.log(this.searchParamService.searchParam.use_coords)
    if(this.searchParamService.searchParam.use_coords){
      console.log("checking the check box");
      this.useGPS  = true;
    }
    this.getImages();

  }

  ngAfterViewInit() {

  }

  enableMultipleSelection():void{
    this.multipleSelectionEnabled = !this.multipleSelectionEnabled;
    this.opened = !this.opened;
  }

  selectImageValue(event: any,imageId):void{
    if(event){
      console.log("select image : " + imageId)
      this.multiSelectedImages.push(imageId)
    }
    else{
      console.log("DEselect image : " + imageId)
      const index = this.multiSelectedImages.indexOf(imageId, 0);
      if (index > -1) {
         this.multiSelectedImages.splice(index, 1);
      }
    }
    console.log("SELECTED ELEMENTS ARE : " )
    this.multiSelectedImages.forEach(function(elt){
      console.log(elt);
    })
  }

  getToolTip(image:Image):string{
    return image.image_id +'\n'+ image.timestamp+ '\n' + image.lat +' - ' +image.lon;
  }

  getImages(): void {
      this.isLoading = true;
    this.imageService.getImages(this.searchParamService.searchParam)
      .subscribe(images=> {
        this.images = images;
      this.isLoading = false;
    });
  }


  getPrevious():void{
    this.searchParamService.searchParam.offset = this.searchParamService.searchParam.offset - this.searchParamService.searchParam.next
    if (this.searchParamService.searchParam.offset<0){
      this.searchParamService.searchParam.offset=0;
    }
    this.getImages();
  }

  getNext():void{
    this.searchParamService.searchParam.offset = this.searchParamService.searchParam.offset + this.searchParamService.searchParam.next
    this.getImages();
  }
  checkValue(event: any){
    console.log(event);
    this.searchParamService.searchParam.use_coords = event
    this.getImages();
  }


}
