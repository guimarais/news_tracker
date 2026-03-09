import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Article } from '../../models/article.model';

@Component({
  selector: 'app-news-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './news-card.component.html',
  styleUrls: ['./news-card.component.css'],
})
export class NewsCardComponent {
  @Input() article!: Article;
}
