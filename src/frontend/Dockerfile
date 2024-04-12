# Stage 1: Build the React app
FROM node:18 AS build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Build the React app
COPY . .
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Copy built assets to nginx html directory
COPY --from=build /app/build /usr/share/nginx/html

# Optional: override default nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

