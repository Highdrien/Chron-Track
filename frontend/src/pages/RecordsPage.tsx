import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getRecords } from '../api/races';
import type { Race } from '../types';
import { formatDuration, formatPace } from '../utils/format';

const CATEGORIES = [
  { key: '5K', label: '5 km' },
  { key: '10K', label: '10 km' },
  { key: '20K', label: '20 km' },
  { key: 'Semi', label: 'Semi-marathon' },
  { key: '30K', label: '30 km' },
  { key: 'Marathon', label: 'Marathon' },
];

export default function RecordsPage() {
  const navigate = useNavigate();
  const [records, setRecords] = useState<Record<string, Race | null>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getRecords()
      .then((data) => setRecords(data.records))
      .catch(() => setRecords({}))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-600 border-t-transparent" />
      </div>
    );
  }

  return (
    <div>
      <h1 className="mb-8 text-2xl font-bold text-gray-900">Records Personnels</h1>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {CATEGORIES.map(({ key, label }) => {
          const race = records[key];
          return (
            <div
              key={key}
              onClick={() => race && navigate(`/races/${race.id}`)}
              className={`rounded-xl border bg-white shadow-sm transition-all ${
                race
                  ? 'cursor-pointer border-gray-200 hover:border-indigo-300 hover:shadow-md'
                  : 'border-dashed border-gray-300'
              }`}
            >
              <div className="border-b border-gray-100 px-5 py-4">
                <h2 className="text-lg font-semibold text-gray-900">{label}</h2>
              </div>

              {race ? (
                <div className="space-y-3 px-5 py-4">
                  <p className="font-medium text-gray-900">{race.name}</p>
                  <p className="text-sm text-gray-500">
                    {new Date(race.date).toLocaleDateString('fr-FR')}
                    {race.location && ` — ${race.location}`}
                  </p>
                  <div className="grid grid-cols-3 gap-3 pt-2">
                    <div>
                      <p className="text-xs font-medium uppercase text-gray-400">Temps</p>
                      <p className="text-sm font-semibold text-indigo-600">
                        {formatDuration(race.time)}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs font-medium uppercase text-gray-400">Allure</p>
                      <p className="text-sm font-semibold text-indigo-600">
                        {formatPace(race.pace)} /km
                      </p>
                    </div>
                    <div>
                      <p className="text-xs font-medium uppercase text-gray-400">Vitesse</p>
                      <p className="text-sm font-semibold text-indigo-600">
                        {parseFloat(race.speed).toFixed(1)} km/h
                      </p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="px-5 py-8 text-center">
                  <p className="text-sm text-gray-400">Pas encore de course sur cette distance</p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
