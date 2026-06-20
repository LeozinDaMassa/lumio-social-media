import { apiRequest } from "./api";

export async function getFeed(page = 1, limit = 10) {
  return apiRequest(`/feed/?page=${page}&limit=${limit}`);
}

export async function createPost(content, mediaUrl = null, mediaType = null) {
  return apiRequest("/posts/", {
    method: "POST",
    body: JSON.stringify({
      content,
      media_url: mediaUrl,
      media_type: mediaType,
    }),
  });
}

export async function likePost(postId) {
  return apiRequest(`/posts/${postId}/like`, { method: "POST" });
}

export async function unlikePost(postId) {
  return apiRequest(`/posts/${postId}/like`, { method: "DELETE" });
}
