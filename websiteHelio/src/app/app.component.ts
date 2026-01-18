import { Component, OnInit, OnDestroy } from '@angular/core';
import { trigger, transition, style, animate, state } from '@angular/animations';

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  animations: [
    trigger('textChange', [
      state('void', style({ opacity: 0, transform: 'translateY(20px)' })),
      transition(':enter', [
        style({ opacity: 0, transform: 'translateY(20px)' }),
        animate('0.3s ease-in', style({ opacity: 1, transform: 'translateY(0)' }))
      ]),
      transition(':leave', [
        animate('0.3s ease-out', style({ opacity: 0, transform: 'translateY(-20px)' }))
      ]),
      transition('* => *', [
        animate('0.6s ease-in-out', style({ transform: 'translateY(0)' }))
      ])
    ])
  ]
})
export class AppComponent implements OnInit, OnDestroy {
  fixedText = 'helio fernandes';
  changingTexts = ['DevOps', 'Develop', 'Arquiteto de software'];
  currentIndex = 0;
  currentText = this.changingTexts[0];
  private intervalId: any;

  ngOnInit() {
    this.intervalId = setInterval(() => {
      this.rotateText();
    }, 3000);
  }

  ngOnDestroy() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }

  rotateText() {
    this.currentIndex = (this.currentIndex + 1) % this.changingTexts.length;
    this.currentText = this.changingTexts[this.currentIndex];
  }
}
