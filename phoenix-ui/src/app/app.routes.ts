import { Routes } from '@angular/router';
import {ListingComponent} from "./components/listing/listing.component";
import {AuthComponent} from "./components/auth/auth.component";
import {ApartmentRentComponent} from "./components/apartment-rent/apartment-rent.component";
import {ApartmentSaleComponent} from "./components/apartment-sale/apartment-sale.component";
import {HouseRentComponent} from "./components/house-rent/house-rent.component";
import {HouseSaleComponent} from "./components/house-sale/house-sale.component";
import {ViewApartmentRentComponent} from "./components/view-apartment-rent/view-apartment-rent.component";

export const routes: Routes = [
  { path: 'list', component: ListingComponent},
  {path: '', component: AuthComponent},
  {path: 'apartment-rent', component: ApartmentRentComponent},
  {path: 'apartment-sale', component: ApartmentSaleComponent},
  {path: 'house-rent', component: HouseRentComponent},
  {path: 'house-sale', component: HouseSaleComponent},
  {path: 'view-apartment-rent', component:ViewApartmentRentComponent},
];
