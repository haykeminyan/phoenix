import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AllApartmentRentComponent } from './all-apartment-rent.component';

describe('ApartmentRentComponent', () => {
  let component: AllApartmentRentComponent;
  let fixture: ComponentFixture<AllApartmentRentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AllApartmentRentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AllApartmentRentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
