export interface Article {
  id: string;
  title: string;
  url: string;
  source: string;
  country: string;
  topic: string;
  published_at?: string;
  description?: string;
  summary?: string;
  bias?: 'biased' | 'unbiased';
  bias_reasoning?: string;
  analyzed: boolean;
}

export interface NewsResponse {
  articles: Article[];
  total: number;
  country: string;
  topic: string;
}

export interface ConfigResponse {
  items: string[];
}
