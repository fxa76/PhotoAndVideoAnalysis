import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { faFastForward,faFastBackward,faGlobe } from '@fortawesome/free-solid-svg-icons';

import { Object_in_image } from '../object_in_image';
import { ObjectsInImagesService } from '../objects-in-images.service';
import { SearchParamService } from '../search-param.service';

@Component({
  selector: 'app-faces',
  templateUrl: './faces.component.html',
  styleUrls: ['./faces.component.css']
})
export class FacesComponent implements OnInit {
  faGlobe=faGlobe;
  faFastForward= faFastForward;
  faFastBackward=faFastBackward;

  @Input() isChecked = false;

  faces:Object_in_image[];
  distinct:boolean = true;
  isLoading:boolean = true;
  accessPath:string = "";

  constructor(private route: ActivatedRoute,private objectsInImagesService: ObjectsInImagesService, private searchParamService: SearchParamService ) { }

  ngOnInit() {

    this.accessPath =  this.route.snapshot.routeConfig.path;
    console.log("route : " + this.route.snapshot.routeConfig.path);
    console.log(this.searchParamService.searchParam.use_coords)
    if(this.searchParamService.searchParam.use_coords){
      console.log("checking the check box");
      this.isChecked  = true;
    }
    if (!this.searchParamService.searchParam.offset){
      this.searchParamService.searchParam.offset=0
    }
    if(!this.searchParamService.searchParam.next){
      this.searchParamService.searchParam.next = 100
    }
    this.getFaces()
  }

  getFaces(){
    this.isLoading = true;

    const id = this.route.snapshot.paramMap.get('id');
    const iteration = this.route.snapshot.paramMap.get('iteration');
    const offset = this.route.snapshot.paramMap.get('offset');
    const next = this.route.snapshot.paramMap.get('next');
    console.log("the id supplied is :" +id + " iteration " + iteration + " offset" + offset + "next "+ next);


    switch(this.accessPath){
      case "faces":
        console.log("getting faces");
        this.distinct = false;
        this.objectsInImagesService.getFaces(this.searchParamService.searchParam)
          .subscribe(faces=> {
            this.faces = faces;
            this.isLoading = false;
          });
        break;
      case "facesdistinct":
        this.distinct = true;
        this.objectsInImagesService.getDistinctFaces(this.searchParamService.searchParam)
          .subscribe(faces=> {
            this.faces = faces;
            this.isLoading = false;
          }
        );
        break;
      case "face/:iteration/:id/:offset/:next":
          this.distinct = false;
          this.searchParamService.searchParam.iteration = iteration;
          this.searchParamService.searchParam.id = id;
          //offset,next
          this.objectsInImagesService.getFacesForIterationFaceId(this.searchParamService.searchParam)
            .subscribe(faces=> {
              this.faces = faces;
              this.isLoading = false;
            });
            break;
      case "faces/:id":
       this.distinct = false;
        console.log("getting similar faces to " + id)
         this.objectsInImagesService.get_similar_face(id)
           .subscribe(faces=> {
                    this.faces = faces;
                    this.isLoading = false;
                  });
         break;
      default:
         console.log("not implemented")
         break;


    }
  }

  checkValue(event: any){
    console.log(event);
    this.searchParamService.searchParam.use_coords = event
    this.getFaces();
  }


  hiddeFace(iteration,face_id){
    this.objectsInImagesService.hiddeFace(iteration,face_id)
        .subscribe(()=>{
          console.log("hiddig face");
          }
        )
  }
  get_similar(object_id){
     this.isLoading = true;
     this.objectsInImagesService.get_similar_face(object_id)
       .subscribe(faces=> {
                this.faces = faces;
                this.isLoading = false;
              });
  }

  getPrevious():void{

    this.searchParamService.searchParam.offset = this.searchParamService.searchParam.offset - this.searchParamService.searchParam.next
    if (this.searchParamService.searchParam.offset<0){
      this.searchParamService.searchParam.offset=0;
    }
    this.getFaces();
  }

  getNext():void{
    this.searchParamService.searchParam.offset = this.searchParamService.searchParam.offset + this.searchParamService.searchParam.next
    this.getFaces();
  }

}
