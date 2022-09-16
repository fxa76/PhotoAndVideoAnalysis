import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject, Observable } from 'rxjs';
import { finalize } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class FileService {
  private fileList: string[] = new Array<string>();
  private fileList$: Subject<string[]> = new Subject<string[]>();
  private displayLoader$: Subject<boolean> = new BehaviorSubject<boolean>(false);

  constructor(private http: HttpClient) { }

  public isLoading(): Observable<boolean> {
    return this.displayLoader$;
  }

  public upload(file: string, filename: string): void {
    const formData = new FormData();

    var myblob = new Blob([file], {
      type: 'text/plain'
    });
    formData.append('file', myblob, filename);
    this.http.post('/fs/v1/upload', formData)
      .pipe(finalize(() => this.displayLoader$.next(false)))
      .subscribe(res => {
      }, error => {
        this.displayLoader$.next(false);
      });

  }

  public list(): Observable<string[]> {
    return this.fileList$;
  }

  public remove(fileName: string) {

  }

  public download(fileName: string) {

  }

  private addFileToList(fileName: string): void {
    this.fileList.push(fileName);
    this.fileList$.next(this.fileList);
  }
}
