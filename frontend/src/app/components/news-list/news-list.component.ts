import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Article } from '../../models/article.model';
import { NewsCardComponent } from '../news-card/news-card.component';

@Component({
  selector: 'app-news-list',
  standalone: true,
  imports: [CommonModule, NewsCardComponent],
  templateUrl: './news-list.component.html',
  styleUrls: ['./news-list.component.css'],
})
export class NewsListComponent {
  @Input() articles: Article[] = [];
  @Input() loading = false;
  @Input() error = '';
}
