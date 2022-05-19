import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CheckImagesService {

  constructor(private http: HttpClient) { }
  
  post(body: any): Observable<any> {
    return this.http.post('http://localhost:8000/tarros/test', body);
  }

}
