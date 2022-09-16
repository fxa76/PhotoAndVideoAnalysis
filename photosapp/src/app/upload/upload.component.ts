import { Component, OnInit } from '@angular/core';

import { FileService } from '../file.service';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent implements OnInit {

  constructor( private fileService: FileService) { }

  ngOnInit() {
  }

  files: any = [];
  aFile : any;
  uploadFile(event) {
    for (let index = 0; index < event.length; index++) {
      let reader = new FileReader();
      let file : File
      file = event[index]
      this.files.push(file.name)
      console.log("file type : " +file.type);

      reader.onload = () => {
        this.aFile = reader.result
        this.fileService.upload(this.aFile, file.name);
      };
      reader.readAsDataURL(file);
    }
   }

  deleteAttachment(index) {
    this.files.splice(index, 1)
  }

}
