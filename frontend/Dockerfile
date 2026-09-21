# BountyCode frontend — production multi-stage build (Vite → Nginx).
# Stage 1: build the static bundle.
FROM node:20-alpine AS build

WORKDIR /app

ENV NODE_ENV=production

# Copy manifests and install deps (cache-friendly).
COPY package.json package-lock.json* ./
RUN npm install

# Build the app. VITE_API_URL is baked at build time by the build server.
ARG VITE_API_URL=/api
ENV VITE_API_URL=${VITE_API_URL}

COPY . .
RUN npm run build

# Stage 2: serve static files with Nginx and proxy /api + /ws to backend.
FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -qO- http://127.0.0.1/ >/dev/null 2>&1 || exit 1

CMD ["nginx", "-g", "daemon off;"]
