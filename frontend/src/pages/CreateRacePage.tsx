import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { createRace } from '../api/races';

interface FormData {
  name: string;
  date: string;
  distance: string;
  hours: string;
  minutes: string;
  seconds: string;
  elevation_gain: string;
  location: string;
  number_of_participants: string;
  global_ranking: string;
  category_ranking: string;
  strava_url: string;
  results_url: string;
}

const initial: FormData = {
  name: '',
  date: '',
  distance: '',
  hours: '',
  minutes: '',
  seconds: '',
  elevation_gain: '',
  location: '',
  number_of_participants: '',
  global_ranking: '',
  category_ranking: '',
  strava_url: '',
  results_url: '',
};

function buildDuration(h: string, m: string, s: string): string {
  return `${h.padStart(2, '0')}:${m.padStart(2, '0')}:${s.padStart(2, '0')}`;
}

export default function CreateRacePage() {
  const navigate = useNavigate();
  const [form, setForm] = useState<FormData>(initial);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  function set(field: keyof FormData) {
    return (e: React.ChangeEvent<HTMLInputElement>) =>
      setForm((f) => ({ ...f, [field]: e.target.value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError('');
    setSubmitting(true);

    try {
      const payload: Record<string, unknown> = {
        name: form.name,
        date: form.date,
        distance: form.distance,
        time: buildDuration(form.hours || '0', form.minutes || '0', form.seconds || '0'),
      };

      if (form.elevation_gain) payload.elevation_gain = form.elevation_gain;
      if (form.location) payload.location = form.location;
      if (form.strava_url) payload.strava_url = form.strava_url;
      if (form.results_url) payload.results_url = form.results_url;
      if (form.number_of_participants)
        payload.number_of_participants = parseInt(form.number_of_participants);
      if (form.global_ranking) payload.global_ranking = parseInt(form.global_ranking);
      if (form.category_ranking) payload.category_ranking = parseInt(form.category_ranking);

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const race = await createRace(payload as any);
      navigate(`/races/${race.id}`);
    } catch {
      setError('Erreur lors de la creation de la course.');
    } finally {
      setSubmitting(false);
    }
  }

  const inputClass =
    'mt-1 block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500';
  const labelClass = 'block text-sm font-medium text-gray-700';

  return (
    <div className="mx-auto max-w-2xl">
      <Link
        to="/"
        className="mb-6 inline-flex items-center gap-1 text-sm font-medium text-indigo-600 hover:text-indigo-500"
      >
        <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        Retour aux courses
      </Link>

      <div className="rounded-xl border border-gray-200 bg-white shadow-sm">
        <div className="border-b border-gray-200 px-6 py-5">
          <h1 className="text-2xl font-bold text-gray-900">Nouvelle course</h1>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 p-6">
          {error && (
            <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</div>
          )}

          {/* Required fields */}
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="name" className={labelClass}>
                Nom *
              </label>
              <input
                id="name"
                type="text"
                required
                value={form.name}
                onChange={set('name')}
                className={inputClass}
              />
            </div>
            <div>
              <label htmlFor="date" className={labelClass}>
                Date *
              </label>
              <input
                id="date"
                type="date"
                required
                value={form.date}
                onChange={set('date')}
                className={inputClass}
              />
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="distance" className={labelClass}>
                Distance (km) *
              </label>
              <input
                id="distance"
                type="number"
                step="0.01"
                min="0"
                required
                value={form.distance}
                onChange={set('distance')}
                className={inputClass}
              />
            </div>
            <div>
              <label className={labelClass}>Temps *</label>
              <div className="mt-1 flex items-center gap-2">
                <input
                  type="number"
                  min="0"
                  placeholder="h"
                  value={form.hours}
                  onChange={set('hours')}
                  className="w-20 rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
                <span className="text-gray-400">:</span>
                <input
                  type="number"
                  min="0"
                  max="59"
                  placeholder="m"
                  required
                  value={form.minutes}
                  onChange={set('minutes')}
                  className="w-20 rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
                <span className="text-gray-400">:</span>
                <input
                  type="number"
                  min="0"
                  max="59"
                  placeholder="s"
                  required
                  value={form.seconds}
                  onChange={set('seconds')}
                  className="w-20 rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
              </div>
            </div>
          </div>

          {/* Optional fields */}
          <div className="border-t border-gray-200 pt-6">
            <h2 className="mb-4 text-sm font-semibold uppercase tracking-wider text-gray-400">
              Informations optionnelles
            </h2>

            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <label htmlFor="location" className={labelClass}>
                  Lieu
                </label>
                <input
                  id="location"
                  type="text"
                  value={form.location}
                  onChange={set('location')}
                  className={inputClass}
                />
              </div>
              <div>
                <label htmlFor="elevation_gain" className={labelClass}>
                  Denivele positif (m)
                </label>
                <input
                  id="elevation_gain"
                  type="number"
                  step="0.01"
                  min="0"
                  value={form.elevation_gain}
                  onChange={set('elevation_gain')}
                  className={inputClass}
                />
              </div>
              <div>
                <label htmlFor="participants" className={labelClass}>
                  Nombre de participants
                </label>
                <input
                  id="participants"
                  type="number"
                  min="1"
                  value={form.number_of_participants}
                  onChange={set('number_of_participants')}
                  className={inputClass}
                />
              </div>
              <div>
                <label htmlFor="global_ranking" className={labelClass}>
                  Classement general
                </label>
                <input
                  id="global_ranking"
                  type="number"
                  min="1"
                  value={form.global_ranking}
                  onChange={set('global_ranking')}
                  className={inputClass}
                />
              </div>
              <div>
                <label htmlFor="category_ranking" className={labelClass}>
                  Classement categorie
                </label>
                <input
                  id="category_ranking"
                  type="number"
                  min="1"
                  value={form.category_ranking}
                  onChange={set('category_ranking')}
                  className={inputClass}
                />
              </div>
              <div>
                <label htmlFor="strava_url" className={labelClass}>
                  Lien Strava
                </label>
                <input
                  id="strava_url"
                  type="url"
                  value={form.strava_url}
                  onChange={set('strava_url')}
                  className={inputClass}
                />
              </div>
              <div>
                <label htmlFor="results_url" className={labelClass}>
                  Lien resultats
                </label>
                <input
                  id="results_url"
                  type="url"
                  value={form.results_url}
                  onChange={set('results_url')}
                  className={inputClass}
                />
              </div>
            </div>
          </div>

          <div className="flex justify-end gap-3 border-t border-gray-200 pt-6">
            <Link
              to="/"
              className="rounded-lg border border-gray-300 px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Annuler
            </Link>
            <button
              type="submit"
              disabled={submitting}
              className="rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 disabled:opacity-50"
            >
              {submitting ? 'Creation...' : 'Creer la course'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
