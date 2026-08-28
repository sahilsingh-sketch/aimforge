export interface AimRating {
  aim: number;
  movement: number;
  positioning: number;
  gameSense: number;
  recoil: number;
  crosshair: number;
  decisions: number;
  utility: number;
}

export interface TimestampEvent {
  id: string;
  timestamp: string;
  seconds: number;
  title: string;
  severity: "critical" | "warning" | "positive" | "info";
  category: string;
  confidence: number;
  description: string;
}

export interface AnalysisResponse {
  jobId: string;
  overallScore: number;
  strengths: string[];
  weaknesses: string[];
  mistakes: string[];
  improvements: string[];
  events: TimestampEvent[];
  ratings: AimRating;
  summary: string;
  recommendations: string[];
  trainingPlan: {
    drills: string[];
    focusAreas: string[];
  };
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp?: number;
}
