# set up frontend
FROM node as build-stage

WORKDIR /frontend

# copy over project
COPY ./frontend/public ./public
COPY ./frontend/src ./src
COPY ./frontend/.env.production .
COPY ./frontend/package-lock.json .
COPY ./frontend/package.json .

# install dependencies
RUN npm install

# build frontend
RUN npm run build


# set up nginx
FROM nginx

# copy over config
COPY nginx.conf /etc/nginx

# copy over frontend build
COPY --from=build-stage /frontend/build /usr/share/nginx/html

EXPOSE 80

# run nginx
CMD ["nginx", "-g", "daemon off;"]
