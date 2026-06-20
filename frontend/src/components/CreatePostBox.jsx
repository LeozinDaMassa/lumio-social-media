import { useState } from "react";
import { createPost } from "../lib/posts";

function CreatePostBox({ onPostCreated }) {
  const [content, setContent] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await createPost(content);
      setContent("");
      onPostCreated(data.post);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-surface border border-border rounded-xl p-4 flex flex-col gap-3"
    >
      {error && <p className="text-red-400 text-sm">{error}</p>}

      <textarea
        placeholder="What's on your mind?"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        className="bg-elevated text-text-primary border border-border rounded-lg px-4 py-3 outline-none focus:border-lavender transition-colors min-h-20 resize-none"
        required
      />

      <button
        type="submit"
        disabled={loading}
        className="bg-lavender text-night font-medium rounded-lg px-4 py-2 self-end hover:opacity-90 transition-opacity disabled:opacity-50"
      >
        {loading ? "Posting..." : "Post"}
      </button>
    </form>
  );
}

export default CreatePostBox;
