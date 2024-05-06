import { Routes } from '@angular/router';
import {ListingComponent} from "./components/listing/listing.component";
import {AuthComponent} from "./components/auth/auth.component";
import {HouseRentComponent} from "./components/house-rent/house-rent.component";
import {HouseSaleComponent} from "./components/house-sale/house-sale.component";
import {CreateApartmentRentComponent} from "./components/create-apartment-rent/create-apartment-rent.component";
import {AllApartmentRentComponent} from "./components/all-apartment-rent/all-apartment-rent.component";
import {AllApartmentSaleComponent} from "./components/all-apartment-sale/all-apartment-sale.component";
import {ApartmentRentComponent} from "./components/apartment-rent/apartment-rent.component";

export const routes: Routes = [
  { path: 'list', component: ListingComponent},
  {path: '', component: AuthComponent},
  {path: 'all-apartment-rent', component: AllApartmentRentComponent},
  {path: 'all-apartment-sale', component: AllApartmentSaleComponent},
  {path: 'house-rent', component: HouseRentComponent},
  {path: 'house-sale', component: HouseSaleComponent},
  {path: 'apartment-rent/:id', component:ApartmentRentComponent},
  {path: 'create-edit-apartment-rent', component:CreateApartmentRentComponent},
  {path: 'create-edit-apartment-rent/:id', component:CreateApartmentRentComponent},
];
