import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

export default function Blogs() {
  const [blogs, setBlogs] = useState<any[]>([]);
  const [tag, setTag] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.blog.list(tag).then((r: any) => {
      setBlogs(r.blogs || []);
      setLoading(false);
    });
  }, [tag]);

  const tags = [...new Set(blogs.flatMap((b) => (b.tags || []).flat()))];

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <h1 className="text-3xl font-bold">Blogs &amp; Interview Prep</h1>
        <div className="flex gap-2 overflow-x-auto pb-1">
          <button
            className={`px-3 py-1 rounded-full border ${
              !tag ? "bg-indigo-600 text-white border-indigo-600" : "bg-white text-gray-900 border-gray-300"
            }`}
            onClick={() => setTag(null)}
          >
            All
          </button>
          {tags.map((t) => (
            <button
              key={t}
              className={`px-3 py-1 rounded-full border ${
                tag === t ? "bg-indigo-600 text-white border-indigo-600" : "bg-white text-gray-900 border-gray-300"
              }`}
              onClick={() => setTag(t)}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <p className="text-gray-500">Loading blogs…</p>
      ) : blogs.length === 0 ? (
        <p className="text-gray-500">No blogs for this topic.</p>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {blogs.map((b) => (
            <article key={b.slug} className="border rounded-xl p-5 hover:shadow-md transition">
              <div className="flex gap-2 mb-2">
                {b.tags?.slice(0, 2).map((t: string) => (
                  <span key={t} className="text-xs bg-gray-100 px-2 py-1 rounded text-gray-600">
                    {t}
                  </span>
                ))}
              </div>
              <Link to={`/blog/${b.slug}`} className="text-lg font-semibold text-indigo-600 hover:underline block mb-1">
                {b.title}
              </Link>
              <p className="text-sm text-gray-600 mb-3">{b.excerpt}</p>
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>{b.topic}</span>
                <span>{b.author}</span>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
