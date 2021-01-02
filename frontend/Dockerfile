# set up frontend
FROM node:15 as build-stage

WORKDIR /frontend

# copy over project
COPY ./frontend .

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
