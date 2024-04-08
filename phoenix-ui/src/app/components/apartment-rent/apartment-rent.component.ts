import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import { PhoenixService } from "../../services/phoenix.service";
import {Router, RouterLink, RouterModule} from "@angular/router";
import {FormsModule, NgControl, ReactiveFormsModule} from "@angular/forms";
import {MatSlider, MatSliderModule, MatSliderRangeThumb} from "@angular/material/slider";
import {MatFormFieldModule, MatLabel} from "@angular/material/form-field";
import {MatButton, MatButtonModule} from "@angular/material/button";
import {MatInput, MatInputModule} from "@angular/material/input";
import {BrowserModule} from "@angular/platform-browser";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {CommonModule, NgForOf, NgIf} from "@angular/common";
import {MatChipListbox, MatChipOption} from "@angular/material/chips";
import {MatCardModule} from "@angular/material/card";
import {MatCheckboxModule} from "@angular/material/checkbox";
import {MatOption, MatSelect} from "@angular/material/select";

@Component({
  selector: 'app-apartment-rent',
  templateUrl: './apartment-rent.component.html',
  standalone: true,
  imports: [
    NgForOf,
    ReactiveFormsModule,
    MatChipListbox,
    MatChipOption,
    FormsModule,
    MatLabel,
    MatCardModule,
    MatFormFieldModule,
    CommonModule,
    RouterLink,
    MatInputModule,
    FormsModule,
    MatCheckboxModule,
    MatSliderModule,
    MatButton,
    MatSelect,
    MatOption,
    NgIf,
  ],
  styleUrls: ['./apartment-rent.component.css']
})
export class ApartmentRentComponent implements OnInit {
  dossiers: any[] = [];
  submitted: boolean = false;
  livingArea: string | undefined;
  livingAreaMin: string | undefined;
  livingAreaMax: string | undefined;
  isLivingAreaValue: boolean = false;
  isLivingAreaSlider: boolean = false;
  rentPrice: string | undefined;
  rentPriceMin: string | undefined;
  rentPriceMax: string | undefined;
  isRentPrice: boolean = false;
  numberOfBedrooms: string | undefined;
  numberOfBedroomsMin: string | undefined;
  numberOfBedroomsMax: string | undefined;
  isNumberOfBedrooms: boolean = false;
  isDropdownVisible: boolean = false;
  params!: { [key: string]: string | undefined; };
  @ViewChild('slider') slider: any;
  @ViewChild('livingAreaFilterButton') livingAreaFilterButton: ElementRef | undefined;
  constructor(
    protected service: PhoenixService,
    private router: Router
  ) {
  }


  toggleDropdown(visible: boolean): void {
    this.isDropdownVisible = visible;
  }
  ngOnInit() {
    this.initializeFilters()
    this.list()
    setTimeout(() => {
      this.livingAreaFilterButton!.nativeElement.click();
    }, 100);
  }

  initializeFilters() {
    this.params = {
      living_area: this.livingArea,
      living_area__lte: this.livingAreaMax,
      living_area__gte: this.livingAreaMin,
      rent_price: this.rentPrice,
      rent_price__lte: this.rentPriceMax,
      rent_price__gte: this.rentPriceMin,
      number_of_bedrooms: this.numberOfBedrooms,
      number_of_bedrooms__lte: this.numberOfBedroomsMax,
      number_of_bedrooms__gte: this.numberOfBedroomsMin,
    };
  }

  formatLabelLivingArea(value: number): string {
    if (value >= 1000) {
      return Math.round(value / 1000) + 'k';
    }
    return `${value}`;
  }

  formatLabelRentPrice(value: number): string {
    if (value >= 10000) {
      return Math.round(value / 1000) + 'k';
    }
    return `${value}`;
  }

  onFilterChange(filter: string) {
    console.log(filter)
    switch (filter) {
      case 'livingArea':
        document.getElementById("livingAreaFilter")!.addEventListener("change",
          (e) => {
            console.log((e.target as HTMLInputElement).id)
            const currentElement = e.target as HTMLInputElement
            if (currentElement.id === 'livingArea') {
              this.livingArea = currentElement.value
            } else if(currentElement.id === 'livingAreaMin'){
              this.livingAreaMin = currentElement.value
            }  else if(currentElement.id === 'livingAreaMax'){
              this.livingAreaMax = currentElement.value
            }
            if (this.livingArea) {
              this.isLivingAreaValue = true
              this.isLivingAreaSlider = false
              this.livingAreaMin = undefined
              this.livingAreaMax = undefined
            } else if (this.livingAreaMin || this.livingAreaMax){
              this.isLivingAreaValue = false
              this.isLivingAreaSlider = true
              this.livingArea = undefined
            }
          })
        break;
      case 'rentPrice':
        document.getElementById("rentPriceFilter")!.addEventListener("change",
          (e) => {
            this.rentPrice = (e.target as HTMLInputElement).value
            if (this.rentPrice) {
              this.isRentPrice = true
              this.rentPriceMin = undefined
              this.rentPriceMax = undefined
            } else if (this.rentPrice === '') {
              this.isRentPrice = false
            }
          })
        break;
      default:
        break;
    }
    this.list();
  }

  list() {
    this.initializeFilters();
    this.service.getListRent(this.params).subscribe({
      next: (result) => {
        const dossierArr = (result.body as unknown as any);
        if (dossierArr) {
          this.dossiers = dossierArr.items;
        }
      },
      error: (err) => {
        console.log(err);
        if (!localStorage.getItem('authenticationFlag')) {
          this.router.navigate(['']);
          alert('You are not authorized!');
        }
      }
    });
  }


  resetSlider(filter: string) {
    switch (filter) {
      case 'livingArea':
        this.isLivingAreaSlider = false
        this.isLivingAreaValue = false
        this.livingAreaMin = '0';
        this.livingAreaMax = '0';
        break;
      case 'rentPrice':
        this.isRentPrice = false
        this.rentPriceMin = '0';
        this.rentPriceMax = '0';
        break;
    }
    this.list();

  }
  resetFilters() {
    this.livingArea = undefined;
    this.livingAreaMin = undefined;
    this.livingAreaMax = undefined;
    this.isLivingAreaSlider = false;
    this.isLivingAreaSlider = false;
    this.rentPrice = undefined;
    this.rentPriceMin = undefined;
    this.rentPriceMax = undefined;
    this.isRentPrice = false;
    this.numberOfBedrooms = undefined;
    this.numberOfBedroomsMin = undefined;
    this.numberOfBedroomsMax = undefined;
    this.isNumberOfBedrooms = false;
    this.list();
  }

}
