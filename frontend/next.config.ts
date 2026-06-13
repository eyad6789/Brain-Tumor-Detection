import type { NextConfig } from "next";

// In dev, proxy /api/* to the FastAPI backend so the browser stays same-origin
// (no CORS, no preflight on the slow /report call). Override the target with
// BACKEND_ORIGIN if the backend runs elsewhere.
const BACKEND_ORIGIN = process.env.BACKEND_ORIGIN ?? "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      { source: "/api/:path*", destination: `${BACKEND_ORIGIN}/api/:path*` },
    ];
  },
};

export default nextConfig;
