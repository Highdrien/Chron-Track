import { useCallback, useEffect, useMemo, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getRaces, type RaceFilters } from '../api/races';
import type { Race } from '../types';
import { formatDuration, formatPace, parseDurationToSeconds } from '../utils/format';

type SortKey = 'date' | 'name' | 'distance' | 'time' | 'pace' | 'speed' | 'location';
type SortDir = 'asc' | 'desc';

export default function HomePage() {
  const navigate = useNavigate();
  const [races, setRaces] = useState<Race[]>([]);
  const [count, setCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [sortKey, setSortKey] = useState<SortKey>('date');
  const [sortDir, setSortDir] = useState<SortDir>('desc');
  const [filters, setFilters] = useState<RaceFilters>({});
  const [showFilters, setShowFilters] = useState(false);
  const [page, setPage] = useState(0);
  const pageSize = 20;

  const fetchRaces = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getRaces({
        ...filters,
        name: search || undefined,
        limit: pageSize,
        offset: page * pageSize,
      });
      setRaces(data.items);
      setCount(data.count);
    } catch {
      setRaces([]);
    } finally {
      setLoading(false);
    }
  }, [filters, search, page]);

  useEffect(() => {
    fetchRaces();
  }, [fetchRaces]);

  const sorted = useMemo(() => {
    const copy = [...races];
    copy.sort((a, b) => {
      let cmp = 0;
      switch (sortKey) {
        case 'date':
          cmp = a.date.localeCompare(b.date);
          break;
        case 'name':
          cmp = a.name.localeCompare(b.name);
          break;
        case 'distance':
          cmp = parseFloat(a.distance) - parseFloat(b.distance);
          break;
        case 'time':
          cmp = parseDurationToSeconds(a.time) - parseDurationToSeconds(b.time);
          break;
        case 'pace':
          cmp = parseFloat(a.pace) - parseFloat(b.pace);
          break;
        case 'speed':
          cmp = parseFloat(a.speed) - parseFloat(b.speed);
          break;
        case 'location':
          cmp = (a.location ?? '').localeCompare(b.location ?? '');
          break;
      }
      return sortDir === 'asc' ? cmp : -cmp;
    });
    return copy;
  }, [races, sortKey, sortDir]);

  function handleSort(key: SortKey) {
    if (sortKey === key) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortKey(key);
      setSortDir('asc');
    }
  }

  const totalPages = Math.ceil(count / pageSize);

  const sortIcon = (key: SortKey) => {
    if (sortKey !== key) return '↕';
    return sortDir === 'asc' ? '↑' : '↓';
  };

  const thClass =
    'px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500 cursor-pointer select-none hover:text-gray-700 transition-colors';

  return (
    <div>
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Mes Courses</h1>
        <div className="flex items-center gap-3">
          <Link
            to="/races/new"
            className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500"
          >
            + Nouvelle course
          </Link>
          <div className="relative">
            <input
              type="text"
              placeholder="Rechercher une course..."
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(0);
              }}
              className="w-64 rounded-lg border border-gray-300 py-2 pl-10 pr-4 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />
            <svg
              className="absolute left-3 top-2.5 h-4 w-4 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`rounded-lg border px-3 py-2 text-sm font-medium transition-colors ${showFilters
                ? 'border-indigo-300 bg-indigo-50 text-indigo-700'
                : 'border-gray-300 text-gray-600 hover:bg-gray-50'
              }`}
          >
            Filtres
          </button>
        </div>
      </div>

      {showFilters && (
        <div className="mb-6 grid grid-cols-2 gap-4 rounded-xl border border-gray-200 bg-white p-4 shadow-sm sm:grid-cols-4">
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">
              Distance min (km)
            </label>
            <input
              type="number"
              step="0.1"
              value={filters.min_distance ?? ''}
              onChange={(e) => {
                setFilters((f) => ({
                  ...f,
                  min_distance: e.target.value || undefined,
                }));
                setPage(0);
              }}
              className="w-full rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">
              Distance max (km)
            </label>
            <input
              type="number"
              step="0.1"
              value={filters.max_distance ?? ''}
              onChange={(e) => {
                setFilters((f) => ({
                  ...f,
                  max_distance: e.target.value || undefined,
                }));
                setPage(0);
              }}
              className="w-full rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Date debut</label>
            <input
              type="date"
              value={filters.date_from ?? ''}
              onChange={(e) => {
                setFilters((f) => ({
                  ...f,
                  date_from: e.target.value || undefined,
                }));
                setPage(0);
              }}
              className="w-full rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Date fin</label>
            <input
              type="date"
              value={filters.date_to ?? ''}
              onChange={(e) => {
                setFilters((f) => ({
                  ...f,
                  date_to: e.target.value || undefined,
                }));
                setPage(0);
              }}
              className="w-full rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />
          </div>
        </div>
      )}

      <div className="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b border-gray-200 bg-gray-50">
              <tr>
                <th className={thClass} onClick={() => handleSort('date')}>
                  Date {sortIcon('date')}
                </th>
                <th className={thClass} onClick={() => handleSort('name')}>
                  Nom {sortIcon('name')}
                </th>
                <th className={thClass} onClick={() => handleSort('distance')}>
                  Distance {sortIcon('distance')}
                </th>
                <th className={thClass} onClick={() => handleSort('time')}>
                  Temps {sortIcon('time')}
                </th>
                <th className={thClass} onClick={() => handleSort('pace')}>
                  Allure {sortIcon('pace')}
                </th>
                <th className={thClass} onClick={() => handleSort('speed')}>
                  Vitesse {sortIcon('speed')}
                </th>
                <th className={thClass} onClick={() => handleSort('location')}>
                  Lieu {sortIcon('location')}
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {loading ? (
                <tr>
                  <td colSpan={7} className="px-4 py-12 text-center">
                    <div className="mx-auto h-6 w-6 animate-spin rounded-full border-4 border-indigo-600 border-t-transparent" />
                  </td>
                </tr>
              ) : sorted.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-4 py-12 text-center text-sm text-gray-500">
                    Aucune course trouvee.
                  </td>
                </tr>
              ) : (
                sorted.map((race) => (
                  <tr
                    key={race.id}
                    onClick={() => navigate(`/races/${race.id}`)}
                    className="cursor-pointer transition-colors hover:bg-indigo-50"
                  >
                    <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-700">
                      {new Date(race.date).toLocaleDateString('fr-FR')}
                    </td>
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">
                      {race.name}
                    </td>
                    <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-700">
                      {race.distance} km
                    </td>
                    <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-700">
                      {formatDuration(race.time)}
                    </td>
                    <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-700">
                      {formatPace(race.pace)} /km
                    </td>
                    <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-700">
                      {parseFloat(race.speed).toFixed(1)} km/h
                    </td>
                    <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-500">
                      {race.location ?? '-'}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {totalPages > 1 && (
          <div className="flex items-center justify-between border-t border-gray-200 bg-gray-50 px-4 py-3">
            <span className="text-sm text-gray-500">
              {count} course{count > 1 ? 's' : ''} au total
            </span>
            <div className="flex items-center gap-2">
              <button
                disabled={page === 0}
                onClick={() => setPage((p) => p - 1)}
                className="rounded-lg border border-gray-300 px-3 py-1 text-sm disabled:opacity-40"
              >
                Precedent
              </button>
              <span className="text-sm text-gray-600">
                {page + 1} / {totalPages}
              </span>
              <button
                disabled={page + 1 >= totalPages}
                onClick={() => setPage((p) => p + 1)}
                className="rounded-lg border border-gray-300 px-3 py-1 text-sm disabled:opacity-40"
              >
                Suivant
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
