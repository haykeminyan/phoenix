import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HouseSaleComponent } from './house-sale.component';

describe('HouseSaleComponent', () => {
  let component: HouseSaleComponent;
  let fixture: ComponentFixture<HouseSaleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HouseSaleComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(HouseSaleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
