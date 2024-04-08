# Use Node.js LTS version as base image
FROM node:lts AS builder

# Set working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY phoenix-ui/package*.json ./

# Install Angular CLI
RUN npm install -g @angular/cli

# Install dependencies
RUN npm install --force

# Copy project files
COPY . .

# Set working directory to Angular project directory
WORKDIR /usr/src/app/phoenix-ui

# Build Angular project for production
RUN /usr/local/bin/ng build --configuration=production


# Use nginx as production server
FROM nginx:stable-alpine
RUN rm -rf /usr/share/nginx/html/phoenix-ui

# Copy built Angular app to nginx directory
COPY --from=builder /usr/src/app/phoenix-ui/dist/phoenix-ui /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
