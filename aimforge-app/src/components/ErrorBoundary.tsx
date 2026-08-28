import { Component, type ErrorInfo, type ReactNode } from "react";

interface Props {
  children?: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught React Error:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }
      return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-zinc-950 text-neutral-50 p-6 text-center">
          <h2 className="text-3xl font-bold mb-4 text-[#ff6467]">Dashboard Crashed</h2>
          <p className="text-[#9f9fa9] mb-4 text-lg">An unexpected rendering error occurred.</p>
          <div className="bg-black/50 border border-white/10 rounded-xl p-6 text-left mb-6 max-w-lg w-full overflow-auto">
            <div className="text-sm text-neutral-300 font-mono whitespace-pre-wrap">
              {this.state.error?.toString()}
            </div>
          </div>
          <button onClick={() => window.location.href = '/'} className="cursor-pointer px-6 py-3 bg-[#f54900] text-white rounded-lg font-semibold hover:bg-[#ff6467] transition-colors">
            Return to Home
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
