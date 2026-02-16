<script setup>
import { computed } from "vue";
import { useConnectivityStore, useSnackbarStore } from "./utils/store";

const connectivityStore = useConnectivityStore();
const snackbarStore = useSnackbarStore();

const statusText = computed(() => connectivityStore.getStatusText);
const statusColor = computed(() =>
  connectivityStore.getIsOnline ? "success" : "error"
);
const pendingSyncCount = computed(() => connectivityStore.getPendingSyncCount);
const failedSyncCount = computed(() => connectivityStore.getFailedSyncCount);
const lastSyncError = computed(() => connectivityStore.getLastSyncError);
const shortSyncError = computed(() => {
  const message = (lastSyncError.value || "").trim();
  if (!message) {
    return "";
  }

  if (message.length <= 70) {
    return message;
  }

  return `${message.slice(0, 67)}...`;
});

const copySyncError = async () => {
  const message = (lastSyncError.value || "").trim();
  if (!message) {
    return;
  }

  try {
    await navigator.clipboard.writeText(message);
    snackbarStore.set("Erro de sincronizacao copiado.", "success");
  } catch (error) {
    snackbarStore.set("Nao foi possivel copiar o erro.", "error");
  }
};
</script>

<template>
  <v-app>
    <div class="status-bar">
      <v-chip size="small" :color="statusColor" variant="flat">
        {{ statusText }}
      </v-chip>
      <v-chip
        v-if="pendingSyncCount > 0"
        size="small"
        color="warning"
        variant="flat"
      >
        Sync pendente: {{ pendingSyncCount }}
      </v-chip>
      <v-chip
        v-if="failedSyncCount > 0"
        size="small"
        color="error"
        variant="flat"
      >
        Sync com erro: {{ failedSyncCount }}
      </v-chip>
      <v-tooltip v-if="lastSyncError" location="bottom">
        <template #activator="{ props }">
          <div class="sync-error-actions" v-bind="props">
            <v-chip
              size="small"
              color="error"
              variant="outlined"
            >
              Erro sync: {{ shortSyncError }}
            </v-chip>
            <v-btn
              size="x-small"
              color="error"
              variant="text"
              @click="copySyncError"
            >
              Copiar
            </v-btn>
          </div>
        </template>
        <span>{{ lastSyncError }}</span>
      </v-tooltip>
    </div>
    <v-main class="background-grey-lighten-4">
      <router-view />
    </v-main>
  </v-app>
</template>

<style>
  .status-bar {
    position: fixed;
    top: 8px;
    right: 8px;
    z-index: 1000;
    display: flex;
    gap: 6px;
  }

  .background-grey-lighten-4 {
    background-color: #F5F5F5;
  }

  .sync-error-actions {
    display: flex;
    align-items: center;
    gap: 4px;
  }
</style>
