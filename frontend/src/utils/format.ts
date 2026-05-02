/**
 * Parse an ISO 8601 duration (e.g. "P0DT01H25M22S") or HH:MM:SS string
 * into total seconds.
 */
export function parseDurationToSeconds(raw: string): number {
  if (!raw) return 0;

  // HH:MM:SS format
  const colons = raw.split(":");
  if (colons.length === 3) {
    return (
      parseInt(colons[0]) * 3600 +
      parseInt(colons[1]) * 60 +
      parseFloat(colons[2])
    );
  }

  // ISO 8601 duration: P[nD]T[nH][nM][nS]
  const match = raw.match(
    /^P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?$/,
  );
  if (match) {
    const days = parseInt(match[1] || "0");
    const hours = parseInt(match[2] || "0");
    const minutes = parseInt(match[3] || "0");
    const seconds = parseFloat(match[4] || "0");
    return days * 86400 + hours * 3600 + minutes * 60 + seconds;
  }

  return 0;
}

/**
 * Format a duration string into a human-readable form like "1h25m22s" or "32m05s".
 */
export function formatDuration(raw: string): string {
  const totalSeconds = parseDurationToSeconds(raw);
  if (totalSeconds <= 0) return raw;
  const h = Math.floor(totalSeconds / 3600);
  const m = Math.floor((totalSeconds % 3600) / 60);
  const s = Math.round(totalSeconds % 60);
  if (h > 0)
    return `${h}h${String(m).padStart(2, "0")}m${String(s).padStart(2, "0")}s`;
  return `${m}m${String(s).padStart(2, "0")}s`;
}

/**
 * Format a decimal pace (min/km) into "M'SS" form, e.g. "5'30"".
 */
export function formatPace(pace: string): string {
  const total = parseFloat(pace);
  if (isNaN(total)) return pace;
  const mins = Math.floor(total);
  const secs = Math.round((total - mins) * 60);
  return `${mins}'${String(secs).padStart(2, "0")}"`;
}
