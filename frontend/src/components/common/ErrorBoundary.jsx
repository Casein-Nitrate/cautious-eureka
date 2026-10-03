import { Component } from 'react';

export default class ErrorBoundary extends Component {
  state = { error: null };
  static getDerivedStateFromError(error) { return { error }; }
  render() {
    if (!this.state.error) return this.props.children;
    return (
      <div className="center-note" role="alert">
        <h2>Something went wrong</h2>
        <p>{String(this.state.error.message || this.state.error)}</p>
        <button className="btn" onClick={() => { this.setState({ error: null }); window.location.href = '/'; }}>Back to home</button>
      </div>
    );
  }
}
