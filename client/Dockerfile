# Use an official Node.js runtime as the base image
FROM node:18 AS build

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json (if available) to install dependencies
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of your project files
COPY . .

# Build the project using Vite
RUN npm run build

# Use a smaller Nginx image to serve the built app
FROM nginx:alpine

# Copy the built files from the build stage to Nginx's HTML directory
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose the port that Nginx will listen on
EXPOSE 80

# Start the Nginx service
CMD ["nginx", "-g", "daemon off;"]
