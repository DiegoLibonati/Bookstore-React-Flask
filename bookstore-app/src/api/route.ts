const protocol = window.location.protocol + "//";
const hostname = window.location.hostname;
const port = window.location.port ? `:${window.location.port}` : "";

const prefix = "/api/v1/bookstore"
export const api_route_books = protocol + hostname + port + prefix + "/books" 
export const api_route_genres = protocol + hostname + port + prefix + "/genres" 
