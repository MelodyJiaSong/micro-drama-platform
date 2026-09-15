import { Component, type ErrorInfo, type ReactNode } from "react";

interface Props {
  pageTitle: string;
  headingLevel?: 1 | 2;
  children: ReactNode;
}

interface State {
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    console.error("render failed", this.props.pageTitle, error, info.componentStack);
  }

  private retry = (): void => {
    this.setState({ error: null });
  };

  render(): ReactNode {
    if (this.state.error === null) return this.props.children;
    const Heading = this.props.headingLevel === 2 ? "h2" : "h1";
    return (
      <section role="alert" className="page-error">
        <Heading>{this.props.pageTitle}：显示出错</Heading>
        <p>{this.state.error.message}</p>
        <button type="button" onClick={this.retry}>
          重试
        </button>
      </section>
    );
  }
}
