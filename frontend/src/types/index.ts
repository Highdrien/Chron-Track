export interface User {
  id: number;
  username: string;
  email: string;
}

export interface Race {
  id: number;
  user: number;
  name: string;
  date: string;
  distance: string;
  elevation_gain: string | null;
  time: string;
  speed: string;
  pace: string;
  strava_url: string | null;
  results_url: string | null;
  location: string | null;
  number_of_participants: number | null;
  global_ranking: number | null;
  category_ranking: number | null;
}

export interface PaginatedResponse<T> {
  items: T[];
  count: number;
}

export interface TokenPair {
  access: string;
  refresh: string;
}

export interface RecordsResponse {
  records: Record<string, Race | null>;
}
