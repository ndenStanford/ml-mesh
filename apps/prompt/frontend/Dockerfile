FROM node:19-alpine AS builder

WORKDIR /frontend

# Copy the package.json and install dependencies
COPY app/package*.json ./
RUN npm install

# Copy rest of the files
COPY app/src ./src/
COPY app/* ./

# Build the project
RUN npx parcel build src/index.html --no-cache --no-source-maps
