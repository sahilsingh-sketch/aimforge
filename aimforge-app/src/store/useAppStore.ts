import { create } from "zustand";
import type { AnalysisResponse, ChatMessage } from "../types";

interface AppState {
  jobId: string | null;
  videoUrl: string | null;
  setVideoUrl: (url: string | null) => void;
  setJobId: (id: string | null) => void;
  
  analysis: AnalysisResponse | null;
  setAnalysis: (data: AnalysisResponse | null) => void;
  
  chatHistory: ChatMessage[];
  addChatMessage: (msg: ChatMessage) => void;
  setChatHistory: (history: ChatMessage[]) => void;
  clearChat: () => void;
  
  currentVideoTime: number;
  setCurrentVideoTime: (time: number) => void;
  resetState: () => void;
  
  // Global Upload State
  uploadFile: File | null;
  setUploadFile: (file: File | null) => void;
  uploadProgress: number;
  setUploadProgress: (progress: number) => void;
  uploadStatus: "idle" | "ready" | "starting" | "validating" | "uploading" | "uploaded" | "queued_for_analysis" | "analyzing" | "report_ready" | "error";
  setUploadStatus: (status: "idle" | "ready" | "starting" | "validating" | "uploading" | "uploaded" | "queued_for_analysis" | "analyzing" | "report_ready" | "error") => void;
  uploadError: string | null;
  setUploadError: (error: string | null) => void;
  uploadEstimatedTime: string;
  setUploadEstimatedTime: (time: string) => void;
  analysisStage: string | null;
  setAnalysisStage: (stage: string | null) => void;
  analysisProgress: number;
  setAnalysisProgress: (progress: number) => void;
  uploadAbortController: AbortController | null;
  setUploadAbortController: (controller: AbortController | null) => void;
  clearUpload: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  jobId: null,
  videoUrl: null,
  setVideoUrl: (url) => set({ videoUrl: url }),
  setJobId: (id) => set({ jobId: id }),
  
  analysis: null,
  setAnalysis: (data) => set({ analysis: data }),
  
  chatHistory: [],
  addChatMessage: (msg) => set((state) => ({ chatHistory: [...state.chatHistory, msg] })),
  setChatHistory: (history) => set({ chatHistory: history }),
  clearChat: () => set({ chatHistory: [] }),
  
  currentVideoTime: 0,
  setCurrentVideoTime: (time) => set({ currentVideoTime: time }),

  uploadFile: null,
  setUploadFile: (file) => set({ uploadFile: file }),
  uploadProgress: 0,
  setUploadProgress: (progress) => set({ uploadProgress: progress }),
  uploadStatus: "idle",
  setUploadStatus: (status) => set({ uploadStatus: status }),
  uploadError: null,
  setUploadError: (error) => set({ uploadError: error }),
  uploadEstimatedTime: "",
  setUploadEstimatedTime: (time) => set({ uploadEstimatedTime: time }),
  analysisStage: null,
  setAnalysisStage: (stage) => set({ analysisStage: stage }),
  analysisProgress: 0,
  setAnalysisProgress: (progress) => set({ analysisProgress: progress }),
  
  uploadAbortController: null,
  setUploadAbortController: (controller) => set({ uploadAbortController: controller }),
  
  clearUpload: () => set({
    uploadFile: null,
    uploadProgress: 0,
    uploadStatus: "idle",
    uploadError: null,
    uploadEstimatedTime: "",
    uploadAbortController: null,
    analysisStage: null,
    analysisProgress: 0
  }),

  resetState: () => set({
    jobId: null,
    videoUrl: null,
    analysis: null,
    currentVideoTime: 0,
    chatHistory: [],
    uploadFile: null,
    uploadProgress: 0,
    uploadStatus: "idle",
    uploadError: null,
    uploadEstimatedTime: "",
    uploadAbortController: null,
    analysisStage: null,
    analysisProgress: 0
  })
}));
