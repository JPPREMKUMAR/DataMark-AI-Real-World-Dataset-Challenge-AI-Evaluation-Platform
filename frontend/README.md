# DataMark AI Frontend

React + Vite + Tailwind dashboard for the existing FastAPI API.

## Setup
1. Install Node.js 20.19+ or 22.12+.
2. Copy `.env.example` to `.env`.
3. Run `npm install`.
4. Run `npm run dev`.
5. Build with `npm run build`.

## Vercel
Set Root Directory to `frontend`, Framework to Vite, Build Command `npm run build`, Output Directory `dist`, and environment variable `VITE_API_BASE_URL=https://datamark-pied.vercel.app`.

## Backend limitations
- `/benchmarks/run` currently returns a readiness instruction; it does not execute a benchmark.
- `/evaluate` evaluates numeric values only, not arbitrary code submissions.
- Vercel serverless filesystem writes are ephemeral. Uploads and cleaned datasets need persistent external storage for production.
- Current demo datasets are synthetic, not authentic real-world datasets.
