import client from './client';
import type { TokenPair, User } from '../types';

export async function login(username: string, password: string): Promise<TokenPair> {
  const { data } = await client.post<TokenPair>('/api/auth/token/pair', {
    username,
    password,
  });
  return data;
}

export async function register(
  username: string,
  password: string,
  email: string
): Promise<TokenPair> {
  const { data } = await client.post<TokenPair>('/api/auth/register', {
    username,
    password,
    email,
  });
  return data;
}

export async function getMe(): Promise<User> {
  const { data } = await client.get<User>('/api/auth/me');
  return data;
}
