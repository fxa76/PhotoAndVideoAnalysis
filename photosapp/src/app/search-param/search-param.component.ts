import { Component, OnInit,Input } from '@angular/core';
import {FormControl} from '@angular/forms';

import { Observable } from 'rxjs';

import { faRedo } from '@fortawesome/free-solid-svg-icons';

import { SearchParamService } from '../search-param.service';
import { SearchParam } from '../searchParam';
import { Description } from '../description';
import { Camera } from '../camera';
import { FileFormat } from '../fileformat';

import { ObjectsInImagesService } from '../objects-in-images.service';

@Component({
  selector: 'app-search-param',
  templateUrl: './search-param.component.html',
  styleUrls: ['./search-param.component.css']
})
export class SearchParamComponent implements OnInit {
  faRedo=faRedo;

  startDate = new FormControl(new Date(2015,10,22,0,0,0,0));
  endDate = new FormControl(new Date(2100,11,12,0,0,0,0));
  dateIsNull = false;
  gpsIsNull = false;
  useCoords = false;

  public descriptions : Description[]=[];
  public descriptionsToBeIncluded : Description[]=[];
  public cameras : Camera[]=[];
  public camerasToBeIncluded : Camera[]=[];
  public fileformats : FileFormat[]=[];
  public fileformatsToBeIncluded : FileFormat[]=[];

  constructor( public searchParamService: SearchParamService, private objInImageService : ObjectsInImagesService  ) {
  }

  ngOnInit() {
    console.log("in")
    this.startDate = new FormControl(new Date(this.searchParamService.searchParam.fromdate*1000));
    this.endDate =  new FormControl(new Date(this.searchParamService.searchParam.todate*1000));
    this.dateIsNull=  this.searchParamService.searchParam.dateIsNull;
    this.gpsIsNull=  this.searchParamService.searchParam.gpsIsNull;
    this.useCoords=  this.searchParamService.searchParam.use_coords;

    this.descriptionsToBeIncluded = this.searchParamService.searchParam.descriptions;
    this.camerasToBeIncluded = this.searchParamService.searchParam.cameramodels;
    this.fileformatsToBeIncluded = this.searchParamService.searchParam.fileformats;

    this.searchParamService.getObjectsDescriptions(this.searchParamService.searchParam)
        .subscribe(descriptions =>{
          this.descriptions = descriptions;
          for (let descInc of this.searchParamService.searchParam.descriptions){
            for (let desc of this.descriptions){
              if(descInc.description === desc.description){
                desc.selected = true;
              }
            }
          }
        });

    this.searchParamService.getCameraModelsDescriptions(this.searchParamService.searchParam)
        .subscribe(cameras =>{
          this.cameras = cameras;
          for (let descInc of this.searchParamService.searchParam.cameramodels){
            for (let desc of this.cameras){
              if(descInc.name === desc.name){
                desc.selected = true;
              }
            }
          }
        });

    this.searchParamService.getFileFormatsDescriptions(this.searchParamService.searchParam)
        .subscribe(fileformats =>{
          this.fileformats = fileformats;
          for (let descInc of this.searchParamService.searchParam.fileformats){
            for (let desc of this.fileformats){
              if(descInc.name === desc.name){
                desc.selected = true;
              }
            }
          }
        });
    console.log("out")
  }

  toggleDateData(event){
    this.searchParamService.searchParam.dateIsNull = event.checked;
  }

  toggleGpsData(event){
    this.searchParamService.searchParam.gpsIsNull = event.checked;
  }

  toggleUseCoordsData(event){
    this.searchParamService.searchParam.use_coords = event.checked;
  }

  getEpochDate(dateString,hoursFix):number {
    var date_text = dateString + " " + hoursFix
    //console.log(date_text)
    var date = new Date(date_text)
    var date_epoch = date.getTime() / 1000
    return date_epoch
  }

  save(): void {
    console.log(this.startDate.value.getTime()/1000)
    console.log(this.endDate.value.getTime()/1000)
    this.searchParamService.searchParam.fromdate =this.startDate.value.getTime()/1000;//this.getEpochDate(this.fromDate,"00:01");
    this.searchParamService.searchParam.todate =this.endDate.value.getTime()/1000;// this.getEpochDate(this.toDate,"23:59");

    this.descriptionsToBeIncluded =[];
    this.camerasToBeIncluded =[];
    this.fileformatsToBeIncluded =[];
    //add selected objects
    for (let desc of this.descriptions){
      if(desc.selected){
        var descToInclude = new Description();
        descToInclude.description = desc.description;
        descToInclude.criteria =  "atleast";
        descToInclude.qty = 1;
        this.descriptionsToBeIncluded.push(descToInclude)
      }
    }
    //add selected cameras
    for (let desc of this.cameras){
      if(desc.selected){
        var descToInclude2 = new Camera();
        descToInclude2.name = desc.name;
        this.camerasToBeIncluded.push(descToInclude2)
      }
    }
    //add sletected file formats
    //add selected cameras
    for (let desc of this.fileformats){
      if(desc.selected){
        var descToInclude2 = new FileFormat();
        descToInclude2.name = desc.name;
        this.fileformatsToBeIncluded.push(descToInclude2)
      }
    }

    console.log(this.descriptionsToBeIncluded);
    this.searchParamService.searchParam.descriptions = this.descriptionsToBeIncluded;
    console.log(this.searchParamService.searchParam);
    //get possible objects for considered search params
    this.searchParamService.getObjectsDescriptions(this.searchParamService.searchParam)
      .subscribe(descriptions =>{
        this.descriptions = descriptions
        for (let desc of this.descriptions){
          for (let descInc of this.descriptionsToBeIncluded){
            if(desc.description == descInc.description){
              desc.selected=true;
            }
          }
        }
      });
      //get cameras  for considered search params
      console.log(this.camerasToBeIncluded);
      this.searchParamService.searchParam.cameramodels = this.camerasToBeIncluded;
      this.searchParamService.getCameraModelsDescriptions(this.searchParamService.searchParam)
        .subscribe(cameras =>{
          this.cameras = cameras
          for (let desc of this.cameras){
            for (let descInc of this.camerasToBeIncluded){
              if(desc.name == descInc.name){
                desc.selected=true;
              }
            }
          }
        });
        //get fileformats  for considered search params
        console.log(this.fileformatsToBeIncluded);
        this.searchParamService.searchParam.fileformats = this.fileformatsToBeIncluded;
        this.searchParamService.getFileFormatsDescriptions(this.searchParamService.searchParam)
          .subscribe(fileformats =>{
            this.fileformats = fileformats
            for (let desc of this.fileformats){
              for (let descInc of this.fileformatsToBeIncluded){
                if(desc.name == descInc.name){
                  desc.selected=true;
                }
              }
            }
          });
  }

  checkValue(event: any){
    console.log(event);
  }

}
