# LectureMind AI

A premium AI‑powered lecture & meeting note generation platform.

## Overview
- Upload audio/video lectures
- Speaker diarization (who said what)
- Select teacher / target speaker
- AI‑generated structured notes, quiz, flashcards
- Multilingual support, PDF export, search, analytics
- 3D immersive UI built with Three.js / React‑Three‑Fiber

## Tech Stack
- **Frontend**: React, TypeScript, Vite, Tailwind, Framer Motion, Three.js, Lucide
- **Backend**: Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL
- **AI**: OpenAI Whisper, pyannote.audio, LLM API (OpenAI compatible), LangChain (optional)
- **Storage**: Local filesystem (with abstraction for S3/GCS)
- **Auth**: JWT, bcrypt

## Project Structure
```
lecturemind-ai/
├─ frontend/
│  └─ src/ ...
├─ backend/
│  └─ app/ ...
├─ storage/
│  ├─ uploads/
│  ├─ processed/
│  └─ generated/
├─ database/migrations/
├─ docs/
├─ docker-compose.yml
├─ .env.example
└─ README.md
```
