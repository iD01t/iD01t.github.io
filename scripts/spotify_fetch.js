// scripts/spotify_fetch.js
// Secure catalog fetcher (Client Credentials flow).
// Env: SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_ARTIST_ID (or SPOTIFY_ARTIST_URL or ARTIST_QUERY)
// Output: assets/data/music.json

import fs from 'node:fs';
import path from 'node:path';

const CLIENT_ID = process.env.SPOTIFY_CLIENT_ID;
const CLIENT_SECRET = process.env.SPOTIFY_CLIENT_SECRET;
const ARTIST_ID = process.env.SPOTIFY_ARTIST_ID || '';
const ARTIST_URL = process.env.SPOTIFY_ARTIST_URL || '';
const ARTIST_QUERY = process.env.ARTIST_QUERY || '';

if (!CLIENT_ID || !CLIENT_SECRET) {
  console.error('Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET');
  process.exit(1);
}

function parseArtistIdFromUrl(url) {
  try {
    const u = new URL(url);
    const parts = u.pathname.split('/').filter(Boolean);
    const idx = parts.findIndex(p => p === 'artist');
    if (idx >= 0 && parts[idx+1]) return parts[idx+1];
    return '';
  } catch { return ''; }
}

async function getToken() {
  const body = new URLSearchParams({ grant_type: 'client_credentials' });
  const res = await fetch('https://accounts.spotify.com/api/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Basic ' + Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString('base64')
    },
    body
  });
  if (!res.ok) throw new Error(`Token error ${res.status}`);
  const data = await res.json();
  return data.access_token;
}

async function api(token, url) {
  const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error(`${url} -> ${res.status}`);
  return res.json();
}

async function resolveArtistId(token) {
  if (ARTIST_ID) return ARTIST_ID;
  const fromUrl = parseArtistIdFromUrl(ARTIST_URL);
  if (fromUrl) return fromUrl;
  if (ARTIST_QUERY) {
    const q = encodeURIComponent(ARTIST_QUERY);
    const data = await api(token, `https://api.spotify.com/v1/search?type=artist&limit=1&q=${q}`);
    const item = data.artists?.items?.[0];
    if (!item) throw new Error('Artist not found for query: ' + ARTIST_QUERY);
    return item.id;
  }
  throw new Error('Provide SPOTIFY_ARTIST_ID or SPOTIFY_ARTIST_URL or ARTIST_QUERY');
}

function pickImage(images = [], prefer = 640) {
  if (!images.length) return '';
  const sorted = [...images].sort((a,b)=>Math.abs((b.width||0)-prefer) - Math.abs((a.width||0)-prefer));
  return sorted[sorted.length-1]?.url || images[0].url || '';
}

async function getAllAlbums(token, artistId) {
  const qs = 'include_groups=album,single,compilation,appears_on&limit=50&market=US';
  let url = `https://api.spotify.com/v1/artists/${artistId}/albums?${qs}`;
  const all = [];
  while (url) {
    const page = await api(token, url);
    for (const a of page.items || []) {
      all.push({
        id: a.id,
        name: a.name,
        album_type: a.album_type, // album | single | compilation
        album_group: a.album_group, // album | single | compilation | appears_on
        release_date: a.release_date,
        release_date_precision: a.release_date_precision,
        year: (a.release_date||'').slice(0,4),
        url: a.external_urls?.spotify || '',
        image: pickImage(a.images),
        total_tracks: a.total_tracks
      });
    }
    url = page.next;
  }
  // Dedup by id
  const map = new Map();
  for (const a of all) map.set(a.id, a);
  return Array.from(map.values()).sort((x,y)=> (y.year||0) - (x.year||0));
}

async function getTopTracks(token, artistId) {
  const data = await api(token, `https://api.spotify.com/v1/artists/${artistId}/top-tracks?market=US`);
  return (data.tracks||[]).map(t=>({
    id: t.id,
    name: t.name,
    url: t.external_urls?.spotify || '',
    image: pickImage(t.album?.images||[]),
    album: t.album?.name || '',
    release_date: t.album?.release_date || '',
    year: (t.album?.release_date||'').slice(0,4),
    duration_ms: t.duration_ms,
    preview_url: t.preview_url
  }));
}

async function main() {
  const token = await getToken();
  const artistId = await resolveArtistId(token);
  const artist = await api(token, `https://api.spotify.com/v1/artists/${artistId}`);
  const albums = await getAllAlbums(token, artistId);
  const top = await getTopTracks(token, artistId);

  const json = {
    generated_at: new Date().toISOString(),
    artist: {
      id: artist.id,
      name: artist.name,
      url: artist.external_urls?.spotify || '',
      followers: artist.followers?.total || 0,
      genres: artist.genres || [],
      image: pickImage(artist.images)
    },
    featured: albums[0] ? { type: 'album', id: albums[0].id, name: albums[0].name, year: albums[0].year, url: albums[0].url, embed:`https://open.spotify.com/embed/album/${albums[0].id}`, image: albums[0].image } : null,
    releases: albums,
    top_tracks: top
  };

  const outPath = path.join('assets','data','music.json');
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(json, null, 2));
  console.log('Wrote', outPath, `(${albums.length} releases, ${top.length} top tracks)`);
}

main().catch(e=>{ console.error(e); process.exit(1); });
