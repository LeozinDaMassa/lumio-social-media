import { useState, useEffect } from "react";
import { getFeed } from "../lib/posts";
import PostCard from "../components/PostCard";
import CreatePostBox from "../components/CreatePostBox";

function Feed() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadFeed();
  }, []);

  async function loadFeed() {
    try {
      const data = await getFeed(1, 10);
      setPosts(data.posts);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleNewPost(newPost) {
    setPosts([newPost, ...posts]);
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-night flex items-center justify-center">
        <p className="text-text-secondary">Loading feed...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-night px-4 py-8">
      <div className="max-w-xl mx-auto flex flex-col gap-4">
        <h1 className="text-2xl text-text-primary tracking-widest mb-2">
          LUMIO
        </h1>

        <CreatePostBox onPostCreated={handleNewPost} />

        {error && <p className="text-red-400">{error}</p>}

        {posts.length === 0 && !error && (
          <p className="text-text-secondary text-center py-12">
            No posts yet. Follow people or create your first post!
          </p>
        )}

        {posts.map((post) => (
          <PostCard key={post.id} post={post} />
        ))}
      </div>
    </div>
  );
}

export default Feed;
