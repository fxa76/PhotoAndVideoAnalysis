import { Component, OnInit } from '@angular/core';

import { Duplicate } from '../duplicate';
import { DuplicatesService } from '../duplicates.service';

@Component({
  selector: 'app-duplicates',
  templateUrl: './duplicates.component.html',
  styleUrls: ['./duplicates.component.css']
})
export class DuplicatesComponent implements OnInit {
  duplicates : Duplicate[];
  isLoading : boolean;

  constructor(private duplicatesService: DuplicatesService) { }

  ngOnInit() {
    this.isLoading = true;
    this.duplicatesService.getDuplicates()
      .subscribe(duplicates=> {
          this.duplicates = duplicates;
          console.log(this.duplicates);
          this.isLoading = false;
    });
  }

}
