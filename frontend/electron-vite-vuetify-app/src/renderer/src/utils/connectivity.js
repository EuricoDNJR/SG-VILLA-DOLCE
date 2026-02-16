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

  const loadSyncSummary = async () => {
    const token = authStore.getToken;
    if (!token) {
      connectivityStore.setSyncSummary({ pending: 0, failed: 0 });
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
      if (summary && (summary.pending > 0 || summary.failed > 0)) {
        await pushPendingSyncQueue();
        await loadSyncSummary();
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
