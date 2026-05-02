import client from './client';
import type { PaginatedResponse, Race, RecordsResponse } from '../types';

export interface RaceFilters {
  name?: string;
  location?: string;
  date_from?: string;
  date_to?: string;
  min_distance?: string;
  max_distance?: string;
  limit?: number;
  offset?: number;
}

export async function getRaces(filters: RaceFilters = {}): Promise<PaginatedResponse<Race>> {
  const params = Object.fromEntries(
    Object.entries(filters).filter(([, v]) => v !== undefined && v !== '')
  );
  const { data } = await client.get<PaginatedResponse<Race>>('/api/races/', {
    params,
  });
  return data;
}

export async function getRace(id: number): Promise<Race> {
  const { data } = await client.get<Race>(`/api/races/${id}`);
  return data;
}

export interface RaceCreatePayload {
  name: string;
  date: string;
  distance: string;
  time: string;
  elevation_gain?: string;
  strava_url?: string;
  results_url?: string;
  location?: string;
  number_of_participants?: number;
  global_ranking?: number;
  category_ranking?: number;
}

export async function createRace(payload: RaceCreatePayload): Promise<Race> {
  const { data } = await client.post<Race>('/api/races/', payload);
  return data;
}

export async function getRecords(): Promise<RecordsResponse> {
  const { data } = await client.get<RecordsResponse>('/api/races/records');
  return data;
}
