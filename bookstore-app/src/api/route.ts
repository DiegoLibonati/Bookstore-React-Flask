const protocol = window.location.protocol + "//";
const hostname = window.location.hostname;
const port = window.location.port ? `:${window.location.port}` : "";

export const api_route = protocol + hostname + port + "/api/v1/bookstore";
