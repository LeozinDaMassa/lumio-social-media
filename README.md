What is built so far — Lumio Backend
A fully functional REST API built with FastAPI and Python, connected to Supabase for database and storage.

Tech Stack
TechnologyRoleFastAPIWeb framework that handles HTTP requestsUvicornServer that listens for requests and runs FastAPISupabasePostgreSQL database + file storage + authJWTToken system that keeps users authenticatedPydanticData validation — enforces correct request shapesPython dotenvLoads secret keys from .env safely

Folder Structure
backend/
├── main.py # Entry point — registers all routers
├── .env # Secret keys — never committed to Git
├── requirements.txt # All dependencies
├── core/
│ ├── config.py # Reads .env variables
│ └── supabase.py # Creates the Supabase client
├── routes/
│ ├── auth.py # Register and login
│ ├── posts.py # Create, fetch, like, comment
│ ├── users.py # Profiles, follow, unfollow
│ ├── feed.py # Paginated feed
│ └── media.py # File uploads
├── models/ # Empty for now, ready for future use
└── middleware/
└── auth.py # JWT verification

Database (Supabase)
Five tables in PostgreSQL:
profiles — stores user data beyond auth
id → links to Supabase auth.users
username
bio
avatar_url
created_at
posts — every post created
id
user_id → profiles
content
media_url → file in Supabase Storage
media_type → "image" or "video"
created_at
likes — one row per like
id
user_id → profiles
post_id → posts
created_at
unique(user_id, post_id) → prevents double liking
comments — one row per comment
id
user_id → profiles
post_id → posts
content
created_at
follows — one row per follow relationship
id
follower_id → profiles
following_id → profiles
created_at
unique(follower_id, following_id) → prevents double following

How auth works
User registers → Supabase creates auth user
→ database trigger fires automatically
→ profile row created in profiles table

User logs in → Supabase verifies password (bcrypt hashed)
→ returns JWT token

Every request → React sends token in Authorization header
→ middleware/auth.py verifies it with Supabase
→ returns user object to the route
→ route knows who is making the request

All API Routes
Auth — /auth
POST /auth/register → create account
POST /auth/login → login and get JWT token
Posts — /posts
POST /posts/ → create post (protected)
GET /posts/ → fetch all posts (public)
POST /posts/{id}/like → like a post (protected)
DELETE /posts/{id}/like → unlike a post (protected)
POST /posts/{id}/comment → add comment (protected)
GET /posts/{id}/comments → fetch comments (public)
Users — /users
GET /users/{id} → get profile (public)
POST /users/{id}/follow → follow user (protected)
DELETE /users/{id}/follow → unfollow user (protected)
GET /users/{id}/followers → get followers (public)
GET /users/{id}/following → get following (public)
Feed — /feed
GET /feed/?page=1&limit=10 → paginated feed (protected)
Media — /media
POST /media/upload → upload image or video (protected)

Key concepts you learned
Virtual environment — isolated Python package box per project. Always activate with source venv/bin/activate before working.
REST API — URL describes what you act on, HTTP method describes what you do. GET fetches, POST creates, DELETE removes.
JWT — self contained token that proves who you are. Sent in every request header as Authorization: Bearer eyJ.... Never stores anything server side.
Middleware — code that runs before your route logic. Your get_current_user function runs on every protected route to verify the token.
Depends() — FastAPI's dependency injection. Automatically runs a function and passes its result to your route. Used for auth on every protected route.
RLS (Row Level Security) — Supabase's database level protection. Rules like "users can only edit their own posts". Always set up alongside each feature.
Pagination — splitting data into pages. page and limit parameters control which chunk to return. Powers infinite scroll on the frontend.
Pydantic models — define the shape of expected data. FastAPI automatically rejects requests that don't match the shape.

What still needs to be done
Backend (minor things):

Clean up the temporary RLS policy on posts and replace with proper user-scoped ones
Add profile update route (update bio, avatar)
Add delete post route

Frontend (React — next phase):

Set up React with Vite and Tailwind CSS
Auth pages (register, login)
Feed page with infinite scroll
Post creation with media upload
Profile pages
Follow/unfollow buttons
Like and comment interactions

Deploy:

Backend → Render
Frontend → Vercel
