import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AllApartmentSaleComponent } from './all-apartment-sale.component';

describe('ApartmentSaleComponent', () => {
  let component: AllApartmentSaleComponent;
  let fixture: ComponentFixture<AllApartmentSaleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AllApartmentSaleComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AllApartmentSaleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
