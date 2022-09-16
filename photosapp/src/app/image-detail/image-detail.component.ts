import { Component, OnInit,Input} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import {MatButtonModule} from '@angular/material/button';
import { ViewChild } from '@angular/core';

import { faArrowCircleLeft,faSave,faObjectGroup } from '@fortawesome/free-solid-svg-icons';

import { Image } from '../image';
import { ImageService } from '../image.service';
import { D3ImageViewerComponent} from '../d3-image-viewer/d3-image-viewer.component';

@Component({
  selector: 'app-image-detail',
  templateUrl: './image-detail.component.html',
  styleUrls: ['./image-detail.component.css']
})
export class ImageDetailComponent implements OnInit {
  faArrowCircleLeft=faArrowCircleLeft;
  faSave=faSave;
  faObjectGroup=faObjectGroup;

  isLoading:boolean = true;
  @Input() image: Image;
  @Input() creationDate = '1900-01-01';
  @Input() creationTime = '12:01:01';
  @Input() milli = '12:01:01';
  @ViewChild('imageViewer', { static: true }) chart: D3ImageViewerComponent;

  file:string;

  constructor(private route: ActivatedRoute,private imageService: ImageService,private location: Location) { }

  ngOnInit() {
    this.getImage();
  }

  isVideo(): boolean{
    console.log("file extension is : " + this.image.fileextensions);
    if ([".jpeg",".jpg",".png",".tiff",".orf",".webp"].includes(this.image.fileextensions)){
      return false;
    }
    else{
      return true;
    }
  }

  getImage(): void {
    const id = +this.route.snapshot.paramMap.get('id');
    this.imageService.getImage(id)
        .subscribe(image => {
          this.image = image;
          var d = new Date(this.image.creationdate*1000);
          this.creationDate = d.toISOString().slice(0,10);
          this.creationTime = d.toISOString().slice(11,19);
          this.milli = d.toISOString().slice(20,25);
          console.log(this.creationTime);
          console.log(image);
          console.log(this.milli);
          //get image details from the service Python
          if ([".jpeg",".jpg",".png",".tiff",".orf",".webp"].includes(image.fileextensions)){
            this.imageService.getImageFile(id)
            .subscribe(image => {
              this.image.image_base64 = image.image_base64;
              this.image.width = image.width;
              this.image.height = image.height;
              this.image.depth = image.depth;
              this.isLoading = false;
            });
          }
          else {
          //get video stream from file server
            this.isLoading = false;
          }
        });


  }

  goBack(): void {
    this.location.back();
  }

  save(): void {
    var d = new Date(this.creationDate + "T"+this.creationTime + "."+this.milli);
    console.log(d.toISOString());
    console.log( (d.getTime())/1000);

    this.image.timestamp = d.toISOString();
    this.image.creationdate = (d.getTime())/1000;

    this.imageService.updateImage(this.image)
      .subscribe(() => this);
  }

}
