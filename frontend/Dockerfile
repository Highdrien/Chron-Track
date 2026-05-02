FROM node:22-alpine AS base

WORKDIR /app

COPY package.json package-lock.json ./

## ------------------------------- Development Stage -------------------------- ##
FROM base AS development

RUN npm ci

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]

## ------------------------------- Production Build --------------------------- ##
FROM base AS build

RUN npm ci

COPY . .

RUN npm run build

## ------------------------------- Production Stage --------------------------- ##
FROM nginx:alpine AS production

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
