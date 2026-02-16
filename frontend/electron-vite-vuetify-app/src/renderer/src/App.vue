<script setup>
import { computed } from "vue";
import { useConnectivityStore } from "./utils/store";

const connectivityStore = useConnectivityStore();

const statusText = computed(() => connectivityStore.getStatusText);
const statusColor = computed(() =>
  connectivityStore.getIsOnline ? "success" : "error"
);
const pendingSyncCount = computed(() => connectivityStore.getPendingSyncCount);
const failedSyncCount = computed(() => connectivityStore.getFailedSyncCount);
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
</style>
