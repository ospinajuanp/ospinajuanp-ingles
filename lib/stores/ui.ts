'use client'
import { create } from 'zustand'

interface UiState {
  syncModalOpen: boolean
  openSyncModal: () => void
  closeSyncModal: () => void
}

export const useUiStore = create<UiState>((set) => ({
  syncModalOpen: false,
  openSyncModal: () => set({ syncModalOpen: true }),
  closeSyncModal: () => set({ syncModalOpen: false }),
}))
