import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Article } from './models/article.model';
import { NewsService } from './services/news.service';
import { NewsListComponent } from './components/news-list/news-list.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, NewsListComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
  countries: string[] = [];
  topics: string[] = [];

  selectedCountry = '';
  selectedTopic = '';
  selectedBias = '';

  articles: Article[] = [];
  filteredArticles: Article[] = [];

  loading = false;
  refreshing = false;
  error = '';

  constructor(private newsService: NewsService) {}

  ngOnInit(): void {
    this.newsService.getCountries().subscribe({
      next: (res) => (this.countries = res.items),
    });
    this.newsService.getTopics().subscribe({
      next: (res) => (this.topics = res.items),
    });
  }

  loadNews(): void {
    if (!this.selectedCountry || !this.selectedTopic) return;
    this.loading = true;
    this.error = '';
    this.articles = [];

    this.newsService.getNews(this.selectedCountry, this.selectedTopic).subscribe({
      next: (res) => {
        this.articles = res.articles;
        this.applyBiasFilter();
        this.loading = false;
      },
      error: () => {
        this.error = 'Failed to load news. Is the backend running?';
        this.loading = false;
      },
    });
  }

  applyBiasFilter(): void {
    this.filteredArticles = this.selectedBias
      ? this.articles.filter((a) => a.bias === this.selectedBias)
      : [...this.articles];
  }

  onFilterChange(): void {
    this.applyBiasFilter();
  }

  refreshAll(): void {
    this.refreshing = true;
    this.newsService.refreshAll().subscribe({
      next: () => {
        this.refreshing = false;
        this.loadNews();
      },
      error: () => {
        this.refreshing = false;
      },
    });
  }

  get canLoad(): boolean {
    return !!this.selectedCountry && !!this.selectedTopic;
  }
}
