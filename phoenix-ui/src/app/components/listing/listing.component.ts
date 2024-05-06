import {Component, OnInit} from '@angular/core';
import {PhoenixService} from '../../services/phoenix.service'
import {HttpClientModule} from "@angular/common/http";
import {Router, RouterLink} from "@angular/router";
import {routes} from "../../app.routes";
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-listing',
  standalone: true,
  imports: [HttpClientModule, RouterLink, NgForOf],
  templateUrl: './listing.component.html',
  styleUrl: './listing.component.css'
})
export class ListingComponent implements OnInit{
  constructor(protected service: PhoenixService,
              private router: Router,) {
  }
  ngOnInit() {

  }

  onSelect(purposeValue: string, propertyValue: string): void {
    console.log(propertyValue)
    console.log(purposeValue)
    if (purposeValue === '1') {
      if (propertyValue == '1'){
        this.router.navigateByUrl('/all-apartment-sale')
      }
      else if (propertyValue == '2'){
        this.router.navigateByUrl('/all-house-sale')
      }
      // TODO
      // expand to other propertyType's
    } else if (purposeValue === '2') {
      if (propertyValue == '1'){
        this.router.navigateByUrl('/all-apartment-rent')
      }
      else if (propertyValue == '2'){
        this.router.navigateByUrl('/all-house-rent')
      }
    }
    else if (propertyValue === 'Type' && purposeValue == 'Purpose'){
      alert('Please choose property value and purpose!')
    }
    else if (propertyValue == 'Type'){
      alert('Please choose property value!')
    }
    else if (purposeValue == 'Purpose') {
      alert('Please choose purpose value!')
    }
  }

  logoutUser() {
    localStorage.removeItem('authenticationFlag')
    this.service.logout().subscribe({
        next: (result)  => {
          console.log(result)
        },
        complete: () =>{},
        error: (err)=>{
          console.log(err)
        }
      }
    )

  }

}
