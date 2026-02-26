# VULA Frontend

Modern Next.js frontend for AI-powered crop disease detection.

## Setup

```bash
npm install
npm run dev
```

Open http://localhost:3000

## Features

- 🔐 Authentication (Login/Register)
- 📊 Dashboard with analytics
- 🔍 Disease detection with image upload
- 📜 Detection history
- 🎨 Modern UI with Tailwind CSS & shadcn/ui
- ✨ Smooth animations with Framer Motion

## Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui
- Framer Motion
- Zustand
- Axios

## Environment Variables

Create `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Pages

- `/login` - Login page
- `/register` - Register page
- `/dashboard` - Dashboard with stats
- `/detect` - Disease detection
- `/history` - Detection history
