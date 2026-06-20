function PostCard({ post }) {
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
        <button className="hover:text-lavender transition-colors">
          ♡ Like
        </button>
        <button className="hover:text-lavender transition-colors">
          💬 Comment
        </button>
        <button className="hover:text-lavender transition-colors">
          ↗ Share
        </button>
      </div>
    </div>
  );
}

export default PostCard;
