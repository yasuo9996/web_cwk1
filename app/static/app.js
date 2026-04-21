const API_KEY = 'dev-secret-key';

const spotifyCatalog = {
  'Blinding Lights|The Weeknd': {
    spotifyUrl: 'https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b',
    coverUrl: 'https://i.scdn.co/image/ab67616d0000b273ffe5776f8f5d5472f0e3d7cb'
  },
  'Levitating|Dua Lipa': {
    spotifyUrl: 'https://open.spotify.com/track/463CkQjx2Zk1yXoBuierM9',
    coverUrl: 'https://i.scdn.co/image/ab67616d0000b273d4daf28d55fe4197ede848be'
  },
  'As It Was|Harry Styles': {
    spotifyUrl: 'https://open.spotify.com/track/4LRPiXqCikLlN15c3yImP7',
    coverUrl: 'https://i.scdn.co/image/ab67616d0000b273b46f74097655d7f353caab14'
  },
  'bad guy|Billie Eilish': {
    spotifyUrl: 'https://open.spotify.com/track/2Fxmhks0bxGSBdJ92vM42m',
    coverUrl: 'https://i.scdn.co/image/ab67616d0000b27350a3147b4edd7701a876c6ce'
  }
};

function getAuthToken() {
  return localStorage.getItem('hs_auth_token');
}

function requireLogin() {
  const isLoginPage = window.location.pathname === '/';
  if (!getAuthToken() && !isLoginPage) {
    window.location.href = '/';
  }
}

function logout() {
  localStorage.removeItem('hs_auth_token');
  localStorage.removeItem('hs_username');
  window.location.href = '/';
}

async function requestJson(url, options = {}) {
  const token = getAuthToken();
  const mergedOptions = {
    ...options,
    headers: {
      'X-API-Key': API_KEY,
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  };

  const res = await fetch(url, mergedOptions);
  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }

  if (!res.ok) {
    const message = data?.detail || `请求失败 (${res.status})`;
    throw new Error(message);
  }

  return data;
}

function showToast(message, type = 'ok') {
  const wrap = document.getElementById('toast-wrap') || document.body;
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  wrap.appendChild(toast);
  setTimeout(() => toast.classList.add('show'), 30);
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 260);
  }, 2200);
}

function formatDuration(durationMs) {
  if (!durationMs) return '--:--';
  const total = Math.floor(durationMs / 1000);
  const m = Math.floor(total / 60);
  const s = String(total % 60).padStart(2, '0');
  return `${m}:${s}`;
}

function enrichTrack(track) {
  const key = `${track.title}|${track.artist}`;
  const ext = spotifyCatalog[key];
  return {
    ...track,
    spotifyUrl: ext?.spotifyUrl || null,
    coverUrl: ext?.coverUrl || 'https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=500&q=80'
  };
}

requireLogin();
