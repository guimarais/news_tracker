import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Article, ConfigResponse, NewsResponse } from '../models/article.model';

@Injectable({ providedIn: 'root' })
export class NewsService {
  private readonly api = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getCountries(): Observable<ConfigResponse> {
    return this.http.get<ConfigResponse>(`${this.api}/config/countries`);
  }

  getTopics(): Observable<ConfigResponse> {
    return this.http.get<ConfigResponse>(`${this.api}/config/topics`);
  }

  getNews(country: string, topic: string): Observable<NewsResponse> {
    const params = new HttpParams().set('country', country).set('topic', topic);
    return this.http.get<NewsResponse>(`${this.api}/news`, { params });
  }

  refreshAll(): Observable<{ message: string }> {
    return this.http.post<{ message: string }>(`${this.api}/news/refresh`, {});
  }
}
