import { Injectable } from '@angular/core';
import {
  HttpClient, HttpHeaders, HttpResponse,
} from "@angular/common/http";
import {Observable} from "rxjs";
import {FormBuilder, FormGroup} from "@angular/forms";
import { v4 as uuidv4 } from 'uuid';


export const cred ={
  username: 'username',
  password: 'password'
}

@Injectable({
  providedIn: 'root'
})
export class PhoenixService {
  authForm: FormGroup | undefined
  constructor(private http: HttpClient,
              private fb:FormBuilder) {

  }

  login(data: any):Observable<HttpResponse<HttpResponse<any>>> {
    const url = 'http://127.0.0.1:8000/admin/login'
    const fd: FormData = new FormData();
    fd.append( 'username', data.username)
    fd.append( 'password', data.password)
    console.log(fd)
    localStorage.setItem('username', data.username)
    localStorage.setItem('password', data.password)
    return this.http.post<HttpResponse<any>>(url, fd, {observe: "response"})
  }

  logout():Observable<HttpResponse<HttpResponse<any>>> {
    const url = 'http://127.0.0.1:8000/admin/logout'
    return this.http.get<HttpResponse<any>>(url, {observe: "response"})
  }

  getListRent(params: { [key: string]: string | undefined }): Observable<HttpResponse<any>> {
    let url = 'http://127.0.0.1:8000/all-apartment-rent';

    let queryParams = Object.entries(params)
      .filter(([_, value]) => value !== undefined && value!==null && value!=='0')
      .map(([key, value]) => `${key}=${value}`)
      .join('&');


    if (queryParams) {
      url += `?${queryParams}`;
    }

    return this.http.get<HttpResponse<any>>(url, { observe: 'response' });
  }

  createApartmentRent(apartmentData: any, file: File | undefined): Observable<HttpResponse<HttpResponse<any>>> {
    const url = 'http://127.0.0.1:8000/apartment-rent';
    const formData = new FormData();
    formData.append('apartment', JSON.stringify(apartmentData));
    const fileInput = (document.getElementById('fileInput') as HTMLInputElement)
    console.log(file)
    for (const elem of Object(fileInput!.files)) {
      formData.append('files',elem)
    }
    return this.http.post<HttpResponse<any>>(url, formData, { observe: 'response' })
  }

  viewApartment(id: string){
    const url = `http://127.0.0.1:8000/apartment-rent/${id}`
    return this.http.get<HttpResponse<any>>(url, { observe: 'response' })
  }

  deleteApartment(id: string){
    const url = `http://127.0.0.1:8000/apartment-rent/${id}`
    return this.http.delete<HttpResponse<any>>(url, { observe: 'response' })
  }

  editApartment(apartmentData: any, file: File , id: string | undefined): Observable<HttpResponse<HttpResponse<any>>> {
    const url = `http://127.0.0.1:8000/apartment-rent/${id}`;
    const fileInput = (document.getElementById('fileInput') as HTMLInputElement)
    const HttpUploadOptions = {
      headers: new HttpHeaders({ "Content-Type": "multipart/form-data"})
    }
    const formData = new FormData();
    formData.append('apartment', JSON.stringify(apartmentData));
    console.log(fileInput.files)
    for (const elem of Object(fileInput!.files)) {
      formData.append('files',elem)
    }
    console.log(file)
    console.log(formData)
    return this.http.put<HttpResponse<any>>(url, formData, HttpUploadOptions)
  }
}
