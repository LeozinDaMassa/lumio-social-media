import { useState } from "react";
import { likePost, unlikePost, addComment, getComments } from "../lib/posts";

function PostCard({ post }) {
  const [liked, setLiked] = useState(false);
  const [likeCount, setLikeCount] = useState(0);
  const [showComments, setShowComments] = useState(false);
  const [comments, setComments] = useState([]);
  const [commentsLoaded, setCommentsLoaded] = useState(false);
  const [newComment, setNewComment] = useState("");
  const [submittingComment, setSubmittingComment] = useState(false);

  async function handleLike() {
    try {
      if (liked) {
        await unlikePost(post.id);
        setLikeCount((c) => c - 1);
      } else {
        await likePost(post.id);
        setLikeCount((c) => c + 1);
      }
      setLiked(!liked);
    } catch (err) {
      console.error(err.message);
    }
  }

  async function toggleComments() {
    if (!showComments && !commentsLoaded) {
      try {
        const data = await getComments(post.id);
        setComments(data.comments);
        setCommentsLoaded(true);
      } catch (err) {
        console.error(err.message);
      }
    }
    setShowComments(!showComments);
  }

  async function handleAddComment(e) {
    e.preventDefault();
    if (!newComment.trim()) return;

    setSubmittingComment(true);
    try {
      const data = await addComment(post.id, newComment);
      setComments([...comments, data.comment]);
      setNewComment("");
    } catch (err) {
      console.error(err.message);
    } finally {
      setSubmittingComment(false);
    }
  }

  return (
    <div className="bg-surface border border-border rounded-xl p-4 flex flex-col gap-3">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-elevated flex items-center justify-center text-text-primary font-medium">
          {post.profiles?.username?.[0]?.toUpperCase() || "?"}
        </div>
        <div>
          <p className="text-text-primary font-medium">
            {post.profiles?.username || "Unknown"}
          </p>
          <p className="text-text-secondary text-xs">
            {new Date(post.created_at).toLocaleDateString()}
          </p>
        </div>
      </div>

      <p className="text-text-primary">{post.content}</p>

      {post.media_url && post.media_type === "image" && (
        <img
          src={post.media_url}
          alt="Post media"
          className="rounded-lg w-full object-cover max-h-96"
        />
      )}

      {post.media_url && post.media_type === "video" && (
        <video
          src={post.media_url}
          controls
          className="rounded-lg w-full max-h-96"
        />
      )}

      <div className="flex items-center gap-6 text-text-secondary text-sm pt-2 border-t border-border">
        <button
          onClick={handleLike}
          className={`hover:text-lavender transition-colors ${liked ? "text-lavender" : ""}`}
        >
          {liked ? "♥" : "♡"} {likeCount > 0 && likeCount}
        </button>
        <button
          onClick={toggleComments}
          className="hover:text-lavender transition-colors"
        >
          💬 {comments.length > 0 && comments.length}
        </button>
        <button className="hover:text-lavender transition-colors">
          ↗ Share
        </button>
      </div>

      {showComments && (
        <div className="flex flex-col gap-3 pt-3 border-t border-border">
          {comments.map((comment) => (
            <div key={comment.id} className="flex items-start gap-2">
              <div className="w-7 h-7 rounded-full bg-elevated flex items-center justify-center text-text-primary text-xs font-medium shrink-0">
                {comment.profiles?.username?.[0]?.toUpperCase() || "?"}
              </div>
              <div>
                <p className="text-text-primary text-sm">
                  <span className="font-medium">
                    {comment.profiles?.username}
                  </span>{" "}
                  {comment.content}
                </p>
              </div>
            </div>
          ))}

          <form onSubmit={handleAddComment} className="flex gap-2">
            <input
              type="text"
              placeholder="Write a comment..."
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              className="flex-1 bg-elevated text-text-primary text-sm border border-border rounded-lg px-3 py-2 outline-none focus:border-lavender transition-colors"
            />
            <button
              type="submit"
              disabled={submittingComment}
              className="text-lavender text-sm font-medium px-3 disabled:opacity-50"
            >
              Post
            </button>
          </form>
        </div>
      )}
    </div>
  );
}

export default PostCard;
