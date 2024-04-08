import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewApartmentSaleComponent } from './view-apartment-sale.component';

describe('ViewApartmentSaleComponent', () => {
  let component: ViewApartmentSaleComponent;
  let fixture: ComponentFixture<ViewApartmentSaleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewApartmentSaleComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ViewApartmentSaleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
