import { Component, OnInit,Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { DomSanitizer, SafeHtml, SafeStyle, SafeScript, SafeUrl, SafeResourceUrl } from '@angular/platform-browser';

import { ViewChild } from '@angular/core';

import { faArrowCircleLeft,faSave,faObjectGroup } from '@fortawesome/free-solid-svg-icons';


import { Image } from '../image';
import { ImageService } from '../image.service';
import {Object_in_image} from '../object_in_image';
import {ObjectsInImagesService} from '../objects-in-images.service';
import { D3ImageAndObjectsViewerComponent} from '../d3-image-and-objects-viewer/d3-image-and-objects-viewer.component';

@Component({
  selector: 'app-image-overlay',
  templateUrl: './image-overlay.component.html',
  styleUrls: ['./image-overlay.component.css']
})
export class ImageOverlayComponent implements OnInit {
  faArrowCircleLeft=faArrowCircleLeft;
  image: Image;
  objects : Object_in_image[]
  columnsToDisplay = ['description','analyzer_version','text_found']; //'objects_id','location'

  @ViewChild('imageViewer', { static: true }) chart: D3ImageAndObjectsViewerComponent;

  constructor(private route: ActivatedRoute,private objectsService : ObjectsInImagesService,  private imageService: ImageService,private location: Location,protected sanitizer: DomSanitizer) { }

  ngOnInit() {
      this.getImage();
    }

    getImage(): void {
        const id = +this.route.snapshot.paramMap.get('id');
        this.imageService.getImageOverlay(id)
            .subscribe(image =>{
              this.image = image;
           });
         this.objectsService.getObjects(id)
              .subscribe(objects =>  {
                objects.forEach(function (value) {
                console.log("object"+ value);
              });
              console.log("got objects" )
              });
    }

    goBack(): void {
      this.location.back();
    }


}
