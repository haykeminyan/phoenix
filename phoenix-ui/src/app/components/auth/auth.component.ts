import {Component, OnInit} from '@angular/core';
import {PhoenixService} from "../../services/phoenix.service";
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from "@angular/forms";
import {Router} from "@angular/router";
import {HttpEvent, HttpHandler, HttpHeaders, HttpInterceptor, HttpRequest} from "@angular/common/http";
import {Observable} from 'rxjs';
import {cred} from "./cred";


@Component({
  selector: 'app-auth',
  standalone: true,
  imports: [
    FormsModule,
    ReactiveFormsModule
  ],
  templateUrl: './auth.component.html',
  styleUrl: './auth.component.css'
})
export class AuthComponent implements OnInit, HttpInterceptor {
  authForm!: FormGroup
  submitted: boolean = false
  authenticationFlag: boolean | undefined

  constructor(private service: PhoenixService,
              private router: Router,
              private formBuilder: FormBuilder
  ) {
  }

  ngOnInit() {
    this.authForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    })


  }

  onSubmit(): void {
    this.submitted = true;
    if (this.authForm.invalid) {
      if (!this.authForm.value.username){
        alert('Please fill username!')
      }
      else if (!this.authForm.value.password){
        alert('Please fill password!')
      }
      return
    }


    this.service.login(this.authForm.value).subscribe({
      next: (result) =>{
        localStorage.setItem('authenticationFlag', 'true')
        this.router.navigate(['list'])},
      complete(): void {
      },
      error: (err)=>{
        if (err.status === 200){
          localStorage.setItem('authenticationFlag', 'true')
          this.router.navigate(['list'])
        }
        else{
          alert(`User ${this.authForm.value.username} is not found`)
        }
        console.log(err)
      }
  })
  }
  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    this.authenticationFlag = Boolean(<string>localStorage.getItem('authenticationFlag'))
    console.log(this.authenticationFlag)
    if (this.authenticationFlag){
      cred.username = <string>localStorage.getItem('username')
      cred.password = <string>localStorage.getItem('password')
    }
    console.log(cred.username)
    console.log(cred.password)
    request=request.clone({ headers: new HttpHeaders({'Authorization': 'Basic ' + btoa(`${cred.username}:${cred.password}`)}),
      withCredentials:true})
    return next.handle(request)
  }


}
