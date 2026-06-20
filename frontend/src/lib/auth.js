import { apiRequest } from "./api";

export async function register(email, password, username) {
  return apiRequest("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password, username }),
  });
}

export async function login(email, password) {
  const data = await apiRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  localStorage.setItem("token", data.token);
  return data;
}

export function logout() {
  localStorage.removeItem("token");
}

export function isLoggedIn() {
  return !!localStorage.getItem("token");
}
