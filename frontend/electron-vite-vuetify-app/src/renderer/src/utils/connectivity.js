import { useAuthStore, useConnectivityStore } from "./store";

async function checkApiHealth(timeoutMs = 2500) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch("http://127.0.0.1:8000/", {
      method: "GET",
      cache: "no-store",
      signal: controller.signal,
    });

    return response.ok;
  } catch (error) {
    return false;
  } finally {
    clearTimeout(timer);
  }
}

export function startConnectivityMonitor() {
  const connectivityStore = useConnectivityStore();
  const authStore = useAuthStore();
  let isChecking = false;

  const getLatestSyncError = (events) => {
    if (!Array.isArray(events) || events.length === 0) {
      return null;
    }

    const failedEvents = events.filter((event) => Boolean(event?.lastError));
    if (failedEvents.length === 0) {
      return null;
    }

    failedEvents.sort((a, b) => {
      const dateA = new Date(a?.updatedAt || a?.createdAt || 0).getTime();
      const dateB = new Date(b?.updatedAt || b?.createdAt || 0).getTime();
      return dateB - dateA;
    });

    return failedEvents[0]?.lastError || null;
  };

  const loadSyncSummary = async () => {
    const token = authStore.getToken;
    if (!token) {
      connectivityStore.setSyncSummary({ pending: 0, failed: 0 });
      connectivityStore.setLastSyncError(null);
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/v1/sync/pending_summary/", {
        method: "GET",
        headers: {
          "jwt-token": token,
        },
        cache: "no-store",
      });

      if (!response.ok) {
        return;
      }

      const summary = await response.json();
      connectivityStore.setSyncSummary(summary);
      return summary;
    } catch (error) {
      // Ignore transient sync-summary errors.
    }

    return null;
  };

  const loadLastSyncError = async () => {
    const token = authStore.getToken;
    if (!token) {
      connectivityStore.setLastSyncError(null);
      return null;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/v1/sync/pending_events/?limit=50", {
        method: "GET",
        headers: {
          "jwt-token": token,
        },
        cache: "no-store",
      });

      if (!response.ok) {
        return null;
      }

      const events = await response.json();
      const latestError = getLatestSyncError(events);
      connectivityStore.setLastSyncError(latestError);
      return latestError;
    } catch (error) {
      // Ignore transient pending-events errors.
    }

    return null;
  };

  const pushPendingSyncQueue = async () => {
    const token = authStore.getToken;
    if (!token) {
      return;
    }

    try {
      await fetch("http://127.0.0.1:8000/v1/sync/push_pending/?limit=20", {
        method: "POST",
        headers: {
          "jwt-token": token,
        },
        cache: "no-store",
      });
    } catch (error) {
      // Ignore transient push errors.
    }
  };

  const check = async () => {
    if (isChecking) {
      return;
    }

    isChecking = true;
    const isOnline = await checkApiHealth();
    connectivityStore.setOnline(isOnline);
    if (isOnline) {
      const summary = await loadSyncSummary();
      await loadLastSyncError();
      if (summary && (summary.pending > 0 || summary.failed > 0)) {
        await pushPendingSyncQueue();
        await loadSyncSummary();
        await loadLastSyncError();
      }
    }
    isChecking = false;
  };

  check();
  const intervalId = setInterval(check, 5000);

  window.addEventListener("online", check);
  window.addEventListener("offline", check);

  return () => {
    clearInterval(intervalId);
    window.removeEventListener("online", check);
    window.removeEventListener("offline", check);
  };
}
