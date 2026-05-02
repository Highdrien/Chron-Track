import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getRace } from '../api/races';
import type { Race } from '../types';
import { formatDuration, formatPace } from '../utils/format';

interface DetailItemProps {
  label: string;
  value: string | number | null | undefined;
  link?: boolean;
}

function DetailItem({ label, value, link }: DetailItemProps) {
  if (value === null || value === undefined) return null;
  return (
    <div className="flex flex-col">
      <dt className="text-xs font-medium uppercase tracking-wider text-gray-500">{label}</dt>
      <dd className="mt-1 text-sm font-medium text-gray-900">
        {link ? (
          <a
            href={String(value)}
            target="_blank"
            rel="noopener noreferrer"
            className="text-indigo-600 underline hover:text-indigo-500"
          >
            Voir
          </a>
        ) : (
          value
        )}
      </dd>
    </div>
  );
}

export default function RaceDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [race, setRace] = useState<Race | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!id) return;
    getRace(Number(id))
      .then(setRace)
      .catch(() => setError('Course introuvable.'))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-600 border-t-transparent" />
      </div>
    );
  }

  if (error || !race) {
    return (
      <div className="py-20 text-center">
        <p className="text-gray-500">{error || 'Course introuvable.'}</p>
        <Link
          to="/"
          className="mt-4 inline-block text-sm font-medium text-indigo-600 hover:text-indigo-500"
        >
          Retour aux courses
        </Link>
      </div>
    );
  }

  return (
    <div>
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
          <h1 className="text-2xl font-bold text-gray-900">{race.name}</h1>
        </div>

        <dl className="grid grid-cols-2 gap-6 p-6 sm:grid-cols-3 lg:grid-cols-4">
          <DetailItem
            label="Date"
            value={new Date(race.date).toLocaleDateString('fr-FR', {
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          />
          <DetailItem label="Distance" value={`${race.distance} km`} />
          <DetailItem label="Temps" value={formatDuration(race.time)} />
          <DetailItem label="Allure" value={`${formatPace(race.pace)} /km`} />
          <DetailItem label="Vitesse" value={`${parseFloat(race.speed).toFixed(1)} km/h`} />
          <DetailItem label="Lieu" value={race.location} />
          <DetailItem
            label="Denivele"
            value={race.elevation_gain ? `${race.elevation_gain} m D+` : undefined}
          />
          <DetailItem label="Participants" value={race.number_of_participants} />
          <DetailItem
            label="Classement general"
            value={
              race.global_ranking && race.number_of_participants
                ? `${race.global_ranking} / ${race.number_of_participants}`
                : race.global_ranking
            }
          />
          <DetailItem label="Classement categorie" value={race.category_ranking} />
          <DetailItem label="Strava" value={race.strava_url} link />
          <DetailItem label="Resultats" value={race.results_url} link />
        </dl>
      </div>
    </div>
  );
}
